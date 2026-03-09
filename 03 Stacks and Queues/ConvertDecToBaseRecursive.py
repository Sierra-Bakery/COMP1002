# algorithm is from a mathstackexchange thread: https://math.stackexchange.com/questions/4568479/general-formula-for-decimal-x-10-to-base-b-conversion
# (modified) string digit idea from javathinking article: https://www.javathinking.com/blog/java-convert-decimal-to-base-recursive/. adapted to python and converted to an array for easier manipulation.

import numpy as np #uses array to store base digits up to 16, in order to comply with prac instructions, as lists are unfortunately not allowed
def dectoBase(a, b):
    digits = np.array(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]) #stores the digits for bases up to 16, as a string for easy output
    if a < b: #base case
        return digits[a]
    else: #recursive case
        return dectoBase(a // b, b) + digits[a % b] #calls function recursively, "//" is used to grab the integer rounded off with no decimals
while True:
    b10decimal = int(input("Enter a base 10 number: "))
    base = int(input("Enter a base to convert to (2-16): "))
    try:
        print(dectoBase(b10decimal, base)) #outputs result
    except (ValueError): #catches invalid value
        print("Invalid input, please try again.")
    except (TypeError): #catches invalid data type
        print("Invalid input, please try again.")