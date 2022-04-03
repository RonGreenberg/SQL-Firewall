from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import cgi

class serverHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, "OK")
        self.send_header('content-type', 'text/html')
        self.end_headers()
        hfile = open("index.html", "r")
        self.wfile.write(bytes(hfile.read(), 'utf-8'))

    def do_POST(self):
        print("hey ron")
        if self.path == '/success':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                reviewer_full_name = fields.get("reviewer_full_name")[0]
                reviewer_full_name = reviewer_full_name[:len(reviewer_full_name)//2]
                print(reviewer_full_name)

                #html = f"<html><head></head><body><h1>Form data successfully recorded!!!</h1></body></html>"
                # self.send_response(200, "OK")
                # self.end_headers()
                # self.wfile.write(bytes(html, "utf-8"))
    # def do_POST(self):
    #     post_body = self.rfile.read(int(self.headers['Content-Length']))
    #     print(post_body)

def main():
    PORT = 5555
    HOST_NAME = "localhost"
    server = HTTPServer((HOST_NAME, PORT), serverHandler)
    print("server running on port %s" % PORT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server stopped successfully")

if __name__ == "__main__":
    main()