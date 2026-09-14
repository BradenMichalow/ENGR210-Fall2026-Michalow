import numpy as np
import matplotlib.pyplot as plt

#finds the three point derivitive
def threePointDeriv(f, x, h):
    '''
    f: callable of a single variable
    x: float
    h: float
    '''
    return ( f(x + h) - f(x - h))/(2*h)

#given cos function from part 1
def myCos_func(x):
    return 2*np.cos(x*np.pi/12)

#given sin function from part 1
def mySin_func(x):
    return 2*np.sin(x*np.pi/12)

# create a step size for the given equation below
step_size = float(input("Please enter your step size: "))

# create an array of points that will have their derivitives calculated and then plotted
derivitive_points = np.linspace(0, 48, 500)

#calculates the deriviative for the sin function above
derivitive = threePointDeriv(mySin_func, derivitive_points, step_size)
#calculates the derivitive for the cos function above
cos_derivitive = threePointDeriv(myCos_func, derivitive_points, step_size)


if __name__ == "__main__":
    #plot the deriviatve and the points derived while labeling graphs for both the sin and cos functions with an amplitude of 2 and period of 24
    plt.figure(1)
    plt.plot(derivitive_points, derivitive)

    plt.xlabel('points derived')
    plt.ylabel('derivitives')
    plt.title('derivation of the sin(x) function')
    plt.grid(True)
    plt.show()
    
    plt.figure(2)
    plt.plot(derivitive_points, cos_derivitive)

    plt.xlabel('points derived')
    plt.ylabel('derivitives')
    plt.title('derivation of the cos(x) function')
    plt.grid(True)
    plt.show()
    
    # for part 2 of problem 2. calculates and graphs error using the computed value and the actual value
    
    step_arr = np.logspace(0, -6, 100)
    err_arr = []
    
    for i in step_arr:
        #calculates computer value
        numerical = threePointDeriv(mySin_func, derivitive_points, i)
        #calculates actual value using the true derivitive of a sin function with an amplitude of 2 and a period of 24
        true = (np.pi/6) * np.cos(derivitive_points* np.pi/12)
        #finds the maximum error
        max_error = np.max(np.abs(numerical - true))
        err_arr.append(max_error)
        
    #plots the error graph
    plt.figure(3)
    plt.loglog(step_arr, err_arr)
    plt.show()