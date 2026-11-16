import math as m
def Bisection(f, bracket, abs_tol):
    
    xL, xU = bracket
#     iters = m.ceil((m.log((xU - xL)/abs_tol))/m.log(2) - 1)
    fxL = f(xL)
    fxU = f(xU)
    err = abs_tol + 1
    
    while abs_tol < err:
        xR = xU - ((f(xU)*(xL-xU))/(f(xL)-f(xU)))
        fxR = f(xR)
        if fxR == 0:
            break
        elif fxR*fxL < 0:
            xU = xR
            fxU = fxR
        else:
            xL = xR
            fxL = fxR
        err = (abs(xL - xU))/2
        print(xL,xU)
    return xU - ((f(xU)*(xL-xU))/(f(xL)-f(xU)))

if __name__=='__main__':
    def my_func(h):
        V, R = 30, 3
        return (9*m.pi*h**2)-(h**3*m.pi)-90
    #print(my_func(32), my_func(64))
    
    result = Bisection(my_func, (0,6), 0.001)
    print(result, 'depth in m')

