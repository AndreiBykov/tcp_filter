#!/usr/bin/python
from bcc import BPF

import sys
import socket
import os

from sys import argv

#arguments
interface="eth0"

if len(argv) == 3:
    if str(argv[1]) == '-i':
        interface = argv[2]

print("USAGE: %s [-i <if_name>]" % argv[0])
print ("binding socket to '%s'" % interface)	
 

bpf = BPF(src_file = "tcp_filter.c", debug = 0)

function_tcp_filter = bpf.load_func("tcp_filter", BPF.SOCKET_FILTER)

BPF.attach_raw_socket(function_tcp_filter, interface)

socket_fd = function_tcp_filter.sock

sock = socket.fromfd(socket_fd, socket.PF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)

sock.setblocking(True)

while 1:
    packet_str = os.read(socket_fd, 2048)
    
    packet_bytearray = bytearray(packet_str)
 
    src_host_ip = str(packet_bytearray[26]) + "." + str(packet_bytearray[27]) + "." + str(packet_bytearray[28]) + "." + str(packet_bytearray[29])
    dest_host_ip = str(packet_bytearray[30]) + "." + str(packet_bytearray[31]) + "." + str(packet_bytearray[32]) + "." + str(packet_bytearray[33])

    src_host_port = packet_bytearray[34] << 8 | packet_bytearray[35]
    dest_host_port = packet_bytearray[36] << 8 | packet_bytearray[37]

    msg = "Src host: " + src_host_ip + ":" + str(src_host_port) + "   Dest host: "+ dest_host_ip + ":" + str(dest_host_port)
    print (msg)
