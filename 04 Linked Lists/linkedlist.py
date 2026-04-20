class DSAListNode: #node class, acts as an object used by linked list class, contains value and pointer attributes
    def __init__(self, value):
        self.value = value
        self.next = None #pointer attribute, points to none as the data structure points to null
        self.prev = None #points to the previous node as it is a doubly linked list

class DSALinkedList:
    def __init__(self, value):
        self.head = None
        self.tail = None
    def isempty(self):
        return self.head is None
    