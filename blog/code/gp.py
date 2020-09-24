"""
A very simple / slow / inefficient / unstable implementation of a Gaussian
process for stellar light curves. We sample lots of surface maps from a 
given distribution of spot sizes / locations / contrasts and compute the
empirical mean and covariance of the resulting distribution. In the limit
that our number of samples is infinite, this yields the meand and covariance
of the desired GP!
"""
import starry
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.linalg import cho_factor
from matplotlib.colors import Normalize


# Spot size distribution (fractional)
r_mu = 0.05
r_sig = 0.01

# Spot latitude distribution (degrees)
lat_mu = 30
lat_sig = 5

# Spot contrast distribution (fractional)
c_mu = 0.1
c_sig = 0.01

# Number of spots per light curve
nspots = 20

# Degree of the sph. harm. expansion
ydeg = 20

# Total number of samples to draw
nsamples = 10000

# Go!
np.random.seed(0)
map = starry.Map(ydeg, lazy=False)
y = np.empty((nsamples, map.Ny))
for n in tqdm(range(nsamples)):
    map.reset()
    for k in range(nspots):
        sigma = r_mu + r_sig * np.random.randn()
        lat = lat_mu + lat_sig * np.random.randn()
        if np.random.random() < 0.5:
            lat *= -1
        intensity = -(c_mu + c_sig * np.random.randn())
        lon = np.random.random() * 360
        map.add_spot(intensity=intensity, sigma=sigma, lat=lat, lon=lon, relative=False)
    y[n] = np.array(map.y)

# Plot a few of them
fig, ax = plt.subplots(1, 5)
for n, axis in enumerate(ax):
    map[:, :] = y[n]
    map.amp = np.pi
    map.show(ax=ax[n], projection="moll", norm=Normalize(vmin=0.75, vmax=1.1))
fig.savefig("../images/starry-process-exact-samples.jpg", bbox_inches="tight", dpi=300)

# Compute the empirical mean and covariance of the process
mu = np.mean(y[:, 1:], axis=0)
C = np.cov(y[:, 1:].T)

# Plot the covariance matrix
fig, ax = plt.subplots(1, 2)
logC = np.log(np.abs(C))
logC -= np.max(logC)
map[1:, :] = mu
map.show(ax=ax[0], projection="moll")
ax[1].imshow(logC[:100, :100], vmin=-10)
ax[1].set_xticks([])
ax[1].set_yticks([])
ax[0].set_title("mean surface")
ax[1].set_title("covariance matrix")
fig.savefig("../images/starry-process-covariance.jpg", bbox_inches="tight", dpi=300)

# Draw a few samples
eps = 1e-6
choC, _ = cho_factor(C + eps * np.eye(C.shape[0]), lower=True)
u = np.random.randn(map.Ny - 1, 5)
y = np.transpose(mu[:, None] + choC @ u)

# Smooth them a bit
smoothing = 0.1
l = np.concatenate([np.repeat(l, 2 * l + 1) for l in range(1, ydeg + 1)])
s = np.exp(-0.5 * l * (l + 1) * smoothing ** 2)
for n in range(5):
    y[n] *= s

fig, ax = plt.subplots(1, 5)
for n, axis in enumerate(ax):
    map[1:, :] = y[n]
    map.amp = np.pi
    map.show(ax=ax[n], projection="moll", norm=Normalize(vmin=0.75, vmax=1.1))
fig.savefig("../images/starry-process-samples.jpg", bbox_inches="tight", dpi=300)

# Draw flux samples at different inclinations
t = np.linspace(0, 2, 1000)
A = [None for i in range(6)]
for i, inc in enumerate([15, 30, 45, 60, 75, 90]):
    map.inc = inc
    A[i] = map.design_matrix(theta=360 * t)
fig, ax = plt.subplots(1, 5, figsize=(16, 2), sharex=True, sharey=True)
cmap = plt.get_cmap("plasma")
for i in range(6):
    flux = (A[i][:, 1:] @ y.T).T
    for n, axis in enumerate(ax):
        ax[n].plot(t, 1e3 * flux[n], lw=1, color=cmap(0.25 + i / 5 / 2))
for axis in ax:
    axis.set_xticks([0, 0.5, 1, 1.5, 2])
    axis.set_xlabel("rotations")
ax[0].set_ylabel("flux [ppt]")
fig.savefig("../images/starry-process-flux-samples.jpg", bbox_inches="tight", dpi=300)
