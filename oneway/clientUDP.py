#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:51:57 2024

@author: widhi
"""
import os
import socket

# Setup client socket
server_address = (
    os.getenv("UDP_HOST", "udp-server"),
    int(os.getenv("UDP_PORT", "12345"))
)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Kirim pesan ke server
message = "Halo server sistem terdistribusi"
client_socket.sendto(message.encode("utf-8"), server_address)

# Terima dua balasan: echo dan word count
data1, _ = client_socket.recvfrom(1024)
print("Response 1:", data1.decode("utf-8"))

data2, _ = client_socket.recvfrom(1024)
print("Response 2:", data2.decode("utf-8"))

# Tutup socket
client_socket.close()