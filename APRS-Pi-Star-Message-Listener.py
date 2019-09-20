#!/usr/bin/python

import socket 
import re
import os



APRS_Server = "rotate.aprs2.net"
TCP_Port = 14580

CALLSIGN = "<Your Call Sign Here>"
PASSCODE = "-1"


TEXTMESSAGEPATH="/usr/local/bin/texttransmit"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((APRS_Server, TCP_Port))

initialRecv = s.recv(1024)
print initialRecv

initialQ = "user " + CALLSIGN + "-N pass -1 vers N0RJC_Pi-STAR APRS-->D-STAR 0.0.1 filter g/" + CALLSIGN + "/\n"

print "Sending Intial Message to APRS server"
print initialQ

s.sendall(initialQ)

while True:
    try:
        data = s.recv(8192)
        if data:
            print "Data: " + data
            if re.search(r"\w*-..\>.*\,.*\:\:" + CALLSIGN + "-.*\s\s", data):
                print "A Messages is recieved"
                #parsing message 
                aprsmessage = re.match("(\w*-..)\>.*\,.*\:\:" + CALLSIGN + "-.*\s\s\:(.*)", data)
                
                aprsSource = aprsmessage.group(1)
                aprsMessage = aprsmessage.group(2)

                print "APRS Source: " + aprsSource
                print "APRS Message: " + aprsMessage

                print "## Dispatch a message to D-STAR TX"
                command = "" + TEXTMESSAGEPATH + " \"" + CALLSIGN + "  B\"" + " -text \"APRSMSG RX:" + aprsSource + ": " + aprsMessage + " \""
                print command

                os.system(command)
                try:
                    time.sleep(0.3)
                    os.system(command)
                except:
                    pass


        else :
            time.sleep(0.1)
    except:
        s.close()
        break

    

