import numpy as np #we are using numpy arrays to implement the heap
import sys
class DSAHeapEntry:
    def __init__(self, priority, value): #intializes the heap entry with a priority and a value
        self.priority = priority
        self.value = value
    def getpriority(self):
        return self.priority
    def setPriority(self, priority):
        self.priority = priority
    def getValue(self):
        return self.value
    def setValue(self, value):
        self.value = value
class DSAHeap:
    def __init__(self, maxSize): #initializes the heap with a maximum size and an array to hold the entries
        self._heap = np.empty(maxSize, dtype=object) #using numpy array to hold heapentry objects. This is literally a heap
        self._count = 0
    def addEntry(self, priority, value):
        if self._count == len(self._heap): #handles if the heap is full, outside, the method should be called with a try and except
            raise Exception("Heap is full")
        entry = DSAHeapEntry(priority, value)
        self._heap[self._count] = entry
        self._trickleUp(self._count)
        self._count += 1
    def _trickleUp(self, curIdx):
        parentIdx = (curIdx - 1)//2 #-1 for a reason, both child formulas have a +1 or +2 and need to map back to the parent node
        while curIdx > 0 and self._heap[curIdx].getpriority() > self._heap[parentIdx].getpriority(): #compares the current priority to te parent priority.:
            temp = self._heap[parentIdx]
            self._heap[parentIdx] = self._heap[curIdx]
            self._heap[curIdx] = temp #swap
            curIdx = parentIdx
            parentIdx = (curIdx-1)//2
    def remove(self):
        #root is always HIGHEST PRIORITY
        if self._count == 0: #checks if the heap is empty by checking the count value
            raise Exception("Heap Empty")
        rootVal = self._heap[0] #saves the root value into a temp variable
        self._heap[0] = self._heap[self._count - 1]
        self._count -= 1
        if self._count > 0:
            self._trickleDown(0)
        return rootVal
    def _trickleDown(self, curIdx):
        lChildIdx = curIdx * 2 + 1
        rChildIdx = lChildIdx + 1
        if lChildIdx < self._count: #is a right child
            largeIdx = lChildIdx #stores index of larger child
            if rChildIdx < self._count:
                if self._heap[lChildIdx].getpriority() < self._heap[rChildIdx].getpriority():
                    largeIdx = rChildIdx
            if self._heap[largeIdx].getpriority() > self._heap[curIdx].getpriority(): #swap
                temp = self._heap[largeIdx]
                self._heap[largeIdx] = self._heap[curIdx]
                self._heap[curIdx] = temp
                curIdx = largeIdx
                lChildIdx = curIdx * 2 + 1
                rChildIdx = lChildIdx + 1
            else:
                lChildIdx = self._count
    def display(self):
        for i in range(self._count):
            entry = self._heap[i]
            print("priority: ", entry.getpriority(), "value ", entry.getValue())

def trickleDown(heapArray, curIdx, numItems): #standalone, based on the method from the class, replaces self._count() and the self._heap array
    lChildIdx = curIdx * 2 + 1
    rChildIdx = lChildIdx + 1

    while lChildIdx < numItems:
        largeIdx = lChildIdx

        if rChildIdx < numItems:
            if heapArray[lChildIdx].getpriority() < heapArray[rChildIdx].getpriority():
                largeIdx = rChildIdx

        if heapArray[largeIdx].getpriority() > heapArray[curIdx].getpriority():
            temp = heapArray[largeIdx]
            heapArray[largeIdx] = heapArray[curIdx]
            heapArray[curIdx] = temp

            curIdx = largeIdx
            lChildIdx = curIdx * 2 + 1
            rChildIdx = lChildIdx + 1
        else:
            lChildIdx = numItems



def heapify(heapArray, numItems): #converts array to heap
    for i in range((numItems//2) -1, -1, -1):
        trickleDown(heapArray, i, numItems) # calls the standalone because we can't use the class method outside the class

def heapSort(heapArray, numItems):
    heapify(heapArray, numItems)
    for i in range(numItems - 1, 0, -1): #swaps
        temp = heapArray[0]
        heapArray[0] = heapArray[i]
        heapArray[i] = temp
        trickleDown(heapArray, 0, i)
def main():
    if len(sys.argv) < 2:
        print("Usage: python heap.py RandomNames7000.csv")
        return

    filename = sys.argv[1]

    file = open(filename, "r")

    lines = file.readlines()

    numItems = len(lines)

    heapArray = np.empty(numItems, dtype=object)

    i = 0

    for line in lines:
        line = line.strip()

        parts = line.split(",")

        priority = int(parts[0])
        value = parts[1]

        heapArray[i] = DSAHeapEntry(priority, value)

        i += 1

    file.close()

    heapSort(heapArray, numItems)

    print("First 10 sorted:")
    for i in range(10):
        print(heapArray[i].getpriority(), heapArray[i].getValue())

    print("Last 10 sorted:")
    for i in range(numItems - 10, numItems):
        print(heapArray[i].getpriority(), heapArray[i].getValue())

# NOTE #
# You need to be able to sort the heap then be able to att and remove/ edit values after.
# NOTE #

main()

#testing
#heap = DSAHeap(10)

#heap.addEntry(50, "A")
#heap.addEntry(90, "B")
#heap.addEntry(20, "C")
#heap.addEntry(100, "D")

#heap.display()

#print("Removed:", heap.remove().getpriority())
#heap.display()