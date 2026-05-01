# linked list method is based on the implementation of the linked list in DSALinkedList.py
class DSAListNode: #node class, acts as an object used by linked list class, contains value and pointer attributes
    def __init__(self, value):
        self.value = value
        self.next = None #pointer attribute, points to none as the data structure points to null
        self.prev = None #points to the previous node as it is a doubly linked list

class DSALinkedList:
    def __init__(self):
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
    def insert_last(self, value):
        #essentially the insert_first class but mirrored
        new_node = DSAListNode(value)
        if self.isempty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
    def peek_first(self):
        if self.isempty():
            raise Exception("List is empty")
        else:
            return self.head.value #returns val ue
    def peek_last(self):
        if self.isempty(): #exception handling
            raise Exception("List is empty")
        else:
            return self.tail.value
    def remove_first(self):
        if self.isempty(): #exception handling
            raise Exception("List is empty")
        elif self.head == self.tail:
            #if head = tail then the head and tail nodes esentially get removed
            temphead = self.head.value #stores the head value tempoarily
            self.head = None 
            self.tail = None
            return temphead
        else:
            temphead = self.head.value
            self.head = self.head.next
            self.head.prev = None
            return temphead
    def remove_last(self):
        if self.isempty(): #exception handling
            raise Exception("List is empty")
        elif self.head == self.tail:
            temphead = self.head.value
            self.head = None
            self.tail = None
            return temphead
        else:
            temptail = self.tail.value
            self.tail = self.tail.prev
            self.tail.next = None
            return temptail
    def display(self):
        if self.isempty():
            print("Empty List")
        else:
            cur = self.head
            while cur is not None:
                print(cur.value)
                cur = cur.next #moves through the linked list

###################################GRAPH CODE######################################

class DSAGraphVertex(): #code for each vertex
    def __init__(self, label, value): #initializes the parts of the graph
        self.label = label
        self.value = value
        self.links = DSALinkedList() #takes linked list class from earlier
        self.visited = False #takes boolean, either visited or not, needed for searching
    def getLabel(self):
        return self.label #the first two get classes are really simple, just outputting the things from the class
    def getValue(self):
        return self.value
    def getAdjacent(self):
        return self.links #gets the whole LinkedList of adjacent nodes
    def addEdge(self, vertex):
        self.links.insert_last(vertex) #adds edge onto tail node of the linked list
    def setVisited(self):
        self.visited = True #just changing the boolean values for visited
    def clearVisited(self):
        self.visited = False
    def getVisited(self):
        return self.visited
    def __str__(self):
        return str(self.label) #returns the label

class DSAGraph(): #we use linked lists here too, to store vertices
    def __init__(self):
        self.vertices = DSALinkedList()

    def getVertex(self, label):
        cur = self.vertices.head
        while cur is not None:
            if cur.value.label == label:
                return cur.value   #returns the DSAGraphVertex object
            cur = cur.next
        raise Exception("Vertex not found")
    def hasVertex(self, label):
        cur = self.vertices.head
        while cur is not None:
            if cur.value.label == label:
                return True
            cur = cur.next
        return False
    def addVertex(self, label, value = None):
        if self.hasVertex(label):
            raise Exception("Vertex already exists")
        else:
            new_vertex = DSAGraphVertex(label, value)
            self.vertices.insert_last(new_vertex)
    def addEdge(self, label1, label2):
        vertex1 = self.getVertex(label1)
        vertex2 = self.getVertex(label2)
        vertex1.addEdge(vertex2) #adds the edge to the first vertex
        vertex2.addEdge(vertex1) #adds the edge to the second vertex, as it is an undirected graph
    def getVertexCount(self):
        count = 0
        cur = self.vertices.head
        while cur is not None:
            count += 1
            cur = cur.next
        return count
    def getEdgeCount(self):
        count = 0
        cur = self.vertices.head
        while cur is not None:
            inner = cur.value.links.head
            while inner is not None:
                count += 1
                inner = inner.next
            cur = cur.next
        return count // 2 #divides by 2 as it is an undirected graph, so each edge is counted twice
    def displayAsList(self):
        temp = self.vertices.head
        while temp is not None: #runs when theres something at the head node of the linked list
            vertex = temp.value
            print(vertex.label, end = "|")
            inner = vertex.links.head
            while inner is not None:
                print(inner.value.label, end = " ")
                inner = inner.next
            print()
            temp = temp.next
    def isAdjacent(self, label1, label2): #helper method to display graph as matrix
        vertex = self.getVertex(label1)
        temp = vertex.links.head
        while temp is not None:
            if temp.value.label == label2: #if found
                return True
            temp = temp.next
        return False #not foundd
    def displayAsMatrix(self):
        #prints header row labels
        print("   ", "")
        temp = self.vertices.head
        while temp is not None:
            print(temp.value.label, end = "  ") #prints the labels of the vertices at the top of the matrix
            temp = temp.next
        print() #new line
        #print rows
        row = self.vertices.head
        while row is not None:
            print(row.value.label, end = " [ ") #prints the label of the vertex at the start of the row
            temp = self.vertices.head
            while temp is not None:
                if self.isAdjacent(row.value.label, temp.value.label):
                    print("1 ", end = "  ") #prints 1 if there is an edge between the two vertices
                else:
                    print("0 ", end = "") #prints 0 if there is no edge between the two vertices
                temp = temp.next
            print("]") #end row
            row = row.next

# create the graph
g = DSAGraph()

# add vertices
g.addVertex("A")
g.addVertex("B")
g.addVertex("C")
g.addVertex("D")
g.addVertex("E")

# add edges (based on the graph from the lecture slides)
g.addEdge("A", "B")
g.addEdge("A", "D")
g.addEdge("A", "E")
g.addEdge("B", "C")
g.addEdge("B", "E")
g.addEdge("C", "D")
g.addEdge("C", "E")

# test display
print("=== Adjacency List ===")
g.displayAsList()

print()
print("=== Adjacency Matrix ===")
g.displayAsMatrix()

print()
print("=== Counts ===")
print("Vertex count:", g.getVertexCount())
print("Edge count:", g.getEdgeCount())