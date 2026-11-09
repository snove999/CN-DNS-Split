#!/usr/bin/env python3
"""Build an optional Loon Host plugin from dnsmasq-china-list."""
from __future__ import annotations
import argparse
import re
import urllib.request
from pathlib import Path

SOURCE_URL = "https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf"
HEADER = """#!name=🇨🇳 CN 国内加速域名（自动生成）
#!desc=基于 dnsmasq-china-list 生成；未命中精选服务商规则的域名使用阿里 DoH
#!author=CN-DNS-Split
#!category=DNS

[Host]
"""

def download(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "CN-DNS-Split updater"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")

def parse_domains(text: str) -> set[str]:
    found = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^(?:server|address|ipset|nftset)=/([^/]+)/", line)
        if m:
            domain = m.group(1).strip(".").lower()
        elif re.fullmatch(r"[A-Za-z0-9.-]+", line):
            domain = line.strip(".").lower()
        else:
            continue
        labels = domain.split(".")
        if "." in domain and len(domain) <= 253 and all(
            re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", p) for p in labels
        ):
            found.add(domain)
    return found

def curated_roots(text: str) -> set[str]:
    roots = set()
    for line in text.splitlines():
        m = re.match(r"^(?:\*\.)?([A-Za-z0-9.-]+)\s*=\s*server:", line.strip())
        if m:
            roots.add(m.group(1).lower().strip("."))
    return roots

def covered(domain: str, roots: set[str]) -> bool:
    return any(domain == root or domain.endswith("." + root) for root in roots)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source", default=SOURCE_URL)
    p.add_argument("--curated", default="plugins/CN-DNS-Split.plugin")
    p.add_argument("--output", default="dist/CN-DNS-Accelerated.plugin")
    p.add_argument("--doh", default="https://dns.alidns.com/dns-query")
    a = p.parse_args()
    upstream = download(a.source)
    curated = Path(a.curated).read_text(encoding="utf-8")
    roots = curated_roots(curated)
    domains = sorted(d for d in parse_domains(upstream) if not covered(d, roots))
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(HEADER + "\n".join(f"{d} = server:{a.doh}" for d in domains) + "\n", encoding="utf-8")
    print(f"Generated {out}: {len(domains)} domains; excluded {len(roots)} curated roots")

if __name__ == "__main__":
    main()
