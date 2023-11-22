from RedBlackTree import RedBlackTree, Book
from minHeap import MinHeap
import sys


class GatorLibrary:
    def __init__(self):
        self.books_rb_tree = RedBlackTree()
        self.reservationHeap = MinHeap()

    #Function to read the input
    def readfile(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                return lines

        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    #Function to print book details
    
    def PrintBook(self, bookID):
    # Search for the book in the Red-Black tree
        node = self.books_rb_tree.search_tree_helper(self.books_rb_tree.root, bookID)

        if node != self.books_rb_tree.TNULL:
            
            print(f'BookID = {node.book.bookID}')
            print(f'Title = "{node.book.bookName}"')
            print(f'Author = "{node.book.author_name}"')
            print(f'Availability = "{"Yes" if node.book.availabilityStatus else "No"}"')
            
            if node.book.borrowedBy:
                print(f'Borrowed by: {", ".join(str(patronID) for patronID in node.book.borrowedBy)}')
            else:
                print("Borrowed by: None")

            print(f'Reservations: {node.book.reservationHeap.get_heap_elements()}\n')
        else:
            print(f'Book {bookID} not found in the Library\n')

    #Function to print books in a range
    def PrintBooks(self, bookID1, bookID2):
        # Iterate through the Red-Black tree and print books within the specified range
        self._print_books(self.books_rb_tree.root, bookID1, bookID2)

    #Function to help print books in a range
    def _print_books(self, node, bookID1, bookID2):
        if node != self.books_rb_tree.TNULL:
            if bookID1 < node.book.bookID:
                self._print_books(node.left, bookID1, bookID2)

            if bookID1 <= node.book.bookID <= bookID2:
                print(f'BookID = {node.book.bookID}')
                print(f'Title = "{node.book.bookName}"')
                print(f'Author = "{node.book.author_name}"')
                print(f'Availability = "{"Yes" if node.book.availabilityStatus else "No"}"')
                if node.book.borrowedBy:
                    print(f"Borrowed by: {', '.join(str(patronID) for patronID in node.book.borrowedBy)}")
                else:
                    print("Borrowed by : None")
                print(f"Reservations: {node.book.reservationHeap.get_heap_elements()}\n\n")
            if bookID2 > node.book.bookID:
                self._print_books(node.right, bookID1, bookID2)

    #Function to insert a book
    def InsertBook(self, bookID, bookName, author_name, availabilityStatus=True, borrowedBy=None, reservationHeap=None):
        # Check if the book with the given ID already exists
        existing_node = self.books_rb_tree.search_tree_helper(self.books_rb_tree.root, bookID)
        if existing_node != self.books_rb_tree.TNULL:
            return

        # If not, create a new book and insert it into the Red-Black tree
        new_book = Book(bookID, bookName, author_name, availabilityStatus, borrowedBy, reservationHeap)
        self.books_rb_tree.insert(bookID, new_book)

    #Function to borrow a book
    def BorrowBook(library, patronID, bookID, patronPriority):
        # Search for the book in the Red-Black tree
        book_node = library.books_rb_tree.search_tree_helper(library.books_rb_tree.root, bookID)
        
        if book_node == library.books_rb_tree.TNULL:
            print(f"Book {bookID} not found in the Library")
            return
        # Check if the book is available
        if book_node.book.availabilityStatus:
            # Check if the patron already has the book in possession
            if patronID not in book_node.book.borrowedBy:
                 # Update book status and borrower information
                book_node.book.availabilityStatus = False
                book_node.book.borrowedBy.append(patronID)
                print(f"Book {bookID} Borrowed by Patron {patronID}\n")
        else:
            # Book is not available, create a reservation node in the heap
            reservationHeap = book_node.book.reservationHeap
            reservationHeap.insert(patronPriority, patronID)
            print(f"Book {bookID} Reserved by Patron {patronID}\n")

    #Function to return a book
    def ReturnBook(self, patronID, bookID):
        # Search for the book in the Red-Black tree
        book_node = self.books_rb_tree.search_tree_helper(self.books_rb_tree.root, bookID)

        if book_node == self.books_rb_tree.TNULL:
            print(f"Book {bookID} not found in the Library")
            return

        # Check if the patron has borrowed the book
        if patronID not in book_node.book.borrowedBy:
            return

        # Update book status and borrower information
        book_node.book.availabilityStatus = True
        book_node.book.borrowedBy.remove(patronID)

        # Assign the book to the patron with the highest priority in the reservation heap (if available)
        reservationHeap = book_node.book.reservationHeap
        if not reservationHeap.is_empty():
            reservation_node = reservationHeap.extract_min()
            next_patronID = reservation_node.value
            book_node.book.availabilityStatus = False
            book_node.book.borrowedBy.append(next_patronID)
            print(f"Book {bookID} Returned by Patron {patronID}\n")
            print(f"Book {bookID} Allotted to Patron {next_patronID}\n")

        else:
            print(f"Book {bookID} Returned by Patron {patronID}\n")

    #Function to delete a book
    def DeleteBook(self, bookID):
        # Search for the book in the Red-Black tree
        book_node = self.books_rb_tree.search_tree_helper(self.books_rb_tree.root, bookID)

        if book_node == self.books_rb_tree.TNULL:
            print(f"Book {bookID} not found in the Library")
            return

        # Notify patrons in the reservation list that the book is no longer available
        reservationHeap = book_node.book.reservationHeap
        if reservationHeap.is_empty():
            print(f"Book {bookID} is no longer available\n")
            
        else:
            print(f"Book {bookID} is no longer available. Reservations made by Patrons ", end="")
    
            while not reservationHeap.is_empty():
                reservation_node = reservationHeap.extract_min()
                patronID = reservation_node.value
                print(patronID, ", ", end="")
            print("have been cancelled! \n")
        # Delete the book from the Red-Black tree
        self.books_rb_tree.delete_node(bookID)

    #Function to find the closest book
    def FindClosestBook(self, target_id):
        # Call the corresponding method in the Red-Black tree class
        closest_books = self.books_rb_tree.find_closest_books(target_id)
        book_count = []
        actual_close=[]
        if closest_books:
            for bookID, book_whatever in closest_books.items():
                book_count.append(bookID)
            if len(book_count)>1:
                closest_lower = abs(target_id-book_count[0])
                closest_higher = abs(book_count[1]-target_id)
                if closest_lower!=closest_higher:
                    if closest_lower<closest_higher:
                        actual_close = [book_count[0]]
                    else:
                        actual_close = [book_count[1]]
                else:
                    actual_close = [book_count[0], book_count[1]]
            for bookID in actual_close:
                self.PrintBook(bookID)
            else:
                for bookID in book_count:
                    if bookID == target_id:
                        self.PrintBook(bookID)
                        return
        else:
            print(f"No books found in the Library.")


    #Function to Quit the program
    def Quit(self):
        print("Program Terminated!!")
        exit()

    #Function to count the number of flips in color
    def ColorFlipCount(self):
        count = self.books_rb_tree.color_flip_count
        print("Colour Flip Count: ",count, "\n")
        return count

# Example usage:
if __name__ == "__main__":
    library = GatorLibrary()
    main_file = sys.argv[1]
    name_file = main_file.split('.')[0]
    run_commands = library.readfile(main_file)
    output_file = f'{name_file}_output_file.txt'

    with open(output_file, 'w') as file:
        sys.stdout = file
        
        for r_command in run_commands:
            r_command = 'library.' + r_command
            exec(r_command)