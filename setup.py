import connection
mycon, myCursor = connection.getConnection()

# Checking if db exists
myCursor.execute("Show databases")

for db in myCursor:
    # if db exists, drop it
    if(db[0] == "library"):
        myCursor.reset()
        myCursor.execute("DROP DATABASE library")

myCursor.execute("CREATE DATABASE library")
myCursor.execute("use library")

# Creating Tables
myCursor.execute("CREATE TABLE books(b_name VARCHAR(255), b_code INTEGER PRIMARY KEY, t_books INTEGER, subject VARCHAR(255))")
myCursor.execute("CREATE TABLE students(stu_code INT PRIMARY KEY, stu_name VARCHAR(255), stu_class INTEGER)")
myCursor.execute("CREATE TABLE issues(stu_code INT, FOREIGN KEY (stu_code) REFERENCES students(stu_code), b_code INTEGER, FOREIGN KEY (b_code) REFERENCES books(b_code), i_date VARCHAR(255), qty INT)")

# Creating Dummy Data
sqlCmd = "INSERT INTO books(b_name, b_code, t_books, subject)"
allBooks = [
    #b_name, b_code, t_books, subject
    ("My Father Pablo Escobar", 1, 5, "biography"),
    ("The Book Of Five Rings", 2, 5, "philosophy"),
    ("Jade Legacy", 3, 10, "fiction"),
    ("Atoms", 4, 5, "science"),
    ("Financial Statements", 6, 2, "accounts"),
    ("Harry Potter", 7, 3, "fiction"),
    ("The Intelligent Investory", 8, 2, "finance"),
    ("Why nations fail", 9, 4, "geography"),
    ("The Psychology Of Money", 10, 4, "finance"),
]

for book in allBooks:
    myCursor.execute(f"{sqlCmd}  VALUES('{book[0]}', {book[1]}, {book[2]}, '{book[3]}')")


# Creating Dummy Data
sqlCmd = "INSERT INTO students(stu_code, stu_name, stu_class)"
allStudents = [
    #b_name, b_code, t_books, subject
    (0, "Nishtha", 12),
    (1, "Coder", 12),
    (2, "Tarun", 12),
    (3, "Rahul", 5),
    (4, "Raju", 10),
]

for student in allStudents:
    myCursor.execute(f"{sqlCmd}  VALUES({student[0]}, '{student[1]}', {student[2]})")
mycon.commit()