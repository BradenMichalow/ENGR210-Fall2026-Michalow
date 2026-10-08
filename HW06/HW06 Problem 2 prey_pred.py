import numpy as np
import matplotlib.pyplot as plt

# Parameters
kgrowth = 0.3
kpredation = 0.01
kdeath = 0.2
khunt = 0.0003

# Initial conditions
prey0 = 700
predator0 = 22

# Time step: 1 month = 1/12 year
dt = 1/12

# Simulate for 50 years
years = 50
N = int(years / dt) + 1

t = np.arange(N) * dt

# -------------------------------------------------
# Define the Lotka-Volterra equations
# -------------------------------------------------

def derivatives(prey, predator):

    dprey = (kgrowth * prey
             - kpredation * prey * predator)

    dpredator = (-kdeath * predator
                 + khunt * prey * predator)

    return dprey, dpredator


# =================================================
# EULER METHOD
# =================================================

prey_euler = np.zeros(N)
predator_euler = np.zeros(N)

prey_euler[0] = prey0
predator_euler[0] = predator0

for i in range(N - 1):

    dprey, dpredator = derivatives(
        prey_euler[i],
        predator_euler[i]
    )

    prey_euler[i+1] = (
        prey_euler[i] + dt * dprey
    )

    predator_euler[i+1] = (
        predator_euler[i] + dt * dpredator
    )


# =================================================
# HEUN'S METHOD
# =================================================

prey_heun = np.zeros(N)
predator_heun = np.zeros(N)

prey_heun[0] = prey0
predator_heun[0] = predator0

for i in range(N - 1):

    # ---- First slope ----
    dprey1, dpredator1 = derivatives(
        prey_heun[i],
        predator_heun[i]
    )

    # ---- Euler prediction ----
    prey_predict = (
        prey_heun[i] + dt * dprey1
    )

    predator_predict = (
        predator_heun[i] + dt * dpredator1
    )

    # ---- Second slope ----
    dprey2, dpredator2 = derivatives(
        prey_predict,
        predator_predict
    )

    # ---- Average slopes ----
    prey_heun[i+1] = (
        prey_heun[i]
        + dt * (dprey1 + dprey2) / 2
    )

    predator_heun[i+1] = (
        predator_heun[i]
        + dt * (dpredator1 + dpredator2) / 2
    )


# =================================================
# PLOT 1: PREY VS TIME
# =================================================

plt.figure(figsize=(9,5))

plt.plot(t, prey_euler, label="Euler")
plt.plot(t, prey_heun, '--', label="Heun")

plt.xlabel("Time (years)")
plt.ylabel("Prey population")
plt.title("Prey Population vs Time")
plt.legend()
plt.grid()

plt.show()


# =================================================
# PLOT 2: PREDATORS VS TIME
# =================================================

plt.figure(figsize=(9,5))

plt.plot(t, predator_euler, label="Euler")
plt.plot(t, predator_heun, '--', label="Heun")

plt.xlabel("Time (years)")
plt.ylabel("Predator population")
plt.title("Predator Population vs Time")
plt.legend()
plt.grid()

plt.show()


# =================================================
# PLOT 3: STATE SPACE
# =================================================

plt.figure(figsize=(7,6))

plt.plot(
    prey_euler,
    predator_euler,
    label="Euler"
)

plt.plot(
    prey_heun,
    predator_heun,
    '--',
    label="Heun"
)

plt.xlabel("Prey population")
plt.ylabel("Predator population")
plt.title("Predator vs Prey")
plt.legend()
plt.grid()

plt.show()