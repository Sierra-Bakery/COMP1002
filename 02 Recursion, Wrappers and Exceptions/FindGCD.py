#implements the Eucleidian algorithm to find the greatest common divisor (denominator) of two numbers
#source: khan academy: https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/the-euclidean-algorithm
def find_gcd(x, y):
    if y == 0: #serves as base case, if y = 0, then the gcd is x
        return x
    else:
        return find_gcd(y, x % y)
while True: #loops program, can be exited using ctrl c
    num1 = int(input("Enter number 1: "))
    num2 = int(input("Enter number 2: "))
    try:
        result = find_gcd(num1, num2) #calls function 
        print("The greatest common denominator of " + str(num1) + " and " + str(num2) + " is: " + str(result))
    except TypeError: #catches invalid data type
        print("Please enter an integer.")
    except ValueError: #catches invalid value
        print("Please enter a valid integer.")
     