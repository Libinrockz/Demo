import mysql.connector
import re
from tabulate import tabulate
from datetime import date, timedelta

# Connect to MySQL database
databaseobj = mysql.connector.connect(
    host='localhost',
    user='root',
    password='faith',
    database='library'
)
login = databaseobj.cursor()

# Create database and tables
login.execute("CREATE DATABASE IF NOT EXISTS library")
login.execute("USE library")

login.execute("CREATE TABLE IF NOT EXISTS Users ("
              "user_id INT AUTO_INCREMENT PRIMARY KEY,"
              "first_name VARCHAR(50),"
              "last_name VARCHAR(50),"
              "mobile_number VARCHAR(10),"
              "email_id VARCHAR(50),"
              "username VARCHAR(50) Unique,"
              "password VARCHAR(50),"
              "role VARCHAR(50))")

login.execute("CREATE TABLE IF NOT EXISTS genre ("
              "genre_id INT AUTO_INCREMENT PRIMARY KEY,"
              "genre_name VARCHAR(50))")

login.execute("CREATE TABLE IF NOT EXISTS author ("
              "author_id INT AUTO_INCREMENT PRIMARY KEY,"
              "author_name VARCHAR(50))")

login.execute("CREATE TABLE IF NOT EXISTS Books ("
              "book_id INT AUTO_INCREMENT PRIMARY KEY,"
              "book_title VARCHAR(50),"
              "author_id INT,"
              "genre_id INT,"
              "published_year Year,"
              "price varchar(50) default '$15',"
              "status varchar(50) default 'Available',"
              "FOREIGN KEY(author_id) REFERENCES author(author_id),"
              "FOREIGN KEY(genre_id) REFERENCES genre(genre_id))")

login.execute("CREATE TABLE IF NOT EXISTS Membership ("
              "mem_id INT AUTO_INCREMENT PRIMARY KEY,"
              "membership_plan VARCHAR(50),"
              "start_date DATE,"
              "end_date DATE,"
              "price varchar(50),"
              "user_id INT,"
              "FOREIGN KEY(user_id) REFERENCES Users(user_id))")

login.execute("CREATE TABLE IF NOT EXISTS Payment ("
              "payment_id INT AUTO_INCREMENT PRIMARY KEY,"
              "payment_method VARCHAR(50),"
              "payment_date DATE,"
              "amount DECIMAL(10,2),"
              "user_id INT,"
              "FOREIGN KEY(user_id) REFERENCES Users(user_id))")

login.execute("CREATE TABLE IF NOT EXISTS Rent ("
              "rent_id INT AUTO_INCREMENT PRIMARY KEY,"
              "rent_amount varchar(50),"
              "rent_start_date DATE,"
              "rent_end_date DATE,"
              "user_id INT,"
              "book_id INT,"
              "FOREIGN KEY(user_id) REFERENCES Users(user_id),"
              "FOREIGN KEY(book_id) REFERENCES Books(book_id))")

# Function to register a user

def register():
    while True:
        try:
            global user_id
            print("To Register! \n Enter Your Details Below...")
            while True:
                first_name = input("Enter the first name: ")
                if re.fullmatch("[A-Za-z]{3,25}", first_name):
                    break
                else:
                    print("Wrong Attempt! Use only alphabets of length 3 to 25.")
            while True:
                last_name = input("Enter the last name: ")
                if re.fullmatch("[A-Za-z]{1,25}", last_name):
                    break
                else:
                    print("Wrong Attempt! Use only alphabets of length 1 to 25.")
            while True:
                mobile_number = input("Enter the phone number: ")
                if re.fullmatch(r'^[6-9]\d{9}$', mobile_number):
                    break
                else:
                    print("Wrong Attempt! Use only numbers.")
            while True:
                email_id = input("Enter the e-mail id: ")
                if re.fullmatch(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email_id):
                    break
                else:
                    print("Wrong Attempt! Use a valid email format.")
            while True:
                username = input("Enter the user name: ")
                if re.fullmatch("[A-Za-z]{3,25}", username):
                    break
                else:
                    print("Wrong Attempt! Use only alphabets of length 3 to 25.")
            while True:
                password = input("Enter the password: ")
                if " " not in password:
                    if re.fullmatch(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+!_]).{6,16}$', password):
                        break
                    else:
                        print("""Password should contain a capital & a small letter with a special character 
                        [eg: Example12@] and should be 6 to 16 characters long.""")
                else:
                    print("INVALID!!! Password should not contain spaces.")

            insert_query = "INSERT INTO Users(first_name, last_name, mobile_number, email_id, username, password)" \
                           "VALUES(%s, %s, %s, %s, %s, %s)"
            login.execute(insert_query, (first_name, last_name, mobile_number, email_id, username, password))
            databaseobj.commit()
            print("You have successfully Signed Up")
            user_login()
            break
        except Exception as e:
            print("Error:", e)




def list_all_book():
    query = '''
        SELECT 
            Books.book_id, 
            Books.book_title, 
            author.author_name, 
            genre.genre_name, 
            Books.published_year, 
            Books.status, 
            Books.price
        FROM 
            Books
        JOIN 
            author ON Books.author_id = author.author_id
        JOIN 
            genre ON Books.genre_id = genre.genre_id
        '''

    login.execute(query)
    query_result = login.fetchall()

    if query_result:
        print(tabulate(query_result,
                       headers=["Book ID", "Book Title", "Author", "Genre", "Published Year", "Status", "Price"],
                       tablefmt="psql"))
    else:
        print("The list is empty.")

def membership_plan():
    query = 'SELECT mem_id, membership_plan, price FROM Membership'
    login.execute(query)
    query_result = login.fetchall()
    print(tabulate(query_result, headers=["mem_id", "membership_plan","price"],tablefmt="psql"))

def monthly_plan():
    query = 'SELECT mem_id, membership_plan, price FROM Membership WHERE membership_plan LIKE "%Monthly%"'
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["mem_id", "membership_plan","price"],tablefmt="psql"))
    else:
        print("No Monthly Plans available.")

def annual_plan():
    query = 'SELECT mem_id, membership_plan, price FROM Membership WHERE membership_plan LIKE "%Annual%"'
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["mem_id", "membership_plan","price"],tablefmt="psql"))
    else:
        print("No Annual Plans available.")


def select_a_plan():
    query = 'SELECT mem_id, membership_plan, price FROM Membership'
    login.execute(query)
    query_result = login.fetchall()
    print(tabulate(query_result, headers=["mem_id", "membership_plan", "price"],tablefmt="psql"))

    user_id = input("Enter your User ID: ").isdigit()
    mem_id = input("Enter the Membership ID of the plan you want to select: ").isdigit()

    # Update the Membership table with the selected plan
    update_query = """
        UPDATE Membership
        SET user_id = %s
        WHERE mem_id = %s
    """
    login.execute(update_query, (user_id, mem_id))
    databaseobj.commit()

    print(f"Membership plan {mem_id} has been selected for User ID {user_id}.")

def plans():
    while True:
        print("""                       
        -> Choose a membership plan to continue:
        1. Monthly Plans
        2. Annual Plans
        3. Show all plans
        4. Select a plan
        5. Go Back
        """)
        choice = input("Enter your choice from above list: ")
        if choice == "1":
            print("Checkout the Monthly Plans")
            monthly_plan()
        elif choice == "2":
            print("Checkout the Annual Plans")
            annual_plan()
        elif choice == "3":
            print("Checkout all the Membership Plans")
            membership_plan()
        elif choice == "4":
            print("Select a Membership Plan")
            select_a_plan()
        elif choice == "5":
            break

        else:
            print("Invalid CHOICE! Enter numbers from 1 to 3 only...")

def search_by_title():
    while True:
        book_title = input("Enter the book title you want to search for: ")
        if re.fullmatch("[A-Za-z]{3,25}", book_title):
            break
        else:
            print("Wrong Attempt! Use only alphabets of length 3 to 25.")
    search_query = "SELECT book_id, book_title FROM Books WHERE book_title=%s"
    login.execute(search_query, (book_title,))
    book = login.fetchone()
    if book:
        print(f"Book found: {book[1]}")
        return book[0], book[1]
    else:
        print("Book not found. Please check the title and try again.")
        return None, None

def search_by_genre():
    genre_query = "SELECT genre_name FROM genre"
    login.execute(genre_query)
    genres = login.fetchall()
    if genres:
        print("Available Genres:")
        for genre in genres:
            print(f"- {genre[0]}")
        genre_name = input("Enter the genre name: ").strip()
        if genre_name in [g[0] for g in genres]:
            search_query = """
                SELECT b.book_id, b.book_title FROM Books b
                JOIN genre g ON b.genre_id = g.genre_id
                WHERE g.genre_name = %s
            """
            login.execute(search_query, (genre_name,))
            books = login.fetchall()
            if books:
                print(f"Books under genre {genre_name}:")
                for book in books:
                    print(f"- {book[1]}")
                return [book[0] for book in books], genre_name
            else:
                print("No books found under this genre.")
                return None, None
        else:
            print("Genre not found. Please check and try again.")
            return None, None
    else:
        print("No genres found.")
        return None, None


def confirm_rental(book_id, book_title):
    confirm = input(f"Do you want to rent '{book_title}' for $15? (yes/no): ").lower()
    if confirm == 'yes':
        rent_amount = 15.00  # Fixed rent amount
        rent_start_date = date.today()  # Today's date
        rent_end_date = rent_start_date + timedelta(weeks=1)  # 1 week later

        user_id = input("Enter your user ID: ")

        # Insert rent details into the Rent table
        rent_query = """
            INSERT INTO Rent (rent_amount, rent_start_date, rent_end_date, user_id, book_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        login.execute(rent_query, (rent_amount, rent_start_date, rent_end_date, user_id, book_id))
        databaseobj.commit()

        print(f"Book '{book_title}' has been rented successfully!")
        print(f"Rent Start Date: {rent_start_date}")
        print(f"Rent End Date: {rent_end_date}")
    else:
        print("You have cancelled renting a book.")


# Function to rent a book, with options to search by title or genre
def rent_book():
    query = 'SELECT * FROM Books'
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result,
                       headers=["book_id", "book_title", "author_id", "genre_id", "published_year", "status", "price",""],tablefmt="psql"))
    else:
        print("The list is empty.")

    while True:
        print("""
        -> Choose an option to search for a book:
        1. Search by Book Title
        2. Search by Genre
        """)
        choice = input("Enter your choice (1 or 2): ")

        if choice == "1":
            book_id, book_title = search_by_title()
            if book_id:
                confirm_rental(book_id, book_title)
                break
        elif choice == "2":
            book_id, book_title = search_by_genre()
            if book_id:
                confirm_rental(book_id, book_title)
                break
        else:
            print("Invalid choice. Please select 1 or 2.")


def list_of_books():
    query = '''
    SELECT 
        Books.book_id, 
        Books.book_title, 
        author.author_name, 
        genre.genre_name, 
        Books.published_year, 
        Books.status, 
        Books.price
    FROM 
        Books
    JOIN 
        author ON Books.author_id = author.author_id
    JOIN 
        genre ON Books.genre_id = genre.genre_id
    '''

    login.execute(query)
    query_result = login.fetchall()

    if query_result:
        print(tabulate(query_result,
                       headers=["Book ID", "Book Title", "Author", "Genre", "Published Year", "Status", "Price"],
                       tablefmt="psql"))
    else:
        print("The list is empty.")


def add_book():
    while True:
        book_title = input("Enter the book name: ").title()
        if re.match("^[A-Za-z\s]+$", book_title):
            break
        else:
            print("Wrong Attempt! Use only alphabets")

    while True:
        author_name = input("Enter the author name: ").title()
        if re.match("^[A-Za-z\s]+$", author_name):
            # Check if the author already exists
            check_author_query = "SELECT author_id FROM author WHERE author_name = %s"
            login.execute(check_author_query, (author_name,))
            author = login.fetchone()
            if author:
                author_id = author[0]
                print(f"Author '{author_name}' already exists.")
            else:
                # Insert the new author into the author table
                insert_author_query = "INSERT INTO author (author_name) VALUES (%s)"
                login.execute(insert_author_query, (author_name,))
                databaseobj.commit()
                author_id = login.lastrowid
                print(f"Author '{author_name}' added successfully.")
            break
        else:
            print("Wrong Attempt! Use only alphabets")

    while True:
        genre_name = input("Enter the genre: ").title()
        if re.match("^[A-Za-z\s]+$", genre_name):
            # Check if the genre already exists
            check_genre_query = "SELECT genre_id FROM genre WHERE genre_name = %s"
            login.execute(check_genre_query, (genre_name,))
            genre = login.fetchone()
            if genre:
                genre_id = genre[0]
                print(f"Genre '{genre_name}' already exists.")
            else:
                # Insert the new genre into the genre table
                insert_genre_query = "INSERT INTO genre (genre_name) VALUES (%s)"
                login.execute(insert_genre_query, (genre_name,))
                databaseobj.commit()
                genre_id = login.lastrowid
                print(f"Genre '{genre_name}' added successfully.")
            break
        else:
            print("Wrong Attempt! Use only alphabets")

    while True:
            published_year = input("Enter the published year (YYYY): ")
            if published_year.isdigit() and len(published_year) == 4 and 1900 <= int(published_year) <= 2024:
                break
            else:
                print("Invalid year. Please enter a valid year between 1900 and 2024.")

    # Insert the book details into the Books table
    insert_book_query = "INSERT INTO Books (book_title, author_id, genre_id, published_year) VALUES (%s, %s, %s, %s)"
    login.execute(insert_book_query, (book_title, author_id, genre_id, published_year))
    databaseobj.commit()

    print(f"Book '{book_title}' added successfully!")



def manage_application():
    while True:
        print("""
        -> Choose an option to manage:
        1. View Application
        2. Add Users
        """)
        choice = input("Enter your choice (1 or 2): ")

        if choice == "1":
            list_of_users()
        elif choice == "2":
            register()
        else:
            print("Invalid choice. Please select 1 or 2.")


def list_of_users():
    query = """
    SELECT username, email_id, mobile_number from Users where username != "admin"
    """
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["username", "email_id", "mobile_number",],tablefmt="psql"))
    else:
        print("The membership list is empty.")

def overdue_books():
    query = """
    SELECT u.username, b.book_title, r.rent_amount, 
           r.rent_end_date,
           CASE 
               WHEN CURDATE() > r.rent_end_date THEN DATEDIFF(CURDATE(), r.rent_end_date)
               ELSE 0
           END AS overdue_days
    FROM Users u
    JOIN Rent r ON u.user_id = r.user_id
    JOIN Books b ON r.book_id = b.book_id
    HAVING overdue_days > 0
    """
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["username", "book_title", "rent_amount", "rent_end_date", "overdue_days"],tablefmt="psql"))
    else:
        print("No overdue books found.")


def add_edit_membership_plan():
    while True:
        print("""
        -----------------------------
           ADD / EDIT MEMBERSHIP PLAN
        -----------------------------
        1. Add a New Membership Plan
        2. Edit an Existing Membership Plan
        3. View All Membership Plans
        4. Go Back
        """)
        choice = input("Enter your choice from the above list: ")

        if choice == "1":
            add_membership_plan()
        elif choice == "2":
            edit_membership_plan()
        elif choice == "3":
            membership_plan()
        elif choice == "4":
            break
        else:
            print("Invalid CHOICE! Enter numbers from 1 to 4 only...")


def add_membership_plan():
    while True:
        membership_plan = input("Enter the name of the membership plan: ").title()
        if re.match("^[A-Za-z\s]+$", membership_plan):
            break
        else:
            print("Wrong Attempt! Use only alphabets and spaces.")

    while True:
        price = input("Enter the price of the membership plan: ")
        if re.match(r"^\$\d+(\.\d{1,2})?$", price):
            break
        else:
            print("Invalid price! Enter a valid numeric value.")

    # Insert the new membership plan into the Membership table
    insert_query = "INSERT INTO Membership (membership_plan, price) VALUES (%s, %s)"
    login.execute(insert_query, (membership_plan, price))
    databaseobj.commit()
    print(f"Membership plan '{membership_plan}' added successfully!")


def edit_membership_plan():
    membership_plan()

    mem_id = input("Enter the Membership ID of the plan you want to edit: ")

    # Check if the selected membership plan exists
    select_query = "SELECT * FROM Membership WHERE mem_id = %s"
    login.execute(select_query, (mem_id,))
    result = login.fetchone()

    if result:
        print(f"Editing Membership Plan ID: {mem_id}")
        print(
            f"Current Details: Plan Name - {result[1]}, Price - {result[2]}")

        new_name = input("Enter the new name of the membership plan (leave blank to keep current): ").title()
        new_price = input("Enter the new price (leave blank to keep current): ")

        # Keep existing values if no new value is provided
        update_query = """
            UPDATE Membership 
            SET membership_plan = %s, price = %s 
            WHERE mem_id = %s
        """
        login.execute(update_query, (
            new_name if new_name else result[1],
            new_price if new_price else result[2],
            mem_id
        ))
        databaseobj.commit()
        print(f"Membership plan ID '{mem_id}' updated successfully!")
    else:
        print(f"No membership plan found with ID: {mem_id}")


def admin_menu():
    while True:
        print("""                             
        -----------------------------
                WELCOME ADMIN
        -----------------------------                          
            -> Choose an option to continue:
            1. List of books
            2. Add a Book
            3. Add/edit Membership Plans
            4. List of Users
            5. View Overdue Books
            6. Logout
        """)
        choice = input("Enter your choice from above list : ")
        if choice == "1":
            list_of_books()
        elif choice == "2":
            add_book()
        elif choice == "3":
            add_edit_membership_plan()
        elif choice == "4":
            list_of_users()
        elif choice == "5":
            overdue_books()
        elif choice == "6":
            print("You have been logged out!!!")
            break
        else:
            print("Invalid CHOICE! Enter numbers from 1 to 6 only...")


def user_login():
    while True:
        username = input("Enter the username: ")
        if username == "":
            print("This field cannot be empty.")
        else:
            break
    while True:
        password = input("Enter the password: ")
        if password == "":
            print("This field cannot be empty.")
        else:
            break

    # Query to select the username and role based on the provided username and password
    select_query = "SELECT username, role FROM Users WHERE username=%s AND password=%s COLLATE utf8mb4_bin"
    login.execute(select_query, (username, password))
    result = login.fetchone()

    if result:
        username, role = result

        if username == "admin" and role == "admin":
            print("Welcome, Admin!")
            admin_menu()  # Redirect to admin menu
        else:
            print(f"Welcome, {username}!")
            user_menu()  # Redirect to user menu
    else:
        print("Invalid username or password. Please try again.")

def guest_user():
    while True:
        print("""                             
        -------------------------------------
                WELCOME GUEST - USER
        -------------------------------------                        
            -> Choose an option to continue:
            1. List all books
            2. View Membership plans
            3. Create / Register an Account
            4. Go Back
        """)
        choice = input("Enter your choice from above list : ")
        if choice == "1":
            list_all_book()
        elif choice == "2":
            membership_plan()
        elif choice == "3":
            register()
        elif choice == "4":
            print("Back to Main Menu")
            break
        else:
            print("Invalid CHOICE! Enter numbers from 1 to 4 only...")

def user_menu():
    while True:
        print("""                             
        -----------------------------
                WELCOME USER
        -----------------------------                          
            -> Choose an option to continue:
            1. List all books
            2. Purchase a Membership plan
            3. Rent a Book
            4. Search a Book by title
            5. Search a Book by genre
            6. Logout
        """)
        choice = input("Enter your choice from above list : ")
        if choice == "1":
            list_all_book()
        elif choice == "2":
            plans()
        elif choice == "3":
            rent_book()
        elif choice == "4":
            search_by_title()
        elif choice == "5":
            search_by_genre()
        elif choice == "6":
            print("You have been logged out!!!")
            break
        else:
            print("Invalid CHOICE! Enter numbers from 1 to 5 only...")

if __name__ == "__main__":
    while True:
        print("""
        ---------------------------------------------------
            WELCOME TO ONLINE LIBRARY MANAGEMENT SYSTEM
        ---------------------------------------------------
              -> Choose an option :
              1. Guest User
              2. Register
              3. Login
              4. Exit
        """)
        number = input("Enter a number from above list : ")
        if number == "1":
            guest_user()
        elif number == "2":
            register()
        elif number == "3":
            print("TO LOGIN  \nUse your Username & Password to Login")
            user_login()
        elif number == "4":
            print("""
            ---------------------------
                    THANK YOU
            ---------------------------
            """)
            break
        else:
            print("Invalid CHOICE! Enter numbers from 1 to 4 only...")

