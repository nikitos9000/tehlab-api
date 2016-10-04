#!/usr/bin/env python
from __future__ import print_function
import sys
import tehapi

def print_url_response(response):
    url, code, prediction = response["url"], response["code"], response["prediction"]
    print("%s (%d):" % (url, code))
    for score, label in prediction:
        print("   ", score, "=>", " / ".join(label))
    print()

def print_status(status):
    print("[API] Input:", status.get("input", 0), file=sys.stderr)
    print("[API] Cached:", status.get("cached", 0), file=sys.stderr)
    print("[API] Queued:", status.get("sent", 0), file=sys.stderr)
    print("[API] Refetched:", status.get("refetch", 0), file=sys.stderr)
    print("[API] Processed:", status.get("done", 0), file=sys.stderr)
    print("[API] Output:", status.get("output", 0), file=sys.stderr)

if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", default="demo")
    parser.add_argument("--file")
    parser.add_argument("--url")
    parser.add_argument("--save")
    parser.add_argument("--uid")
    args = parser.parse_args()

    api = tehapi.start(args.token)

    if args.url and not args.file and not args.save:
        for response in tehapi.push_fetch_urls(api, [args.url]):
            print_url_response(response)
        sys.exit(0)

    if args.file:
        uid = tehapi.push_urls_from_file(api, args.file)
    elif args.url:
        uid = tehapi.push_urls(api, [args.url])
    elif args.uid:
        uid = args.uid
    else:
        parser.print_help()
        sys.exit(1)

    print("[API] Fetch UID:",  uid)

    if args.save:
        tehapi.fetch_urls_to_file(api, args.save, uid)
    else:
        for response in tehapi.fetch_urls(api, uid):
            print_url_response(response)

    print_status(tehapi.status(args.token, uid))
