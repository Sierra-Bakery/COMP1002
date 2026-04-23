#
#uses the DSALinkedList class to implement a stack data structure
#removed numpy as it is not needed for this implementation
#uses methods from DSALL (the python file with the linked list implementation)

from DSALL import DSALinkedList #imports the DSALL file which contains the DSALinkedList class which is used to implement the stack data structure

class DSAStack:
    def __init__(self): #constructor is simplified massively by DSALinkedList implementation
        self._list = DSALinkedList()  # DSALinkedList not DSAList!

    def push(self, value):
        self._list.insert_first(value)

    def pop(self):
        value = self._list.peek_first()  # peeks first
        self._list.remove_first() #then removes
        return value

    def top(self):
        return self._list.peek_first()

    def is_empty(self):
        return self._list.is_empty()

    def display(self):
        self._list.display()