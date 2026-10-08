import numpy as np
import matplotlib.pyplot as plt


v0 = 22      #initial velocity
m = 0.014    #mass in kg
CD = 1.3e-3  # drag coefficient
g = 9.81     # acceleration due to gravity
t0 = 0        # initial time
# theta = np.radians(45)   # choose an angle
# x, y = 0,0   # initial positions
# vx0 = v0*np.cos(theta)     # horizontal velocity
# vy0 = v0*np.sin(theta)     # Vertical Velocity
# Initial_State = [x, y, vx0, vy0]        # vector is equal to the initial position in x and y as well as the velocity on x and y

def simulate(angle):
    theta = np.radians(angle)

    x0 = 0
    y0 = 0

    vx0 = v0 * np.cos(theta)
    vy0 = v0 * np.sin(theta)

    Initial_State = [x0, y0, vx0, vy0]

    t, solution, land_range, land_time = rk4(
        wif_ball,
        0,
        Initial_State,
        10,
        0.001
    )

    return land_range, land_time, t, solution

def wif_ball(t, state):
    '''
    t: float?
    state: 4 variable vector
    '''
    x, y, vx, vy = state      
    v = np.sqrt(vx**2 + vy**2)
    dxdt = vx
    dydt = vy
    dvxdt = -(CD/m)*v*vx
    dvydt = -g -(CD/m)*v*vy
    return np.array([dxdt, dydt, dvxdt, dvydt])

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
    
    landing_range = None
    landing_time = None
    
    lastIndex = n
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

            # ------------------------------------------------
        # Check whether the ball has crossed the ground
        # ------------------------------------------------

        previous_y = y[i, 1]
        current_y = y[i + 1, 1]

        if previous_y > 0 and current_y <= 0:

            # --------------------------------------------
            # Interpolate to estimate exact landing point
            # --------------------------------------------

            fraction = previous_y / (previous_y - current_y)

            landing_time = (
                t[i] +
                fraction * (t[i + 1] - t[i])
            )

            landing_range = (
                y[i, 0] +
                fraction * (y[i + 1, 0] - y[i, 0])
            )

            last_index = i + 1

            break
            # Trim arrays so that they only contain
    # values up to the landing point
    t = t[:last_index + 1]
    y = y[:last_index + 1]

    return t, y, landing_range, landing_time
    
# ============================================================
# FIND MAXIMUM RANGE
# ============================================================

angles = np.arange(1, 90, 1)

ranges = []

best_range = 0
best_angle = 0

for angle in angles:

    land_range, land_time, t, solution = simulate(angle)

    ranges.append(land_range)

    if land_range > best_range:
        best_range = land_range
        best_angle = angle


print("Maximum Range Results")
print("-----------------------------")
print(f"Best launch angle: {best_angle:.2f} degrees")
print(f"Maximum range:     {best_range:.4f} m")


# t, solution, land_range, land_time = rk4(wif_ball, 0, Initial_State, 50, 0.001)
# 
# print(t)
# print(solution)
# print(land_range, land_time)