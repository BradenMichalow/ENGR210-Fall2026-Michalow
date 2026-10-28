import numpy as np
import matplotlib.pyplot as plt


def Actual_calc(x):
    actual = Tambient + (Tleft - Tambient)*(
        np.cosh(np.sqrt(hpr)*(L-x))
        + htip/np.sqrt(hpr)*np.sinh(np.sqrt(hpr)*(L-x))
    )/(
        np.cosh(np.sqrt(hpr)*L)
        + htip/np.sqrt(hpr)*np.sinh(np.sqrt(hpr)*L)
    )
    return actual


# Coefs
hpr = 0.01  # 1/m2
htip = 0.001  # 1/m
L = 10  # m
Tleft, Tambient = 200, 20  # deg C
dx_steps = [1, 0.1, 0.01]  # wanted step sizes


for dx in dx_steps:

    n = int(L/dx) + 1

    # Create A and B
    A = np.zeros((n, n), dtype=float)
    B = np.zeros(n, dtype=float)

    # Left boundary condition: T(0) = Tleft
    A[0, 0] = 1
    B[0] = Tleft

    # Fill in A and B for interior nodes
    for i in range(1, n-1):
        A[i, i-1] = 1
        A[i, i] = -(2+hpr*dx**2)
        A[i, i+1] = 1
        B[i] = -hpr*dx**2*Tambient

    # Right boundary condition: heat loss at the tip
    A[-1, -3] = 1
    A[-1, -2] = -4
    A[-1, -1] = 3 + 2*dx*htip
    B[-1] = 2*dx*htip*Tambient

    # Run Linalg.solve to find T
    T = np.linalg.solve(A, B)

    x_arr = np.linspace(0, L, n)

    # Calculate analytical solution and error
    T_actual = Actual_calc(x_arr)
    error = abs(T-T_actual)

    # Plot temperature in a separate figure for each dx
    plt.figure(figsize=(6, 5))
    plt.plot(x_arr, T, label='Numerical solution')
    x_exact = np.linspace(0, L, 1000)
    plt.plot(x_exact, Actual_calc(x_exact), 'k--',
             label='Analytical solution')
    plt.xlabel('Distance (m)')
    plt.ylabel('Temperature (deg C)')
    plt.title(f'Temperature Profile (dx = {dx} m)')
    plt.legend()
    plt.grid()

    # Plot error in a separate figure for each dx
    plt.figure(figsize=(6, 5))
    plt.plot(x_arr, error, label='Absolute error')
    plt.xlabel('Distance (m)')
    plt.ylabel('Absolute Error (deg C)')
    plt.title(f'Error Profile (dx = {dx} m)')
    plt.legend()
    plt.grid()

plt.show()

