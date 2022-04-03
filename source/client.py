import mysql.connector
from getpass import getpass

pswd = getpass("Enter password: ")

conn = mysql.connector.connect(
	host="localhost",
	user="root",
	password=pswd,
	database="online_movie_rating"
)
cursor = conn.cursor()

# SQL injection demonstration #1 - input ' OR ''=' in the console
print("SQL injection demonstration #1 - OR ''='")
user_input = input("Enter Reviewer First Name: ")
query = "SELECT * FROM reviewers WHERE first_name='" + user_input + "';"
cursor.execute(query)
print(cursor.fetchall())

# SQL injection demonstration #2 - input 2019 OR 1=1 in the console
print("SQL injection demonstration #2 - OR 1=1")
user_input = input("Enter Release Year: ")
query = "SELECT * FROM movies WHERE release_year=" + user_input + ";"
cursor.execute(query)
print(cursor.fetchall())

# SQL injection demonstration #3 - input 2019; CREATE TABLE Movies2019 AS SELECT * FROM movies WHERE release_year=2019 in the console
print("SQL injection demonstration #3 - Stacking queries")
user_input = input("Enter Release Year: ")
query = "SELECT * FROM movies WHERE release_year=" + user_input + ";"
cursor.execute(query)
print(cursor.fetchall())

# SQL injection demonstration #4 - input  in the console
# print("SQL injection demonstration #4 - Using comment")
# user_input = input("Enter Release Year: ")
# query = "SELECT * FROM movies WHERE release_year=" + user_input + ";"
# cursor.execute(query)
# print(cursor.fetchall())
