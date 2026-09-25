import numpy as np
import matplotlib.pyplot as plt


def rk4(f, t0, y0, tf, h):
    """
    Classical fourth-order Runge-Kutta method.

    Solves the initial-value problem
        y' = f(t, y),  y(t0) = y0

    Parameters
    ----------
    f : callable
        Function f(t, y).
    t0 : float
        Initial time.
    y0 : float or array_like
        Initial condition.
    tf : float
        Final time.
    h : float
        Step size.

    Returns
    -------
    t : ndarray
        Time points.
    y : ndarray
        Numerical solution at each time point.
    """

    y0 = np.asarray(y0, dtype=float)
    if y0.ndim == 0:
        y0 = y0.reshape(1)

    n = int(np.ceil((tf - t0) / h))
    t = np.linspace(t0, tf, n + 1)

    # Adjust the actual step size so that tf is reached exactly.
    h_actual = (tf - t0) / n

    y = np.zeros((n + 1, len(y0)))
    y[0] = y0

    for i in range(n):
        ti = t[i]
        yi = y[i]

        k1 = np.asarray(f(ti, yi))
        k2 = np.asarray(f(ti + h_actual / 2,
                          yi + h_actual * k1 / 2))
        k3 = np.asarray(f(ti + h_actual / 2,
                          yi + h_actual * k2 / 2))
        k4 = np.asarray(f(ti + h_actual,
                          yi + h_actual * k3))

        y[i + 1] = yi + (h_actual / 6) * (
            k1 + 2*k2 + 2*k3 + k4
        )

    return t, y

# Example: y' = -y, y(0) = 1


def f(t, y):
    return -y


t, y = rk4(f, 0.0, [1.0], 5.0, 0.1)

exact = np.exp(-t)

plt.plot(t, y[:, 0], "o-", label="RK4")
plt.plot(t, exact, "--", label="Exact")
plt.xlabel("t")
plt.ylabel("y")
plt.legend()
plt.grid()
plt.show()


# verify 4th order

errors = []
steps = [0.4, 0.2, 0.1, 0.05, 0.025]

for h in steps:
    t, y = rk4(f, 0.0, [1.0], 1.0, h)
    error = abs(y[-1, 0] - np.exp(-1.0))
    errors.append(error)

print("     h             error          observed order")
print("-" * 50)

for i, h in enumerate(steps):
    if i == 0:
        print(f"{h:8.5f}   {errors[i]:12.5e}       ---")
    else:
        order = np.log(errors[i-1] / errors[i]) / np.log(2)
        print(f"{h:8.5f}   {errors[i]:12.5e}     {order:8.4f}")



def rk4_amplification(z):
    """RK4 stability function R(z)."""
    return 1 + z + z**2/2 + z**3/6 + z**4/24



omega = 10.0
h = 0.2

z = 1j * omega * h
R = rk4_amplification(z)

print("\nStability test")
print("z =", z)
print("R(z) =", R)
print("|R(z)| =", abs(R))

if abs(R) <= 1:
    print("The RK4 solution is stable for this z.")
else:
    print("The RK4 solution is unstable for this z.")