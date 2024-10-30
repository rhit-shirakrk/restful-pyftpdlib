from flask import Flask
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

DEFAULT_USERNAME = "user"
DEFAULT_PASSWORD = "12345"
DEFAULT_PORT = 10000

app = Flask(__name__)

# Instantiate a dummy authorizer for managing 'virtual' users
authorizer = DummyAuthorizer()

# Define a new user having full r/w permissions and a read-only
# anonymous user
authorizer.add_user(DEFAULT_USERNAME, DEFAULT_PASSWORD, ".", perm="elradfmwMT")

# Instantiate FTP handler class
handler = FTPHandler
handler.authorizer = authorizer

# Define a customized banner (string returned when client connects)
handler.banner = "pyftpdlib based FTP server ready."

# Specify a masquerade address and the range of ports to use for
# passive connections.  Decomment in case you're behind a NAT.
# handler.masquerade_address = '151.25.42.11'
# handler.passive_ports = range(60000, 65535)
# Instantiate FTP server class and listen on all interfaces, port 10000
address = ("", DEFAULT_PORT)
server = FTPServer(address, handler)

# set a limit for connections
server.max_cons = 256
server.max_cons_per_ip = 5

# setup api endpoints
@app.route("/get_demo", methods=["GET"])
def run_get_demo():
    return "Received a GET request"

@app.route("/post_demo", methods=["POST"])
def run_post_demo():
    return "Received a POST request"

@app.route("/put_demo", methods=["PUT"])
def run_put_demo():
    return "Received a PUT request"

@app.route("/delete_demo", methods=["DELETE"])
def run_delete_demo():
    return "Received a DELETE request"

# start ftp server
print(
    f"To access the RESTful server, connect with username {DEFAULT_USERNAME}, password {DEFAULT_PASSWORD}, on port {DEFAULT_PORT}"
)
server.serve_forever()
