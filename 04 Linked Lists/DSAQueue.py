# Adapted from previously submitted DSAQueue.py
# Not using numpy for implementation as its not necessary as we have linked lists
from DSALL import DSALinkedList, DSAListNode

# Base class

class DSAQueue:

    DEFAULT_CAPACITY = 100
    # Constructor

    def __init__(self):
        self._list = DSALinkedList()  # DSALinkedList
    # def get_count(self): //not used anymore


    def is_empty(self):
        return self._list.isempty()

    # def is_full(self): //not used anymore as linked lists do not have a fixed capacity 



    def enqueue(self, value):
        return self._list.insert_last(value)

    def dequeue(self):
        value = self._list.peek_first()
        self._list.remove_first()
        return value

    def peek(self):
        return self._list.peek_first()
    
    def display(self):
        self._list.display()

    # def __str__(self): // not used anymore

#Subclass 1 — Shuffling Queue is REMOVED because it is not efficient and not needed for this implementation as my DSAQueue implemented is so much more efficient hahaha