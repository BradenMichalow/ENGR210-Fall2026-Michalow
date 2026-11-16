# Problem 1 work
    
    #Bracket is [0,6]m. the min and max of the liquid volume possible in the container

# Problem 2 work
#     v= pi*(h**2)*((3*R-h)/3)
#     where R = 3 and h is varied


# 1st iteration

#     h = (0+6)/2 = 3
#     v= pi*(3**2)*((3*3-3)/3) = 18 pi = 56.54

#2nd iteration

    #56.54>30 so replace 6 with 3

    #[0,3]
    #(0+3)/2 = 1.5
    #v=pi*1.5**2*((3*3-1.5)/3) = 5.625pi = 17.76

#3rd iteration
    #[1.5,3]
    #(1.5+4.5)/2 = 2.25
    #v=pi*2.25**2*((3*3-2.25)/3) = 11.39pi = 35.78



import math as m
def Bisection(f, bracket, abs_tol):
    
    xL, xU = bracket
    iters = m.ceil((m.log((xU - xL)/abs_tol))/m.log(2) - 1)
    fxL = f(xL)
    fxU = f(xU)
    
    for i in range(iters):
        xR = (xL + xU)/2
        fxR = f(xR)
        if fxR == 0:
            break
        elif fxR*fxL < 0:
            xU = xR
            fxU = fxR
        else:
            xL = xR
            fxL = fxR
        print(xL,xU)
    
    return (xL +xU)/2

if __name__=='__main__':
    def my_func(h):
        V, R = 30, 3
        return (9*m.pi*h**2)-(h**3*m.pi)-90
    #print(my_func(32), my_func(64))
    
    result = Bisection(my_func, (0,6), 0.001)
    print(result, 'depth in m')
