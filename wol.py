#!/usr/bin/env python3
""""
Wake on LAN

wol.py computer1
wol.py computer1 computer2
wol.py 00:11:22:33:44:55

todo Use regex to check mac address validity
todo use with for socket
todo Test with a mac computer
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


def wake_on_lan(mac_address):
    # Build the 6 Bytes(octets) hardware address
    add_oct = mac_address.split(':')
    if len(add_oct) != 6:
        print('Not a valid MAC address')
        return

    hwa = struct.pack('BBBBBB',
                      int(add_oct[0], 16),
                      int(add_oct[1], 16),
                      int(add_oct[2], 16),
                      int(add_oct[3], 16),
                      int(add_oct[4], 16),
                      int(add_oct[5], 16))

    # Build the magic packet
    msg = b'\xff' * 6 + hwa * 16

    # Send packet to broadcast address using UDP port 9
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        for i in broadcast:
            s.sendto(msg, (i, wol_port))

if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        computer = sys.argv[i]
        if ":" in computer:
            # Wake up using MAC address
            wake_on_lan(computer)
            print('Waking up', computer)
        else:
            # Wake up known computers
            if computer in my_computers.keys():
                wake_on_lan(my_computers[computer])
                print('Waking up', computer)
            else:
                print('Unknown computer', computer)
else:
    print('No machine to wake. Use: wol.py computer or wol.py'
          ' 00:11:22:33:44:55')