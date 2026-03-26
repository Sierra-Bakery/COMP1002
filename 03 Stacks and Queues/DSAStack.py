import numpy as np


class DSAStack:
    """
    A general-purpose Stack (Last-In, First-Out) data structure.

    HOW A STACK WORKS
    -----------------
    Think of a stack like a stack of plates.  You can only ever:
      - Put a new plate on TOP  (push)
      - Take the top plate OFF  (pop)
      - Look at the top plate without removing it  (top / peek)

    The last item you pushed on is always the first one you get back — this
    is called LIFO (Last-In, First-Out).

    INTERNAL STORAGE
    ----------------
    Internally we use a fixed-size numpy array of dtype=object.
    Using dtype=object means the array can hold ANY Python value
    (integers, strings, floats, characters, other objects …) — just
    like an Object[] array in Java.  This makes the stack "general-purpose".

    We track how many real items are in the stack with the integer _count.
    The valid elements always live at indices 0 .. _count-1.
    Index _count-1 is therefore the "top" of the stack.

    WHY NOT USE A PYTHON LIST?
    --------------------------
    Python lists have a built-in .pop() method and grow automatically.
    We are forbidden from using those conveniences so that we understand
    how the data structure works at a lower level.  Instead we manage the
    array and _count manually.

    Restrictions honoured
    ---------------------
    * No built-in pop()  – removal is done by decrementing _count.
    * No list[]          – backing store is a numpy dtype=object array.
    * No del             – vacated slots are cleared by setting them to None.
    """

    # Class-level constant: the default maximum number of items the stack
    # can hold if the caller does not specify a capacity.
    DEFAULT_CAPACITY = 100

    # ------------------------------------------------------------------
    # Constructor
    # ------------------------------------------------------------------

    def __init__(self, capacity=DEFAULT_CAPACITY):
        """
        Create an empty stack that can hold up to *capacity* items.

        Parameters
        ----------
        capacity : int
            Maximum number of elements the stack can hold.
            Defaults to DEFAULT_CAPACITY (100).

        What happens here
        -----------------
        1. We store the capacity so we can check for overflow later.
        2. We allocate a fixed-size numpy array of that capacity.
           dtype=object means every slot can hold any Python object.
        3. We set _count to 0, meaning "the stack is currently empty".
        """
        self._capacity = capacity

        # np.empty() allocates the array without filling it with a specific
        # value — it is faster than np.zeros() because it skips
        # initialisation.  We use dtype=object so any type can be stored.
        self._array = np.empty(self._capacity, dtype=object)

        # _count tells us two things at once:
        #   - how many real items are in the stack
        #   - the index at which the NEXT push will write
        # When _count == 0 the stack is empty.
        self._count = 0

    # ------------------------------------------------------------------
    # State-query helpers
    # ------------------------------------------------------------------

    def get_count(self):
        """
        Return the number of items currently in the stack.

        This is simply the value of _count, which we keep up-to-date
        every time we push or pop.
        """
        return self._count

    def is_empty(self):
        """
        Return True if the stack contains no items, False otherwise.

        The stack is empty when _count is 0 — there are no valid
        elements stored in the array at all.
        """
        return self._count == 0

    def is_full(self):
        """
        Return True if the stack has reached its maximum capacity.

        When _count equals _capacity every slot in the array is occupied
        and we cannot push any more items without overflowing.
        """
        return self._count == self._capacity

    # ------------------------------------------------------------------
    # Core stack operations
    # ------------------------------------------------------------------

    def push(self, value):
        """
        Push (add) *value* onto the top of the stack.

        How it works
        ------------
        Because _count always points to the next FREE slot, we can write
        the new value directly there, then increment _count.

        Example — pushing 10, then 20, then 30:

            After push(10):  array = [10, _, _, ...]   _count = 1
            After push(20):  array = [10, 20, _, ...]  _count = 2
            After push(30):  array = [10, 20, 30, ...] _count = 3
                                                top ^

        Parameters
        ----------
        value : any
            The item to place on top of the stack.

        Raises
        ------
        Exception if the stack is already full (overflow).
        """
        # Guard: if every slot is taken we cannot store another item
        if self.is_full():
            raise Exception("Stack is full – cannot push.")

        # Write the value into the next available slot …
        self._array[self._count] = value

        # … then move _count up by one so it again points to the next
        # free slot (and so that the top is now at _count - 1).
        self._count += 1

    def pop(self):
        """
        Remove and return the item currently on top of the stack.

        IMPORTANT — how we avoid using the built-in pop()
        --------------------------------------------------
        Python lists have a .pop() method we are not allowed to use.
        Instead, we perform the removal manually in three steps:

          1. Decrement _count  →  the top index is now _count (before the
             decrement it was _count - 1, so after decrement it is _count).
          2. Read the value at that index.
          3. Set that slot to None to release the reference (good hygiene —
             avoids keeping objects alive in memory longer than needed).

        Example — starting with [10, 20, 30], _count = 3:

            Step 1: _count becomes 2
            Step 2: value = array[2]  →  30
            Step 3: array[2] = None
            Result: [10, 20, None, ...]  _count = 2   (top is now 20)

        Returns
        -------
        The item that was on top of the stack.

        Raises
        ------
        Exception if the stack is empty (underflow).
        """
        # Guard: nothing to remove if the stack is empty
        if self.is_empty():
            raise Exception("Stack is empty – cannot pop.")

        # Step 1: Move _count down — the slot at the new _count value is
        # now logically "outside" the stack (it was the top).
        self._count -= 1

        # Step 2: Read the value we are about to return.
        value = self._array[self._count]

        # Step 3: Clear the slot so we don't hold a dangling reference.
        # We use assignment to None rather than del (which is forbidden).
        self._array[self._count] = None

        return value

    def top(self):
        """
        Return (but do NOT remove) the item currently on top of the stack.

        This is sometimes called "peek".  It is useful when you need to
        inspect the top element before deciding whether to pop it — for
        example, in the equation solver we check the precedence of the
        top operator before deciding whether to pop it.

        The top element lives at index _count - 1 because:
          - indices 0 .. _count-1 hold the real items
          - the highest occupied index is therefore _count - 1

        Returns
        -------
        The item at the top of the stack (not removed).

        Raises
        ------
        Exception if the stack is empty.
        """
        if self.is_empty():
            raise Exception("Stack is empty – no top element.")

        # _count - 1 is always the index of the topmost item
        return self._array[self._count - 1]

    # ------------------------------------------------------------------
    # String representation (for debugging / printing)
    # ------------------------------------------------------------------

    def __str__(self):
        """
        Build and return a human-readable string showing the stack contents
        from bottom to top.

        We walk indices 0 .. _count-1 and concatenate each element into a
        single string.  We do NOT use any list or join() — just a manual
        loop with string concatenation.

        Example output:  "DSAStack (bottom->top): [10, 20, 30]"
        """
        parts = ""
        for i in range(self._count):
            if i > 0:
                parts += ", "          # add a separator before every item
                                       # except the first
            parts += str(self._array[i])
        return "DSAStack (bottom->top): [" + parts + "]"
