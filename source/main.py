#Link to tutorial: https://realpython.com/python-mysql/#other-ways-to-connect-python-and-mysql

from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user=input("Enter username: "),
        password=input("Enter password: "),
    ) as connection:
        print(connection)
        ### CREATE NEW DB
        create_db_query = "CREATE DATABASE online_movie_rating"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)

        ### WATCH ALL EXISTING DBS:
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            for db in cursor:
                print(db)
except Error as e:
    print(e)
