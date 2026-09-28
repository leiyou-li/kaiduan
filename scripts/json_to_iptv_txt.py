#!/usr/bin/env python3
"""Convert kaiduan IPTV JSON to DIYP/TVBox-style txt playlist."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def clean_url(url: str) -> str:
    """Strip player UA query params; keep other query string values."""
    url = url.strip()
    if not url:
        return url

    parts = urlsplit(url)
    query_items = [
        (k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k.lower() != "ua"
    ]
    query = urlencode(query_items, doseq=True)
    cleaned = urlunsplit((parts.scheme, parts.netloc, parts.path, query, parts.fragment))

    # Match sample style: drop a lone trailing slash on path-only URLs.
    if cleaned.endswith("/") and "?" not in cleaned and "#" not in cleaned:
        cleaned = cleaned.rstrip("/")

    return cleaned


def iter_urls(urls: Any) -> list[str]:
    result: list[str] = []
    if not isinstance(urls, list):
        return result

    for item in urls:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, dict):
            url = item.get("url")
            if isinstance(url, str):
                result.append(url)
    return result


def convert(data: Any) -> str:
    if not isinstance(data, list):
        raise ValueError("Expected a JSON array of categories")

    lines: list[str] = []
    for category in data:
        if not isinstance(category, dict):
            continue
        cat_name = str(category.get("name") or "").strip()
        if not cat_name:
            continue

        lines.append(f"{cat_name},#genre#")
        datas = category.get("datas") or []
        if not isinstance(datas, list):
            continue

        for channel in datas:
            if not isinstance(channel, dict):
                continue
            ch_name = str(channel.get("name") or "").strip()
            if not ch_name:
                continue
            for raw_url in iter_urls(channel.get("urls")):
                url = clean_url(raw_url)
                if url:
                    lines.append(f"{ch_name}, {url}")

    return "\n".join(lines) + ("\n" if lines else "")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Input JSON file")
    parser.add_argument("output", type=Path, help="Output txt file")
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    text = convert(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8", newline="\n")
    print(f"Wrote {args.output} ({len(text.splitlines())} lines)")


if __name__ == "__main__":
    main()
