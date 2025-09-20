#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 17:02:45 2024

@author: widhi
"""

import os, re
from flask import Flask, request, jsonify

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# --- Utilitas Regex untuk olah teks ---
_ws_re = re.compile(r"\s+", re.UNICODE)         # Pola: satu/lebih whitespace (spasi, tab, newline)
_non_alnum_re = re.compile(r"[^a-z0-9\-]+")     # Pola: karakter selain a-z, 0-9, atau tanda '-'
_dash_re = re.compile(r"-+")                    # Pola: dua/lebih '-' berurutan

def slugify(s: str) -> str:
    s = s.lower().strip()                       # Ubah ke huruf kecil & buang spasi pinggir
    s = _ws_re.sub("-", s)                      # Semua whitespace → ganti jadi '-'
    s = _non_alnum_re.sub("-", s)               # Karakter non-alfanumerik → ganti '-'
    s = _dash_re.sub("-", s).strip("-")         # Rangkai '-' yang dobel → satu, lalu pangkas '-' di tepi
    return s                                    # Kembalikan slug yang rapi

def collapse_ws(s: str) -> str:
    return _ws_re.sub(" ", s).strip()           # Rapatkan spasi berlebih (jadi satu spasi) + pangkas tepi

# Endpoint untuk cek kesehatan service
@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200       # Balas JSON sederhana untuk pengecekan

# Endpoint untuk Word Count (WC)
@app.get("/wc")
def wc():
    text = request.args.get("text", "")         # Ambil parameter query ?text=...
    lines = text.count("\n") + (1 if text != "" else 0)  # Hitung baris (heuristik sederhana)
    words = len(text.split())                   # Hitung jumlah kata (dipisah whitespace)
    chars = len(text)                           # Hitung total karakter (termasuk spasi)
    chars_no_space = len(                       # Hitung karakter tanpa whitespace umum
        text.replace(" ", "").replace("\n", "").replace("\t", "")
    )
    return jsonify({                            # Kembalikan metrik lengkap
        "text": text,
        "lines": lines,
        "words": words,
        "chars": chars,
        "chars_no_space": chars_no_space
    }), 200

# Endpoint untuk membuat slug dari teks
@app.get("/slugify")
def slugify_ep():
    text = request.args.get("text", "")         # Ambil ?text=...
    return jsonify({"text": text, "slug": slugify(text)}), 200  # Balik teks + slug hasil

# Endpoint untuk transformasi teks (POST JSON)
@app.post("/transform")
def transform():
    if not request.is_json:                     # Validasi Content-Type
        return jsonify({"error": "Content-Type must be application/json"}), 415

    body = request.get_json(silent=True) or {}  # Ambil body JSON; jika gagal → dict kosong
    text = str(body.get("text", ""))            # Ambil field 'text'
    ops = body.get("ops", [])                   # Ambil daftar operasi ['upper','strip',...]
    if not isinstance(ops, list):               # Pastikan ops adalah list
        return jsonify({"error": "ops must be a list"}), 400

    applied = []                                 # Catat operasi yang benar-benar diterapkan
    for op in ops:                               # Terapkan berurutan sesuai daftar 'ops'
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
        else:
            continue                              # Operasi tak dikenal → dilewati (sengaja tidak error)

    return jsonify({"result": text, "applied": applied}), 200  # Balik hasil + daftar operasi yang dipakai

# Jalankan server di port 5151
if __name__ == '__main__':
    # BACA dari ENV agar konsisten dengan compose; default tetap 5151
    port = int(os.getenv("PORT", "5151"))
    # PENTING: TANPA spasi, harus persis "0.0.0.0"
    app.run(
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
        host='0.0.0.0',
        port=port
    )
