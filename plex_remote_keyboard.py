#!/usr/bin/env python

import os
import sys    
import termios
import fcntl
import time
import urllib2
import argparse

DEFAULT_IP_ADDRESS = "192.168.1.104"
DEFAULT_PORT = 3005

def main():

    parser = argparse.ArgumentParser(description='Uses the Plex Home Theatre REST API to remotely control Plex with a keyboard.')
    parser.add_argument('-a', '--address', type=str, default=DEFAULT_IP_ADDRESS, help="IP address of PHT host. (default: %s)" % DEFAULT_IP_ADDRESS)
    parser.add_argument('-p', '--port', type=str, default=DEFAULT_PORT, help="Port where PHT host can be reached. (default: %d)" % DEFAULT_PORT)

    # Parse and validate input.
    args = parser.parse_args()

    print_header()
    IP_Address = can_reach_address(args.address)
    print_instructions()

    url_prefix = "http://%s:%d" % (IP_Address, args.port)

    input_loop(url_prefix)

def input_loop(url_prefix):

    while True:
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

        try:        
            while 1:          
                try:
                    c = sys.stdin.read(3)
                    break
                except IOError:
                    time.sleep(0.1)  
                    pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

            if c == '\x1b[A':
                suffix = "/player/navigation/moveUp"
            elif c == '\x1b[B':
                suffix = "/player/navigation/moveDown"
            elif c == '\x1b[C':
                suffix = "/player/navigation/moveRight"
            elif c == '\x1b[D':
                suffix = "/player/navigation/moveLeft"
            elif c == '\n':
                suffix = "/player/navigation/select"
            elif c == 'h':
                suffix = "/player/navigation/home"
            elif c == '\x1b':
                suffix = "/player/navigation/back"
            elif c == ' ':
                suffix = "/player/playback/play"
            elif c == 'x':
                suffix = "/player/playback/stop"
            elif c == 'f':
                suffix = "/player/playback/stepForward"
            elif c == 'b':
                suffix = "/player/playback/stepBack"
            elif c == 'q':
                exit(0)
            else:
                suffix = None
            if suffix:
                urllib2.urlopen(url_prefix + suffix).read()

def can_reach_address(IP_ADDRESS):

    print "Reaching out to remote host...",
    sys.stdout.flush()

    if not is_online(IP_ADDRESS):
        print " FAIL"
        print ""
        print "No response at default address (%s)." % IP_ADDRESS
        print "Enter another IP address or leave blank to exit:"
        alt = raw_input("> ")
        print ""
        if alt == "":
            print "Exiting."
            exit(0)
        else:
            return can_reach_address(alt)
    print "   OK"
    print ""

    return IP_ADDRESS

def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')

    print "####################################"
    print "# PLEX HOME THEATRE NETWORK REMOTE #"
    print "####################################"
    print ""

def print_instructions():
    print "//================================\\\\"
    print "|| Key(s)      | Action           ||"
    print "||================================||"
    print "|| Q           | [Q]uit (this)    ||"
    print "||-------------|------------------||"
    print "|| Arrow keys  | Navigation       ||"
    print "|| ENTER       | Select           ||"
    print "|| ESCAPE      | Back             ||"
    print "|| H           | [H]ome           ||"
    print "||-------------|------------------||"
    print "|| SPACE       | Play/Pause       ||"
    print "|| X           | Stop             ||"
    print "|| N           | Skip [F]orward   ||"
    print "|| B           | Skip [B]ackward  ||"
    print "\\\\================================//"
    print ""
    print "Use your keyboard to control Plex. ",

def is_online(IP_Address):
    try:
        response = os.system("ping -c 1 -W 2000 -t 3 %s > /dev/null 2>&1" % IP_Address)
        return response == 0
    except:
        return False

if __name__ == "__main__":
    main()