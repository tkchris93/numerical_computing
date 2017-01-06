from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import os

chats = dict()

# Create custom HTTPRequestHandler class
class NameServerHTTPRequestHandler(BaseHTTPRequestHandler):

    # Handle GET command
    def do_GET(self):
        self.send_response(200)

        parsed_path = urlparse.urlparse(self.path)
        try:
            params = dict([p.split('=') for p in parsed_path[4].split('&')])
        except:
            params = {}

        # Send header first
        self.send_header('Content-type','text-html')
        self.end_headers()

        # Write all the names and messages in the chats dictionary 
        for name, messages in chats.iteritems():
            self.wfile.write(name + ':\n')
            for m in messages:
                self.wfile.write('\t' + m + '\n')
                
        return


    def do_PUT(self):
        self.send_response(200)

        parsed_path = urlparse.urlparse(self.path)
        try:
            params = dict([p.split('=') for p in parsed_path[4].split('&')])
        except:
            params = {}

        # Send header first
        self.send_header('Content-type','text-html')
        self.end_headers()

        # Update chats dictionary
        if params['name'] not in chats:
            chats[params['name']] = [params['message']]
        else: chats[params['name']].append(params['message'])

        return

def run():
    # Print('http server is starting...')
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, NameServerHTTPRequestHandler)
    print('http server is running...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
