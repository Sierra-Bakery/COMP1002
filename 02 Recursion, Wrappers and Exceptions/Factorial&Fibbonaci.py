#Code inspired by the ones present on the lecture slides, modified to implement error handling
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
def iterative_factorial_get_n(n):
    if n < 0: #basic error handling
        return "factorial does not work with negative numbers"
    result = 1
    for i in range(1, n + 1):
        result = result * i
    return result
def recursive_factorial_get_n(n):
    if n < 0: #basic error handling
        return "factorial does not work with negative numbers"
    if n == 0: #base case, factorial of 0 is 1
        return 1
    else:
        return n * recursive_factorial_get_n(n - 1) #calls the function recursively to calculate the product of n and the factorial of n-1
while True: #loops program, can be exited usinc ctrl  
    try: #attempts to catch invalid input
        factnumber = int(input("Enter a number to calculate its factorial: "))
        fibnumber = int(input("Enter a number to calculate its fibonacci: "))
        print("Calculating fibonacci sequence starting from one ") #the values starting from 0 and 1 are drastically different so this notifies the user
        print("Iterative Fibonacci: " + str(iterative_fibonacci_get_n(fibnumber))) #takes argument for n and executes iteratively
        print("Recursive Fibonacci: " + str(recursive_fibonacci_get_n(fibnumber))) #takes argument for n and execcutes recursively
        print("Iterative Factorial: " + str(iterative_factorial_get_n(factnumber))) #takes argument for n and executes iteratively
        print("Recursive Factorial: " + str(recursive_factorial_get_n(factnumber))) #takes argument for n and executes recursively
    except (ValueError): #catches invalid value
        print("Error: invalid input, please enter a non-negative integer")
    except (TypeError): #catches invalid data type
        print("Error: invalid input for factorial, please enter a non-negative integer")