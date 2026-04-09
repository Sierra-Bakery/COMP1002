"""
DSA Practical 05 - Binary Search Tree
--------------------------------------
Implements:
  - DSATreeNode
  - DSABinarySearchTree  (insert, find, delete, min, max, height, balance,
                          inorder, preorder, postorder, display)
  - Interactive menu

Restrictions honoured — none of the following are used:
  sort(), sorted(), remove(), del (list elements), pop(),
  tuples, dict, list[], find(), index(), collections.*,
  heapq, any automatic sorting/searching,
  high-level structures (HashMap, treelib, binarytree, etc.)

Custom DSAQueueNode / DSAQueue replace built-in lists entirely
for traversal output.
"""


# ═══════════════════════════════════════════════════════════
#  DSAQueueNode  —  single node in the queue's linked chain
# ═══════════════════════════════════════════════════════════
class DSAQueueNode:
    def __init__(self, key, value):
        self.key   = key
        self.value = value
        self.next  = None


# ═══════════════════════════════════════════════════════════
#  DSAQueue  —  simple FIFO queue backed by a linked chain
#  (no built-in list, no pop, no remove, no tuples)
# ═══════════════════════════════════════════════════════════
class DSAQueue:
    def __init__(self):
        self._head  = None
        self._tail  = None
        self._count = 0

    def enqueue(self, key, value):
        """Add a key/value pair to the back of the queue."""
        node = DSAQueueNode(key, value)
        if self._tail is None:
            self._head = node
            self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._count += 1

    def dequeue(self):
        """Remove and return key, value from the front as two separate values."""
        if self._head is None:
            raise IndexError("Queue is empty.")
        node        = self._head
        self._head  = self._head.next
        if self._head is None:
            self._tail = None
        self._count -= 1
        return node.key, node.value

    def is_empty(self):
        return self._head is None

    def size(self):
        return self._count


# ═══════════════════════════════════════════════════════════
#  DSATreeNode
# ═══════════════════════════════════════════════════════════
class DSATreeNode:
    def __init__(self, key, value):
        self.key   = key
        self.value = value
        self.left  = None
        self.right = None

    def __str__(self):
        return "(" + str(self.key) + ": " + str(self.value) + ")"


# ═══════════════════════════════════════════════════════════
#  DSABinarySearchTree
# ═══════════════════════════════════════════════════════════
class DSABinarySearchTree:
    def __init__(self):
        self._root = None

    # ── insert ──────────────────────────────────────────────
    def insert(self, key, value):
        self._root = self._insert_rec(self._root, key, value)

    def _insert_rec(self, node, key, value):
        if node is None:
            return DSATreeNode(key, value)
        if key < node.key:
            node.left  = self._insert_rec(node.left,  key, value)
        elif key > node.key:
            node.right = self._insert_rec(node.right, key, value)
        else:
            node.value = value          # duplicate key -> update value
        return node

    # ── find ────────────────────────────────────────────────
    def find(self, key):
        return self._find_rec(self._root, key)

    def _find_rec(self, node, key):
        if node is None:
            raise KeyError("Key '" + str(key) + "' not found in tree.")
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._find_rec(node.left,  key)
        else:
            return self._find_rec(node.right, key)

    # ── delete ──────────────────────────────────────────────
    def delete(self, key):
        self._root = self._delete_rec(self._root, key)

    def _delete_rec(self, node, key):
        if node is None:
            raise KeyError("Key '" + str(key) + "' not found in tree.")
        if key < node.key:
            node.left  = self._delete_rec(node.left,  key)
        elif key > node.key:
            node.right = self._delete_rec(node.right, key)
        else:
            # Node to delete found
            if node.left is None:
                return node.right                   # 0 or 1 child (right)
            elif node.right is None:
                return node.left                    # 1 child (left)
            else:
                # 2 children -> replace with in-order successor
                successor  = self._min_node(node.right)
                node.key   = successor.key
                node.value = successor.value
                node.right = self._delete_rec(node.right, successor.key)
        return node

    def _min_node(self, node):
        """Walk left to the leftmost node — used internally by delete."""
        while node.left is not None:
            node = node.left
        return node

    # ── min / max ───────────────────────────────────────────
    def min(self):
        if self._root is None:
            raise ValueError("Tree is empty.")
        return self._min_rec(self._root)

    def _min_rec(self, node):
        if node.left is None:
            return node.key
        return self._min_rec(node.left)

    def max(self):
        if self._root is None:
            raise ValueError("Tree is empty.")
        return self._max_rec(self._root)

    def _max_rec(self, node):
        if node.right is None:
            return node.key
        return self._max_rec(node.right)

    # ── height ──────────────────────────────────────────────
    def height(self):
        return self._height_rec(self._root)

    def _height_rec(self, node):
        if node is None:
            return 0
        left_h  = self._height_rec(node.left)
        right_h = self._height_rec(node.right)
        if left_h > right_h:
            return 1 + left_h
        return 1 + right_h

    # ── balance ─────────────────────────────────────────────
    def balance(self):
        """
        Balance percentage (0-100%).
        Compares actual node count to the theoretical maximum
        for the current height (2^h - 1).  A perfect tree = 100%.
        """
        h = self.height()
        if h == 0:
            return 100.0
        actual    = self._count_nodes(self._root)
        max_nodes = (2 ** h) - 1
        return (actual / max_nodes) * 100.0

    def _count_nodes(self, node):
        if node is None:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    # ── traversals  (return a DSAQueue, NOT a list) ─────────
    def inorder(self):
        q = DSAQueue()
        self._inorder_rec(self._root, q)
        return q

    def _inorder_rec(self, node, q):
        if node is not None:
            self._inorder_rec(node.left,  q)
            q.enqueue(node.key, node.value)
            self._inorder_rec(node.right, q)

    def preorder(self):
        q = DSAQueue()
        self._preorder_rec(self._root, q)
        return q

    def _preorder_rec(self, node, q):
        if node is not None:
            q.enqueue(node.key, node.value)
            self._preorder_rec(node.left,  q)
            self._preorder_rec(node.right, q)

    def postorder(self):
        q = DSAQueue()
        self._postorder_rec(self._root, q)
        return q

    def _postorder_rec(self, node, q):
        if node is not None:
            self._postorder_rec(node.left,  q)
            self._postorder_rec(node.right, q)
            q.enqueue(node.key, node.value)

    # ── ASCII display ────────────────────────────────────────
    def display(self):
        """Print a sideways ASCII tree (right branch on top)."""
        self._display_rec(self._root, 0)

    def _display_rec(self, node, level):
        if node is not None:
            self._display_rec(node.right, level + 1)
            print("    " * level + "[" + str(node.key) + "]")
            self._display_rec(node.left,  level + 1)

    # ── empty check ─────────────────────────────────────────
    def is_empty(self):
        return self._root is None


# ═══════════════════════════════════════════════════════════
#  Helper: drain and print a DSAQueue
# ═══════════════════════════════════════════════════════════
def print_queue(label, q):
    """Drain the queue and print every key:value pair."""
    if q.is_empty():
        print("  (empty)")
        return
    count  = q.size()
    output = label + " traversal (" + str(count) + " nodes):\n  "
    first  = True
    while not q.is_empty():
        k, v = q.dequeue()
        if not first:
            output += " -> "
        output += str(k) + ":" + str(v)
        first = False
    print(output)


# ═══════════════════════════════════════════════════════════
#  Interactive Menu
# ═══════════════════════════════════════════════════════════
def print_menu():
    print("\n" + "=" * 42)
    print("    Binary Search Tree  --  Main Menu")
    print("=" * 42)
    print("  1.  Add node")
    print("  2.  Delete node")
    print("  3.  Find / search for a node")
    print("  4.  Display tree (choose traversal)")
    print("  5.  Show tree structure (ASCII)")
    print("  6.  Tree statistics (min/max/height/balance)")
    print("  0.  Exit")
    print("=" * 42)


def display_traversal(bst):
    print("\n  Traversal type:")
    print("    1. Inorder   (Left -> Root -> Right)  -- sorted order")
    print("    2. Preorder  (Root -> Left -> Right)")
    print("    3. Postorder (Left -> Right -> Root)")
    choice = input("  Choose [1-3]: ").strip()

    if choice == "1":
        q     = bst.inorder()
        label = "Inorder"
    elif choice == "2":
        q     = bst.preorder()
        label = "Preorder"
    elif choice == "3":
        q     = bst.postorder()
        label = "Postorder"
    else:
        print("  Invalid choice.")
        return

    print()
    print_queue(label, q)


def main():
    bst = DSABinarySearchTree()
    print("\nWelcome to the Binary Search Tree explorer!")

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            # ── Add node ────────────────────────────
            raw = input("  Enter key (integer): ").strip()
            try:
                key   = int(raw)
                value = input("  Enter value (string): ").strip()
                bst.insert(key, value)
                print("  Node (" + str(key) + ": " + value + ") inserted.")
            except ValueError:
                print("  Key must be an integer.")

        elif choice == "2":
            # ── Delete node ─────────────────────────
            if bst.is_empty():
                print("  Tree is empty -- nothing to delete.")
            else:
                raw = input("  Enter key to delete: ").strip()
                try:
                    key = int(raw)
                    bst.delete(key)
                    print("  Node with key " + str(key) + " deleted.")
                except ValueError:
                    print("  Key must be an integer.")
                except KeyError as e:
                    print("  " + str(e))

        elif choice == "3":
            # ── Find node ───────────────────────────
            if bst.is_empty():
                print("  Tree is empty.")
            else:
                raw = input("  Enter key to find: ").strip()
                try:
                    key   = int(raw)
                    value = bst.find(key)
                    print("  Found: key=" + str(key) + ", value=" + str(value))
                except ValueError:
                    print("  Key must be an integer.")
                except KeyError as e:
                    print("  " + str(e))

        elif choice == "4":
            # ── Traversal ───────────────────────────
            if bst.is_empty():
                print("  Tree is empty.")
            else:
                display_traversal(bst)

        elif choice == "5":
            # ── ASCII display ───────────────────────
            if bst.is_empty():
                print("  Tree is empty.")
            else:
                print("\n  Tree structure (rotated 90 deg -- right branch on top):\n")
                bst.display()

        elif choice == "6":
            # ── Statistics ──────────────────────────
            if bst.is_empty():
                print("  Tree is empty.")
            else:
                bal = bst.balance()
                # Round to 1 decimal place manually (no formatting helpers)
                bal_rounded = int(bal * 10 + 0.5) / 10
                print("\n  Min key    : " + str(bst.min()))
                print("  Max key    : " + str(bst.max()))
                print("  Height     : " + str(bst.height()))
                print("  Balance    : " + str(bal_rounded) + "%")
                print("  Node count : " + str(bst._count_nodes(bst._root)))

        elif choice == "0":
            print("\nGoodbye!\n")
            break

        else:
            print("  Invalid option -- please choose from the menu.")


if __name__ == "__main__":
    main()
