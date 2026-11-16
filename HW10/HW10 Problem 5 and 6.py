# problem 5 work

    #rearange originol equation for h to get m.sqrt(90 / (m.pi * (9 - h)))
    # take the derivitive to get (90/pi)**1/2*.5*(9-h)**-3/2
    #plug in h=6 to show max convergance to get g'(6) = 0.515
    #this is less than 1 so it works



import math as m

def fixedpoint(g, x_guess, tol):
    err = tol + 1
    while err > tol:
        x_new = g(x_guess)
        err = abs(x_new - x_guess)
        x_guess = x_new
        print(x_guess)
    return x_guess


if __name__ == '__main__':

    def my_func(h):
        V, R = 30, 3
        return m.sqrt(90 / (m.pi * (9 - h)))

    result = fixedpoint(my_func, 6, 0.001)

    print(result, 'depth in m')
