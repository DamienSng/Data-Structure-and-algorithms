# Damien Sng
# 234647B
# BF2302
# IT2852

import shelve
import logging
from collections import deque


logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')
Que_customer_requests = deque()

class Book:
    def __init__(self, Title, Publisher, Language, NumberOfCopies, AgeRating, Genre, Author):
        self.Title = Title
        self.Publisher = Publisher
        self.Language = Language
        self.NumberOfCopies = NumberOfCopies
        if self.NumberOfCopies > 0:
            self.Availability = True
        else:
            self.Availability = False
        self.AgeRating = AgeRating
        self.Genre = Genre
        self.Author = Author
        self.borrowed = None

    def __str__(self):
        return (f"\nBook Title: {self.Title}\n"
                f"Publisher: {self.Publisher}\n"
                f"Language: {self.Language}\n"
                f"NumberOfCopies: {self.NumberOfCopies}\n"
                f"Availability: {self.Availability}\n"
                f"AgeRating: {self.AgeRating}\n"
                f"Genre: {self.Genre}\n"
                f"Author: {self.Author}\n"
                f"\n{'=' * 30}")


class User:
    def __init__(self, name, Password):
        if len(ReginsteredUsers)==0:
            self.ID = 1
        else:
            self.ID = ReginsteredUsers[-1].ID + 1
        self.name = name
        self.Password = Password
        self.borrow = False
        self.book = ''
        self.request = []


    def __str__(self):
        return (f"\nID: {self.ID}\n" 
                f"User: {self.name}\n"
                f"Password: {self.Password}\n"
                f"Borrowed: {self.borrow}\n"
                f"book: {self.book}\n"
                f"\n{'=' * 30}")

class ClassCustomerRequest:
    def __init__(self, Customer_ID, Customer_request):
        self.Customer_ID = Customer_ID
        self.Customer_request = Customer_request
    def __str__(self):
        return (f"\nRequest: {self.Customer_request}\n"
                f"\n{'=' * 30}")


# Staff accounts
librarians = {}
librarians["Staff1"] = "1234"
librarians["Staff2"] = "abc"
librarians["Staff3"] = "qwer"


library = {}

# If ['library'] in inside file, open it and copy to library dictionary, if not create it
with shelve.open('LibraryDB') as db:
    if 'library' in db:
        library = db['library']
    else:
        db['library'] = library

ReginsteredUsers = []

# If ['User'] in inside file, open it and copy to ReginsteredUsers list, if not create it
with shelve.open('UserDB') as db:
    if 'User' in db:
        ReginsteredUsers = db['User']
    else:
        db['User'] = ReginsteredUsers

# Display all the books in the dictionary, ISBN not shown
def display_all_books():
    if library.values():
        print(f"\n{'=' * 30}")
        for value in library.values():
            print(value)
    else:
        print(f"\n{'=' * 43}")
        print(f'Apologies, our registry is currently empty')
        print(f"{'=' * 43}")

# Display all the books in the dictionary, ISBN shown
def staff_display_all_books():
    if library.values():
        print(f"\n{'=' * 30}")
        for value in library.values():
            value_to_find = value
            for key, value in library.items():
                if value == value_to_find:
                    print(f"ISBN: {key}")
                    break
            print(value)
    else:
        print(f"\n{'=' * 43}")
        print(f'Apologies, our registry is currently empty')
        print(f"{'=' * 43}")

# Seq search for when adding book, checking if ISBN is in the dictionary
def sequentialSearch(theDict, target):
    for key in theDict:
        # If the target is in the keys of the dictionary, return the key
        if key == target:
            return True
    return False  # If not found, return False

# Search for the existance of a specific book, tells you which section/genre it is in
def bookSearch():
    book_list = list(library.values())
    book = input("Book Title: ")
    found = False
    for books in book_list:
        if book.lower().strip() in books.Title.lower().strip():
            found = True
            if books.Availability == True:
                print(f'\n{"=" * (56+len(books.Genre))}\n'
                      f'That book is available! you can find it in our {books.Genre} section\n'
                      f'{"=" * (56+len(books.Genre))}\n')
                break
            else:
                print(f'\n{"=" * 57}\nThat book currently not available! Comeback another day!\n{"=" * 57}\n')
                break
    if not found:
        print(f'\n{"=" * 43}\nApologies, that book is not in our registry\n{"=" * 43}\n')

# Add book to the dictionary, only staff is able to access (Logs)
def add_book():
    while True:
        print(f"{'=' * 38}")
        ISBNnumber = input("Enter your book's ISBN: ")
        print(f"{'=' * 38}")

        # Return from menu / terminate process
        if ISBNnumber == '':
            break

        # If input is not numerical, keep prompting user
        while not ISBNnumber.isnumeric():
            print(f"\n{'=' * 27}")
            print(f'Please input only numbers!')
            print(f"{'=' * 27}")
            print(f"{'=' * 38}")
            ISBNnumber = input("Enter your book's ISBN: ")
            print(f"{'=' * 38}")
            if ISBNnumber == '':
                break
        if ISBNnumber == '':
            break
        ISBNnumber = int(ISBNnumber)

        # Check if ISBN is registered alr
        if sequentialSearch(library.keys(), ISBNnumber):
            print(f"\n{'=' * 28}")
            NumberOfCopies = input("Enter number of copies: ")
            print(f"{'=' * 28}")

            # If input is not numerical, keep prompting user
            while not NumberOfCopies.isnumeric():
                print(f"\n{'=' * 27}")
                print(f'Please input only numbers!')
                print(f"{'=' * 27}")
                print(f"\n{'=' * 28}")
                NumberOfCopies = input("Enter number of copies: ")
                print(f"{'=' * 28}")
            NumberOfCopies = int(NumberOfCopies)

            library[ISBNnumber].NumberOfCopies += NumberOfCopies
            # Log actions and save
            logging.info(f'{staff} added {NumberOfCopies} copies of "{library[ISBNnumber].Title}"')
            with shelve.open('LibraryDB') as db:
                db['library'] = library
            break

        # Add a new index to the library abt the new book
        else:
            print(f"\n{'=' * 33}")
            Title = input("Enter book title: ")
            Publisher = input("Enter book publisher: ")
            Language = input("Enter book Language: ")
            NumberOfCopies = input("Enter number of copies: ")

            # If input is not numerical, keep prompting user
            while not NumberOfCopies.isnumeric():
                print(f"\n{'=' * 27}")
                print(f'Please input only numbers!')
                print(f"{'=' * 27}")
                NumberOfCopies = input("Enter number of copies: ")
            NumberOfCopies = int(NumberOfCopies)

            AgeRating = input("Enter book AgeRating: ")
            Genre = input("Enter book Genre: ")
            Author = input("Enter book Author: ")
            print(f"{'=' * 33}")

            library[ISBNnumber] = Book(Title, Publisher, Language, NumberOfCopies, AgeRating, Genre, Author)

            # Log actions and save
            logging.info(f'{staff} added ISBN {ISBNnumber}')
            with shelve.open('LibraryDB') as db:
                db['library'] = library
            break


# Dummy data
library[9780743273565] = Book("The Great Gatsby", "Charles Scribner's Sons", "English", 0, 'PG-13', 'Fiction',
                              'F. Scott Fitzgerald')
library[9780451524935] = Book("1984", "Signet Classic", "English", 30, '18+', 'Fiction', 'George Orwell')
library[9780446310789] = Book("To Kill a Mockingbird", "Grand Central Publishing", "English", 20, 'PG-13', 'Fiction',
                              'Harper Lee')
library[9780060850524] = Book("Brave New World", "Harper Perennial Modern Classics", "English", 15, 'PG-13', 'Fiction',
                              'Aldous Huxley')
library[9781503280786] = Book("Moby Dick", "CreateSpace Independent Publishing Platform", "English", 10, '8+',
                              'Fiction', 'Herman Melville')


# Turn dictionary into a list with all the values and Publishers sort alphabetically from a - z
def publisher_bubble_sort():
    # Convert the library dictionary to a list of books
    book_list = list(library.values())

    n = len(book_list)
    # Number of passes
    for i in range(n):
        # A flag to check if any swapping occurred
        swapped = False
        for j in range(0, n - i - 1):
            # Compare the publishers alphabetically,
            # .lower is employed to make a fair comparison
            # As ASCII upper and lower have different values
            if book_list[j].Publisher.lower() > book_list[j + 1].Publisher.lower():
                # Swap the books if they are in the wrong order
                book_list[j], book_list[j + 1] = book_list[j + 1], book_list[j]
                # Set the flag to True because a swap occurred
                swapped = True
        if not swapped:
            break

    # Check if book list has items
    if book_list:
        print(f"\n{'=' * 30}")
        # Print the sorted list of books
        for book in book_list:
            print(book)
    # Book list has no items
    else:
        print(f"\n{'=' * 43}")
        print(f'Apologies, our registry is currently empty')
        print(f"{'=' * 43}")

# Turn dictionary into a list with all the values and sort by Number of Copies in decending order
def NOC_insertion_sort():
    # Convert the library dictionary to a list of books
    book_list = list(library.values())

    for i in range(1, len(book_list)):
        # Start at index 1, not 0
        CurrentElement = book_list[i]
        PrevElement = i - 1
        # If the CurrentElement is greater than PrevElement,
        # PrevElement is pushed to the right
        while PrevElement >= 0 and CurrentElement.NumberOfCopies > book_list[PrevElement].NumberOfCopies:
            book_list[PrevElement + 1] = book_list[PrevElement]
            PrevElement -= 1
        # Imagine our number is 19 and this list has no duplicate numbers
        # Now the list looks like [21, 20, 18, 18, 15 ,14, 3]
        # In this case our elements are pushed 1 pos to the right(+1) and 18 of index[2] is a duplicate
        # So now we override the duplicate
        book_list[PrevElement + 1] = CurrentElement

    # Check if book list has items
    if book_list:
        print(f"\n{'=' * 30}")
        # Print the sorted list of books
        for book in book_list:
            print(book)
    # Book list has no items
    else:
        print(f"\n{'=' * 43}")
        print(f'Apologies, our registry is currently empty')
        print(f"{'=' * 43}")

def quick_sort_books_by_title(books_list):
    if len(books_list) <= 1:
        return books_list
    else:
        pivot = books_list[len(books_list) // 2]
        left = [book for book in books_list if book.Title < pivot.Title]
        middle = [book for book in books_list if book.Title == pivot.Title]
        right = [book for book in books_list if book.Title > pivot.Title]
        return quick_sort_books_by_title(left) + middle + quick_sort_books_by_title(right)


def sort_and_display_books_by_title():
    books_list = list(library.values())
    sorted_books = quick_sort_books_by_title(books_list)

    print("Books sorted by Title (ascending order):")
    for book in sorted_books:
        print(f"Title: {book.Title}, ISBN: {list(library.keys())[list(library.values()).index(book)]}")


def merge_sort_books_by_language_and_isbn(books_list):
    if len(books_list) <= 1:
        return books_list

    mid = len(books_list) // 2
    left = merge_sort_books_by_language_and_isbn(books_list[:mid])
    right = merge_sort_books_by_language_and_isbn(books_list[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i, j = 0, 0

    while i < len(left) and j < len(right):
        if left[i].Language < right[j].Language or (left[i].Language == right[j].Language and list(library.keys())[
            list(library.values()).index(left[i])] < list(library.keys())[
                                                        list(library.values()).index(right[j])]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def sort_and_display_books_by_language_and_isbn():
    books_list = list(library.values())
    sorted_books = merge_sort_books_by_language_and_isbn(books_list)

    print("Books sorted by Language and ISBN (ascending order):")
    for book in sorted_books:
        isbn = list(library.keys())[list(library.values()).index(book)]
        print(f"Language: {book.Language}, ISBN: {isbn}, Title: {book.Title}")

# Login process for staff access (Logs)
def staffLogin():
    attempts = 0
    while attempts < 3:
        print(f"\n{'=' * 54}")
        name = input("Enter your name (enter nothing to return): ")

        # Return from menu / terminate process
        if name == '':
            print(f'Terminating login process')
            print(f"{'=' * 54}")
            # Log process termination
            logging.warning(f'Staff login process terminated')
            return False
        password = input("Enter your password: ")
        print(f"{'=' * 54}")

        # Check if Username and password match up to the staff accounts
        for key in librarians:
            if key == name and librarians[key] == password:
                print(f"\n{'=' * (28 + len(name))}")
                print(f'Access granted. logged as {name}')
                print(f"{'=' * (28 + len(name))}")
                # Log actions
                logging.info(f'Staff Login: {name}')
                return name

        # If invalid, add 1 to attempt and prompt again
        else:
            attempts += 1
            if attempts < 3:
                print(f'\n{"=" * 30}\nIncorrect details. Try again.\n{"=" * 30}')
    # If 3 invalid attempts log it and terminate process
    logging.warning(f'Failed staff login attempt')
    print(f'\n{"=" * 43}\nToo many failed attempts. Try again later.\n{"=" * 43}')

# Login process for User access (Logs)
def userLogin():
    attempts = 0
    while attempts < 3:
        print(f"\n{'=' * 54}")
        name = input("Enter your name (enter nothing to return): ")

        # Return from menu / terminate process
        if name == '':
            logging.warning(f'User login process terminated')
            print(f'Terminating login process')
            print(f"{'=' * 54}")
            return False
        password = input("Enter your password: ")
        print(f"{'=' * 54}")

        # Check if Username and password match up to the staff accounts
        for Username in ReginsteredUsers:
            if Username.name == name and Username.Password == password:
                print(f"\n{'=' * (28 + len(name))}")
                print(f'Access granted. logged as {name}')
                print(f"{'=' * (28 + len(name))}")
                logging.info(f'User Login: {name}')
                return name

        # If invalid, add 1 to attempt and prompt again
        else:
            attempts += 1
            if attempts < 3:
                print(f'\n{"=" * 30}\nIncorrect details. Try again.\n{"=" * 30}\n')
    # If 3 invalid attempts log it and terminate process
    logging.warning(f'Failed user login attempt')
    print(f'\n{"=" * 43}\nToo many failed attempts. Try again later.\n{"=" * 43}')

# Edit any attribute of a book in the dictionary, only staff is able to access (Logs)
def update_records():
    def update_attribute(isbn, attribute, new_value):
        logging.info(f'{staff} replaced {attribute} of {isbn} from '
                     f'{getattr(library[isbn], attribute)} to {new_value}')
        setattr(library[isbn], attribute, new_value)
        # Check number of copies and update avalibility accordingly
        if library[isbn].NumberOfCopies <= 0:
            library[ISBNtoUpdate].Availability = False
        else:
            library[ISBNtoUpdate].Availability = True
        with shelve.open('LibraryDB') as db:
            db['library'] = library

    attributes = {
        '1': 'Title',
        '2': 'Publisher',
        '3': 'Language',
        '4': 'NumberOfCopies',
        '5': 'AgeRating',
        '6': 'Genre',
        '7': 'Author'
    }
    while True:
        print(f"\n{'=' * 64}")
        ISBNtoUpdate = input("Enter the book's ISBN (enter nothing to return): ")
        print(f"{'=' * 64}")

        # Return from menu / terminate process
        if ISBNtoUpdate == '':
            break

        # If input is not numerical, keep prompting user
        while not ISBNtoUpdate.isnumeric():
            print(f"\n{'=' * 27}")
            print(f'Please input only numbers!')
            print(f"{'=' * 27}")
            ISBNtoUpdate = input("Enter your book's International Standard Book Number(ISBN): ")
        ISBNtoUpdate = int(ISBNtoUpdate)

        # Check if ISBN is in the registry
        if ISBNtoUpdate in library:
            print(f"\n{'=' * 33}")
            print("What would you like to Change?")
            print("1. Title")
            print("2. Publisher")
            print("3. Language")
            print("4. NumberOfCopies")
            print("5. AgeRating")
            print("6. Genre")
            print("7. Author")
            print("8. ISBN")
            print("Enter nothing to return from menu")
            print(f"{'=' * 33}")
            option = input("Select an option: ")
            if option in attributes or option == '8':
                print(f"\n{'=' * 60}")
                new_value = input("Enter new details (Enter nothing to return): ")
                print(f"{'=' * 60}")
                if new_value == '':
                    break
                if option == '4' or option =='8':
                    try:
                        new_value = int(new_value)
                        if option == '4':
                            update_attribute(ISBNtoUpdate, attributes[option], new_value)
                        elif option == '8':
                            logging.info(f'{staff} replaced ISBN {ISBNtoUpdate} to {new_value}')
                            library[new_value] = library[ISBNtoUpdate]
                            del library[ISBNtoUpdate]
                            with shelve.open('LibraryDB') as db:
                                db['library'] = library
                    except ValueError:
                        print(f'Enter only numbers')
                else:
                    update_attribute(ISBNtoUpdate, attributes[option], new_value)
            else:
                print(f'\n{"=" * 30}\n '
                      f'Please select a valid option\n'
                      f'{"=" * 30}\n')


# Delete book from the dictionary, only staff is able to access (Logs)
def del_book():
    while True:
        delete = input("\nEnter ISBN you wish to delete (enter nothing to return): ")
        if delete == '':
            break

        while not delete.isnumeric():
            print(f"\n{'=' * 27}")
            print(f'Please input only numbers!')
            print(f"{'=' * 27}")
            delete = input("\nEnter ISBN you wish to delete (enter nothing to return): ")
        delete = int(delete)

        if delete in library.keys():
            print(f"\n{'=' * (9 + len(library[delete].Title))}")
            print(f'Deleted {library[delete].Title}')
            print(f"{'=' * (9 + len(library[delete].Title))}")

            # Log actions and save
            logging.info(f'{staff} deleted {library[delete].Title}')
            del library[delete]
            with shelve.open('LibraryDB') as db:
                db['library'] = library
            break
        else:
            print(f"\n{'=' * 16}")
            print(f'ISBN not found!')
            print(f"{'=' * 16}")

# Menu for making any changes to the library registry
def bookRecordMenu():
    while True:
        print(f"\n{'=' * 24}")
        print("1. Add book records")
        print("2. Delete book records")
        print("3. Amend book records")
        print("Enter nothing to Return")
        print(f"{'=' * 24}")
        option = input("Select an option: ")
        if option == '1':
            add_book()
        elif option == '2':
            del_book()
        elif option == '3':  # ascending
            update_records()
        elif option == '':
            break
        else:
            print(f'\n{"=" * 30}\n Please select a valid option\n{"=" * 30}\n')

# Staff can create user accounts for patrons so that they can borrow books (Logs)
def userCreation():
    print(f"\n{'=' * 28}")
    Username = input("Username: ")
    password = input("Password: ")
    print(f"{'=' * 28}")
    ReginsteredUsers.append(User(Username, password))

    # Log actions and save
    with shelve.open('UserDB') as db:
        db['User'] = ReginsteredUsers
    logging.info(f'{staff} created Username: {Username} Password: {password}')

# Staff can list all user details (Logs)
def listUsers():
    if ReginsteredUsers:
        print(f"{'=' * 30}")
        for person in ReginsteredUsers:
            print(person)

        # Log actions
        logging.info(f"{staff} viewed all user details")
    else:
        print(f"\n{'=' * 35}")
        print(f'Our user list is currently empty!')
        print(f"{'=' * 35}")

# TODO
# Sorts an array or list using the recursive quick sort algorithm
def quickSort(theSeq):
    n = len(theSeq)
    recQuickSort(theSeq, 0, n - 1)


# The recursive "in-place" implementation
def recQuickSort(theSeq, first, last):
    # Check the base case (range is trivially sorted)
    if first >= last:
        return
    else:
        # Partition the sequence and obtain the pivot position
        pos = partitionSeq(theSeq, first, last)
        # Repeat the process on the two subsequences
        recQuickSort(theSeq, first, pos - 1)
        recQuickSort(theSeq, pos + 1, last)


# Partitions the subsequence using the first key as the pivot
def partitionSeq(theSeq, first, last):
    # Save a copy of the pivot value.
    pivot = theSeq[first]  # first element of range is pivot

    # Find the pivot position and move the elements around the pivot
    left = first + 1  # will scan rightward
    right = last  # will scan leftward
    while left <= right:
        # Scan until reaches value equal or larger than pivot (or right marker)
        while left <= right and theSeq[left] < pivot:
            left += 1
        # Scan until reaches value equal or smaller than pivot (or left marker)
        while left <= right and theSeq[right] > pivot:
            right -= 1

        # Scans did not strictly cross
        if left <= right:
            # swap values
            theSeq[left], theSeq[right] = theSeq[right], theSeq[left]
            # Shrink range (Recursion: Progress towards base case)
            left += 1
            right -= 1

    # Put the pivot in the proper position (marked by the right index)
    theSeq[first], theSeq[right] = theSeq[right], pivot

    # Return the index position of the pivot value.
    return right


# Staff can list the details of a specific book
def bookDetail():
    while True:
        print(f"\n{'=' * 32}")
        print(f"enter nothing to return")
        bookISBN = input("ISBN of the book: ")
        print(f"{'=' * 32}")

        # Return from menu / terminate process
        if bookISBN == '':
            break

        # If input is not numerical, keep prompting user
        while not bookISBN.isnumeric():
            print(f"\n{'=' * 27}")
            print(f'Please input only numbers!')
            print(f"{'=' * 27}")
            print(f"\n{'=' * 32}")
            bookISBN = input("ISBN of the book: ")
            print(f"{'=' * 32}")
        bookISBN = int(bookISBN)

        if bookISBN in library.keys():
            print(f"\n{'=' * 30}")
            print(library[bookISBN])
            break
        else:
            print(f"\n{'=' * (16 + len(str(bookISBN)))}")
            print(f'ISBN {bookISBN} not found')
            print(f"{'=' * (16 + len(str(bookISBN)))}")

# Users can return the book they have borrowed (Logs)
def Return():
    for Username in ReginsteredUsers:
        if Username.name == user:
            if Username.borrow:
                for value in library.values():
                    if value.Title == Username.book:
                        value.NumberOfCopies += 1
                        value.Availability = True
                        break
                print(f"\n{'=' * (21 + len(Username.book))}")
                print(f'{Username.book} has been returned!')
                print(f"{'=' * (21 + len(Username.book))}")

                # Log actions and save
                logging.info(f"{user} has returned {Username.book}")
                Username.book = ''
                Username.borrow = False
                with shelve.open('LibraryDB') as db:
                    db['library'] = library

                with shelve.open('UserDB') as db:
                    db['User'] = ReginsteredUsers
            else:
                print(f"\n{'=' * 33}")
                print(f"You don't have a book to return")
                print(f"{'=' * 33}")

# Add Customer Request
def add_customer_request():
    exist = False
    customer_id = input("\nEnter Customer ID: ")
    while not customer_id.isnumeric():
        if customer_id == '':
            break
        print(f"\n{'=' * 27}")
        print(f'Please input only numbers!')
        print(f"{'=' * 27}")
        customer_id = input("\nEnter Customer ID: ")
    if not customer_id == '':
        for Cust in ReginsteredUsers:
            if Cust.ID == int(customer_id):
                exist = True
                customer_request = input("Enter Customer's Request: ")

                # Sequential search validation for entire request
                if sequential_search_customer_request(Que_customer_requests, customer_id, customer_request):
                    print("Customer request already exists in the queue.")
                else:
                    Que_customer_requests.append(ClassCustomerRequest(customer_id, customer_request))
                    print("Customer request added successfully.\n")
        if not exist:
            print(f'ID does not exist')


# Sequential Search for Customer Request
def sequential_search_customer_request(queue, target_request_id, target_request):
    for request in queue:
        if request.Customer_ID == target_request_id and request.Customer_request == target_request:
            return True
    return False


def view_number_of_customer_requests():
    print(f"\nNumber of customer requests in the queue: {len(Que_customer_requests)}")

# Process Next Customer Request
def process_next_customer_request():
    if len(Que_customer_requests) == 0:
        print("\nNo customer requests in the queue.")
    else:
        next_request = Que_customer_requests.popleft()
        for Cust in ReginsteredUsers:
            if Cust.ID == int(next_request.Customer_ID):
                print(f"\nProcessing customer request for Customer {Cust}")
                print(f"\nRequests: {next_request.Customer_request}")
                break
        print(f"Number of remaining customer requests: {len(Que_customer_requests)}")

def manage_customer_requests():
    while True:
        print(f"\n{'=' * 30}")
        print("Manage Customer Requests")
        print("1. Add Customer Request")
        print("2. View Number of Customer Requests")
        print("3. Process Next Customer Request")
        print("Enter nothing to Return to Main Menu")
        print(f"{'=' * 30}")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_customer_request()
        elif choice == '2':
            view_number_of_customer_requests()
        elif choice == '3':
            process_next_customer_request()
        elif choice == '':
            break
        else:
            print(f'\n{"=" * 30}\n Please select a valid option\n{"=" * 30}\n')

# Menu that staff will see (Logs on log out)
def staffMenu():
    while True:
        print(f"\n{'=' * 50}")
        print("1. Display all book records")
        print("2. Append/Amend book records")
        print("3. Sort books by their Publisher alphabetically")
        print("4. Sort books by their Number of Copies")
        print("5. Create user")
        print("6. List all users")
        print("7. List the details of a book")
        print("8. Sort books by their Title alphabetically ")
        print("9. Sort books by their Language and ISBN")
        print("10. Manage Customer Requests")
        print("Enter nothing to Logout")
        print(f"{'=' * 50}")
        option = input("Select an option: ")
        if option == '1':
            staff_display_all_books()
        elif option == '2':
            bookRecordMenu()
        elif option == '3':  # ascending
            publisher_bubble_sort()
        elif option == '4':  # descending
            NOC_insertion_sort()
        elif option == '5':
            userCreation()
        elif option == '6':
            listUsers()
        elif option == '7':
            bookDetail()
        elif option == '8':
            sort_and_display_books_by_title()
        elif option == '9':
            sort_and_display_books_by_language_and_isbn()
        elif option == '10':
            manage_customer_requests()
        elif option == '':
            # Log actions
            logging.info(f'{staff} logged out')
            break
        else:
            print(f'\n{"=" * 30}\n Please select a valid option\n{"=" * 30}\n')

# Menu that guest will see (Logs on log out)
def guestMenu():
    while True:
        print(f'\n{"=" * (50)}')
        print("1. Display all book records")
        print("2. Sort books by their Publisher alphabetically")
        print("3. Sort books by their Number of Copies")
        print("4. Search for a book")
        print("5. Sort books by their Title alphabetically ")
        print("6. Sort books by their Language and ISBN")
        print("Enter nothing to Logout")
        print(f'{"=" * (50)}')
        option = input("Select an option: ")
        if option == '1':
            display_all_books()
        elif option == '2':  # ascending
            publisher_bubble_sort()
        elif option == '3':  # descending
            NOC_insertion_sort()
        elif option == '4':
            bookSearch()
        elif option == '5':
            sort_and_display_books_by_title()
        elif option == '6':
            sort_and_display_books_by_language_and_isbn()
        elif option == '':
            # Log actions
            logging.info(f'Guest logged out')
            break
        else:
            print(f'\n{"=" * 30}\n Please select a valid option\n{"=" * 30}\n')

# Menu that users will see (Logs on log out)
def UserMenu():
    while True:
        print(f"\n{'=' * 50}")
        print("1. Display all book records")
        print("2. Sort books by their Publisher alphabetically")
        print("3. Sort books by their Number of Copies")
        print("4. Search for a book")
        print("5. Borrow a book")
        print("6. Book return")
        print("7. Sort books by their Title alphabetically ")
        print("8. Sort books by their Language and ISBN")
        print('9. Display popular books')
        print("Enter nothing to Logout")
        print(f"{'=' * 50}")
        option = input("Select an option: ")
        if option == '1':
            display_all_books()
        elif option == '2':  # ascending
            publisher_bubble_sort()
        elif option == '3':  # descending
            NOC_insertion_sort()
        elif option == '4':
            bookSearch()
        elif option == '5':
            Borrow()
        elif option == '6':
            Return()
        elif option == '7':
            sort_and_display_books_by_title()
        elif option == '8':
            sort_and_display_books_by_language_and_isbn()
        elif option == '9':
            popular()
        elif option == '':
            # Log actions
            logging.info(f'{user} logged out')
            break
        else:
            print(f'\n{"=" * 30}\n Please select a valid option\n{"=" * 30}\n')

def popular():
    # Create a list of tuples (ISBN, book) sorted by borrowed count
    sorted_books = sorted(library.items(), key=lambda x: x[1].borrowed or 0, reverse=True)

    # Display the top 5 books
    print("Top 5 Most Popular Books:")
    for i, (isbn, book) in enumerate(sorted_books[:5], 1):
        print(f"{i}. '{book.Title}' by {book.Author} - Borrowed {book.borrowed or 0} times")


# Users can borrow a book (Logs)
def Borrow():
    for Username in ReginsteredUsers:
        if Username.name == user:

            if Username.borrow:
                print(f"\n{'=' * (42 + len(Username.book))}")
                print(f'Please return {Username.book} before borrowing another!')
                print(f"{'=' * (42 + len(Username.book))}")
            else:
                while True:
                    print(f"\n{'=' * 82}")
                    borrowBook = input("Enter the name of the book you want to borrow (enter nothing to return): ").lower().strip()
                    print(f"{'=' * 82}")
                    if borrowBook == '':
                        break
                    book_list = list(library.values())
                    found = False
                    for book in book_list:
                        if borrowBook in book.Title.lower().strip():
                            if book.Availability:
                                print(f'\n{"=" * (36 + len(book.Title))}\n'
                                      f'{book.Title} borrowed! Please return in a week!\n'
                                      f'{"=" * (36 + len(book.Title))}')

                                # Log actions and save
                                logging.info(f'{user} borrowed {book.Title}')
                                found = True
                                Username.borrow = True
                                Username.book = book.Title
                                book.NumberOfCopies -= 1
                                if book.borrowed == None:
                                    book.borrowed = 1
                                else:
                                    book.borrowed += 1
                                if book.NumberOfCopies <= 0:
                                    book.Availability = False
                                with shelve.open('LibraryDB') as db:
                                    db['library'] = library
                                with shelve.open('UserDB') as db:
                                    db['User'] = ReginsteredUsers

                            else:
                                print(f'\n{"=" * 57}\n'
                                      f'That book currently not available! Comeback another day!\n'
                                      f'{"=" * 57}')
                                found = True
                    if not found:
                        print(f'\n{"=" * (36+ len(borrowBook))}\n'
                              f'Apologies, {borrowBook} is not in our registry\n'
                              f'{"=" * (36+ len(borrowBook))}')
                    elif found:
                        break

# Main menu that ask users to continue as guest or log in
def main():
    while True:
        print(f'\n{"=" * (34)}')
        print("1. Continue as guest")
        print("2. Login as Staff")
        print("3. Login as User")
        print("Enter nothing to exit the program")
        print(f'{"=" * (34)}')
        option = input("Select an option: ")
        if option == '2':
            global staff
            staff = staffLogin()

            if not staff:
                pass
            else:
                staffMenu()

        elif option == '1':
            # Log actions
            logging.info(f'Guest login')
            guestMenu()

        elif option == '3':
            global user
            user = userLogin()

            if not user:
                pass
            else:
                UserMenu()
        elif option == '':
            # Log actions
            logging.critical(f'Program closed')
            break
        else:
            print(f'\n{"=" * 30}\n'
                  f'Please select a valid option\n'
                  f'{"=" * 30}')

logging.critical(f'Program Initiation')
main()

# override the old library with the new one to reflect the changes
with shelve.open('LibraryDB') as db:
    db['library'] = library

with shelve.open('UserDB') as db:
    db['User'] = ReginsteredUsers
