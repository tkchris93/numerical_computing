# HTTPchatnameserver.py
"""Vol 3B: Web Tech 1 (Internet Protocols). Solutions file."""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import os

Names = {}

# Create custom HTTPRequestHandler class
class NameServerHTTPRequestHandler(BaseHTTPRequestHandler):

    # Handle GET command
    def do_GET(self):
        self.send_response(200)

        # parsed_path gives a result like this: ParseResult(scheme='', netloc='', path='/', params='', query='lastname=AllNames', fragment='')
        parsed_path = urlparse.urlparse(self.path)
        print parsed_path

        try:
            # Pull out the queries and put them in a dictionary, else make the dictionary empty
            # Example params: {'lastname': 'AllNames'}
            params = dict([p.split('=') for p in parsed_path[4].split('&')])
        except:
            params = {}

        # Send header first
        self.send_header('Content-type','text-html')
        self.end_headers()

        # Send content to client
        for name in Names:
            # Check for a match in first letters of lastname and AllNames case
            if params['name'] == name[0:len(params['name'])]:
                self.wfile.write(Names[name])
            elif params['name'] == 'AllNames':
                self.wfile.write(name + ', ' + Names[name] + '\n')
        return

    def do_PUT(self):
        # Only changes from GET are in the try at the end
        self.send_response(200)

        parsed_path = urlparse.urlparse(self.path)
        print parsed_path
        try:
            params = dict([p.split('=') for p in parsed_path[4].split('&')])
            print params
        except:
            params = {}

        self.send_header('Content-type','text-html')
        self.end_headers()

        # Update first name or create a new person
        try:
            Names[params['name']] = params['ipaddressport']
        except:
            self.wfile.write('Something went wrong.')
        return

def run():
    # Print('http server is starting...')
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, NameServerHTTPRequestHandler)
    print('http server is running...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
