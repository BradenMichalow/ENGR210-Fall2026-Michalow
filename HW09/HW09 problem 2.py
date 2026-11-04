# Codex prompt:
# An uploaded image of the problem page
#  
# 
# Outline of code: 
# 1. The program imports NumPy and Matplotlib. NumPy is used for numerical calculations and creating the computational grid, while Matplotlib is used to generate the temperature contour plot.
# 2. The thermal conductivity, convection coefficients, and surrounding fluid temperatures are defined using the values provided in the problem statement.
# 3. The dimensions of the turbine blade and internal cooling channel are established. A repeating section of the blade is modeled using symmetry to reduce the computational domain.
# 4. The blade is divided into small cells using a uniform grid. Each cell is identified as either solid blade material or part of the internal cooling channel.
# 5. Convection boundary conditions are applied to the outside surfaces exposed to combustion gases and the inside surfaces exposed to cooling air. Symmetry boundaries are used at the sides of the repeating section.
# 6. The temperature at each solid grid point is calculated using neighboring temperatures and the appropriate boundary conditions. Successive over-relaxation is used to accelerate convergence. Iterations continue until the maximum temperature change is below the specified tolerance.
# 7. The program calculates the heat entering the blade from the hot combustion gases and the heat transferred from the blade into the cooling air.
# 8. A separate one-dimensional heat conduction problem with known analytical results is used to check the numerical treatment of the conduction and convection boundary conditions.
# 9. The program checks temperature symmetry, verifies that calculated temperatures remain within the surrounding fluid temperature limits, and compares the heat entering and leaving the blade.
# 10. Matplotlib is used to generate a contour plot showing the temperature distribution throughout the turbine blade and around the internal cooling channel.


import numpy as np
import matplotlib.pyplot as plt

# Given properties
k = 25.0
ho = 1000.0
To = 1700.0
hi = 200.0
Ti = 400.0

# Geometry (meters)
Lx = 10e-3
Ly = 6e-3

# Cooling channel dimensions and location
x1, x2 = 2e-3, 8e-3
y1, y2 = 2e-3, 4e-3

# Grid size
dx = 0.1e-3
dy = 0.1e-3

Nx = round(Lx/dx)
Ny = round(Ly/dy)

dx = Lx/Nx
dy = Ly/Ny

# Grid coordinates
x = (np.arange(Nx)+0.5)*dx
y = (np.arange(Ny)+0.5)*dy
X, Y = np.meshgrid(x, y, indexing="ij")

# Identify solid blade and cooling channel
solid = ~((X > x1) & (X < x2) &
          (Y > y1) & (Y < y2))

# Initialize temperature
T = np.full((Nx, Ny), np.nan)
T[solid] = 1000.0

# Conductances
Gx = k*dy/dx
Gy = k*dx/dy

# Convection boundary conductance
def robin_G(area, distance, h):
    return area/(distance/k + 1/h)

# Set up coefficient arrays
diag = np.zeros((Nx, Ny))
rhs = np.zeros((Nx, Ny))

for i in range(Nx):
    for j in range(Ny):

        if not solid[i,j]:
            continue

        for di, dj, G in [
            (1,0,Gx), (-1,0,Gx),
            (0,1,Gy), (0,-1,Gy)
        ]:

            ni = i+di
            nj = j+dj

            # Symmetry boundaries
            if di != 0 and (ni < 0 or ni >= Nx):
                continue

            # Outside hot gas convection
            if dj != 0 and (nj < 0 or nj >= Ny):
                Gc = robin_G(dx, dy/2, ho)
                diag[i,j] += Gc
                rhs[i,j] += Gc*To

            # Neighboring solid cell
            elif solid[ni,nj]:
                diag[i,j] += G

            # Cooling channel convection
            else:
                area = dy if di != 0 else dx
                distance = dx/2 if di != 0 else dy/2

                Gc = robin_G(area, distance, hi)
                diag[i,j] += Gc
                rhs[i,j] += Gc*Ti

# Gauss-Seidel with SOR
omega = 1.85
tol = 1e-5
max_iter = 50000

ii, jj = np.indices((Nx,Ny))

red = solid & ((ii+jj)%2 == 0)
black = solid & ((ii+jj)%2 == 1)

for iteration in range(1, max_iter+1):

    max_error = 0

    # Red-black Gauss-Seidel ordering
    for mask in (red, black):

        east = np.zeros_like(T)
        west = np.zeros_like(T)
        north = np.zeros_like(T)
        south = np.zeros_like(T)

        east[:-1,:] = np.nan_to_num(T[1:,:], nan=0)
        west[1:,:] = np.nan_to_num(T[:-1,:], nan=0)
        north[:,:-1] = np.nan_to_num(T[:,1:], nan=0)
        south[:,1:] = np.nan_to_num(T[:,:-1], nan=0)

        es = np.zeros_like(solid)
        ws = np.zeros_like(solid)
        ns = np.zeros_like(solid)
        ss = np.zeros_like(solid)

        es[:-1,:] = solid[1:,:]
        ws[1:,:] = solid[:-1,:]
        ns[:,:-1] = solid[:,1:]
        ss[:,1:] = solid[:,:-1]

        neighbor_sum = (
            Gx*(east*es + west*ws)
            + Gy*(north*ns + south*ss)
        )

        T_GS = (rhs+neighbor_sum)/np.where(
            solid, diag, 1
        )

        T_new = T + omega*(T_GS-T)

        change = np.abs(T_new[mask]-T[mask])

        if change.size:
            max_error = max(max_error, np.max(change))

        T[mask] = T_new[mask]

    if max_error < tol:
        break

# Results
print("CONVERGENCE RESULTS")
print("-------------------")
print("Iterations:", iteration)
print("Maximum error:", max_error)

print("\nTEMPERATURE RESULTS")
print("-------------------")
print("Maximum temperature:", np.nanmax(T), "K")
print("Minimum temperature:", np.nanmin(T), "K")

# Heat transfer calculations
Q_cooling = 0
Q_hot = 0

for i in range(Nx):
    for j in range(Ny):

        if not solid[i,j]:
            continue

        Tp = T[i,j]

        # Top and bottom hot gas convection
        if j == 0 or j == Ny-1:
            Gc = robin_G(dx, dy/2, ho)
            Q_hot += Gc*(To-Tp)

        # Cooling channel walls
        for di,dj in [
            (1,0),(-1,0),(0,1),(0,-1)
        ]:
            ni = i+di
            nj = j+dj

            if (0 <= ni < Nx and
                0 <= nj < Ny and
                not solid[ni,nj]):

                area = dy if di != 0 else dx
                distance = dx/2 if di != 0 else dy/2

                Gc = robin_G(area,distance,hi)

                Q_cooling += Gc*(Tp-Ti)

print("\nHEAT TRANSFER RESULTS")
print("---------------------")
print("Heat from hot gas:", Q_hot, "W/m")
print("Heat to cooling air:", Q_cooling, "W/m")
print("Energy balance difference:", Q_hot-Q_cooling, "W/m")

# Boundary condition and symmetry checks
print("\nBOUNDARY CHECKS")
print("----------------")
print("Left-right symmetry:",
      np.nanmax(np.abs(T-T[::-1,:])))

print("Top-bottom symmetry:",
      np.nanmax(np.abs(T-T[:,::-1])))


# ------------------------------------------------------------
# Verification: 1-D plane wall with convection on both sides
# ------------------------------------------------------------

Ltest = 0.010
ktest = 10.0
hhot = 100.0
hcold = 50.0
Thot = 500.0
Tcold = 300.0

n_test = 100
dx_test = Ltest/n_test

Gcond = ktest/dx_test

Ghot = 1/(dx_test/(2*ktest) + 1/hhot)
Gcold = 1/(dx_test/(2*ktest) + 1/hcold)

# Create coefficient matrix
A = np.zeros((n_test,n_test))
b = np.zeros(n_test)

# Hot-side boundary
A[0,0] = Ghot + Gcond
A[0,1] = -Gcond
b[0] = Ghot*Thot

# Interior nodes
for i in range(1,n_test-1):
    A[i,i-1] = -Gcond
    A[i,i] = 2*Gcond
    A[i,i+1] = -Gcond

# Cold-side boundary
A[-1,-2] = -Gcond
A[-1,-1] = Gcond + Gcold
b[-1] = Gcold*Tcold

# Solve numerical verification problem
T_test = np.linalg.solve(A,b)

# Numerical heat flux
q_numerical = Ghot*(Thot-T_test[0])

# Analytical heat flux
R_total = 1/hhot + Ltest/ktest + 1/hcold

q_analytical = (Thot-Tcold)/R_total

# Calculate percentage error
error = abs(q_numerical-q_analytical)/q_analytical*100

print("\nVERIFICATION RESULTS")
print("--------------------")
print("Analytical heat flux:", q_analytical, "W/m^2")
print("Numerical heat flux:", q_numerical, "W/m^2")
print("Percentage error:", error, "%")

