from Evtx.Evtx import Evtx
from lxml import etree
import base64
import binascii

EVTX_FILE = "Windows_Logs.evtx"
TARGET_GUID = "7E323F7D-3983-41D9-9D7F-F961D53EB7B8"

def try_decode(value):
    results = []

    # 1) coba decode hex
    try:
        decoded_hex = binascii.unhexlify(value)
        results.append(("hex", decoded_hex.decode(errors="ignore")))
    except Exception:
        pass

    # 2) coba decode base64
    try:
        decoded_b64 = base64.b64decode(value)
        results.append(("base64", decoded_b64.decode(errors="ignore")))
    except Exception:
        pass

    return results


with Evtx(EVTX_FILE) as log:
    for record in log.records():
        xml = record.xml()
        root = etree.fromstring(xml.encode())

        # cari teks yang memuat GUID
        if TARGET_GUID.lower() in xml.lower():
            print("=" * 80)
            print(f"[EVENT MATCH] Record#: {record.record_id()}")
            print(xml)

            # cari semua param/value
            for elem in root.findall(".//EventData/*"):
                text = (elem.text or "").strip()

                if not text:
                    continue

                # jika ada string panjang (mungkin encoded)
