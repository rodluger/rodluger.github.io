import matplotlib.pyplot as plt

# True values
alpha_true = 2.0
beta_true = 0.33

# Array of alpha values to test
alpha_arr = np.linspace(1.5, 2.5, 1000)

# Let's simulate 50 different `y` datasets, each with k=1000 points
np.random.seed(0)
for k in range(50):

    # Draw our data: this is what we observe
    y = Beta.rvs(alpha_true, beta_true, size=1000)

    # Compute the log likelihood using the true likelihood function
    # Exponentiate it and divide by the evidence to get the posterior
    ll = np.array([log_likelihood(alpha, beta_true, y) for alpha in alpha_arr])
    ll -= np.nanmax(ll)
    pdf = np.exp(ll) / np.trapz(np.exp(ll))

    # Now do the same thing using the synthetic likelihood function
    ll_sl = np.array(
        [log_likelihood_synthetic(alpha, beta_true, y) for alpha in alpha_arr]
    )
    ll_sl -= np.nanmax(ll_sl)
    pdf_sl = np.exp(ll_sl) / np.trapz(np.exp(ll_sl))

    # Plot the two distributions
    plt.plot(alpha_arr, pdf, color="C0", alpha=0.25, lw=1)
    plt.plot(alpha_arr, pdf_sl, color="C1", alpha=0.25, lw=1)

plt.axvline(alpha_true, color="k", lw=1, ls="--", alpha=0.5)
