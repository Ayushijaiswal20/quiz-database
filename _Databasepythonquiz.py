import mysql.connector as my
from mysql.connector import Error
import hashlib

def create_connection():
    try:
        con = my.connect(
            host="localhost",
            port="3306",
            user="root",
            password="@aryadivy06",
            database="Quiz"
        )
        if con.is_connected():
            return con
    except Error as e:
        print(f"Error: {e}")
    return None

def close_connection(con):
    if con.is_connected():
        con.close()

def fetch_data(con, query):
    try:
        cur = con.cursor()
        cur.execute(query)
        return cur.fetchall()
    except Error as e:
        print(f"Error: {e}")
    return []

def execute_query(con, query, data=None):
    try:
        cur = con.cursor()
        if data:
            cur.execute(query, data)
        else:
            cur.execute(query)
        con.commit()
    except Error as e:
        print(f"Error: {e}")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(con):
    print("Enter the information\n")
    name = input("Enter your name: ")
    enroll = input("Enter your enrollment: ")
    uid = input("Create user id for account: ")

    user_ids = [user[0] for user in fetch_data(con, "SELECT user_id FROM register")]

    if uid in user_ids:
        print("\nUser already exists, go to login or enter a new userid")
        return

    password = input("Create Password: ")
    hashed_password = hash_password(password)
    marks = 0

    query = "INSERT INTO register(Name, enrollment, user_id, password, marks) VALUES (%s, %s, %s, %s, %s)"
    data = (name, enroll, uid, hashed_password, marks)
    execute_query(con, query, data)
    print("Registration successful!")

def login(con):
    global login_status, user_id

    print("Enter your details")
    user_id = input("Enter your user id: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)

    user_data = fetch_data(con, "SELECT user_id, password FROM register WHERE user_id = %s", (user_id,))

    if user_data and user_data[0][1] == hashed_password:
        login_status = True
        print("Login successful!")
    else:
        print("Invalid user id or password")

def profile(con):
    if login_status:
        user_data = fetch_data(con, f"SELECT * FROM register WHERE user_id = '{user_id}'")
        if user_data:
            user = user_data[0]
            print(f"\nThe {user_id} information are")
            print(f"Name = {user[0]}")
            print(f"Enrollment = {user[1]}")
            print(f"User ID = {user[2]}")
            print("Password = *****")
            print(f"Marks = {user[4]}\n")
    else:
        print("\nFirst login or register")

def attempt_quiz(con):
    global marks
    if login_status:
        while True:
            print("\nChoose Subject \n1.DBMS \n2.DSA \n3.Python \n0.Exit\n")
            choice = int(input("Enter your choice: "))

            if choice == 0:
                print("\nMarks =", marks)
                break

            subject = {1: 'dbms', 2: 'dsa', 3: 'python'}.get(choice)
            if not subject:
                print("Invalid choice")
                continue

            questions = fetch_data(con, f"SELECT * FROM {subject}")
            for i, q in enumerate(questions):
                print(f"\nQue{i+1}: {q[0]}")
                for j in range(1, 5):
                    print(f"{j}. {q[j]}")
                answer = int(input("Enter your answer: "))
                if answer == q[-1]:
                    marks += 1

            query = f"UPDATE register SET marks = {marks} WHERE user_id = '{user_id}'"
            execute_query(con, query)
    else:
        print("First login")
s
def main():
    con = create_connection()
    if not con:
        return

    print("---------Welcome to Python Programming Quiz Application---------")

    while True:
        if login_status:
            print("Choose from below\n")
            print("3. Profile")
            print("4. Attempt Quiz")
            print("5. Exit")
        else:
            print("\n---Welcome---")
            print("1. Register")
            print("2. Login")
            print("3. Profile")
            print("4. Attempt Quiz")
            print("5. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            register(con)
        elif choice == 2:
            login(con)
        elif choice == 3:
            profile(con)
        elif choice == 4:
            attempt_quiz(con)
        elif choice == 5:
            print("Logging out...")
            break
        else:
            print("Invalid choice")

    close_connection(con)

if _name_ == "_main_":
    login_status = False
    user_id = ""
    marks = 0
    main()
