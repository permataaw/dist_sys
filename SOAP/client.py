#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:52:27 2024

@author: widhi
"""

import os
import sys
import time
import argparse
import logging
from zeep import Client
from zeep.exceptions import XMLSyntaxError
import requests

# Default: gunakan DNS service antar-container 'soap-server'
DEFAULT_WSDL = os.getenv('SOAP_WSDL', 'http://soap-server:8000/?wsdl')


def wait_for_wsdl(url, timeout=10, interval=0.5):
    """Try to GET WSDL until success or timeout (seconds).
    Returns True if reachable, False otherwise."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200 and r.text:
                return True
        except requests.RequestException:
            pass
        time.sleep(interval)
    return False


def main():
    ap = argparse.ArgumentParser(description="SOAP WordCount client")
    ap.add_argument('--text', default='sistem terdistribusi kelas B')
    ap.add_argument('--wsdl', default=DEFAULT_WSDL, help='WSDL URL')
    ap.add_argument('--wait', type=float, default=5.0, help='Seconds to wait for WSDL')
    ap.add_argument('--debug', action='store_true')
    args = ap.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format='%(levelname)s: %(message)s')

    wsdl = args.wsdl
    logging.info('Using WSDL: %s', wsdl)

    if args.wait > 0:
        logging.info('Waiting up to %.1fs for WSDL...', args.wait)
        if not wait_for_wsdl(wsdl, timeout=args.wait):
            logging.error('WSDL not available after %.1fs: %s', args.wait, wsdl)
            return 2

    try:
        client = Client(wsdl=wsdl)
    except Exception as e:
        logging.exception('Failed to create SOAP client: %s', e)
        return 3

    try:
        count = client.service.wc(args.text)
        print(f"wc -> {count} kata")
    except Exception as e:
        logging.exception('SOAP call failed: %s', e)
        return 4

    return 0


if __name__ == '__main__':
    sys.exit(main())
