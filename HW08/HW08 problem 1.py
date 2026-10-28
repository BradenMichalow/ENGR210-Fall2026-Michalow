import numpy as np
import matplotlib.pyplot as plt


def Actual_calc(x):
    actual = Tambient + (Tleft - Tambient)*np.sinh(np.sqrt(hpr)*(L-x))/np.sinh(np.sqrt(hpr)*L) + (Tright - Tambient)*np.sinh(np.sqrt(hpr)*x)/np.sinh(np.sqrt(hpr)*L)
    return actual
#coefs
hpr = 0.01 #1/m2
L = 10 #m
Tleft, Tright, Tambient = 200, 40, 20 # deg C
dx_steps = [1, 0.1, 0.01] # wanted step sizes

for dx in dx_steps:
    n = int(L/dx) + 1 #rearanged equation from example problem to get n instead. Also, has int(L/dx) because arrays need integers
    
    # Create A and B
    A = np.zeros((n,n), dtype=float) # 2D arrays with shape nxn where n is the number of points
    B = np.zeros(n, dtype=float)
    
    # Fill in A and B
    np.fill_diagonal(A[1:-1, 1:-1], -(2+hpr*dx**2))
    np.fill_diagonal(A[1:-1, 0:-2], 1)
    np.fill_diagonal(A[1:-1, 2:], 1)
    A[0,0], A[-1,-1] = 1, 1 #Fixed temperature BCs
    print(A)
    
    B[1:-1] = -hpr*dx**2*Tambient #need to change this from -hpr*Tambient because the governing equation added on to the example one makes this the RHS of the equation instead    
    B[0], B[-1] = 200, 40 #Fixed Temperature BCs
    print(B)

    # Run Linalg.solve to find T
    T = np.linalg.solve(A, B)

    x_arr = np.linspace(0,L,n)
    
    T_actual = Actual_calc(x_arr)
    error = abs(T-T_actual)
    plt.figure(figsize=(5,5))
    plt.plot(x_arr, T, label=f'dx = {dx} m')
    plt.xlabel('Distance (m)')
    plt.ylabel('Temperature (deg C)')
    plt.title(f'Temperature Profile (dx = {dx} m)') #helps determine which graph is for what step size
    plt.figure(figsize=(5,5))
    plt.plot(x_arr, error, label='error of {dx} m')
    plt.xlabel('Distance (m)')
    plt.ylabel('error')
    plt.title(f'Temperature Profile (dx = {dx} m)') #helps determine which graph is for what step size

plt.show()
