import numpy as np
import matplotlib.pyplot as plt

# Differential equation
def f(t, y):
    return -1000*y + 3000 - 2000*np.exp(-t)

# Exact solution
def exact_solution(t):
    return 3 - 0.998*np.exp(-1000*t) - 2.002*np.exp(-t)

# Heun's method
def heun(f, t0, tf, y0, h):
    N = int(round((tf - t0) / h))

    t = np.linspace(t0, tf, N + 1)
    y = np.zeros(N + 1)
    y[0] = y0

    for n in range(N):
        # Predictor step
        k1 = f(t[n], y[n])
        y_predict = y[n] + h*k1

        # Corrector step
        k2 = f(t[n] + h, y_predict)
        y[n+1] = y[n] + (h/2)*(k1 + k2)

    return t, y


# Initial conditions
t0 = 0.0
tf = 1.0
y0 = 0.0

# Test different time steps
steps = [0.001, 0.0005, 0.00025, 0.000125]

errors = []

print("Step size       Maximum error")

for h in steps:
    t, y = heun(f, t0, tf, y0, h)

    y_exact = exact_solution(t)

    # Maximum absolute error over the interval
    error = np.max(np.abs(y - y_exact))
    errors.append(error)

    print(f"{h:.7f}     {error:.6e}")


# Calculate observed order of accuracy
print("\nObserved order of accuracy:")

for i in range(len(steps)-1):
    p = np.log(errors[i]/errors[i+1]) / np.log(2)
    print(f"h = {steps[i]:.7f}: p = {p:.4f}")


# Plot numerical and exact solutions
t, y = heun(f, t0, tf, y0, steps[-1])

plt.plot(t, y, label="Heun's method")
plt.plot(t, exact_solution(t), '--',
         label="Exact solution")

plt.xlabel("Time t")
plt.ylabel("y(t)")
plt.title("Heun's Method vs Exact Solution")
plt.legend()
plt.grid(True)
plt.show()