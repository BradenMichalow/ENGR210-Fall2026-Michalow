
def NewtonRaphson(f, fprime, x0, tol=1e-3, maxiters=1000):
    xguess = x0
    converged = False

    for i in range(maxiters):
        xnew = xguess - f(xguess)/fprime(xguess)
        err = abs(xnew - xguess)
        xguess = xnew

        if err < tol:
            converged = True
            break

    return xguess, converged


if __name__ == '__main__':
    import math as m

    def my_func(h):
        return 9*m.pi*h**2 - m.pi*h**3 - 90

    def my_func_prime(h):
        return 18*m.pi*h - 3*m.pi*h**2

    result = NewtonRaphson(my_func, my_func_prime, 3)

    print(result, 'depth in m')
