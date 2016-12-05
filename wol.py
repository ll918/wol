#!/usr/bin/env python3
""""
Wake on LAN

wol.py computer1
wol.py computer1 computer2
wol.py 00:11:22:33:44:55

todo Use regex to check mac address validity
todo use with for socket
todo Test with a mac input
todo better user input validation
"""
import os
import socket
import struct
import sys

broadcast = ['192.168.1.255', '192.168.0.255']
wol_port = 9

# The MAC address is stored in environment variables.
my_computers = {'dell5150': os.environ['dell5150'], 'imac': os.environ['imac']}


def validate_mac(mac_address):
    """Gets a MAC address as a string, validate mac address format and returns
    True or False
    """
    # todo use regex to validate
    status = False
    if len(mac_address) != 17:
        print('Not a valid MAC address')
    else:
        status = True
    return status


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
    UDP port 9
    """
    msg = build_magic_packet(mac_address)
    if msg != '':
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            for i in broadcast:
                s.sendto(msg, (i, wol_port))


if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        input = sys.argv[i]
        if ":" in input:
            # Wake up using MAC address
            if validate_mac(input) is True:  # Validation should be moved
                wake_on_lan(input)
                print('Waking up', input)
        else:
            # Wake up known computers
            if input in my_computers.keys():
                wake_on_lan(my_computers[input])
                print('Waking up', input)
            else:
                print('Unknown input', input)
else:
    print('No machine to wake. Use: wol.py input or wol.py'
          ' 00:11:22:33:44:55')
