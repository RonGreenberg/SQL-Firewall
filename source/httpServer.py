from http.server import HTTPServer, SimpleHTTPRequestHandler
import cgi
from mysql.connector import connect, Error
from getpass import getpass
from detector import Detector

class serverHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, "OK")
        self.send_header('content-type', 'text/html')
        self.end_headers()
        hfile = open("index.html", "r")
        self.wfile.write(bytes(hfile.read(), 'utf-8'))

    def do_POST(self):
        if self.path == '/test':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                textbox = str(fields.get("textbox")[0])
                selection = str(fields.get("query")[0])
                if selection == "always_true1":
                    query = "SELECT * FROM reviewers WHERE first_name='" + textbox + "';"
                elif selection == "always_true2":
                    query = "SELECT * FROM movies WHERE release_year=" + textbox + ";"
                elif selection == "always_true3":
                    query = "SELECT * FROM ratings WHERE movie_id=" + textbox + ";"
                elif selection == "always_false":
                    query = "SELECT * FROM ratings WHERE reviewer_id=" + textbox + ";"
                elif selection == "comment":
                    query = "SELECT * FROM ratings WHERE reviewer_id=" + textbox + " AND rating=8.5;"
                elif selection == "stacking_queries":
                    query = "SELECT * FROM movies WHERE title='" + textbox + "';"
                elif selection == "union_set":
                    query = "SELECT * FROM reviewers WHERE first_name='" + textbox + "';"

                detector = Detector()
                self.send_response(200, "OK")
                self.end_headers()
                if detector.isInjected(query):
                    self.wfile.write(
                        bytes("""<html><h1 style="color: Red">SQL Injection Detected!</h1><h3 style="color: Red">\nInjection type/s: """ + str(detector.detectedInjectionTypes) + "</h3></html>", "utf-8"))
                else:
                    try:
                        with connect(
                                host="localhost",
                                user=mysql_user,
                                password=mysql_password,
                                database="online_movie_rating",
                        ) as mysql_conn:
                            with mysql_conn.cursor(buffered=True) as cursor:
                                cursor.execute(query)
                                #mysql_conn.commit()
                                result = """<html><h1>Result:</h1><table border=1 style="width: 100%; text-align: center"><tr>"""
                                for tuple in cursor.description:
                                    result += "<th>" + tuple[0] + "</th>"
                                result += "</tr>"
                                for row in cursor.fetchall():
                                    result += "<tr>"
                                    for column_value in row:
                                        result += "<td>" + str(column_value) + "</td>"
                                    result += "</tr>"
                                result += "</table></html>"
                                self.wfile.write(bytes(result, "utf-8"))
                    except Error as e:
                        print(e)

    # def do_POST(self):
    #     post_body = self.rfile.read(int(self.headers['Content-Length']))
    #     print(post_body)

global mysql_user
global mysql_password

def main():
    PORT = 5555
    HOST_NAME = "localhost"
    server = HTTPServer((HOST_NAME, PORT), serverHandler)
    print("Server running on port %s" % PORT)

    global mysql_user
    mysql_user = input("Enter MySQL username: ")
    global mysql_password
    mysql_password = getpass("Enter MySQL password: ")

    try:
        connect(
                host="localhost",
                user=mysql_user,
                password=mysql_password,
                database="online_movie_rating",
        )
    except Error as e:
        print(e)
        exit()

    print("Server waiting for connection...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server stopped successfully")

if __name__ == "__main__":
    main()