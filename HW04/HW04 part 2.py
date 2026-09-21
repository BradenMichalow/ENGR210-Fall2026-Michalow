import numpy as np
import matplotlib.pyplot as plt

def Trap_int(x, x_i, y, y_i):
    
    Int_sum = ((y_i + y) *0.5) * (x_i - x)
    
    return Int_sum

data = np.loadtxt(r'C:/Users/brade/Downloads/ENGR210 Fa2026 HW04 Prob2 Data.csv',
                  delimiter=',',
                  skiprows =1)

data = np.array(data)

y_values = data[:,0]
x_values = data[:,1]
length = len(data)
# print(length)
# print(data)
# print(y_values)
# print(x_values)
Overall_sum = 0
for i in range(length - 1):
    
    integral_sum = Trap_int(x_values[i], x_values[i+1], y_values[i], y_values[i +1])
    Overall_sum += integral_sum
    
print(Overall_sum)
    
plt.figure(1)
plt.plot(data[:,1], data[:,0])
plt.show()

    
    

