#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 20:43:48 2024

@author: widhi
"""

from jsonrpc import JSONRPCResponseManager, dispatcher
from http.server import BaseHTTPRequestHandler, HTTPServer
import re

# --- Utilitas untuk olah teks ---
_ws_re = re.compile(r"\s+", re.UNICODE)

def collapse_ws(s: str) -> str:
    return _ws_re.sub(" ", s).strip()

# RPC: Word Count
@dispatcher.add_method
def wc(text: str):
    lines = text.count("\n") + (1 if text.strip() else 0)
    words = len(text.split())
    chars = len(text)
    chars_no_space = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))
    return {
        "text": text,
        "lines": lines,
        "words": words,
        "chars": chars,
        "chars_no_space": chars_no_space
    }

# RPC: Transform
@dispatcher.add_method
def transform(text: str, ops: list):
    applied = []
    for op in ops:
        op = str(op).lower()
        if op == "upper":
            text = text.upper(); applied.append(op)
        elif op == "lower":
            text = text.lower(); applied.append(op)
        elif op == "title":
            text = text.title(); applied.append(op)
        elif op == "reverse":
            text = text[::-1]; applied.append(op)
        elif op == "strip":
            text = text.strip(); applied.append(op)
        elif op == "collapse_ws":
            text = collapse_ws(text); applied.append(op)
    return {"result": text, "applied": applied}

# HTTP Handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        response = JSONRPCResponseManager.handle(post_data, dispatcher)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response.json.encode())

# Run server
def run(server_class=HTTPServer, handler_class=RequestHandler, port=4000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting JSON-RPC TextTool server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
