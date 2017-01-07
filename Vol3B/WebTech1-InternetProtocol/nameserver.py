# nameserver.py
"""Vol 3B: Web Tech 1 (Internet Protocols). Auxiliary file.
<Name>
<Class>
<Date>
"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import os

names = {   "Babbage": "Charles",
            "Berners-Lee": "Tim",
            "Boole": "George",
            "Cerf":"Vint",
            "Dijkstra":"Edsger",
            "Hopper":"Grace",
            "Knuth":"Donald",
            "von Neumann":"John",
            "Russel":"Betrand",
            "Shannon":"Claude",
            "Turing":"Alan"        }

class NameServerHTTPRequestHandler(BaseHTTPRequestHandler):
    """Custom HTTPRequestHandler class"""

    def do_GET(self):
        """Handle GET command"""
        self.send_response(200)

        parsed_path = urlparse.urlparse(self.path)
        try:
            params = dict([p.split('=') for p in parsed_path[4].split('&')])
        except:
            params = {}

        # Send header first
        self.send_header("Content-type","text-html")
        self.end_headers()

        # Send content to client
        try:
            self.wfile.write(names[params["lastname"]])
        except:
            self.wfile.write("I don\'t know that person.")
        return

def run():
    # Print("http server is starting...")
    server_address = ("0.0.0.0", 8000)
    httpd = HTTPServer(server_address, NameServerHTTPRequestHandler)
    print("http server is running...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
