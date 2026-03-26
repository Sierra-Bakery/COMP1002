import numpy as np


# ===========================================================================
# Base class
# ===========================================================================

class DSAQueue:
    """
    Abstract base class for a general-purpose Queue (First-In, First-Out).

    HOW A QUEUE WORKS
    -----------------
    Think of a queue like a line of people waiting at a shop counter.
    New people join at the REAR (back) of the line, and the person at
    the FRONT is served (removed) first.  This is called FIFO
    (First-In, First-Out) — the first item added is always the first
    one removed.

    Key operations:
      enqueue  — add an item to the REAR
      dequeue  — remove and return the item at the FRONT
      peek     — look at the front item without removing it

    WHY AN ABSTRACT BASE CLASS?
    ---------------------------
    There are two common ways to implement a queue with an array:
      1. ShufflingQueue  — simple but slow (O(n) per dequeue)
      2. CircularQueue   — more clever and fast (O(1) per dequeue)

    Both share the same interface (enqueue / dequeue / peek) and the
    same internal array.  We put the shared code here in the base class
    and let each subclass supply only what differs.

    INTERNAL STORAGE
    ----------------
    A fixed-size numpy dtype=object array.  dtype=object means any Python
    value can be stored, making this a general-purpose structure.
    _count tracks how many real items are currently in the queue.

    Restrictions honoured
    ---------------------
    * No built-in pop()  – removal done via index arithmetic.
    * No list[]          – backing store is a numpy dtype=object array.
    * No del             – vacated slots are cleared by setting to None.
    """

    DEFAULT_CAPACITY = 100

    # ------------------------------------------------------------------
    # Constructor
    # ------------------------------------------------------------------

    def __init__(self, capacity=DEFAULT_CAPACITY):
        """
        Initialise the shared state used by both queue subclasses.

        Parameters
        ----------
        capacity : int
            Maximum number of elements the queue can hold.

        What happens here
        -----------------
        1. Store the capacity for overflow/underflow checks.
        2. Allocate a fixed-size numpy object array.
        3. Set _count to 0  →  queue starts empty.

        Note: subclasses call super().__init__(capacity) to run this code
        before adding their own extra setup.
        """
        self._capacity = capacity

        # Allocate the backing array.  Every slot can hold any Python object
        # because dtype=object.  The array size never changes at runtime —
        # we manage logical size via _count (and _front/_rear in CircularQueue).
        self._array = np.empty(self._capacity, dtype=object)

        # _count tracks the number of items currently stored.
        # Keeping this explicitly avoids tricky edge cases when distinguishing
        # "queue is full" from "queue is empty" purely from front/rear indices.
        self._count = 0

    # ------------------------------------------------------------------
    # State-query helpers  (shared by both subclasses)
    # ------------------------------------------------------------------

    def get_count(self):
        """
        Return the number of items currently in the queue.

        _count is updated by enqueue (incremented) and dequeue (decremented)
        so it always reflects the true number of stored elements.
        """
        return self._count

    def is_empty(self):
        """
        Return True if the queue contains no items.

        We check _count == 0 rather than comparing front and rear indices
        because that index comparison becomes ambiguous in a circular queue
        (the same front == rear condition can mean EITHER empty OR full).
        """
        return self._count == 0

    def is_full(self):
        """
        Return True if the queue has reached its maximum capacity.

        When _count equals _capacity there is no room for another element.
        """
        return self._count == self._capacity

    # ------------------------------------------------------------------
    # Abstract interface — subclasses MUST override these
    # ------------------------------------------------------------------

    def enqueue(self, value):
        """
        Add *value* to the rear of the queue.
        Subclasses must provide a concrete implementation.
        """
        raise NotImplementedError("Subclasses must implement enqueue().")

    def dequeue(self):
        """
        Remove and return the item at the front of the queue.
        Subclasses must provide a concrete implementation.
        """
        raise NotImplementedError("Subclasses must implement dequeue().")

    def peek(self):
        """
        Return (without removing) the item at the front of the queue.
        Subclasses must provide a concrete implementation.
        """
        raise NotImplementedError("Subclasses must implement peek().")

    def __str__(self):
        """Return a human-readable string of the queue contents."""
        raise NotImplementedError("Subclasses must implement __str__().")


# ===========================================================================
# Subclass 1 — Shuffling Queue
# ===========================================================================

class ShufflingQueue(DSAQueue):
    """
    A queue that keeps the front element at index 0 at all times.

    HOW IT WORKS
    ------------
    Items are always added to the rear (index _count) and removed from
    the front (index 0).  After removing the front element every remaining
    item is shifted one position toward index 0 so the front is always at
    index 0.

    Diagram — enqueue A, B, C  then dequeue:

        After enqueue(A):  [A, _, _, _]   _count=1
        After enqueue(B):  [A, B, _, _]   _count=2
        After enqueue(C):  [A, B, C, _]   _count=3
        After dequeue():   returns A
                           shuffle: B→[0], C→[1]
                           [B, C, _, _]   _count=2

    TRADE-OFF
    ---------
    Simple to understand, but the shuffle is O(n) — if there are 1000
    items in the queue, a single dequeue causes 999 copy operations.
    The CircularQueue solves this inefficiency.

    Inherits
    --------
    All of __init__, get_count, is_empty, is_full from DSAQueue.
    """

    def __init__(self, capacity=DSAQueue.DEFAULT_CAPACITY):
        """
        Create an empty ShufflingQueue.

        We call super().__init__() to run DSAQueue's constructor, which
        sets up the shared numpy array and _count.  No extra fields are
        needed here because the front is always at index 0.
        """
        super().__init__(capacity)

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def enqueue(self, value):
        """
        Add *value* to the rear of the queue.

        How it works
        ------------
        Because we always keep the array packed from index 0, the rear
        is always at index _count.  We write there and then increment
        _count to record the new size.

        Example — queue currently holds [A, B],  _count = 2:
            Write value at index 2  →  [A, B, value]
            Increment _count        →  _count = 3

        Parameters
        ----------
        value : any
            The item to add to the rear.

        Raises
        ------
        Exception if the queue is already full.
        """
        if self.is_full():
            raise Exception("Queue is full – cannot enqueue.")

        # Place the new item at the first free slot (index _count)
        self._array[self._count] = value

        # Update _count to reflect the queue now has one more item
        self._count += 1

    def dequeue(self):
        """
        Remove and return the item at the front (index 0) of the queue,
        then shuffle every remaining item one slot towards index 0.

        How the shuffle works
        ---------------------
        After grabbing the front value, we use a while-loop to copy each
        element at index i+1 down to index i.  This effectively moves the
        whole queue one step to the left.  Finally we:
          - decrement _count  (one fewer item)
          - set the now-vacant last slot to None  (clean up)

        Example — queue holds [A, B, C],  _count = 3:
            Save array[0]  →  value = A
            Shuffle:  array[0]=B,  array[1]=C
            _count becomes 2
            array[2] = None  (clear old tail)
            Result: [B, C, None, ...]   return A

        Why this is O(n)
        ----------------
        Every dequeue has to touch every remaining element in the array
        to shift it.  For a queue with n elements that is n-1 copies —
        far more work than the CircularQueue's single-step advance.

        Returns
        -------
        The item that was at the front of the queue.

        Raises
        ------
        Exception if the queue is empty.
        """
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
        """
        Return (without removing) the item at the front of the queue.

        Because we always keep items packed from index 0, the front
        element is always at index 0.  We simply return it without
        modifying anything.

        Returns
        -------
        The item at the front of the queue.

        Raises
        ------
        Exception if the queue is empty.
        """
        if self.is_empty():
            raise Exception("Queue is empty – no front element.")

        # Front is always at index 0 in the shuffling queue
        return self._array[0]

    # ------------------------------------------------------------------
    # String representation
    # ------------------------------------------------------------------

    def __str__(self):
        """
        Return a human-readable string showing queue contents front to rear.

        We walk indices 0 .. _count-1 (the valid items) and build up a
        single string with manual concatenation — no list or join().

        Example output:  "ShufflingQueue (front->rear): [A, B, C]"
        """
        parts = ""
        for i in range(self._count):
            if i > 0:
                parts += ", "
            parts += str(self._array[i])
        return "ShufflingQueue (front->rear): [" + parts + "]"


# ===========================================================================
# Subclass 2 — Circular Queue
# ===========================================================================

class CircularQueue(DSAQueue):
    """
    A queue that avoids the shuffle by treating the array as a circle.

    THE CORE IDEA
    -------------
    Instead of always keeping the front at index 0 (like ShufflingQueue),
    we let the front "chase" the rear around the array.  We track two
    index pointers:

      _front — index of the element to dequeue NEXT
      _rear  — index where the NEXT enqueue will write

    After each operation we advance the relevant pointer by 1, but we
    use the modulo operator (%) to wrap back to 0 when we reach the end
    of the array.  This makes the array behave like a circle.

    Both enqueue and dequeue are O(1) — no shifting needed at all.

    Diagram (capacity = 5, showing indices 0-4):

        Start:         [_, _, _, _, _]   front=0  rear=0  count=0
        enqueue(A):    [A, _, _, _, _]   front=0  rear=1  count=1
        enqueue(B):    [A, B, _, _, _]   front=0  rear=2  count=2
        enqueue(C):    [A, B, C, _, _]   front=0  rear=3  count=3
        dequeue()→A:   [_, B, C, _, _]   front=1  rear=3  count=2
        dequeue()→B:   [_, _, C, _, _]   front=2  rear=3  count=1
        enqueue(D):    [_, _, C, D, _]   front=2  rear=4  count=2
        enqueue(E):    [_, _, C, D, E]   front=2  rear=0  count=3
          ↑ rear wraps to 0 (modulo 5)
        enqueue(F):    [F, _, C, D, E]   front=2  rear=1  count=4
        dequeue()→C:   [F, _, _, D, E]   front=3  rear=1  count=3

    WHY TRACK _count SEPARATELY?
    ----------------------------
    When front == rear, it could mean the queue is EMPTY (just drained)
    OR FULL (completely filled).  Keeping _count avoids this ambiguity —
    we only need to look at _count to know the difference.

    Inherits
    --------
    All of __init__, get_count, is_empty, is_full from DSAQueue.
    """

    def __init__(self, capacity=DSAQueue.DEFAULT_CAPACITY):
        """
        Create an empty CircularQueue.

        Calls the parent constructor to set up the shared array and _count,
        then adds the two extra index pointers specific to circular operation.

        _front  — starts at 0; moves forward on each dequeue
        _rear   — starts at 0; moves forward on each enqueue
        Both wrap around using modulo when they reach _capacity.
        """
        super().__init__(capacity)

        # _front is the index of the oldest item (the one to dequeue next).
        # It advances by 1 (mod capacity) on every dequeue.
        self._front = 0

        # _rear is the index where the next item will be written.
        # It advances by 1 (mod capacity) on every enqueue.
        self._rear = 0

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def enqueue(self, value):
        """
        Add *value* to the rear of the circular queue.

        How it works
        ------------
        1. Write the value at index _rear.
        2. Advance _rear by 1, wrapping with modulo so it cycles back
           to 0 if it would go past the end of the array.
        3. Increment _count.

        The modulo wrap is the key to the circular behaviour:
            new_rear = (old_rear + 1) % capacity

        Example (capacity = 4, rear is currently at index 3):
            Write value at array[3]
            _rear = (3 + 1) % 4 = 0   ← wraps back to the start!
            _count += 1

        Parameters
        ----------
        value : any
            The item to add to the rear.

        Raises
        ------
        Exception if the queue is already full.
        """
        if self.is_full():
            raise Exception("Queue is full – cannot enqueue.")

        # Write at the current rear position
        self._array[self._rear] = value

        # Advance rear, wrapping around to 0 if we've reached the end
        self._rear = (self._rear + 1) % self._capacity

        # One more item is now in the queue
        self._count += 1

    def dequeue(self):
        """
        Remove and return the item at the front of the circular queue.

        How it works
        ------------
        1. Read the value at index _front.
        2. Clear that slot (set to None).
        3. Advance _front by 1, wrapping with modulo.
        4. Decrement _count.

        There is NO shuffling — we simply move the front pointer forward.
        This makes dequeue O(1) regardless of queue size.

        Example (capacity = 4, front is currently at index 3):
            value = array[3]
            array[3] = None
            _front = (3 + 1) % 4 = 0   ← wraps back to the start
            _count -= 1

        Returns
        -------
        The item that was at the front of the queue.

        Raises
        ------
        Exception if the queue is empty.
        """
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
        """
        Return (without removing) the item at the front of the queue.

        Unlike the ShufflingQueue where the front is always at index 0,
        here the front can be anywhere in the array — we use _front to
        find it.  No modification to _front, _rear, or _count.

        Returns
        -------
        The item at the front of the queue.

        Raises
        ------
        Exception if the queue is empty.
        """
        if self.is_empty():
            raise Exception("Queue is empty – no front element.")

        # _front always points to the oldest item in the queue
        return self._array[self._front]

    # ------------------------------------------------------------------
    # String representation
    # ------------------------------------------------------------------

    def __str__(self):
        """
        Return a human-readable string showing queue contents front to rear.

        Because the items might wrap around the end of the physical array,
        we cannot simply iterate from 0 to _count.  Instead we compute the
        LOGICAL index for position i as:

            physical_index = (_front + i) % _capacity

        This correctly handles wrap-around — for example, if _front = 3
        and capacity = 4, logical positions 0, 1, 2 map to physical
        indices 3, 0, 1 respectively.

        Example output:  "CircularQueue (front->rear): [C, D, E, F]"
        """
        parts = ""
        for i in range(self._count):
            # Compute where the i-th logical element actually sits in the array
            idx = (self._front + i) % self._capacity
            if i > 0:
                parts += ", "
            parts += str(self._array[idx])
        return "CircularQueue (front->rear): [" + parts + "]"
