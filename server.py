#!/usr/bin/env python

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
    * HTTPS only, if token are sent in HTTP they will be reset
"""

import subprocess

from flask import Flask, request
from flask_httpauth import HTTPTokenAuth

from storage import Storage

storage = Storage("storage.yml")

app = Flask(__name__)

auth = HTTPTokenAuth(scheme="Bearer")

tokens = storage.tokens
users = storage.users
sessions = storage.sessions


@auth.verify_token
def verify_token(token):
    """Check the token of the user."""
    if token in tokens:
        return tokens[token]


@app.route("/")
@auth.login_required
def index():
    return f"Hello, {auth.current_user}!"


@app.route("/run")
@auth.login_required
def run():
    """Run the code request given the following POST parameters.:
    - stdin: code to run
    """
    stdin = open("./stdin")
    stdout = open("./stdout")
    sdterr = open("./sdterr")
    stdin.write(request.POST.get("stdin"))
    subprocess.run("python", stdin=stdin, stdout=stdout,
                   stderr=stderr, shell=True)
    stdin.close()
    stdout.close()
    sdterr.close()

    return dict(data=data)


# if __name__ == "__main__":
#     app.run()
