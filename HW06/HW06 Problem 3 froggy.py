import numpy as np
import matplotlib.pyplot as plt

#initial conditions and arrays

m = 2.0
k = 20.0
x0 = 0.5
v0 = 0.0
dt = 0.1
T = 200.0

# Number of time steps
N = int(T / dt)


t = np.zeros(N + 1)
x = np.zeros(N + 1)
v = np.zeros(N + 1)


t[0] = 0.0
x[0] = x0
v[0] = v0


#leapfrog method

t_current = 0.0
i = 0

while t_current < T and i < N:

    # Calculate acceleration at current position
    a = -(k / m) * x[i]

    # Half-step velocity
    v_half = v[i] + 0.5 * dt * a

    # Full-step position
    x[i + 1] = x[i] + dt * v_half

    # Calculate acceleration at new position
    a_new = -(k / m) * x[i + 1]

    # Finish velocity step
    v[i + 1] = v_half + 0.5 * dt * a_new

    # Advance time
    t_current = t_current + dt
    t[i + 1] = t_current

    # Move to next array index
    i = i + 1


#exact and error calculations
x_exact = x0 * np.cos(np.sqrt(k / m) * t)


error = np.abs(x - x_exact)

#plots

# first 10 seconds (helps show oscillations because the second graph gets real messy and big...
plt.figure()

plt.plot(t, x_exact, label="Exact")
plt.plot(t, x, label="Leapfrog")

plt.xlim(0, 10)

plt.xlabel("Time (s)")
plt.ylabel("Displacement (m)")
plt.title("Leapfrog vs Exact Solution")
plt.legend()
plt.grid()

plt.show()


# 2nd graph thta contains all time plots. gets really messy
plt.figure()

plt.plot(t, x_exact, label="Exact")
plt.plot(t, x, label="Leapfrog")

plt.xlabel("Time (s)")
plt.ylabel("Displacement (m)")
plt.title("Mass-Spring System: Leapfrog")
plt.legend()
plt.grid()

plt.show()


# error vs time graph
plt.figure()

plt.plot(t, error, label="Leapfrog Error")

plt.xlabel("Time (s)")
plt.ylabel("Absolute Error (m)")
plt.title("Leapfrog Numerical Error")
plt.legend()
plt.grid()

plt.show()