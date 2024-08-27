import mysql.connector
import re
from tabulate import tabulate
import datetime


databaseobj = mysql.connector.connect(
    host="localhost",
    user="root",
    password="faith",
    database="Hotel"
)

login = databaseobj.cursor()

login.execute("CREATE DATABASE IF NOT EXISTS Hotel")
login.execute("USE Hotel")

login.execute("CREATE TABLE IF NOT EXISTS Users ("
              "user_id INT AUTO_INCREMENT PRIMARY KEY,"
              "first_name VARCHAR(50),"
              "last_name VARCHAR(50),"
              "mobile_number VARCHAR(10),"
              "email_id VARCHAR(50),"
              "username VARCHAR(50) Unique,"
              "password VARCHAR(50),"
              "role VARCHAR(50))")

login.execute("CREATE TABLE IF NOT EXISTS Rooms ("
              "Room_id INT AUTO_INCREMENT PRIMARY KEY,"
              "category VARCHAR(50),"
              "price_per_day_with_tax INT,"
              "status varchar(50))")

login.execute("CREATE TABLE IF NOT EXISTS PreBooking ("
              "booking_id varchar(50) PRIMARY KEY,"
              "customer_name VARCHAR(50),"
              "room_id INT,"
              "date_of_booking date,"
              "date_of_occupancy date,"
              "number_of_days int,"
              "advance_received int)")

login.execute("CREATE TABLE IF NOT EXISTS Customer ("
              "customer_id INT AUTO_INCREMENT PRIMARY KEY,"
              "booking_id varchar(50),"
              "room_id INT,"
              "contact_number varchar(15),"
              "address varchar(50),"
              "FOREIGN KEY(booking_id) REFERENCES PreBooking(booking_id),"
              "FOREIGN KEY(room_id) REFERENCES Rooms(room_id))")

print("tables created")

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


def category_list():
    select_query = "Select Room_id,category,price_per_day_with_tax from Rooms"
    login.execute(select_query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result,headers=["Room_id","category","price_per_day_with_tax",""],tablefmt="psql"))
    else:
        print("No list found")

def occupied_room_list():
    today = datetime.date.today()
    query = '''
        SELECT r.Room_id, r.category, pb.date_of_occupancy,pb.customer_name
        FROM Rooms r
        JOIN PreBooking pb ON r.Room_id = pb.room_id
        WHERE pb.date_of_occupancy BETWEEN %s AND %s AND r.status = "Occupied"
    '''
    login.execute(query, (today, today + datetime.timedelta(days=2)))
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["Room_id", "category", "date_of_occupancy","customer_name"], tablefmt="psql"))
    else:
        print("No rooms are occupied in the next two days.")

def list_of_rooms_pricewise():
    select_query = "Select Room_id,category,price_per_day_with_tax from Rooms order by price_per_day_with_tax asc"
    login.execute(select_query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["Room_id", "category", "price_per_day_with_tax", ""], tablefmt="psql"))
    else:
        print("No list found")

import re

def Search_by_booking_id():

    while True:
        booking_id = input("Enter the booking ID to search (e.g., BI123): ")
        if re.fullmatch(r"^[A-Z]{2}\d{3}$", booking_id):
            break
        else:
            print("Invalid Booking ID format! It should consist of 2 letters followed by 3 digits (e.g., AB123).")

    selectquery = """
        Select pb.booking_id, pb.customer_name, pb.Room_id, pb.date_of_booking, pb.date_of_occupancy, pb.number_of_days, pb.advance_received
        From PreBooking pb
        JOIN Customer c ON pb.booking_id = c.booking_id
        WHERE pb.booking_id = %s
    """
    login.execute(selectquery, (booking_id,))
    result = login.fetchall()
    if result:
        print(tabulate(result,
                       headers=["Booking Id", "Customer Name", "Room Id", "Date of Booking", "Date of Occupancy",
                                "Number of Days", "Advance Received"], tablefmt="psql"))
    else:
        print("No list found")

def Unoccupied_rooms():
    select_query = "Select Room_id,category,price_per_day_with_tax,status from Rooms where status = 'Unoccupied'";
    login.execute(select_query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result,headers=["Room ID", "Room Name", "Price Per Day", "Status"],tablefmt="psql"))
    else:
        print("No rooms are available")


def update_rooms():
    # Prompt the user for the Room ID
    while True:
        room_id = input("Enter the Room ID to update to 'Unoccupied': ")
        if room_id.isdigit():
            break
        else:
            print("Use only numbers")

    # Check if the room is currently occupied
    select_query = "SELECT status FROM Rooms WHERE Room_id = %s"
    login.execute(select_query, (room_id,))
    result = login.fetchone()

    if result:
        current_status = result[0]
        if current_status == "Occupied":
            # Update the room status to 'Unoccupied'
            update_query = "UPDATE Rooms SET status = 'Unoccupied' WHERE Room_id = %s"
            login.execute(update_query, (room_id,))
            databaseobj.commit()
            print(f"Room ID {room_id} has been updated to 'Unoccupied'.")
        else:
            print(f"Room ID {room_id} is already unoccupied.")
    else:
        print(f"No room found with ID {room_id}.")

def store_and_display_file():
    login.execute("SELECT * FROM Rooms")
    rooms = login.fetchall()
    with open('rooms_records.txt', 'w') as file:
        file.write(tabulate(rooms, headers=['Room ID', 'Category', 'Price per Day', 'Status'], tablefmt='plsql'))
    print("Records have been written to rooms_records.txt")
    with open('rooms_records.txt', 'r') as file:
        print(file.read())

def list_available_rooms():
    select_query = "Select Room_id,category,price_per_day_with_tax,status from Rooms where status = 'Unoccupied'";
    login.execute(select_query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["Room ID", "Room Name", "Price Per Day", "Status"], tablefmt="psql"))
    else:
        print("No rooms are available")

def book_a_room():
    try:
        # Display available rooms
        Unoccupied_rooms()

        # Prompt the user for room selection
        while True:
            room_id = input("Enter the Room ID you want to book: ")
            if room_id.isdigit():
                room_id = int(room_id)
                # Check if the room is available (Unoccupied)
                login.execute("SELECT status FROM Rooms WHERE Room_id = %s", (room_id,))
                room_status = login.fetchone()

                if room_status and room_status[0] == "Unoccupied":
                    break
                else:
                    print("The room is either occupied or does not exist. Please choose another room.")
            else:
                print("Please enter a valid Room ID (numbers only).")

        customer_name = input("Enter customer name: ")

        # Date of booking (current date)
        date_of_booking = datetime.date.today()

        # Date of occupancy (when the customer starts occupying the room)
        while True:
            try:
                date_of_occupancy = input("Enter the date you want to stay (YYYY-MM-DD): ")
                date_of_occupancy = datetime.datetime.strptime(date_of_occupancy, "%Y-%m-%d").date()
                if date_of_occupancy >= date_of_booking:
                    break
                else:
                    print("Date of occupancy cannot be before the date of booking.")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

        # Number of days the customer will occupy the room
        while True:
            try:
                number_of_days = int(input("Enter the number of days you will occupy the room: "))
                if number_of_days > 0:
                    break
                else:
                    print("Number of days must be positive.")
            except ValueError:
                print("Please enter a valid number of days.")

        # Advance received
        while True:
            try:
                advance_received = int(input("Enter the advance payment to pay: "))
                if advance_received >= 0:
                    break
                else:
                    print("Advance payment cannot be negative.")
            except ValueError:
                print("Please enter a valid amount.")

        # Generate a unique booking ID (you can customize this as needed)
        booking_id = f"BI{room_id}{int(datetime.datetime.now().timestamp())}"

        # Insert the booking into the PreBooking table
        prebooking_query = """
            INSERT INTO PreBooking (booking_id, customer_name, room_id, date_of_booking, date_of_occupancy, number_of_days, advance_received)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        login.execute(prebooking_query, (booking_id, customer_name, room_id, date_of_booking, date_of_occupancy, number_of_days, advance_received))

        # Insert the customer details into the Customer table
        customer_contact = input("Enter the contact number: ")
        customer_address = input("Enter the address: ")

        customer_query = """
            INSERT INTO Customer (booking_id, room_id, contact_number, address)
            VALUES (%s, %s, %s, %s)
        """
        login.execute(customer_query, (booking_id, room_id, customer_contact, customer_address))

        # Update the room status to "Occupied"
        update_room_query = "UPDATE Rooms SET status = 'Occupied' WHERE Room_id = %s"
        login.execute(update_room_query, (room_id,))

        # Commit the transaction
        databaseobj.commit()

        print(f"Room ID {room_id} has been successfully booked under Booking ID {booking_id}.")

    except Exception as e:
        print("An error occurred during the booking process:", e)

def user_menu():
    while True:
        print("""                             
        -----------------------------
                WELCOME USER
        -----------------------------                          
            -> Choose an option to continue:
            1. List all Available Rooms
            2. Book a room
            3. Logout
        """)
        choice = input("Enter your choice from above list : ")
        if choice == "1":
            list_available_rooms()
        elif choice == "2":
            book_a_room()
        elif choice == "3":
            print("You have been logged out!!!")
            break
        else:
            print("Invalid CHOICE! Enter numbers from 1 to 3 only...")

def admin_menu():
    while True:
        print("""                             
        -----------------------------
                WELCOME ADMIN
        -----------------------------                          
            -> Choose an option to continue:
            1. Display the Category wise list of rooms and their Rate per day
            2. List of all rooms which are occupied for next two days
            3. Display the list of all rooms in Their increasing order of rate per day
            4. Search Rooms based on BookingID and display the customer details.
            5. Display rooms which are not booked.
            6. Update room when the customer lefts to Unoccupied.
            7. Store all records in file and display from file
            8. Exit
        """)
        choice = input("Enter your choice from above list : ")
        if choice == "1":
            category_list()
        elif choice == "2":
            occupied_room_list()
        elif choice == "3":
            list_of_rooms_pricewise()
        elif choice == "4":
            Search_by_booking_id()
        elif choice == "5":
            Unoccupied_rooms()
        elif choice == "6":
            update_rooms()
        elif choice == "7":
            store_and_display_file()
        elif choice == "8":
            print("You have been logged out!!!")
            break
        else:
            print("Invalid CHOICE! Enter numbers from 1 to 8 only...")


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


if __name__ == "__main__":
    while True:
        print("""
        ---------------------------------------------------
            WELCOME TO HOTEL BOOKING MANAGEMENT SYSTEM
        ---------------------------------------------------
              -> Choose an option :
              1. Register
              2. Login
              3. Exit
        """)
        number = input("Enter a number from above list : ")
        if number == "1":
            register()
        elif number == "2":
            print("TO LOGIN  \nUse your Username & Password to Login")
            user_login()
        elif number == "3":
            print("""
            ---------------------------
                    THANK YOU
            ---------------------------
            """)
            break
        else:
            print("Invalid CHOICE! Enter numbers from 1 to 3 only...")