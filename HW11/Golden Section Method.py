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