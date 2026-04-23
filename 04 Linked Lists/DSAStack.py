#removed numpy as it is not neeeded for stack implementation, as we can use a LINKED list instead


class DSAStack:


    # Class-level constant: the default maximum number of items the stack
    # can hold if the caller does not specify a capacity.
    DEFAULT_CAPACITY = 100

    # Constructor

    def __init__(self, capacity=DEFAULT_CAPACITY):

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

    # State-query helpers

    def get_count(self):
        return self._count

    def is_empty(self):
        return self._count == 0

    def is_full(self):
        return self._count == self._capacity

    # Core stack operations

    def push(self, value):
        # Guard: if every slot is taken we cannot store another item
        if self.is_full():
            raise Exception("Stack is full – cannot push.")

        # Write the value into the next available slot …
        self._array[self._count] = value

        # … then move _count up by one so it again points to the next
        # free slot (and so that the top is now at _count - 1).
        self._count += 1

    def pop(self):
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
        if self.is_empty():
            raise Exception("Stack is empty – no top element.")

        # _count - 1 is always the index of the topmost item
        return self._array[self._count - 1]

    # String representation (for debugging / printing)

    def __str__(self):
        parts = ""
        for i in range(self._count):
            if i > 0:
                parts += ", "          # add a separator before every item
                                       # except the first
            parts += str(self._array[i])
        return "DSAStack (bottom->top): [" + parts + "]"
