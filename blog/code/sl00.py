import numpy as np
from scipy.stats import beta as Beta


def mu(alpha, beta):
    """The mean of the Beta distribution."""
    return alpha / (alpha + beta)


def sigma(alpha, beta):
    """The standard deviation of the Beta distribution."""
    var = alpha * beta / (alpha + beta) ** 2 / (alpha + beta + 1)
    return np.sqrt(var)


def log_likelihood_synthetic(alpha, beta, y):
    """The synthetic log-likelihood function."""
    mean = mu(alpha, beta)
    std = sigma(alpha, beta)
    var = std ** 2
    ll = -0.5 * np.sum((y - mean) ** 2 / var)
    ll -= 0.5 * len(y) * np.log(var)
    ll -= 0.5 * len(y) * np.log(2 * np.pi)
    return ll


def log_likelihood(alpha, beta, y):
    """The true log-likelihood function."""
    return np.sum(Beta.logpdf(y, alpha, beta))

