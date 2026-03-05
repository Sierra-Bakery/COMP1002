#implements the Eucleidian algorithm to find the greatest common divisor (denominator) of two numbers
#source: khan academy: https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/the-euclidean-algorithm
def find_gcd(x, y):
    if y == 0: #base case: if y is 0, then the gcd is x
        return x
    else:
        return find_gcd(y, x % y)

num1 = int(input("Enter number 1: "))
num2 = int(input("Enter number 2:"))
result = find_gcd(num1, num2) #calls function 
print("The greatest common denominator of " + str(num1) + " and " + str(num2) + " is: " + str(result))
