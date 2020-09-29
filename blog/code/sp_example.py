from starry_process import StarryProcess
import matplotlib.pyplot as plt
import numpy as np

sp = StarryProcess(
    sa=0.3, sb=0.75, la=0.9, lb=0.7, ca=0.75, cb=0.0, period=1.0, inc=60.0
)
t = np.linspace(0, 3, 500)
flux = sp.sample(t, nsamples=10).eval()

for k in range(10):
    plt.plot(t, 1e3 * flux[k])

plt.xlabel("time [d]")
plt.ylabel("flux [ppt]")
plt.show()
