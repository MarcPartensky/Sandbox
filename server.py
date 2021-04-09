"""
Main server for running untrusted python shell commands.

Typically an admin will create a secret token which can be used as a post
variable. The server would use it to identify the user and let him run python
code each time a new command is being sent.

HTTP request:
    * stdin
    * token
HTTP response:
    * stderr
    * stdout

Security:
    * Token authentication
    * Role system
    * IP whitelist
    * Epicbox
    * HTTPS only, if token are sent in HTTP they will be reset
"""
import pickle
import epicbox

from flask import Flask, request

storage = Storage("storage.yml")

app = Flask(__name__)
epicbox.configure(
    profiles=[
        epicbox.Profile('python', 'python:3.9')
    ]
)

@app.route('/')
def index():
    """Main view."""
    if request.method != 'POST':
        return "Only post methods are accepted"

    login(request)
    run(request)

def login(request):
    """Throw error if login fails."""
    user = storage.token[request.token]

def run():
    """Run the request."""
    files = [{'name': 'main.py', 'content': bytes(request.stdin)}]
    limits = {'cputime': 1, 'memory': 64}
    result = epicbox.run('python', 'python3 main.py', files=files, limits=limits)

