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
        leftIdx = A[:mid]
        rightIdx = A[mid:]
        
        # Sort each half
        mergeSort(leftIdx)
        mergeSort(rightIdx)
        
        # Merge the two sorted blocks
        i=0
        j=0
        k=0
        while i < len(leftIdx) and j < len(rightIdx):
            if leftIdx[i] < rightIdx[j]:
                A[k]    = leftIdx[i]
                i += 1
            else:
                A[k]    = rightIdx[j]
                j += 1
            k += 1
        
        #Add remaining elements on left
        while i < len(leftIdx):
            A[k] = leftIdx[i]
            i += 1
            k += 1
        
        #Add remaining elements on right
        while j < len(rightIdx):
            A[k] = rightIdx[j]
            j += 1
            k += 1
    return A

def mergeSortRecurse(A, leftIdx, rightIdx):
    if leftIdx < rightIdx:
        midIdx = (leftIdx + rightIdx) // 2

        # Recursively sort both halves
        mergeSortRecurse(A, leftIdx, midIdx)
        mergeSortRecurse(A, midIdx + 1, rightIdx)

        # Merge them
        merge(A, leftIdx, midIdx, rightIdx)

def merge(A, leftIdx, midIdx, rightIdx):
    # Create temporary arrays
    left = A[leftIdx:midIdx + 1]
    right = A[midIdx + 1:rightIdx + 1]

    i = 0
    j = 0
    k = leftIdx

    # Merge back into A
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            A[k] = left[i]
            i += 1
        else:
            A[k] = right[j]
            j += 1
        k += 1

    # Remaining elements
    while i < len(left):
        A[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        A[k] = right[j]
        j += 1
        k += 1

def quickSort(A):
    """ quickSort - front-end for kick-starting the recursive algorithm
    """
    quickSortRecurse(A, 0, len(A) - 1)
    return A

def quickSortRecurse(A, leftIdx, rightIdx):
    if leftIdx < rightIdx:
        pivotIdx = (leftIdx + rightIdx) // 2

        # Partition around pivot
        pivotNewIdx = doPartitioning(A, leftIdx, rightIdx, pivotIdx)

        # Recursively sort partitions
        quickSortRecurse(A, leftIdx, pivotNewIdx - 1)
        quickSortRecurse(A, pivotNewIdx + 1, rightIdx)

def doPartitioning(A, leftIdx, rightIdx, pivotIdx):
    pivotValue = A[pivotIdx]

    # Move pivot to end
    A[pivotIdx], A[rightIdx] = A[rightIdx], A[pivotIdx]

    storeIdx = leftIdx

    for i in range(leftIdx, rightIdx):
        if A[i] < pivotValue:
            A[i], A[storeIdx] = A[storeIdx], A[i]
            storeIdx += 1

    # Move pivot to final place
    A[storeIdx], A[rightIdx] = A[rightIdx], A[storeIdx]

    return storeIdx
