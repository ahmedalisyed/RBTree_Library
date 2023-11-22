from minHeap import MinHeap

class RBTreeNode:
    def __init__(self, book):
        self.book = book
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1  # 1 for red, 0 for black

class Book:
    def __init__(self, bookID, bookName, author_name, availabilityStatus=True, borrowedBy=None, reservationHeap=None):
        self.bookID = bookID
        self.bookName = bookName
        self.author_name = author_name
        self.availabilityStatus = availabilityStatus
        self.borrowedBy = borrowedBy or []
        self.reservationHeap = MinHeap() if reservationHeap is None else reservationHeap

    def __str__(self):
        return f"Book ID: {self.bookID}, Title: {self.bookName}, Author: {self.author_name}, Available: {self.availabilityStatus}"

class RedBlackTree:
    def __init__(self):
        self.TNULL = RBTreeNode(None)
        self.TNULL.color = 0  # Set color of TNULL to black
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL
        self.color_flip_count = 0

    def search_tree_helper(self, node, key):
        if node == self.TNULL or key == node.book.bookID:
            return node

        if key < node.book.bookID:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    def color_flip_count_reset(self):
        self.color_flip_count = 0

    def color_flip_count_increment(self):
        self.color_flip_count += 1

    def update_count(self, previous, updated):
        if previous != updated:
            self.color_flip_count_increment()

    def balanced_delete(self, x):
        original_color = x.color
        while x != self.root and x.color == original_color:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    self.update_count(1, s.color)
                    existing = x.parent.color
                    x.parent.color = 1
                    self.update_count(existing, x.parent.color)
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    existing = s.color
                    s.color = 1
                    self.update_count(existing, s.color)
                    x = x.parent
                else:
                    if s.right.color == 0:
                        existing = s.left.color
                        s.left.color = 0
                        self.update_count(existing, s.left.color)
                        existing = s.color
                        s.color = 1
                        self.update_count(existing, s.color)
                        self.right_rotate(s)
                        s = x.parent.right

                    existing = s.color
                    s.color = x.parent.color
                    self.update_count(existing, s.color)
                    existing = x.parent.color
                    x.parent.color = 0
                    self.update_count(existing, x.parent.color)
                    existing = s.right.color
                    s.right.color = 0
                    self.update_count(existing, s.right.color)
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    self.update_count(1, s.color)
                    existing = x.parent.color
                    x.parent.color = 1
                    self.update_count(existing, x.parent.color)
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == 0 and s.right.color == 0:
                    existing = s.color
                    s.color = 1
                    self.update_count(existing, s.color)
                    x = x.parent
                else:
                    if s.left.color == 0:
                        existing = s.right.color
                        s.right.color = 0
                        self.update_count(existing, s.right.color)
                        existing = s.color
                        s.color = 1
                        self.update_count(existing, s.color)
                        self.left_rotate(s)
                        s = x.parent.left

                    existing = s.color
                    s.color = x.parent.color
                    self.update_count(existing, s.color)

                    existing = x.parent.color
                    x.parent.color = 0
                    self.update_count(existing, x.parent.color)

                    existing = s.left.color
                    s.left.color = 0
                    self.update_count(existing, s.left.color)
                    self.right_rotate(x.parent)
                    x = self.root

            if x == self.root:
                break
        x.color = 0

    def balanced_insert(self, k):
        original_color = k.parent.color
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left  # uncle
                if u.color == 1:
                    existing = u.color
                    u.color = 0
                    self.update_count(existing, u.color)

                    existing = k.parent.color
                    k.parent.color = 0
                    self.update_count(existing, k.parent.color)

                    existing = k.parent.parent.color
                    k.parent.parent.color = 1
                    self.update_count(existing, k.parent.parent.color)

                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)

                    existing = k.parent.color
                    k.parent.color = 0
                    self.update_count(existing, k.parent.color)

                    existing = k.parent.parent.color
                    k.parent.parent.color = 1
                    self.update_count(existing, k.parent.parent.color)
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right  # uncle

                if u.color == 1:
                    existing = u.color
                    u.color = 0
                    self.update_count(existing, u.color)

                    existing = k.parent.color
                    k.parent.color = 0
                    self.update_count(existing, k.parent.color)

                    existing = k.parent.parent.color
                    k.parent.parent.color = 1
                    self.update_count(existing, k.parent.parent.color)
                    k = k.parent.parent  # move x up
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)

                    existing = k.parent.color
                    k.parent.color = 0
                    self.update_count(existing, k.parent.color)

                    existing = k.parent.parent.color
                    k.parent.parent.color = 1
                    self.update_count(existing, k.parent.parent.color)
                    self.right_rotate(k.parent.parent)

            if k == self.root:
                break
        self.root.color = 0

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, key, book):
        node = RBTreeNode(book)
        node.parent = None
        node.book = book
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1  # new node must be red

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.book.bookID < x.book.bookID:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.book.bookID < y.book.bookID:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = 0
            return

        if node.parent.parent is None:
            return

        self.balanced_insert(node)

    def get_min(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def get_max(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node

    def delete_node(self, key):
        self.delete_node_helper(self.root, key)

    def delete_node_helper(self, root, key):
        z = self.TNULL
        while root != self.TNULL:
            if root.book.bookID == key:
                z = root

            if root.book.bookID <= key:
                root = root.right
            else:
                root = root.left

        if z == self.TNULL:
            print("Couldn't find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.get_min(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == 0:
            self.balanced_delete(x)

    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def find_closest_books(self, target_id):
        closest_books = {}
        closest_lower = self.find_closest_lower(self.root, target_id)
        closest_higher = self.find_closest_higher(self.root, target_id)
        if closest_lower is not None:
            closest_books[closest_lower.book.bookID] = {
                'bookName': closest_lower.book.bookName,
                'author_name': closest_lower.book.author_name,
                'availabilityStatus': closest_lower.book.availabilityStatus
            }

        if closest_higher is not None:
            closest_books[closest_higher.book.bookID] = {
                'bookName': closest_higher.book.bookName,
                'author_name': closest_higher.book.author_name,
                'availabilityStatus': closest_higher.book.availabilityStatus
            }

        return closest_books

    def find_closest_lower(self, node, target_id):
        current_closest = None

        while node != self.TNULL:
            if node.book.bookID == target_id:
                return node
            elif node.book.bookID < target_id:
                current_closest = node
                node = node.right
            else:
                node = node.left

        return current_closest

    def find_closest_higher(self, node, target_id):
        current_closest = None

        while node != self.TNULL:
            if node.book.bookID == target_id:
                return node
            elif node.book.bookID > target_id:
                current_closest = node
                node = node.left
            else:
                node = node.right

        return current_closest
