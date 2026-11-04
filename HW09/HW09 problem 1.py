import numpy as np
import matplotlib.pyplot as plt
#Initialize with correct boundry conditions
Nx, Ny = 101, 101
T_arr = np.ones((Nx, Ny), dtype=float)*50
tol = 1e-4
max_err = tol + 1
T_arr[1:-1, 0] = 0 #bottom boundry conditions
T_arr[1:-1, -1] = 100 #top boundry condition
T_arr[0, 1:-1] = 75 #left boundry condition
T_arr[-1, 1:-1] = 50 #right boundry condition
T_arr[0,0], T_arr[-1,0], T_arr[-1,-1], T_arr[0,-1] = (0+75)/2, (0+50)/2, (50+100)/2, (100+75)/2
#loop until error converges
# while max_err > tol:
for iters in range(10000):
    max_err = 0
    #loop over all grid points
    for i in range(1, Nx-1):  #no outside values
        for j in range(1, Ny-1):
            T_new = (T_arr[i-1][j] + T_arr[i+1][j] + T_arr[i][j-1] + T_arr [i][j+1])/4
            T_new = 1.9*T_new + (1-1.9)*T_arr[i][j]
            max_err = max(max_err, abs(T_new - T_arr[i][j]) ) # keeps the biggest error
            T_arr[i,j] = T_new
    if max_err < tol:
        print("converged")
        break
plt.imshow(T_arr.T, origin='lower')
plt.show()

plt.figure()
plt.contour(T_arr.T, levels=15)
plt.colorbar(label="Temperature")
plt.xlabel("x grid point")
plt.ylabel("y grid point")
plt.title("Temperature Contour Plot")
plt.show()
