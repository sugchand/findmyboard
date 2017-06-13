#!/usr/bin/python
# encoding: utf-8
'''
findmyboard -- Find the board with its name/IP/MAC

findmyboard is a simple script to find board by its name. The information
is extracted from the information webpage published by lab.

@author:     Sugesh Chandran

@copyright:  2017 Intel corp. All rights reserved.

@license:    Apache License 2.0

@contact:    sugeshchandran@gmail.com
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2017-06-12'
__updated__ = '2017-06-12'


def extract_board_data(line=None):

    # The dictionary used to map html tags to ascci chars
    html_tags_dic = {
                     "&nbsp" : " ", #space in html
                     "("     : " ",
                     ")"     : " "
                    }
    name = None
    mac = None
    ip = None
    if not line:
        return [name, mac, ip]
    for key, value in html_tags_dic.iteritems():
        if key in line:
            line = line.replace(key, value)
        blist = line.split()
        blen = len(blist)
        if blen == 3 :
            # The entry has name, mac and IP
            name = blist[0].strip()
            mac = blist[2].strip()
            ip = blist[1].strip()
        elif blen == 2 :
            # Only IP and mac address are present in the entry
            ip = blist[0].strip()
            mac = blist[1].strip()
    return [name, mac, ip]
    
def find_board_match(line = None, name = None, ip = None, mac = None):
    '''
    If a match found on line with given details, return the line,
    Or else return None
    '''
    [entryName, entryMac, entryIp] = extract_board_data(line)
    if entryName and name and name in entryName:
        return True
    if entryIp and ip and ip in entryIp:
        return True
    if entryMac and mac and mac in entryMac:
        return True
    return False

def get_board_details(name = None, mac = None, ip = None, all=False):
    '''
        Collect the board details from the lab page
    '''
    import urllib

    LAB_BOARD_URL = "http://silnetwork.ir.intel.com/live/"
    try:
        import requests
    except ImportError:
        sys.stderr.write("Install requests module by \"pip install requests\"")
        return []
    try:
        f = requests.get(LAB_BOARD_URL)
    except Exception as e:
        sys.stderr.write("Exception in opening web url" + ": " + repr(e) + "\n")
        return []

    matchName = None
    matchMac = None
    matchIp = None
    board_list = []
    try:
        if not f:
            sys.stderr.write("Empty webpage, try again..")
            return []
        board_data = f.text
        board_data = board_data.encode(encoding='utf_8')
        for line in board_data.splitlines():
            if not line:
                continue
            if not find_board_match(line, name, ip, mac):
                continue
            # Got a match on line, get the name, mac and ip
            [matchName, matchMac, matchIp] = extract_board_data(line)
            board_list.append([matchName, matchMac, matchIp])
            if not all:
                # We are looking for only one entry match.
                break
    except Exception as e:
        sys.stderr.write("Exception in reading the webpage" + ": " + repr(e) + "\n")
    finally:
        # returns list of [name, mac, IP]
        return(board_list)


def print_board_details(name = None, macaddr = None, ipaddr = None):
    board_details = '''
*****************************************

        Board name        :    %s
        MAC address       :    %s
        IP address        :    %s

*****************************************
''' % (name, macaddr, ipaddr)
    print(board_details)

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Sugesh Chandran on %s.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument("-ip", dest="ipaddr", help="Ip address of the board to search(partial search is allowed).")
        parser.add_argument("-mac", dest="macaddr", help="Mac address of the board to search(partial search is allowed).")
        parser.add_argument("-n", "--name", dest="name", help="Hostname of the board to search(partial search is allowed).")
        parser.add_argument("-a", "--all", dest="allboards", action="store_true", 
                            help="Find all matches for the given input.")
        # Process arguments
        args = parser.parse_args()
        name = args.name
        macaddr = args.macaddr
        ipaddr = args.ipaddr
        allboards = args.allboards
        board_list = get_board_details(name=name, ip=ipaddr,
                                       mac=macaddr, all=allboards)
        for item in board_list:
            name = None
            macaddr = None
            ipaddr = None
            if len(item) == 3:
                # A proper 3 entry item.
                name = item[0]
                macaddr = item[1]
                ipaddr = item[2]
            elif len(item) == 2:
                #No name present.
                macaddr = item[0]
                ipaddr = item[1]
            print_board_details(name, macaddr, ipaddr)
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help\n")
        return 2

if __name__ == "__main__":
    sys.exit(main())