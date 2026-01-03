#!/bin/bash

set -e

echo "=============================================="
echo "      picoCTF Visual Forensics Solver"
echo "=============================================="
echo

INPUT="logs.txt"

# STEP 1 — Input validation
echo "[1] Checking input file..."
[ -f "$INPUT" ] || { echo "    ❌ logs.txt not found"; exit 1; }
echo "    ✅ logs.txt found"
echo

# STEP 2 — Base64 decode
echo "[2] Decoding Base64 log → binary file..."
base64 -d "$INPUT" > decoded.bin
echo "    ✅ Base64 decoded"
echo

# STEP 3 — Identify decoded file
echo "[3] Identifying decoded file type..."
FILE_TYPE=$(file decoded.bin)
echo "    ℹ️  $FILE_TYPE"

if [[ "$FILE_TYPE" != *"PNG image data"* ]]; then
    echo "    ❌ Decoded file is not a PNG"
    exit 1
fi

mv decoded.bin image.png
echo "    ✅ PNG confirmed"
echo

# STEP 4 — Visual forensic notice
echo "[4] PNG contains VISUAL text (not ASCII)"
echo "    ℹ️  Switching to OCR-based extraction"
echo

# STEP 5 — OCR extraction
echo "[5] Extracting text from image using OCR..."
tesseract image.png ocr -l eng --psm 6 >/dev/null 2>&1
echo "    ✅ OCR completed"
echo

# STEP 6 — Hex reconstruction
echo "[6] Reconstructing hexadecimal string..."
HEX=$(grep -Eo '[0-9a-fA-F]+' ocr.txt | tr -d '\n')

if [ ${#HEX} -lt 32 ]; then
    echo "    ❌ Hex reconstruction failed"
    exit 1
fi

echo "    ✅ Hex reconstructed"
echo

# STEP 7 — Decode hex → ASCII
echo "[7] Decoding hexadecimal → ASCII..."
ASCII=$(echo "$HEX" | xxd -r -p 2>/dev/null)
echo "    ✅ Hex decoded"
echo

# STEP 8 — Extract picoCTF flag only
echo "[8] Extracting picoCTF flag..."
FLAG=$(echo "$ASCII" | grep -o 'picoCTF{[^}]*}')

if [ -z "$FLAG" ]; then
    echo "    ❌ Flag not found"
    exit 1
fi

echo
echo "=============================================="
echo " 🎉 FLAG FOUND 🎉"
echo "=============================================="
echo
echo "$FLAG"
echo
echo "=============================================="
