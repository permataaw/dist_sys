#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:49:40 2024

@author: widhi
"""

from spyne import Application, rpc, ServiceBase, Unicode, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import argparse
import logging
import os


class WordCountService(ServiceBase):
    @rpc(Unicode, _returns=Integer)
    def wc(ctx, text):
        # Normalisasi None -> ""
        s = text or ""
        # Hitung kata sederhana: split by whitespace
        return len(s.split())


def create_app():
    return Application(
        [WordCountService],
        tns=os.getenv('SOAP_TNS', 'examples.wordcount'),
        in_protocol=Soap11(),
        out_protocol=Soap11(),
    )


def main():
    ap = argparse.ArgumentParser(description='SOAP WordCount server')
    ap.add_argument('--host', default=os.getenv('HOST', '0.0.0.0'))
    ap.add_argument('--port', type=int, default=int(os.getenv('PORT', '8000')))
    ap.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = ap.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format='%(levelname)s: %(message)s')

    app = create_app()
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(app)
    server = make_server(args.host, args.port, wsgi_app)
    logging.info('SOAP WordCount listening on http://%s:%d (WSDL: /?wsdl)', args.host, args.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info('Shutting down server')


if __name__ == '__main__':
    main()