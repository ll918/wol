#!/usr/bin/env python3
""""
Wake on LAN

wol.py computer1
wol.py computer1 computer2
wol.py 00:11:22:33:44:55
"""
import os
import re
import socket
import struct
import sys

broadcast = ['192.168.1.255', '192.168.0.255']
wol_port = 9

# The MAC address is stored in environment variables.
# TODO: get my_computers from file. json?
my_computers = {'dell5150': os.environ['dell5150'], 'imac': os.environ['imac']}


def validate_mac(mac_address):
    """Gets a MAC address as a string, validate mac address format and returns
    True or False
    """
    valid = False
    # no need to compile just for one match
    r = re.compile('^' + '[:]'.join(['([0-9a-f]{2})'] * 6) + '$',
                   re.IGNORECASE)
    if r.match(mac_address):
        valid = True
    else:
        print('Not a valid MAC address')
    return valid


def build_magic_packet(mac_address):
    """Gets a MAC address as a string and return the wol magic packet as a
     string.
    """
    msg = ''
    # Build the 6 Bytes(octets) hardware address
    add_oct = mac_address.split(':')
    hwa = struct.pack('BBBBBB',
                      int(add_oct[0], 16),
                      int(add_oct[1], 16),
                      int(add_oct[2], 16),
                      int(add_oct[3], 16),
                      int(add_oct[4], 16),
                      int(add_oct[5], 16))
    # Build the magic packet
    msg = b'\xff' * 6 + hwa * 16
    return msg


def wake_on_lan(mac_address):
    """Gets a MAC address as a string then broadcast the magic packet using
    UDP port 9.
    """
    if validate_mac(mac_address) is True:  # is the "is True" necessary?
        msg = build_magic_packet(mac_address)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            for i in broadcast:
                s.sendto(msg, (i, wol_port))
        print('Waking up')
    else:
        pass


if len(sys.argv) > 1:
    input = sys.argv[1]
    if ":" in input:
        # Wake up using MAC address
        wake_on_lan(input)
    else:
        # Wake up known computers
        if input in my_computers:
            wake_on_lan(my_computers[input])
        else:
            print('Unknown machine:', input)
else:
    print('No machine to wake. Use: wol.py computer or wol.py'
          ' 00:11:22:33:44:55')
