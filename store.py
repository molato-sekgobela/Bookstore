# load sqlite3 library
import sqlite3 as sql
# import spacy library
import spacy

# This will return a Language object containing all components and data needed to process text.
nlp = spacy.load('en_core_web_md')


# display book with highest similarity in title as recommended book
def similarity(cursor, book_title):
    # select all books from database
    cursor.execute('''SELECT*FROM books''')
    # declare list variables
    split_list = []
    similarity_list = []

    # declare and initialize npl model
    model_sentence = nlp(book_title)

    # initialize counter to store number of book records in database
    cnt = 0

    # iterate through database records
    for i in cursor:
        # get list of books and their attributes and append to nested list
        split_list.append([])
        split_list[cnt].append(i[0])
        split_list[cnt].append(i[1])
        split_list[cnt].append(i[2])
        split_list[cnt].append(i[3])
        # increment counter
        cnt += 1

    # iterate through list and compare title with book titles in database
    for i in range(0, cnt):
        # check similarity between the book title with with those in database
        similarity_list.append(nlp(split_list[i][1]).similarity(model_sentence))

    # get the maximum similarity value
    max_similarity = max(similarity_list)
    # get index of highest similarity value
    max_similarity_index = similarity_list.index(max_similarity)

    # print highest similar book as recommendation in the database
    print('{:<20}{:<50}{:<20}{}'.format("ID", "Title", "Author", "Quantity"))
    print('{:<20}{:<50}{:<20}{}'.format(split_list[max_similarity_index][0], split_list[max_similarity_index][1],
                                        split_list[max_similarity_index][2], split_list[max_similarity_index][3]))


# create and populate books table
def populate_database(cursor):
    cursor.execute('''DROP TABLE IF EXISTS books''')
    # query for creating a table
    cursor.execute('''CREATE TABLE books(id INTEGER PRIMARY KEY NOT NULL UNIQUE, Title TEXT,Author TEXT,Qty INTEGER)''')
    # Query to Populate records into the books table
    cursor.execute('''INSERT INTO books(id,Title,Author,Qty)VALUES(?,?,?,?)''',
                   (3001, "A Tale of Two Cities", "Charles Dickens", 30))
    cursor.execute('''INSERT INTO books(id,Title,Author,Qty)VALUES(?,?,?,?)''',
                   (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40))
    cursor.execute('''INSERT INTO books(id,Title,Author,Qty)VALUES(?,?,?,?)''',
                   (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25))
    cursor.execute('''INSERT INTO books(id,Title,Author,Qty)VALUES(?,?,?,?)''',
                   (3004, "The Lord of The Rings", "J.R.R Tolkien", 37))
    cursor.execute('''INSERT INTO books(id,Title,Author,Qty)VALUES(?,?,?,?)''',
                   (3005, "Alice in Wonderland", "Lewis Carrol", 12))


# view all books in the database
def view_table(cursor):
    # query for creating a table
    cursor.execute('''SELECT*FROM books''')
    print('===========================================================================================================')
    print('                                          EBOOKSTORE INVENTORY                                             ')
    print('===========================================================================================================')
    # select all books and their attributes in database
    cursor.execute('''SELECT *FROM books''')
    db.commit()

    # print records in tabular format
    print('{:<20}{:<50}{:<20}{}'.format("ID", "Title", "Author", "Quantity"))
    for row in cursor:
        print('{:<20}{:<50}{:<20}{}'.format(row[0], row[1], row[2], row[3]))
    print("\n")


# add book to database
def add_book(cursor):
    # ask user to enter book information
    book_id = input("Enter book ID: ")
    book_title = input("Enter book Title: ")
    book_author = input("Enter book Author: ")
    book_quantity = input("Enter book quantity: ")
    # execute insert query
    cursor.execute('''INSERT INTO BOOKS(id,Title,Author,Qty) VALUES(?,?,?,?)''',
                   (book_id, book_title, book_author, book_quantity))
    print("Book Added!")
    # call view table function to refresh table in database to see added book
    view_table(cursor)
    print("Book Added!")


# update book in database
def update_book(cursor):
    """please note i went a step ahead and used the update as a way to update the quantity value as a book is sold, please advice if this is not correct"""
    # select all books with their attributes in the database
    cursor.execute('''SELECT*FROM books''')
    # prompt user to enter the book title
    book_title = input("Enter Book Title to Sell: ")
    # flag to check if book title is found
    book_available = False

    # loop through all books to get matching title
    for row in cursor:
        if row[1].upper() == book_title.upper():
            # display the book that is found and being sold
            print("Book Found!! See Details Below:")
            print('{:<20}{:<50}{:<20}{}'.format("ID", "Title", "Author", "Quantity"))
            print('{:<20}{:<50}{:<20}{}'.format(row[0], row[1], row[2], row[3]))
            # get current quantity of books in inventory
            quantity = row[3]
            # remove one book from inventory
            updated_qty = quantity - 1
            # update Qty field with updated Qty number to show number of books left in the inventory
            cursor.execute('''UPDATE books set Qty =? WHERE id =?''', (updated_qty, row[0]))
            # view updated table in database
            view_table(cursor)
            print("Book Sold!, Database updated!")
            # change book flag
            book_available = True
            # break loop
            break

    # if title was not found display message to clerk
    if not book_available:
        print("Book does not exist in the Database!!")


# delete book from database
def delete_book(cursor):
    # return all books from database
    cursor.execute('''SELECT*FROM books''')
    # prompt user to enter id of book to delete
    book_id = int(input("Enter book ID to delete: "))
    # declare flag to check if book exists
    book_available = False
    # loop through books
    for i in cursor:
        if i[0] == book_id:
            # delete book record if found in database
            cursor.execute('''DELETE FROM books WHERE id = ?''', (book_id,))
            # view updated table to see deleted book from database
            view_table(cursor)
            print("Book Deleted!!")
            # set flag
            book_available = True
            # break and end loop
            break
    # if book does not exist display relevant message
    if not book_available:
        print("Book does not exist in the Database!!")


# search book by title
def search_book(cursor):
    # select all books from database
    cursor.execute('''SELECT*FROM books''')
    # prompt user to enter book title
    book_title = input("Enter Book Title to search: ")

    # loop through books compare title
    for row in cursor:
        # check if title exists "not case sensitive"
        if row[1].upper() == book_title.upper():
            # delete book where title matches
            # cursor.execute('''DELETE FROM books WHERE Title= ?''', (book_title,))
            # view updated table
            view_table(cursor)
            print("Book Found!! See Details Below:")
            print('{:<20}{:<50}{:<20}{}'.format("ID", "Title", "Author", "Quantity"))
            print('{:<20}{:<50}{:<20}{}'.format(row[0], row[1], row[2], row[3]))
            # break loop
            break
        else:
            # use spacy to check highest similar book in database with title " call function to perform that"
            print("Recommendation! Similar book found according to title")
            # call function to perform similarity check
            similarity(cursor, book_title)


# try catch DB exceptions
try:
    # connect to student database
    db = sql.connect('ebookstore')
    # Get a cursor object
    cursor = db.cursor()
    db.commit()

    # create ebookstore database and books table and populate
    populate_database(cursor)
    # view database table
    view_table(cursor)

    # ask user for task to perform
    print("1. Add Book\n2. Update Book\n3. Delete Book\n4. Search Book\n0. Exit")
    user_input = input("Please Enter your option:")

    # check user input
    while user_input != "0":
        if user_input == "1":
            add_book(cursor)
        elif user_input == "2":
            update_book(cursor)
        elif user_input == "3":
            delete_book(cursor)
        elif user_input == "4":
            search_book(cursor)

        # keep prompting user to enter option
        print("1. Add Book\n2. Update Book\n3. Delete Book\n4. Search Book\n0. Exit")
        user_input = input("Please Enter your option:")
    # print terminated program message
    print("Program Terminated!")
except Exception as e:
    # Roll back any change if something goes wrong
    db.rollback()
    raise e
finally:
    # Close the db connection
    db.close()
