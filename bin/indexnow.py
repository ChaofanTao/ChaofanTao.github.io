#!/usr/bin/env python3
"""Submit every URL in the built sitemap to IndexNow (Bing, Yandex, Naver, Seznam, ...).

Waits until the deployed key file is publicly reachable, because IndexNow verifies
ownership by fetching https://<host>/<key>.txt.

Usage: python3 bin/indexnow.py [--site _site] [--dry-run]
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from xml.etree import ElementTree

HOST = "chaofantao.top"
ENDPOINT = "https://api.indexnow.org/indexnow"
EXTRA_PATHS = ["/llms.txt", "/llms-full.txt"]


def find_key(repo: Path) -> str:
    keys = [p.stem for p in repo.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}", p.stem)]
    if len(keys) != 1:
        sys.exit(f"expected exactly one IndexNow key file in {repo}, found {keys}")
    return keys[0]


def sitemap_urls(site: Path) -> list[str]:
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    root = ElementTree.parse(site / "sitemap.xml").getroot()
    urls = [loc.text.strip() for loc in root.findall("s:url/s:loc", ns)]
    return urls + [f"https://{HOST}{p}" for p in EXTRA_PATHS if (site / p.lstrip("/")).exists()]


def wait_for_key(key: str, timeout: int) -> None:
    url = f"https://{HOST}/{key}.txt"
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{url}?t={int(time.time())}", timeout=15) as r:
                if r.status == 200 and r.read().decode().strip() == key:
                    print(f"key file live: {url}")
                    return
        except urllib.error.URLError:
            pass
        time.sleep(15)
    sys.exit(f"key file not reachable after {timeout}s: {url}")


def submit(key: str, urls: list[str]) -> None:
    body = json.dumps(
        {"host": HOST, "key": key, "keyLocation": f"https://{HOST}/{key}.txt", "urlList": urls}
    ).encode()
    req = urllib.request.Request(
        ENDPOINT, data=body, headers={"Content-Type": "application/json; charset=utf-8"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow HTTP {r.status}: submitted {len(urls)} URLs")
    except urllib.error.HTTPError as e:
        # 200 = accepted, 202 = accepted pending key validation; 4xx means the request was rejected.
        sys.exit(f"IndexNow HTTP {e.code}: {e.read().decode(errors='replace')[:300]}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="_site")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parent.parent
    key = find_key(repo)
    urls = sitemap_urls(Path(args.site))
    print("\n".join(urls))
    if args.dry_run:
        return
    wait_for_key(key, args.timeout)
    submit(key, urls)


if __name__ == "__main__":
    main()
