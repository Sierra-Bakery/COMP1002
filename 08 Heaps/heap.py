"""
DSA Practical 08 - Heaps
"""

import numpy as np

# DSAHeapEntry
class DSAHeapEntry:
    """Stores a single (priority, value) pair."""

    def __init__(self, priority: int, value: object):
        self._priority = priority
        self._value = value

    # getters and setters
    def getPriority(self) -> int:
        return self._priority

    def setPriority(self, priority: int) -> None:
        self._priority = priority

    def getValue(self) -> object:
        return self._value

    def setValue(self, value: object) -> None:
        self._value = value

    def __repr__(self):
        return f"DSAHeapEntry(priority={self._priority}, value={self._value!r})"


# DSAHeap max heap with a fixed-size array
class DSAHeap:
    """Array-based max-heap.  Larger priority == higher priority."""

    DEFAULT_CAPACITY = 7000  # large enough for RandomNames7000.csv

    def __init__(self, maxSize: int = DEFAULT_CAPACITY):
        # numpy object array so we can store DSAHeapEntry references
        self._heap = np.empty(maxSize, dtype=object)
        self._count = 0

    # interface
    def add(self, priority: int, value: object) -> None:
        """Insert a new entry and restore heap order (trickle-up)."""
        if self._count >= len(self._heap):
            raise OverflowError("Heap is full")
        entry = DSAHeapEntry(priority, value)
        self._heap[self._count] = entry
        self._trickleUp(self._count)
        self._count += 1

    def remove(self) -> DSAHeapEntry:
        """Remove and return the highest-priority entry (root)."""
        if self._count == 0:
            raise IndexError("Heap is empty")
        # Save root
        top = self._heap[0]
        # Move last element to root, shrink count
        self._count -= 1
        self._heap[0] = self._heap[self._count]
        self._heap[self._count] = None      # clear stale reference
        if self._count > 0:
            self._trickleDown(0)
        return top

    def display(self) -> None:
        """Print all entries currently in the heap (in array order)."""
        print(f"Heap ({self._count} entries):")
        for i in range(self._count):
            e = self._heap[i]
            print(f"  [{i}] priority={e.getPriority()}, value={e.getValue()!r}")

    # Private helpers
    def _trickleUp(self, curIdx: int) -> None:
        """Iterative trickle-up: restore heap property after insertion."""
        parentIdx = (curIdx - 1) // 2
        while (curIdx > 0 and
               self._heap[curIdx].getPriority() > self._heap[parentIdx].getPriority()):
            # swap
            temp = self._heap[parentIdx]
            self._heap[parentIdx] = self._heap[curIdx]
            self._heap[curIdx] = temp
            curIdx = parentIdx
            parentIdx = (curIdx - 1) // 2

    def _trickleDown(self, curIdx: int) -> None:
        """Iterative trickle-down: restore heap property after removal."""
        lChildIdx = curIdx * 2 + 1
        rChildIdx = lChildIdx + 1
        keepGoing = True
        while keepGoing and lChildIdx < self._count:
            keepGoing = False
            largeIdx = lChildIdx
            if rChildIdx < self._count:
                if (self._heap[lChildIdx].getPriority() <
                        self._heap[rChildIdx].getPriority()):
                    largeIdx = rChildIdx
            if self._heap[largeIdx].getPriority() > self._heap[curIdx].getPriority():
                # swap
                temp = self._heap[largeIdx]
                self._heap[largeIdx] = self._heap[curIdx]
                self._heap[curIdx] = temp
                keepGoing = True
                curIdx = largeIdx
                lChildIdx = curIdx * 2 + 1
                rChildIdx = lChildIdx + 1

# Stand-alone heap-sort functions (in-place, no extra heap object needed)
def _trickleDownSort(heapArray: np.ndarray, curIdx: int, numItems: int) -> None:
    """Iterative trickle-down used by heapify / heapSort."""
    lChildIdx = curIdx * 2 + 1
    rChildIdx = lChildIdx + 1
    keepGoing = True
    while keepGoing and lChildIdx < numItems:
        keepGoing = False
        largeIdx = lChildIdx
        if rChildIdx < numItems:
            if heapArray[lChildIdx].getPriority() < heapArray[rChildIdx].getPriority():
                largeIdx = rChildIdx
        if heapArray[largeIdx].getPriority() > heapArray[curIdx].getPriority():
            temp = heapArray[largeIdx]
            heapArray[largeIdx] = heapArray[curIdx]
            heapArray[curIdx] = temp
            keepGoing = True
            curIdx = largeIdx
            lChildIdx = curIdx * 2 + 1
            rChildIdx = lChildIdx + 1


def heapify(heapArray: np.ndarray, numItems: int) -> None:
    """Convert an arbitrary array of DSAHeapEntry into a max-heap in-place."""
    # Start at last non-leaf and work backwards
    for ii in range((numItems // 2) - 1, -1, -1):
        _trickleDownSort(heapArray, ii, numItems)


def heapSort(array: np.ndarray, numItems: int) -> None:
    """Sort array of DSAHeapEntry in-place (ascending by priority)."""
    heapify(array, numItems)
    for ii in range(numItems - 1, 0, -1):
        # Swap root (largest) with last unsorted element
        temp = array[0]
        array[0] = array[ii]
        array[ii] = temp
        # Re-heap the reduced array
        _trickleDownSort(array, 0, ii)


# CSV reader  (no split() for whole file processing, no dict/list builtins)
def loadCSV(filename: str) -> tuple:
    """
    Read from file.
    Returns (npArray, count) where npArray is a numpy object array of
    DSAHeapEntry with priority=number, value=name.
    We read character-by-character to avoid split() on the whole file.
    """
    # Pre-allocate generously; we will trim to actual count later.
    MAX_ROWS = 7500
    entries = np.empty(MAX_ROWS, dtype=object)
    count = 0

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            # Strip newline manually
            line = line.rstrip("\n").rstrip("\r")
            if len(line) == 0:
                continue

            commaPos = -1
            for ci in range(len(line)):
                if line[ci] == ",":
                    commaPos = ci
                    break

            if commaPos == -1:
                continue  # malformed line

            numStr = line[:commaPos]
            name   = line[commaPos + 1:]

            # Convert numStr to int manually (handles leading/trailing spaces)
            numStr = numStr.strip()
            priority = 0
            for ch in numStr:
                priority = priority * 10 + (ord(ch) - ord("0"))

            entries[count] = DSAHeapEntry(priority, name)
            count += 1

    return entries, count

def main():
    import sys

    csv_file = "RandomNames7000.csv"
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]

    # HeapSort on Random names
    print(f"PART 2 – HeapSort on {csv_file}")
    print("-------------------------------------------")


    try:
        entries, count = loadCSV(csv_file)
    except FileNotFoundError:
        print(f"  [!] '{csv_file}' not found – skipping HeapSort demo.")
        print("      Place the file in the same directory and re-run.")
        return

    print(f"  Loaded {count} records.")
    print("  First 5 before sort:")
    for i in range(min(5, count)):
        e = entries[i]
        print(f"    [{i}] {e.getPriority():>6}  {e.getValue()}")

    heapSort(entries, count)

    print("  First 5 after HeapSort (ascending by number):")
    for i in range(min(5, count)):
        e = entries[i]
        print(f"    [{i}] {e.getPriority():>6}  {e.getValue()}")

    print("  Last 5 after HeapSort:")
    for i in range(max(0, count - 5), count):
        e = entries[i]
        print(f"    [{i}] {e.getPriority():>6}  {e.getValue()}")

    print(f"\n  HeapSort complete.  {count} records sorted.")


if __name__ == "__main__":
    main()