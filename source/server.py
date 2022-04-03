import client
from detector import Detector
import socket
from getpass import getpass
from mysql.connector import connect, Error

print("Welcome!")

def server_program():
    try:
        with connect(
            host="localhost",
            user=input("Enter username: "),
            password=getpass("Enter password: "),
            database="online_movie_rating",
        ) as mysql_conn:
            #create detector
            detector = Detector()

            # get the hostname
            host = socket.gethostname()
            port = 5000  # initiate port no above 1024

            server_socket = socket.socket()  # get instance
            # look closely. The bind() function takes tuple as argument
            server_socket.bind((host, port))  # bind host address and port together

            # configure how many client the server can listen simultaneously
            print("Waiting for connection...")
            server_socket.listen(2)
            socket_conn, address = server_socket.accept()  # accept new connection
            print("Connection from: " + str(address))

            message = "SQL injection demonstration #1 - OR ''='" \
                      "\nEnter Reviewer First Name: "
            socket_conn.send(message.encode())
            user_input = socket_conn.recv(1024).decode()
            query = "SELECT * FROM reviewers WHERE first_name='" + user_input + "';"
            if detector.isInjected(query):
                result = str("SQL injection detected! \n" + detector.detectedInjectionTypes)
                socket_conn.send(str(result).encode())  # send data to the client
            else:
                result = run_query(mysql_conn, query)
                socket_conn.send(str(result).encode())  # send data to the client
            detector.detectedInjectionTypes.clear()

            message = "\nSQL injection demonstration #2 - OR 1=1" \
                      "\nEnter Release Year: "
            socket_conn.send(message.encode())
            user_input = socket_conn.recv(1024).decode()
            query = "SELECT * FROM movies WHERE release_year=" + user_input + ";"
            if detector.isInjected(query):
                result = str("SQL injection detected! \n" + detector.detectedInjectionTypes)
                socket_conn.send(str(result).encode())  # send data to the client
            else:
                result = run_query(mysql_conn, query)
                socket_conn.send(str(result).encode())  # send data to the client
            detector.detectedInjectionTypes.clear()

            message = "\nSQL injection demonstration #3 - Stacking queries" \
                      "\nEnter Release Year: "
            socket_conn.send(message.encode())
            user_input = socket_conn.recv(1024).decode()
            query = "SELECT * FROM movies WHERE release_year=" + user_input + ";"
            if detector.isInjected(query):
                result = str("SQL injection detected! \n" + detector.detectedInjectionTypes)
                socket_conn.send(str(result).encode())  # send data to the client
            else:
                result = run_query(mysql_conn, query)
                socket_conn.send(str(result).encode())  # send data to the client
            detector.detectedInjectionTypes.clear()

            socket_conn.send("bye".encode())
            socket_conn.close()  # close the connection
    except Error as e:
        print(e)

def run_query(mysql_conn, query):
    with mysql_conn.cursor(buffered=True) as cursor:
        cursor.execute(query)
        mysql_conn.commit()
        return cursor.fetchall()

if __name__ == '__main__':
    server_program()