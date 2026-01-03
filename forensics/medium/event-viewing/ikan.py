#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from Evtx.Evtx import Evtx
from xml.etree import ElementTree as ET

def parse_event(record):
    try:
        xml = ET.fromstring(record.xml())

        # handle namespaces
        ns = {"e": xml.tag.split("}")[0].strip("{")}

        system = xml.find("e:System", ns)

        event_id_node = system.find("e:EventID", ns) if system is not None else None
        event_id = event_id_node.text if event_id_node is not None else "UNKNOWN"

        time_node = system.find("e:TimeCreated", ns) if system is not None else None
        time_created = time_node.attrib.get("SystemTime") if time_node is not None else ""

        provider_node = system.find("e:Provider", ns) if system is not None else None
        provider = provider_node.attrib.get("Name") if provider_node is not None else ""

        return {
            "event_id": event_id,
            "time": time_created,
            "provider": provider,
            "xml": record.xml()
        }

    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(description="Simple EVTX Parser")
    parser.add_argument("file", help="Path to EVTX file")
    parser.add_argument("--filter", help="Filter by specific Event ID (e.g., 4624)", default=None)
    parser.add_argument("--output", help="Write JSON output file", default="logs.json")
    args = parser.parse_args()

    events = []
    counts = Counter()

    with Evtx(args.file) as evtx:
        for record in evtx.records():
            event = parse_event(record)
            if not event:
                continue

            counts[event["event_id"]] += 1

            if args.filter is None or args.filter == event["event_id"]:
                events.append(event)

    # print summary
    print("\n=== Event ID Summary ===")
    for eid, total in counts.most_common():
        print(f"EventID {eid}: {total} events")

    # write filtered/full logs
    with open(args.output, "w") as f:
        json.dump(events, f, indent=2)

    print(f"\nSaved {len(events)} records to: {args.output}")

if __name__ == "__main__":
    main()
