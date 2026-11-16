#!/usr/bin/env python3
"""Resolve an official stable Ruby release and its source checksum."""

import json
import re
import sys
import urllib.request

import yaml

with urllib.request.urlopen(
    "https://raw.githubusercontent.com/ruby/www.ruby-lang.org/master/_data/releases.yml",
    timeout=60,
) as response:
    releases = yaml.safe_load(response)
stable = [r for r in releases if re.fullmatch(r"\d+\.\d+\.\d+", r["version"])]
requested = sys.argv[1] if len(sys.argv) > 1 else "latest"
if requested == "latest":
    release = max(stable, key=lambda r: tuple(map(int, r["version"].split("."))))
else:
    release = next((r for r in stable if r["version"] == requested), None)
    if release is None:
        sys.exit(f"Unknown stable Ruby version: {requested}")
url = release["url"]["xz"]
checksum = release["sha256"]["xz"]
if not url.startswith("https://cache.ruby-lang.org/pub/ruby/"):
    sys.exit("Unexpected source host")
if not re.fullmatch(r"[0-9a-f]{64}", checksum):
    sys.exit("Invalid source checksum")
print(json.dumps({"version": release["version"], "url": url, "sha256": checksum}))
