import numpy as np
import matplotlib.pyplot as plt

#functions to be integrated
def xsq(x):
    return x**2

def sin_func(x):
    return np.sin(x)

def cos_func(x):
    return np.cos(x)

def Trapazoid_integral(f, a, b, N):
    
    #calculate step size
    h = (b-a)/N
    
    # limit integral terms
    Int_Sum = (f(a) + f(b))/2
    
    # middle integral terms
    for i in range(1, N):
        count = a + i*h
        Int_Sum += f(count)
        
    return Int_Sum*h
    
#chosen upper and lower limit
Upper_Lim = 5
Lower_Lim = 0

#chosen trapazoid count
Trap_count = 20

xsq_sum = Trapazoid_integral(xsq, Lower_Lim, Upper_Lim, Trap_count)
sin_sum = Trapazoid_integral(sin_func, Lower_Lim, Upper_Lim, Trap_count)
cos_sum = Trapazoid_integral(cos_func, Lower_Lim, Upper_Lim, Trap_count)

# print out sums
# print("The Sum of x squared is ", xsq_sum)
# print("The Sum of sin(x) is ", sin_sum)
# print("The Sum of cos(x) is ", cos_sum)


#verifications and graphs
if __name__ == "__main__":
    
    
    # Verification 1: proving it functions as it would with a variable limit
    
    
    #array to simulate the variable 'x' in the upper limit
    x_values = np.linspace(0, 2*np.pi, 100)
    
    #create arrays for graphs
    computed_Trap_Sin_values = []
    exact_integral_Sin_values = []
    computed_Trap_Cos_values = []
    exact_integral_Cos_values = []
    
    for i in x_values:
        
        # find the trapzoid value for sin x limit values
        Computed_Trap_Sin_Value = Trapazoid_integral(sin_func, 0, i, Trap_count)
        computed_Trap_Sin_values.append(Computed_Trap_Sin_Value)
        
        # find the trapazoid value for cos x limit values
        Computed_Trap_Cos_Value = Trapazoid_integral(cos_func, 0, i, Trap_count)
        computed_Trap_Cos_values.append(Computed_Trap_Cos_Value)
         
        # evaluation of an actual definite integral for sinx
        Actual_Sin_Integral = (-np.cos(i)) - (-np.cos(Lower_Lim))
        exact_integral_Sin_values.append(Actual_Sin_Integral)
        
        Actual_cos_Integral = np.sin(i) - np.sin(Lower_Lim)
        exact_integral_Cos_values.append(Actual_cos_Integral)
        
    # graph for sin integral
    plt.figure(1)
    plt.plot(x_values, computed_Trap_Sin_values, label='Trapazoid sin value', color='r', linestyle='--')
    plt.plot(x_values, exact_integral_Sin_values, label='actual definite integral', color='b', linestyle='-.')
    plt.xlabel("Variable x for upper limit")
    plt.ylabel("Integral output")
    plt.legend()
#     plt.show()
    
    #graph for cos integral
    plt.figure(2)
    plt.plot(x_values, computed_Trap_Cos_values, label='Trapazoid cos value', color='r', linestyle='--')
    plt.plot(x_values, exact_integral_Cos_values, label='actual definite integral', color='b', linestyle='-.')
    plt.xlabel("Variable x for upper limit")
    plt.ylabel("Integral output")
    plt.legend()
#     plt.show()
    
    
    #verification 2: finding the truncation error (gets more accurate as h rises (step size))
    
    sin_two = Trapazoid_integral(sin_func, 0, np.pi, 100)
    sin_zero = Trapazoid_integral(sin_func, 0, 2*np.pi, 100)
    cos_one = Trapazoid_integral(cos_func, 0, np.pi/2, 100)
    cos_zero = Trapazoid_integral(cos_func, 0, np.pi, 100)
     
    print("integral of sin from 0 to pi is ", sin_two)
    print("integral of sin from 0 to 2 pi is ", sin_zero)
    print("integral of cos from 0 to pi/2 is ", cos_one)
    print("integral of cos from 0 to pi is ", cos_zero)
    
    # for sin_two
    
    #calculated exact vaule for this integral would be... (cos pi equals -1 and cos 0 = 1 which equals 2)
    exact_value_sin_two = 2
    exact_value_sin_zero = 0
    exact_value_cos_one = 1
    exact_value_cos_zero = 0
    
    #create arrays to append to/ simulate changing trapazoid count (and therefore changing step size)
    N_arr = [4, 8, 16, 32, 64, 128, 256]
    h_to_pi = []
    h_to_halfpi = []
    h_to_doublepi = []
    err_sin_two = []
    err_sin_zero = []
    err_cos_one = []
    err_cos_zero = []
    
    for i in N_arr:
        
        #calculate each h
        h_to_pi_list = (np.pi-0)/ i
        h_to_pi.append(h_to_pi_list)
        
        h_to_halfpi_list = ((np.pi/2)-0)/ i
        h_to_halfpi.append(h_to_halfpi_list)
        
        h_to_doublepi_list = ((np.pi*2)-0)/i
        h_to_doublepi.append(h_to_doublepi_list)
        
        #get the integrals for each set of steps and trapazoids
        computed_value_sin_two = Trapazoid_integral(sin_func, 0, np.pi, i)
        computed_value_sin_zero = Trapazoid_integral(sin_func, 0, 2*np.pi, i)
        computed_value_cos_one = Trapazoid_integral(cos_func, 0, np.pi/2, i)
        computed_value_cos_zero = Trapazoid_integral(cos_func, 0, np.pi, i)
        
        #get the difference with this error
        error_sin_two = abs(computed_value_sin_two - exact_value_sin_two)
        error_sin_zero = abs(computed_value_sin_zero - exact_value_sin_zero)
        error_cos_one = abs(computed_value_cos_one - exact_value_cos_one)
        error_cos_zero = abs(computed_value_cos_zero - exact_value_cos_zero)
        
        err_sin_two.append(error_sin_two)
        err_sin_zero.append(error_sin_zero)
        err_cos_one.append(error_cos_one)
        err_cos_zero.append(error_cos_zero)
        
    #graph it
    plt.figure(3)
    plt.loglog(h_to_pi, err_sin_two, label='error for sin 0-pi', color='darkkhaki')
    plt.loglog(h_to_doublepi, err_sin_zero, label='error for sin 0-2pi', color='magenta')
    plt.loglog(h_to_halfpi, err_cos_one, label='error for cos 0-pi/2', color='blue')
    plt.loglog(h_to_pi, err_cos_zero, label='error for cos 0-pi', color='red')
    plt.xlabel('step sizes due to N')
    plt.ylabel('error from exact and computed')
    plt.show()
    