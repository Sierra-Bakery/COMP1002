def iterative_fibonacci_get_n(n):
    # calculates the nth fibonacci number iteratively
    if n <= 1:
        return n
    #Initialize the first two numbers in the sequence
    x = 0 
    y = 1

    for i in range(2, n+1): #loops from 2nd to the nth number
        z = y #stores the current value of y before updating it
        y = x + y #calculates the next number in the sequence
        x = z #updates x to the previous value of y for the next iteration
    return y
def recursive_fibonacci_get_n(n):
    # calculates the nth fibonacci number recursively
    if n <= 1:
        return n
    return recursive_fibonacci_get_n(n-1) + recursive_fibonacci_get_n(n-2) #calls the function recursively to calculate the sum of the two preceding numbers
print("Iterative: " + str(iterative_fibonacci_get_n(10)))
print("Recursive: " + str(recursive_fibonacci_get_n(10)))