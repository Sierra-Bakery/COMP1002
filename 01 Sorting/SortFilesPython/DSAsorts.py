#
# Data Structures and Algorithms COMP1002
#
# Python file to hold all sorting methods
#

def bubbleSort(A):
    n = len(A)
    # Goes thorugh every arraty element
    for i in range(n):
        # Sort by i element in last place
        moved = False
        for j in range(0, n - i - 1):
            # Move through array from 0 to end and swap if greater than next]
            # swapping simulaineously
            if A[j] > A[j+1]:
                A[j], A[j+1] = A[j+1], A[j]
                moved = True
        if not moved:
            break
    return A
        

def insertionSort(A):
    # Goes through every array element
    for i in range(1, len(A)):
        key = A[i]
        #Move element that are greater than next
        j = i - 1
        while j >= 0 and key < A[j]:
            A[j+1] = A[j]
            j -=1
        A[j+1] = key
    return A 

def selectionSort(A):
    ...

def mergeSort(A):
    """ mergeSort - front-end for kick-starting the recursive algorithm
    """
    ...

def mergeSortRecurse(A, leftIdx, rightIdx):
    ...

def merge(A, leftIdx, midIdx, rightIdx):
    ...

def quickSort(A):
    """ quickSort - front-end for kick-starting the recursive algorithm
    """
    ...

def quickSortRecurse(A, leftIdx, rightIdx):
    ...

def doPartitioning(A, leftIdx, rightIdx, pivotIdx):
    ...


