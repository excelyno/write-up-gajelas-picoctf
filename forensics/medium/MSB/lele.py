import os
from PIL import Image
import string

INPUT_FILE = "Ninja-and-Prince-Genji-Ukiyoe-Utagawa-Kunisada.flag.png"
OUTDIR = "output_msb"


def ensure_outdir():
    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)


def save(img, name):
    path = os.path.join(OUTDIR, name)
    img.save(path)
    print(f"[+] saved -> {path}")


def extract_bit_plane(img, bit):
    """Return grayscale image representing a specific bit-plane 0–7"""
    w, h = img.size
    out = Image.new("L", (w, h))
    p_in = img.load()
    p_out = out.load()

    mask = 1 << bit
    for y in range(h):
        for x in range(w):
            r, g, b = p_in[x, y][:3]
            v = ((r & mask) | (g & mask) | (b & mask))
            # normalize to 0/255
            p_out[x, y] = 255 if v else 0
    return out


def extract_msb_image(img):
    """Shortcut specifically for MSB"""
    return extract_bit_plane(img, 7)


def extract_ascii_stream(img):
    """Interpret MSB of RGB channels as a bitstream -> ASCII"""
    w, h = img.size
    bits = []

    p = img.load()
    for y in range(h):
        for x in range(w):
            r, g, b = p[x, y][:3]
            bits.append((r & 0x80) >> 7)
            bits.append((g & 0x80) >> 7)
            bits.append((b & 0x80) >> 7)

    data = []
    for i in range(0, len(bits), 8):
        byte = 0
        for b in bits[i:i+8]:
            byte = (byte << 1) | b
        data.append(byte)

    raw = bytes(data)
    # try printable portion
    printable = "".join(chr(c) if chr(c) in string.printable else "." for c in raw)
    return raw, printable


def main():
    ensure_outdir()
    img = Image.open(INPUT_FILE).convert("RGB")

    print("[*] generating bit-plane images (0–7)...")
    for bit in range(8):
        bp = extract_bit_plane(img, bit)
        save(bp, f"bitplane_{bit}.png")

    print("[*] generating MSB image...")
    msb_img = extract_msb_image(img)
    save(msb_img, "msb_only.png")

    print("[*] extracting ASCII from MSB bitstream...")
    raw, printable = extract_ascii_stream(img)

    with open(os.path.join(OUTDIR, "msb_bits.bin"), "wb") as f:
        f.write(raw)
    print(f"[+] saved -> {OUTDIR}/msb_bits.bin")

    with open(os.path.join(OUTDIR, "msb_printable.txt"), "w") as f:
        f.write(printable)
    print(f"[+] saved -> {OUTDIR}/msb_printable.txt")

    print("\nDone. Periksa file berikut:")
    print(" - bitplane_0..7.png   (lihat mana yang tampak seperti teks/QR/pola)")
    print(" - msb_only.png        (biasanya mengandung pesan utama)")
    print(" - msb_bits.bin        (bitstream mentah)")
    print(" - msb_printable.txt   (teks yang mungkin terbaca)")


if __name__ == "__main__":
    main()
