import theano
import theano.tensor as tt
from theano.tensor import slinalg
from theano.ifelse import ifelse
import scipy.linalg
import numpy as np


__all__ = ["cho_factor", "cho_solve", "normalize", "log_likelihood", "CosineKernel"]


# Force double precision in Theano
tt.config.floatX = "float64"
tt.config.cast_policy = "numpy+floatX"


class Solve(slinalg.Solve):
    """
    Subclassing to override errors due to NaNs.
    Instead, just set the output to NaN.
    
    """

    def perform(self, node, inputs, output_storage):
        A, b = inputs
        if np.any(np.isnan(A)) or np.any(np.isnan(b)):
            rval = np.ones_like(b) * np.nan
        else:
            if self.A_structure == "lower_triangular":
                rval = scipy.linalg.solve_triangular(A, b, lower=True)
            elif self.A_structure == "upper_triangular":
                rval = scipy.linalg.solve_triangular(A, b, lower=False)
            else:
                rval = scipy.linalg.solve(A, b)
        output_storage[0][0] = rval

    def L_op(self, inputs, outputs, output_gradients):
        """
        Reverse-mode gradient updates for matrix solve operation c = A \\\ b.

        Symbolic expression for updates taken from [#]_.

        References
        ----------
        .. [#] M. B. Giles, "An extended collection of matrix derivative results
          for forward and reverse mode automatic differentiation",
          http://eprints.maths.ox.ac.uk/1079/

        """
        A, b = inputs
        c = outputs[0]
        c_bar = output_gradients[0]
        trans_map = {
            "lower_triangular": "upper_triangular",
            "upper_triangular": "lower_triangular",
        }
        trans_solve_op = Solve(
            # update A_structure and lower to account for a transpose operation
            A_structure=trans_map.get(self.A_structure, self.A_structure),
            lower=not self.lower,
        )
        b_bar = trans_solve_op(A.T, c_bar)
        # force outer product if vector second input
        A_bar = -tt.outer(b_bar, c) if c.ndim == 1 else -b_bar.dot(c.T)
        if self.A_structure == "lower_triangular":
            A_bar = tt.tril(A_bar)
        elif self.A_structure == "upper_triangular":
            A_bar = tt.triu(A_bar)
        return [A_bar, b_bar]


class Cholesky(slinalg.Cholesky):
    """
    Subclassing to override errors due to NaNs.
    Instead, just set the output to NaN.
    
    """

    def perform(self, node, inputs, outputs):
        x = inputs[0]
        z = outputs[0]
        try:
            z[0] = scipy.linalg.cholesky(x, lower=self.lower).astype(x.dtype)
        except (scipy.linalg.LinAlgError, ValueError):
            if self.on_error == "raise":
                raise
            else:
                z[0] = (np.zeros(x.shape) * np.nan).astype(x.dtype)


cho_factor = Cholesky(on_error="nan")


def cho_solve(cho_A, b):
    solve_lower = Solve(A_structure="lower_triangular", lower=True)
    solve_upper = Solve(A_structure="upper_triangular", lower=False)
    return solve_upper(tt.transpose(cho_A), solve_lower(cho_A, b))


class AlphaBetaOp(tt.Op):
    """

    """

    __props__ = ("N",)

    def __init__(self, N=20):
        self.N = N

    def make_node(self, z):
        inputs = [tt.as_tensor_variable(z).astype(tt.config.floatX)]
        outputs = [
            tt.TensorType(dtype=tt.config.floatX, broadcastable=[])() for n in range(4)
        ]
        return theano.gof.Apply(self, inputs, outputs)

    def infer_shape(self, node, shapes):
        return [(), (), (), ()]

    def perform(self, node, inputs, outputs):
        z = inputs[0]
        fac = 1.0
        alpha = 0.0
        beta = 0.0
        dadz = 0.0
        dbdz = 0.0
        dfdz = 0.0
        for n in range(0, self.N + 1):
            dadz += dfdz
            dbdz += 2 * n * dfdz
            dfdz = (2 * n + 3) * (dfdz * z + fac)
            alpha += fac
            beta += 2 * n * fac
            fac *= z * (2 * n + 3)
        outputs[0][0] = np.array(alpha)
        outputs[1][0] = np.array(beta)
        outputs[2][0] = np.array(dadz)
        outputs[3][0] = np.array(dbdz)

    def grad(self, inputs, gradients):
        z = inputs[0]
        ba = gradients[0]
        bb = gradients[1]
        a, b, dadz, dbdz = self(*inputs)

        # Derivs of derivs not implemented
        for i, g in enumerate(list(gradients[2:])):
            if not isinstance(g.type, theano.gradient.DisconnectedType):
                raise ValueError(
                    "can't propagate gradients wrt parameter {0}".format(i + 1)
                )

        bz = tt.as_tensor_variable(0.0)
        for dxdz, bx in zip([dadz, dbdz], [ba, bb]):
            if not isinstance(bx.type, theano.gradient.DisconnectedType):
                bz += dxdz * bx

        return [bz]

    def R_op(self, inputs, eval_points):
        if eval_points[0] is None:
            return eval_points
        return self.grad(inputs, eval_points)


def normalize(mu, cov, zmax=0.023, N=20):
    """
    Return the series expansion of the normalized covariance matrix.

    See Luger (2021) for details.

    """
    K = cov.shape[0]
    j = tt.ones((K, 1))
    m = tt.mean(cov)
    q = tt.dot(cov, j) / (K * m)
    z = m / mu ** 2
    p = j - q
    get_alpha_beta = AlphaBetaOp(N=N)
    alpha, beta, _, _ = get_alpha_beta(z)
    ppT = tt.dot(p, tt.transpose(p))
    qqT = tt.dot(q, tt.transpose(q))
    normC = (alpha / mu ** 2) * cov + z * ((alpha + beta) * ppT - alpha * qqT)
    return (
        tt.ones_like(tt.as_tensor_variable(mu)),
        ifelse(tt.gt(z, zmax), tt.ones_like(cov) * np.inf, normC),
    )


def CosineKernel(x, t):
    dt = tt.abs_(tt.reshape(t, (-1, 1)) - tt.reshape(t, (1, -1)))
    return tt.exp(x[0]) * tt.cos(2 * np.pi * dt / tt.exp(x[1]))


def log_likelihood(
    x, t, y, mean=1.0, sigma=None, normalized=True, kernel=CosineKernel, **kwargs
):
    cov = kernel(x, t)
    K = cov.shape[0]
    if normalized:
        mean, cov = normalize(mean, cov, **kwargs)
    if sigma is not None:
        cov += tt.eye(K) * sigma ** 2
    cho_cov = cho_factor(cov)
    r = tt.reshape(y, (-1, 1)) - tt.reshape(mean, (-1, 1))
    lnlike = -0.5 * tt.dot(tt.transpose(r), cho_solve(cho_cov, r))
    lnlike -= tt.sum(tt.log(tt.diag(cho_cov)))
    lnlike -= 0.5 * K * tt.log(2 * np.pi)
    return ifelse(tt.isnan(lnlike[0, 0]), -np.inf, lnlike[0, 0])
