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
    # Goes though every array element
    for i in range(len(A)):
        #Find minimum element in the array
        mini = i
        for j in range(i + 1, len(A)):
            if A[j] < A[mini]:
                mini = j
        # Swap the element simultaneously
        A[i], A[mini] = A[mini], A[i]
    return A

def mergeSort(A):
    """ mergeSort - front-end for kick-starting the recursive algorithm
    """
    if len(A) > 1:
        # Devide into 2 sides
        mid = len(A) // 2
        left_part = A[:mid]
        right_part = A[mid:]
        
        # Sort each half
        mergeSort(left_part)
        mergeSort(right_part)
        
        # Merge the two sorted blocks
        i=0
        j=0
        k=0
        while i < len(left_part) and j < len(right_part):
            if left_part[i] < right_part[j]:
                A[k]    = left_part[i]
                i += 1
            else:
                A[k]    = right_part[j]
                j += 1
            k += 1
        
        #Add remaining elements on left
        while i < len(left_part):
            A[k] = left_part[i]
            i += 1
            k += 1
        
        #Add remaining elements on right
        while j < len(right_part):
            A[k] = right_part[j]
            j += 1
            k += 1
    return A

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


if __name__ == '__main__':
    A = []
    A = [1,45,21,23,34,12,23,43,45,12,34,199]
    print(A)
    AB = bubbleSort(A)
    print(AB)
    A = [1,45,21,23,34,12,23,43,45,12,34,199]
    AI = insertionSort(A)
    print(AI)
    A = [1,45,21,23,34,12,23,43,45,12,34,199]
    AS = selectionSort(A)
    print(AS)
    A = [1,45,21,23,34,12,23,43,45,12,34,199]