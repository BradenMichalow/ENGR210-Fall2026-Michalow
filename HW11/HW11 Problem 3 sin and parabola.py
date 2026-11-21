import math as m

def golden_section(f,xL,xU, tol):
    
    R = (m.sqrt(5)-1)/2
    h = xU - xL
    
    x1 = xL + h*R
    x2 = xU - h*R
    
    f1 = f(x1)
    f2 = f(x2)
    
    err = h/2
    
    while err > tol:
        if f1>f2:
            xL = x2
            x2 = x1
            f2 = f1
            
            h = xU - xL
            x1 = xL + h*R
            f1 = f(x1)
            
        else:
            xU = x1
            x1 = x2
            f1 = f2
            
            h = xU - xL
            x2 = xU - h*R
            f2 = f(x2)
            
        err = h/2
        
    return (xU + xL)/2

def parabola(x):
    return -2*x**2 + 8*x + 1

def sin_func(x):
    return m.sin(x)

result1 = golden_section(parabola, 0, 5, 1e-6) # 0, 5 because when plugged into known solution, it makes x= 2
print(result1)
print(parabola(result1))

result2 = golden_section(sin_func, 0, m.pi*2, 1e-6)
print(result2) #pi/2 is approximately 1.57
print(sin_func(result2))

