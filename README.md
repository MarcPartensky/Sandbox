# sandbox

## Context

In computer security, a sandbox is a security mechanism for separating running programs, usually in an effort to mitigate system failures and/or software vulnerabilities from spreading. It is often used to execute untested or untrusted programs or code, possibly from unverified or untrusted third parties, suppliers, users or websites, without risking harm to the host machine or operating system. A sandbox typically provides a tightly controlled set of resources for guest programs to run in, such as storage and memory scratch space. Network access, the ability to inspect the host system or read from input devices are usually disallowed or heavily restricted.
> https://en.wikipedia.org/wiki/Sandbox_(computer_security)

## Introduction
This project is a rest api that gives people arbitrary remote code execution and empowers them with a python shell.
It could later be used to run python commands inside of discord using a bot to send http requests to this server.

## Description

Main server for running untrusted python shell commands.

Typically an admin will create a secret token which can be used as a post
variable. The server would use it to identify the user and let him run python
code each time a new command is being sent.

### HTTP request
* stdin
* token

### HTTP response
* stderr
* stdout

### Security
* Token authentication
* Role system
* IP whitelist
* Epicbox
* Logs are saved
* HTTPS only, if token are sent in HTTP they will be reset

## Features
* Token authentication required
* Role system : 1 owner, * admin, * staff, * user

## Main dependencies
* Flask
* Epicbox
* Docker
