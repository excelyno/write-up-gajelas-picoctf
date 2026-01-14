with open("whitepages.txt", "r", encoding="utf-8") as f:
    data = f.read()

print("".join(
    "0" if c == "\u2003" else
    "1" if c == " " else
    ""
    for c in data
))
