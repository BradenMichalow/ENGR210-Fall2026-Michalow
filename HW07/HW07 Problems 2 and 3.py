A = [[2.0, -2.0, 3.0, -3.0],
     [1.0,  1.0, 1.0,  0.0],
     [1.0, -1.0, 2.0, -1.0],
     [1.0, -1.0, 4.0,  3.0]]

B = [-20.0,
      -2.0,            # reordered as Original 1st equation as 3rd, Original 2nd as 1st, Original 3rd as 2nd, and Original last as last still
      -8.0,
       4.0]

n = len(B)
#Gauss Elimination
for k in range(n-1):
    for i in range(k+1, n):
        factor = A[i][k]/A[k][k]
        for j in range(0, n): #could do k+1 to n but that wont show zeros
            A[i][j] = A[i][j] - factor*A[k][j]
        B[i] = B[i] - factor*B[k]
print(A)

#back substitution
B[n-1] = B[n-1]/A[n-1][n-1]
for i in range(n-2, -1,-1):
    sumation = B[i]
    for j in range(i+1, n):
        sumation = sumation - B[j]*A[i][j]
    B[i] = sumation/A[i][i]
print(B)




