import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import celerite
from celerite import terms

np.random.seed(0)

pad = 25
log_omega0 = 3
log_S0 = 0
log_Q = 2.0
amp = 10
nrot = 30
npts = 1000
nsamples = 5

x = np.linspace(0, nrot * 2 * np.pi / np.exp(log_omega0), npts, endpoint=False)

yerr = 1e2 * np.ones_like(x)
yerr[:pad] = np.logspace(-12, 2, pad)
yerr[-pad:] = np.logspace(2, -12, pad)


kernel = terms.SHOTerm(log_S0=log_S0, log_Q=log_Q, log_omega0=log_omega0)
gp = celerite.GP(kernel)
gp.compute(x, yerr)

y = [None for k in range(nsamples)]
for k in range(nsamples):
    y0 = (
        amp
        * np.exp(log_S0)
        * np.sin(np.exp(log_omega0) * x + 2 * np.pi * np.random.random())
    )
    y[k] = gp.sample_conditional(y0)
    y[k] = (y[k] - y[k].min()) / (y[k].max() - y[k].min())


fig, ax = plt.subplots(figsize=(3.6, 3.2), facecolor="#e5e5e5")
fig.patch.set_facecolor("#e5e5e5")
fig.subplots_adjust(left=0, bottom=0, top=1, right=1)
ax.set(xlim=(0, 1), ylim=(-0.1, 1.1))
ax.axis("off")
line = [None for k in range(nsamples)]
point = [None for k in range(nsamples)]
for k in range(nsamples):
    data = np.array(y[k])
    data[99:] = np.nan
    (line[k],) = ax.plot(x, data, lw=1.5, alpha=0.5)

    data = np.array(data)
    data[:98] = np.nan
    (point[k],) = ax.plot(x, data, "o", color=line[k].get_color(), ms=2)


colors = np.ones((1, 2, 4))
colors[:, :, 0] = 229 / 255
colors[:, :, 1] = 229 / 255
colors[:, :, 2] = 229 / 255
colors[0, 0, -1] = 1
colors[0, 1, -1] = 0

ax.imshow(colors, interpolation="bicubic", zorder=99, extent=(0, 0.75, -0.1, 1.1))


def animate(i):
    for k in range(nsamples):
        data = np.roll(y[k], -i)
        data[99:] = np.nan
        line[k].set_ydata(data)
        data = np.array(data)
        data[:98] = np.nan
        point[k].set_ydata(data)


anim = FuncAnimation(fig, animate, interval=20, frames=npts - 1, repeat=True)
anim.save("gp.gif", writer="imagemagick", savefig_kwargs=dict(facecolor="#e5e5e5"))
