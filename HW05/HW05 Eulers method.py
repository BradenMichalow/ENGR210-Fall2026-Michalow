import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# 1. DEFINE THE DIFFERENTIAL EQUATION AND EXACT SOLUTION
# =====================================================

# IVP: dy/dt = -y, y(0) = 1

def f(t, y):
    return -y

def exact_solution(t):
    return np.exp(-t)


# =====================================================
# 2. EULER'S METHOD
# =====================================================

def euler_method(y0, t0, T, h):

    N = int(round((T - t0) / h))

    t = np.linspace(t0, T, N + 1)
    y = np.zeros(N + 1)

    # Initial condition
    y[0] = y0

    # Euler iteration
    for n in range(N):
        y[n + 1] = y[n] + h * f(t[n], y[n])

    return t, y


# =====================================================
# 3. INITIAL PARAMETERS
# =====================================================

y0 = 1.0
t0 = 0.0
T = 5.0
h = 0.1

# Stability condition: 0 < h < 2
if not (0 < h < 2):
    raise ValueError("Step size must satisfy 0 < h < 2")


# =====================================================
# 4. COMPUTE NUMERICAL AND EXACT SOLUTIONS
# =====================================================

t, y_num = euler_method(y0, t0, T, h)

y_exact = exact_solution(t)

# RMS error (as defined in the assignment)
rms_error = np.sqrt(
    h * np.sum((y_num[:-1] - y_exact[:-1])**2)
)


# =====================================================
# 5. DISPLAY NUMERICAL RESULTS
# =====================================================

print("========== EULER'S METHOD ==========")
print(f"Initial condition: y(0) = {y0}")
print(f"Final time: T = {T}")
print(f"Time step: h = {h}")
print(f"Number of steps: {len(t) - 1}")

print(f"\nNumerical solution at T = {T}: "
      f"{y_num[-1]:.8f}")

print(f"Exact solution at T = {T}: "
      f"{y_exact[-1]:.8f}")

print(f"RMS error: {rms_error:.8f}")

print("\nStability condition: 0 < h < 2")

if 0 < h < 2:
    print("The selected step size is stable.")


# =====================================================
# 6. PLOT NUMERICAL SOLUTION VS EXACT SOLUTION
# =====================================================

plt.figure(figsize=(8, 5))

plt.plot(t, y_num, 'o-', markersize=3,
         label="Euler numerical solution")

plt.plot(t, y_exact, '-',
         label="Exact solution: exp(-t)")

plt.xlabel("Time t")
plt.ylabel("y(t)")
plt.title("Euler's Method vs Exact Solution")

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# =====================================================
# 7. RMS ERROR AND CONVERGENCE ANALYSIS
# =====================================================

h_values = [0.2, 0.1, 0.05, 0.025, 0.0125]

rms_errors = []

print("\n========== RMS ERROR ANALYSIS ==========")
print(f"{'Step size':<15}{'RMS error':<20}")

for step in h_values:

    t_test, y_test = euler_method(y0, t0, T, step)

    y_true = exact_solution(t_test)

    # RMS error formula from the assignment
    error = np.sqrt(
        step * np.sum((y_test[:-1] - y_true[:-1])**2)
    )

    rms_errors.append(error)

    print(f"{step:<15.5f}{error:<20.10f}")


# =====================================================
# 8. CALCULATE OBSERVED CONVERGENCE ORDER
# =====================================================

log_h = np.log(h_values)
log_error = np.log(rms_errors)

slope, intercept = np.polyfit(log_h, log_error, 1)

print(f"\nObserved convergence order = {slope:.6f}")

if abs(slope - 1.0) < 0.1:
    print("The method demonstrates first-order convergence.")


# =====================================================
# 9. PLOT RMS ERROR VS TIME STEP
# =====================================================

plt.figure(figsize=(8, 5))

plt.loglog(h_values, rms_errors, 'o-',
           label="Euler RMS error")

# Reference line with first-order slope
reference = rms_errors[0] * (
    np.array(h_values) / h_values[0]
)

plt.loglog(h_values, reference, '--',
           label="First-order reference (slope = 1)")

plt.xlabel("Time step h")
plt.ylabel("RMS error")
plt.title("RMS Error vs Time Step")

plt.legend()
plt.grid(True, which="both")
plt.tight_layout()
plt.show()





