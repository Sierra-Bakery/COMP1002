# the formula for the number of moves is 2^n - 1, where n is the number of disks
# source: https://www.geeksforgeeks.org/python/python-program-for-tower-of-hanoi/
# multiple functions are used because it makes things much simpler
def moveDisk(n, src, dest, level): #function moves the 
    indent = ""
    i = 1
    while i < level:
        indent = indent + "    " # "blank" string, allows indentation for each level of recursion
        i = i + 1

    print(indent + "Recursion Level=" + str(level)) #prints the current level of recursion
    print(indent + "Moving Disk " + str(n) + " from Source " + str(src) + " to Destination " + str(dest))
    print(indent + "n=" + str(n) + ", src=" + str(src) + ", dest=" + str(dest))

def towers(n, src, dest, level): 
    aux = 6 - src - dest

    if n == 1: #base case, if theres only 1 disk the problem is trivial
        moveDisk(n, src, dest, level)
    else:
        towers(n-1, src, aux, level+1) #moves the top n-1 disks from source to auxiliary becaues you can only remove the top disk
        moveDisk(n, src, dest, level) #then the nth disk is moved from source to destination
        towers(n-1, aux, dest, level+1)

n = int(input("Enter number of disks: "))
towers(n, 1, 3, 1)
print("There are " + str((2 ** n) - 1) + " moves for this problem.")





