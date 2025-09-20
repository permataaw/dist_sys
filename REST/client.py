#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 17:05:25 2024

@author: widhi
"""

import os, time, sys, argparse, requests        # Import util (ENV, delay, exit), argparse (CLI), requests (HTTP)

BASE = os.environ.get('REST_BASE', 'http://rest-server:5151')


# Fungsi untuk menunggu server siap (/health), retry sederhana
def wait_health(retry=5, delay=1):
    for i in range(1, retry+1):
        try:
            r = requests.get(f"{BASE}/health", timeout=2)  # Cek endpoint /health
            if r.status_code == 200:
                print("Server healthy")                    # Jika OK → lanjut
                return True
        except Exception as e:
            print(f"[{i}/{retry}] health check gagal: {e}")# Tampilkan kegagalan
        time.sleep(delay)                                  # Tunggu sebelum mencoba lagi
    print("Server belum siap.")                            # Gagal setelah beberapa percobaan
    return False

# Fungsi memanggil /wc dengan query ?text=...
def do_wc(text):
    try:
        r = requests.get(f"{BASE}/wc", params={"text": text}, timeout=5)
        print(r.status_code, r.text)                       # Cetak status + body respon
    except requests.RequestException as e:
        print(f"wc request failed: {e}")

# Fungsi memanggil /slugify dengan query ?text=...
def do_slugify(text):
    try:
        r = requests.get(f"{BASE}/slugify", params={"text": text}, timeout=5)
        print(r.status_code, r.text)
    except requests.RequestException as e:
        print(f"slugify request failed: {e}")

# Fungsi memanggil /transform (POST JSON {text, ops})
def do_transform(text, ops):
    try:
        r = requests.post(f"{BASE}/transform",
                          json={"text": text, "ops": ops},
                          timeout=5)
        print(r.status_code, r.text)
    except requests.RequestException as e:
        print(f"transform request failed: {e}")

# Entry point CLI
def main():
    # Definisi argumen baris perintah
    ap = argparse.ArgumentParser(description="Text Tools client (wc, slugify, transform)")
    ap.add_argument("--op", required=True, choices=["wc","slugify","transform","demo"])  # Pilih operasi
    ap.add_argument("--text", default="Halo   Dunia\tREST")                              # Teks default bila tidak diisi
    ap.add_argument("--ops", default="upper,collapse_ws",                                # Daftar operasi default (transform)
                    help="Comma-separated ops: upper,lower,title,reverse,strip,collapse_ws")
    args = ap.parse_args()                                                               # Parse argumen

    # Allow CLI override of base URL
    global BASE
    # If user provided REST_BASE in env or via CLI, use it
    if os.environ.get('REST_BASE'):
        BASE = os.environ.get('REST_BASE')

    ap.add_argument("--base", default=None, help="Base URL for REST server, overrides REST_BASE env")
    args = ap.parse_args()                                                               # Parse argumen

    if args.base:
        BASE = args.base

    # Pastikan server siap sebelum mengirim request
    if not wait_health():
        return 1
    # Cabang eksekusi berdasarkan pilihan --op
    if args.op == "wc":                      # Jika perintah 'wc' → hitung kata/karakter/baris
        do_wc(args.text)

    elif args.op == "slugify":               # Jika perintah 'slugify' → buat slug dari teks
        do_slugify(args.text)

    elif args.op == "transform":             # Jika perintah 'transform' → terapkan serangkaian operasi
        # Ubah string "a,b,c" menjadi list ['a','b','c'] dan buang item kosong/spasi
        ops = [o.strip() for o in args.ops.split(",") if o.strip()]
        do_transform(args.text, ops)

    elif args.op == "demo":                  # Mode demo: jalankan beberapa contoh sekaligus
        do_wc("  Ini\ncontoh   teks  ")
        do_slugify("Belajar REST & Docker: WSL2 Edition!!")
        do_transform("  Teks   dengan   Spasi  Ganda ", ["collapse_ws","title"]) 

    return 0                                  # Exit code 0 menandakan sukses

if __name__ == '__main__':
    sys.exit(main())
