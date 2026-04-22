class DSAListNode: #node class, acts as an object used by linked list class, contains value and pointer attributes
    def __init__(self, value):
        self.value = value
        self.next = None #pointer attribute, points to none as the data structure points to null
        self.prev = None #points to the previous node as it is a doubly linked list

class DSALinkedList:
    def __init__(self, value):
        #specifies the first and last node
        self.head = None 
        self.tail = None
    def isempty(self):
        return self.head is None
        #returns if the list is empty
    def insert_first(self, value):
        new_node = DSAListNode(value)
        if self.isempty():
            #means it is the only node in the list, so it is both the head and tail (new node)
            self.head = new_node
            self.tail = new_node
        else:
            #links new node to the current head
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node