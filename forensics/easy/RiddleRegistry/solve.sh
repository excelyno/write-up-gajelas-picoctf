#!/bin/bash

# ==========================================
# picoCTF - Riddle Registry (Educational)
# Target: confidential.pdf
# ==========================================

FILE="confidential.pdf"

echo "=========================================="
echo " picoCTF Forensics Solver - Riddle Registry"
echo "=========================================="
echo

# Step 0: Cek file
echo "[STEP 0] Checking file..."
if [ ! -f "$FILE" ]; then
  echo "[ERROR] File $FILE not found."
  exit 1
fi
echo "[OK] File found: $FILE"
echo

# Step 1: Jelaskan apa itu metadata
echo "[STEP 1] What is happening?"
echo "PDF files store extra information called METADATA."
echo "This metadata acts like a 'registry' for the document."
echo "Attackers and CTF challenges often hide secrets there."
echo
read -p "Press ENTER to continue..."

# Step 2: Tampilkan metadata mentah
echo
echo "[STEP 2] Extracting readable strings from PDF..."
echo "We use 'strings' to see hidden text inside the file."
echo

strings "$FILE" | head -n 20
echo
read -p "Press ENTER to search for suspicious metadata..."

# Step 3: Cari field Author
echo
echo "[STEP 3] Searching for Author field..."
AUTHOR_LINE=$(strings "$FILE" | grep "/Author")

if [ -z "$AUTHOR_LINE" ]; then
  echo "[ERROR] Author field not found."
  exit 1
fi

echo "[FOUND] Raw Author field:"
echo "$AUTHOR_LINE"
echo

# Step 4: Jelaskan Base64
echo "[STEP 4] Why this looks suspicious?"
echo "The Author value uses characters typical of Base64 encoding."
echo "Base64 is NOT encryption, just text encoding."
echo
read -p "Press ENTER to clean and decode it..."

# Step 5: Bersihkan escape \075
ENCODED=$(echo "$AUTHOR_LINE" | sed -n 's/.*Author (\(.*\)).*/\1/p' | sed 's/\\075/=/g')

echo
echo "[STEP 5] Cleaned encoded text:"
echo "$ENCODED"
echo

# Step 6: Decode Base64
echo "[STEP 6] Decoding Base64..."
FLAG=$(echo "$ENCODED" | base64 -d 2>/dev/null)

if [ -z "$FLAG" ]; then
  echo "[ERROR] Base64 decoding failed."
  exit 1
fi

echo
echo "=========================================="
echo " 🎉 FLAG FOUND!"
echo "=========================================="
echo
echo "$FLAG"
echo
echo "=========================================="
echo "Explanation:"
echo "- The flag was hidden in PDF metadata"
echo "- The 'Author' field acted like a registry key"
echo "- The value was Base64 encoded"
echo "=========================================="
