#! /usr/bin/env python3
import socket, sys, re, os, time
sys.path.append("../lib")       # for params
import params
from archive import *

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    if os.fork() == 0:      # child becomes server
        print('Connected by', addr)
        path = "sockets.txt"
        if os.path.exists(path):

            encoded_file = archive(path) # encode the file given the path
            size = len(encoded_file) # keep track of size 
            totalsent = 0

            while totalsent < size:
                sent = conn.send(encoded_file[totalsent:])

                if sent == 0: #check for error
                    raise RuntimeError("Socket connection broken.")
                totalsent += sent
                
            time.sleep(0.25);       # delay 1/4s
            conn.shutdown(socket.SHUT_WR)
            sys.exit(0)