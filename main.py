import connection
from datetime import datetime as dt

mycon, myCursor = connection.getConnection()
myCursor.execute("USE library")

print(""" 
 _     _ _
| |   (_) |
| |    _| |__  _ __ __ _ _ __ _   _ 
| |   | | '_ \| '__/ _` | '__| | | |
| |___| | |_) | | | (_| | |  | |_| |
\_____/_|_.__/|_|  \__,_|_|   \__, |
                               __/ |
                              |___/ 
- Library Management System\n
""")


def main():
    while True:
        choice = input("(cmd)$ ").lower()
        myCursor.reset()
        if choice == 'a':
            add_book()
        elif choice == 'i':
            issue_book()
        elif choice == 'r':
            return_book()
        elif choice == 'd':
            delete_book()
        elif choice == 's':
            add_student()
        elif choice == 'c':
            delete_student()
        elif choice == 'h':
            help()
        elif choice == 'q':
            print("Bye...\n")
            exit()
        else:
            print(f"unkown cmd: {choice}")


def add_book():
    sqlCmd = "INSERT INTO books(b_name, b_code, t_books, subject)"

    try:
        b_name = input("\tBook name: ")
        b_code = int(input("\tBook code: "))
        t_books = int(input("\tTotal number of books: "))
        subject = input("\tSubject: ")

        if b_name and b_code and t_books and subject:
            myCursor.execute(
                f"{sqlCmd}  VALUES('{b_name}', {b_code}, {t_books}, '{subject}')")
            mycon.commit()
            print("Book Added\n")
        else:
            print("Missing fields - Book not added\n")
    except:
        print("Error Occured - Book not added\n")


def add_student():
    sqlCmd = "INSERT INTO students(stu_code, stu_name, stu_class)"

    try:
        stu_code = int(input("\tStudent code: "))
        stu_name = input("\tStudent name: ")
        stu_class = int(input("\tStudent class: "))

        if stu_code and stu_name and stu_class:
            myCursor.execute(
                f"{sqlCmd}  VALUES({stu_code}, '{stu_name}', {stu_class})")
            mycon.commit()
            print("Student Added\n")
        else:
            print("Missing fields - Student not added\n")
    except:
        print("Error Occured - Student not added\n")


def issue_book():
    sqlCmd = "INSERT INTO issues(stu_code, b_code, i_date, qty)"
    findBook = "SELECT * FROM books WHERE b_code ="
    alterBook = "UPDATE books set t_books="

    try:
        b_code = int(input("\tEnter book code: "))
        myCursor.execute(findBook + str(b_code))
        bookInfo = myCursor.fetchone()
        if not bookInfo:
            print(f"Book not found: {b_code}\n")
            return

        bookQty = bookInfo[2]
        if bookQty <= 0:
            print("All copies of this book issued\n")
            return

        myCursor.reset()
        stu_code = int(input("\tEnter Student Code: "))
        myCursor.execute(f"SELECT * FROM students WHERE stu_code={stu_code}")
        studentInfo = myCursor.fetchone()
        if not studentInfo:
            print(f"Student not found: {stu_code}\n")
            return

        i_date = dt.now().date()
        myCursor.reset()
        myCursor.execute(
            f"SELECT * FROM issues WHERE stu_code={stu_code} and b_code={b_code}")
        issueInfo = myCursor.fetchone()

        myCursor.reset()
        if not issueInfo:
            myCursor.execute(
                f"{sqlCmd} VALUES({stu_code}, {b_code}, '{i_date}', 1)")
        else:
            myCursor.execute(
                f"UPDATE issues set qty={issueInfo[3]+1} where stu_code={stu_code} and b_code={b_code}")

        myCursor.execute(f"{alterBook} {bookQty-1} WHERE b_code = {b_code}")
        mycon.commit()
        print(
            f"Book: {bookInfo[0]}, issued to: {studentInfo[1]}, class: {studentInfo[2]}\n")

    except:
        print("Error occured - Book not issued\n")


def return_book():
    try:
        stu_code = int(input("\tEnter Student Code: "))
        b_code = int(input("\tEnter book code: "))
        myCursor.execute(f"SELECT * FROM issues WHERE stu_code={stu_code} and b_code={b_code}")
        issueInfo = myCursor.fetchone()
        if not issueInfo:
            print("No result found\n")
            return
        myCursor.reset()

        myCursor.execute(f"SELECT * FROM students WHERE stu_code={stu_code}")
        studentInfo = myCursor.fetchone()
        myCursor.reset()
        
        myCursor.execute(f"SELECT * FROM books WHERE b_code={b_code}")
        bookInfo = myCursor.fetchone()
        
        myCursor.reset()
        if issueInfo[3] <= 1:
            myCursor.execute(f"DELETE FROM issues where stu_code={stu_code} and b_code={b_code}")
            myCursor.execute(f"UPDATE books set t_books={bookInfo[2]+1} WHERE b_code={b_code}")
        else:
            myCursor.execute(f"UPDATE issues set qty={issueInfo[3]-1} WHERE stu_code={stu_code} and b_code={b_code}")
            myCursor.execute(f"UPDATE books set t_books={bookInfo[2]+1} WHERE b_code={b_code}")
        
        mycon.commit()
        print(f"Student: {studentInfo[1]}, Returned: {bookInfo[0]}\n")
    except:
        print("Error occured - Book not returned\n")


def delete_student():
    try:
        stu_code = int(input("\tEnter Student Code: "))
        myCursor.execute(f"SELECT * FROM students WHERE stu_code={stu_code}")
        studentInfo = myCursor.fetchone()
        if not studentInfo:
            print(f"Student not found: {stu_code}\n")
            return
        print(f"\t---- Remove: {studentInfo[1]}, of class: {studentInfo[2]}")
        confirm = input("\tAre you sure?(y/n)").lower()
        if not  (confirm ==  "y"):
            print("Student not removed\n")
        else:
            myCursor.reset()
            myCursor.execute(f"DELETE FROM students where stu_code={stu_code}")
            mycon.commit()
            print("Student removed\n")
    except:
        print("Error occured - Student not removed\n")


def delete_book():
    try:
        b_code = int(input("\tEnter book Code: "))
        myCursor.execute(f"SELECT * FROM books WHERE b_code={b_code}")
        bookInfo = myCursor.fetchone()
        if not bookInfo:
            print(f"Book not found: {b_code}\n")
            return
        print(f"\t---- Remove: {bookInfo[0]}, of subject: {bookInfo[3]}")
        confirm = input("\tAre you sure?(y/n)").lower()
        if not  (confirm ==  "y"):
            print("Book not removed\n")
        else:
            myCursor.reset()
            myCursor.execute(f"DELETE FROM issues where b_code={b_code}")
            myCursor.execute(f"DELETE FROM books where b_code={b_code}")
            mycon.commit()
            print("Book removed\n")
    except KeyError:
        print("Error occured - Book not removed\n")


def help():
    print('\nCommands\n\ta = Add Books\n\ti = Issue Books\n\tr = Return Book\n\td = Delete Book\n\ts = Add Student\n\tc = Remove Student\n\th = Help\n\tq = Quit\n')


def login():
    actualPassword = open("passwd.txt", "r").readline()
    userPassword = input("Enter password: ")
    if userPassword == actualPassword:
        help()
        main()
    else:
        print("wrong password, try again\n")
    login()


login()
