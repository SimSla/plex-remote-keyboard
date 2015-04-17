#!/usr/bin/env python

import re
import os
import sys    
import termios
import fcntl
import time
import urllib2
import argparse
import ConfigParser
from appdirs import user_data_dir

APPNAME = "plex-remote-keyboard"
APPAUTHOR = "simonslangen"

DEFAULT_ADDRESS = "127.0.0.1"
DEFAULT_PORT = 3005

global plex_keys
plex_keys = {'\x1b[A' : "/player/navigation/moveUp",
            '\x1b[B' :  "/player/navigation/moveDown",
            '\x1b[C' :  "/player/navigation/moveRight",
            '\x1b[D' :  "/player/navigation/moveLeft",
            '\n' :      "/player/navigation/select",
            'h' :       "/player/navigation/home",
            '\x1b' :    "/player/navigation/back",  # escape key
            ' ' :       "/player/playback/play",
            'x' :       "/player/playback/stop",
            'f' :       "/player/playback/stepForward",
            'b' :       "/player/playback/stepBack"}

def main():
    # Retrieve defaults.
    try:
        default_address, default_port = get_defaults()
    except:
        if len(sys.argv) > 1:
            default_address, default_port = init_defaults(DEFAULT_ADDRESS, DEFAULT_PORT)
        else:
            default_address, default_port = init_defaults_i()

    # Parse arguments.
    parser = argparse.ArgumentParser(description='Uses the Plex Home Theater REST API to remotely control Plex with a keyboard.')
    parser.add_argument('-a', '--address', type=str, default=default_address, help="IP address of PHT host. (default: %s)" % default_address)
    parser.add_argument('-p', '--port', type=str, default=default_port, help="Port where PHT host can be reached. (default: %d)" % default_port)
    parser.add_argument('-u', '--update_defaults', action='store_true', help='Causes the current defaults to be overwritten with the supplied address and/or port.')

    args = parser.parse_args()

    # Make pretty header.
    print_header()

    # Check IP address validity.
    IP_Address = can_reach_address(args.address)

    # Update defaults. 
    if args.update_defaults and (IP_Address != default_address or args.port != default_port):
        # If current address updated during runtime ask for confirmation
        if IP_Address == args.address or query_continue("Do you still wish to change the default IP address to '%s'?"):
            # Ask confirmation.
            change_defaults(IP_Address, args.port)

    print_instructions()

    url_prefix = "http://%s:%d" % (IP_Address, args.port)

    input_loop(url_prefix)

# Character reading based on code by Danny Yoo (under PSF license)
# source: http://code.activestate.com/recipes/134892/
def input_loop(url_prefix):
    global plex_keys

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
            if c == 'q':
                clear()
                exit(0)
            elif c == '*':
                print "\n"
                change_defaults_i()
                del sys.argv[1:]
                main()
            elif c in plex_keys:
                urllib2.urlopen(url_prefix + plex_keys[c]).read()

def can_reach_address(IP_ADDRESS):
    print "Reaching out to remote host %s..." % IP_ADDRESS,
    sys.stdout.flush()

    if not is_online(IP_ADDRESS):
        print "FAIL"
        print ""
        print "No response at address (%s)." % IP_ADDRESS
        print "Enter another IP address or leave blank to exit:"
        alt = raw_input("> ")
        print ""
        if alt == "":
            print "Exiting."
            exit(0)
        else:
            return can_reach_address(alt)
    print "OK"
    print ""

    return IP_ADDRESS

def get_config_path():
    app_dir = user_data_dir(APPNAME, APPAUTHOR)
    return os.path.join(app_dir, 'settings.cfg')

def get_defaults():
    config = ConfigParser.RawConfigParser()
    config.read(get_config_path())
    address = config.get('defaults', 'address')
    port = config.getint('defaults', 'port')
    return address, port

def change_defaults_i():
    change_defaults(query_address("Enter the address of your PHT host:"),
                        query_integer("Enter the port number:"))

def change_defaults(address, port):
    config = ConfigParser.ConfigParser()
    config.add_section('defaults')
    config.set('defaults', 'address', address)
    config.set('defaults', 'port', port)

    with open(get_config_path(), 'wb') as configfile:
        config.write(configfile)

def init_defaults(address, port):
    app_dir = os.path.split(get_config_path())[0]
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
    change_defaults(address, port)
    return address, port

def init_defaults_i():
    print "The default network location of your"
    print "Plex Home Theater host has not been set."
    if query_continue("Do you want to do this now?"):
        return init_defaults(query_address("Enter the address of your PHT host:"),
                            query_integer("Enter the port number:"))
    else:
        exit(0)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear()

    print "####################################"
    print "# PLEX HOME THEATER NETWORK REMOTE #"
    print "####################################"
    print ""

def print_instructions():
    print "//================================\\\\"
    print "|| Key(s)      | Action           ||"
    print "||================================||"
    print "|| Q           | [Q]uit (this)    ||"
    print "|| *           | Settings         ||"
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

def query_address(query):
    while True:
        print query
        choice = raw_input("> ").strip().lower()
        if is_valid_address(choice):
            return choice
        else:
            print "Not a valid address. Please try again (e.g. '127.0.0.1').\n"

def is_valid_address(address):
    regex = re.compile(
            r'^(?:(?:http|https)://)?' # http:// or https:// or no protocol
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', re.IGNORECASE) # or ip
    return regex.match(address)

def query_integer(query, default = 3005):
    prompt = " [%d] " % default
    while True:
        print query + prompt
        choice = raw_input("> ").strip()
        if choice == "":
            return default
        try:
            num = int(choice)
            return num
        except:
            print ("Please respond with an integer.\n")

def query_continue(question, default=True):
    valid = {"yes": True, "y": True, "ye": True,
         "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default:
        prompt = " [Y/n] "
    else:
        prompt = " [y/N] "

    while True:
        print question + prompt
        choice = raw_input("> ").lower()
        if default is not None and choice == '':
            return default
        elif choice in valid:
            return valid[choice]
        else:
            print ("Please respond with 'y' or 'n' ,"
                "or 'yes' or 'no').\n")

if __name__ == "__main__":
    main()