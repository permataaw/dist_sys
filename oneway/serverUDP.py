#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:51:14 2024

@author: widhi
"""

import os
import socket

def word_count(s: str) -> int:
    return len((s or "").split())

port = int(os.getenv("UDP_PORT", "12345"))
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", port))

print(f"UDP server up and listening on 0.0.0.0:{port}")

while True:
    data, client_address = server_socket.recvfrom(1024)
    text = data.decode("utf-8")
    print(f"Received message from {client_address}: {text}")

    # Balasan echo
    echo_message = f"Hello, {client_address}. You said: {text}"
    server_socket.sendto(echo_message.encode("utf-8"), client_address)
    print(f"[SENT] {echo_message}")

    # Balasan word count
    count = word_count(text)
    wc_message = f"Jumlah kata: {count}"
    server_socket.sendto(wc_message.encode("utf-8"), client_address)
    print(f"[SENT] {wc_message}")