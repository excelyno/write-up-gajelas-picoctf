def swap_chunks(data, size):
    out = bytearray()
    for i in range(0, len(data), size):
        chunk = data[i:i+size]
        out.extend(chunk[::-1])
    return bytes(out)

with open("challengefile", "rb") as f:
    data = f.read()

# Swap per 2-byte
sw2 = swap_chunks(data, 2)
with open("fixed_2byte.jpg", "wb") as f:
    f.write(sw2)

# Swap per 4-byte
sw4 = swap_chunks(data, 4)
with open("fixed_4byte.jpg", "wb") as f:
    f.write(sw4)

print("Selesai. Coba buka fixed_2byte.jpg dan fixed_4byte.jpg")
