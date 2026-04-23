#Not using numpy for implementation as its not necessary as we have linked lists
from DSALL import DSALinkedList, DSAListNode

# Base class

class DSAQueue:

    DEFAULT_CAPACITY = 100
    # Constructor

    def __init__(self, capacity=DEFAULT_CAPACITY):
        self._capacity = capacity

        # Allocate the backing array.  Every slot can hold any Python object
        # because dtype=object.  The array size never changes at runtime —
        # we manage logical size via _count (and _front/_rear in CircularQueue).
        self._array = np.empty(self._capacity, dtype=object)

        # _count tracks the number of items currently stored.
        # Keeping this explicitly avoids tricky edge cases when distinguishing
        # "queue is full" from "queue is empty" purely from front/rear indices.
        self._count = 0

    # State-query helpers  (shared by both subclasses)

    def get_count(self):
        return self._count

    def is_empty(self):
        return self._count == 0

    def is_full(self):
        return self._count == self._capacity

    # Abstract interface — subclasses MUST override these

    def enqueue(self, value):
        raise NotImplementedError("Subclasses must implement enqueue().")

    def dequeue(self):
        raise NotImplementedError("Subclasses must implement dequeue().")

    def peek(self):
        raise NotImplementedError("Subclasses must implement peek().")

    def __str__(self):
        raise NotImplementedError("Subclasses must implement __str__().")


# Subclass 1 — Shuffling Queue

class ShufflingQueue(DSAQueue):

    def __init__(self, capacity=DSAQueue.DEFAULT_CAPACITY):
        super().__init__(capacity)

    # Core operations

    def enqueue(self, value):
        if self.is_full():
            raise Exception("Queue is full – cannot enqueue.")

        # Place the new item at the first free slot (index _count)
        self._array[self._count] = value

        # Update _count to reflect the queue now has one more item
        self._count += 1

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue is empty – cannot dequeue.")

        # Save the front element so we can return it after the shuffle
        value = self._array[0]

        # Shift every element one position toward the front.
        # We start at index 0 and copy from index 1, 2, … _count-1
        # down to 0, 1, … _count-2  respectively.
        i = 0
        while i < self._count - 1:
            self._array[i] = self._array[i + 1]
            i += 1

        # One fewer item in the queue
        self._count -= 1

        # The old last slot is now a duplicate — clear it so we don't
        # hold a stale reference.  We use assignment rather than del.
        self._array[self._count] = None

        return value

    def peek(self):
        if self.is_empty():
            raise Exception("Queue is empty – no front element.")

        # Front is always at index 0 in the shuffling queue
        return self._array[0]

    # ------------------------------------------------------------------
    # String representation
    # ------------------------------------------------------------------

    def __str__(self):
        parts = ""
        for i in range(self._count):
            if i > 0:
                parts += ", "
            parts += str(self._array[i])
        return "ShufflingQueue (front->rear): [" + parts + "]"


# Subclass 2 — Circular Queue

class CircularQueue(DSAQueue):
    """
    The queue that avoids the shuffle by treating the array as a circle.
    Instead of always keeping the front at index 0 (ShufflingQueue),
    let the front "chase" the rear around the array. track two
    index pointers:
    """

    def __init__(self, capacity=DSAQueue.DEFAULT_CAPACITY):
        super().__init__(capacity)

        # _front is the index of the oldest item (the one to dequeue next).
        # It advances by 1 (mod capacity) on every dequeue.
        self._front = 0

        # _rear is the index where the next item will be written.
        # It advances by 1 (mod capacity) on every enqueue.
        self._rear = 0

    # Core operations

    def enqueue(self, value):
        if self.is_full():
            raise Exception("Queue is full – cannot enqueue.")

        # Write at the current rear position
        self._array[self._rear] = value

        # Advance rear, wrapping around to 0 if we've reached the end
        self._rear = (self._rear + 1) % self._capacity

        # One more item is now in the queue
        self._count += 1

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue is empty – cannot dequeue.")

        # Grab the front value before we move the pointer
        value = self._array[self._front]

        # Clear the slot we are vacating (avoids holding stale references)
        self._array[self._front] = None

        # Advance front, wrapping around if needed
        self._front = (self._front + 1) % self._capacity

        # One fewer item in the queue
        self._count -= 1

        return value

    def peek(self):
        if self.is_empty():
            raise Exception("Queue is empty – no front element.")

        # _front always points to the oldest item in the queue
        return self._array[self._front]

    # String representation

    def __str__(self):
        parts = ""
        for i in range(self._count):
            # Compute where the i-th logical element actually sits in the array
            idx = (self._front + i) % self._capacity
            if i > 0:
                parts += ", "
            parts += str(self._array[idx])
        return "CircularQueue (front->rear): [" + parts + "]"
