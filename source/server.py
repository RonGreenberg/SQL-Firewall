import client
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
        ) as connection:
            # get the hostname
            host = socket.gethostname()
            port = 5000  # initiate port no above 1024

            server_socket = socket.socket()  # get instance
            # look closely. The bind() function takes tuple as argument
            server_socket.bind((host, port))  # bind host address and port together

            # configure how many client the server can listen simultaneously
            server_socket.listen(2)
            conn, address = server_socket.accept()  # accept new connection
            print("Connection from: " + str(address))
            data = "SQL injection demonstration #1 - OR ''='" \
                   "\nEnter Reviewer First Name: "
            conn.send(data.encode())
            while True:
                # receive data stream. it won't accept data packet greater than 1024 bytes
                data = conn.recv(1024).decode()
                if not data:
                    # if data is not received break
                    break
                # print("from connected user: " + str(data))
                query = "SELECT * FROM reviewers WHERE first_name='" + data + "';"
                with connection.cursor(buffered=True) as cursor:
                    cursor.execute(query)
                    connection.commit()
                    data = cursor.fetchall()
                conn.send(str(data).encode())  # send data to the client

            conn.close()  # close the connection
    except Error as e:
        print(e)


if __name__ == '__main__':
    server_program()