import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# Parameters
# -------------------------

m = 2.0
k = 20.0
x0 = 0.5
v0 = 0.0
dt = 0.1
T = 200.0

N = int(T / dt)


# -------------------------
# Create arrays
# -------------------------

t = np.zeros(N + 2)

x_euler = np.zeros(N + 2)
v_euler = np.zeros(N + 2)

x_rk4 = np.zeros(N + 2)
v_rk4 = np.zeros(N + 2)


# -------------------------
# Initial conditions
# -------------------------

t[0] = 0.0

x_euler[0] = x0
v_euler[0] = v0

x_rk4[0] = x0
v_rk4[0] = v0


# -------------------------
# Euler method
# -------------------------

t_current = 0.0
i = 0

while t_current < T:

    a = -(k / m) * x_euler[i]

    x_euler[i + 1] = x_euler[i] + dt * v_euler[i]
    v_euler[i + 1] = v_euler[i] + dt * a

    t_current = t_current + dt
    t[i + 1] = t_current

    i = i + 1


# -------------------------
# RK4 method
# -------------------------

t_current = 0.0
i = 0

while t_current < T:

    # k1
    k1x = v_rk4[i]
    k1v = -(k / m) * x_rk4[i]

    # k2
    k2x = v_rk4[i] + 0.5 * dt * k1v
    k2v = -(k / m) * (x_rk4[i] + 0.5 * dt * k1x)

    # k3
    k3x = v_rk4[i] + 0.5 * dt * k2v
    k3v = -(k / m) * (x_rk4[i] + 0.5 * dt * k2x)

    # k4
    k4x = v_rk4[i] + dt * k3v
    k4v = -(k / m) * (x_rk4[i] + dt * k3x)

    # Update x and v
    x_rk4[i + 1] = x_rk4[i] + (dt / 6) * (
        k1x + 2*k2x + 2*k3x + k4x
    )

    v_rk4[i + 1] = v_rk4[i] + (dt / 6) * (
        k1v + 2*k2v + 2*k3v + k4v
    )

    # Advance time
    t_current = t_current + dt
    t[i + 1] = t_current

    i = i + 1


# -------------------------
# Exact solution
# -------------------------

x_exact = x0 * np.cos(np.sqrt(k / m) * t)


# -------------------------
# Errors
# -------------------------

error_euler = np.abs(x_euler - x_exact)
error_rk4 = np.abs(x_rk4 - x_exact)


# -------------------------
# Plot solutions
# -------------------------

plt.figure()

plt.plot(t, x_exact, label="Exact", linestyle='-.')
plt.plot(t, x_euler, label="Euler", linestyle='-')
plt.plot(t, x_rk4, label="RK4", linestyle='--')

plt.xlabel("Time (s)")
plt.ylabel("Displacement (m)")
plt.title("Mass-Spring System")
plt.legend()
plt.grid()

plt.show()


# -------------------------
# Plot errors
# -------------------------

plt.figure()

plt.semilogy(t, error_euler, label="Euler Error", )
plt.semilogy(t, error_rk4, label="RK4 Error", linestyle='--')

plt.xlabel("Time (s)")
plt.ylabel("Absolute Error (m)")
plt.title("Numerical Error")
plt.legend()
plt.grid()

plt.show()