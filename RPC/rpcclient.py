#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 20:45:15 2024

@author: widhi
"""

import requests, json

# Fungsi panggil RPC
def call_rpc(method, params):
    url = "http://rpc-server:4000"
    headers = {"content-type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    return response

# Word Count
res_wc = call_rpc("wc", ["Halo sistem terdistribusi kelas B"])
print("WC:", res_wc["result"])

# Transform
res_trans = call_rpc("transform", ["  teks   dengan   Spasi  Ganda ", ["collapse_ws", "title"]])
print("Transform:", res_trans["result"])
