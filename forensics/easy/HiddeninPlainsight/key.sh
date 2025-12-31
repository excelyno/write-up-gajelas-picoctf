#!/bin/bash

# ======================================
# picoCTF Forensics Solver (Enhanced)
# Base64 multi-layer + steghide extract
# ======================================

FILE="img.jpg"

echo "[*] Target file : $FILE"
echo "[*] Scanning strings..."

# Step 1: Ambil kandidat Base64 dari strings
BASE64_L1=$(strings "$FILE" | grep -E '^[A-Za-z0-9+/=]{20,}$' | head -n 1)

if [ -z "$BASE64_L1" ]; then
  echo "[!] No Base64 string found"
  exit 1
fi

echo "[+] Base64 Layer-1 found : $BASE64_L1"

# Step 2: Decode Base64 layer 1
DECODE_L1=$(echo "$BASE64_L1" | base64 -d 2>/dev/null)

if [ -z "$DECODE_L1" ]; then
  echo "[!] Base64 layer-1 decode failed"
  exit 1
fi

echo "[+] Decoded Layer-1     : $DECODE_L1"

# Expected format: steghide:<base64_password>
PASSWORD_L1=$(echo "$DECODE_L1" | cut -d':' -f2)

if [ -z "$PASSWORD_L1" ]; then
  echo "[!] Password layer-1 not found"
  exit 1
fi

echo "[+] Password Layer-1    : $PASSWORD_L1"

# Step 3: Decode Base64 layer 2 (real password)
PASSWORD_REAL=$(echo "$PASSWORD_L1" | base64 -d 2>/dev/null)

if [ -z "$PASSWORD_REAL" ]; then
  echo "[!] Base64 layer-2 decode failed"
  exit 1
fi

echo "[+] Password REAL       : $PASSWORD_REAL"

# Step 4: Extract steghide payload
echo "[*] Extracting steghide data..."
steghide extract -sf "$FILE" -p "$PASSWORD_REAL" -f

echo "[+] Extraction finished"
ls -lah
