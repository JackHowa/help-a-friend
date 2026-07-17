#!/usr/bin/env python3
"""
Downloads image URLs (e.g. ones PageSpeed Insights flagged as oversized)
and re-saves them as optimized JPEG + WebP, organized into format folders
so you can hand the org "lead with webp/, jpg/ as fallback."

Doesn't resize — only recompresses/reformats — so the output is safe to
reuse anywhere the original was used (mobile, desktop, any breakpoint).

Requires Pillow: pip3 install --user Pillow

Usage:
    python3 optimize_images.py --output findings/image-optimization \
        https://example.org/wp-content/uploads/2024/big-photo.png \
        https://example.org/wp-content/uploads/2024/other.jpg
"""

import argparse
import os
import re
import sys
import urllib.error
import urllib.request

try:
    from PIL import Image
except ImportError:
    print("Pillow is required: pip3 install --user Pillow", file=sys.stderr)
    sys.exit(1)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
QUALITY = 80


def slugify(url):
    name = url.split("/")[-1]
    name = re.sub(r"\.(png|jpe?g|webp|gif)$", "", name, flags=re.I)
    name = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
    return name or "image"


def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def has_real_transparency(img):
    if img.mode != "RGBA":
        return False
    alpha = img.split()[-1]
    lo, hi = alpha.getextrema()
    return lo < 255


def optimize(url, output_dir):
    slug = slugify(url)
    for sub in ("original", "jpg", "webp"):
        os.makedirs(os.path.join(output_dir, sub), exist_ok=True)

    try:
        raw = download(url)
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"  ⚠️  {url}: download failed ({e})", file=sys.stderr)
        return None

    ext = url.split(".")[-1].split("?")[0].lower()
    original_path = os.path.join(output_dir, "original", f"{slug}-original.{ext}")
    with open(original_path, "wb") as f:
        f.write(raw)

    import io
    img = Image.open(io.BytesIO(raw))
    original_size = len(raw)

    if has_real_transparency(img):
        print(f"  ⚠️  {url}: has real transparency, skipping lossy JPEG "
              f"(would lose transparency) — keeping only the downloaded original", file=sys.stderr)
        return {"url": url, "original_size": original_size, "skipped": "transparency"}

    img = img.convert("RGB")
    jpg_path = os.path.join(output_dir, "jpg", f"{slug}-optimized.jpg")
    webp_path = os.path.join(output_dir, "webp", f"{slug}-optimized.webp")
    img.save(jpg_path, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    img.save(webp_path, "WEBP", quality=QUALITY, method=6)

    jpg_size = os.path.getsize(jpg_path)
    webp_size = os.path.getsize(webp_path)
    return {
        "url": url,
        "dimensions": img.size,
        "original_size": original_size,
        "jpg_size": jpg_size,
        "webp_size": webp_size,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("urls", nargs="+", help="Image URLs to download and optimize")
    parser.add_argument("--output", default="image-optimization", help="Output directory")
    args = parser.parse_args()

    results = []
    for url in args.urls:
        print(f"Processing {url} ...", file=sys.stderr)
        result = optimize(url, args.output)
        if result:
            results.append(result)

    print("\n--- Summary ---")
    total_before = total_jpg = total_webp = 0
    for r in results:
        if r.get("skipped"):
            print(f"{r['url']}: skipped ({r['skipped']})")
            continue
        before_kb = r["original_size"] / 1024
        jpg_kb = r["jpg_size"] / 1024
        webp_kb = r["webp_size"] / 1024
        savings = round((1 - r["webp_size"] / r["original_size"]) * 100)
        print(f"{r['url']}: {before_kb:.0f}KB -> jpg {jpg_kb:.0f}KB / webp {webp_kb:.0f}KB ({savings}% smaller via webp)")
        total_before += r["original_size"]
        total_jpg += r["jpg_size"]
        total_webp += r["webp_size"]

    if total_before:
        print(f"\nTotal: {total_before/1024:.0f}KB -> jpg {total_jpg/1024:.0f}KB / webp {total_webp/1024:.0f}KB")
    print(f"\nFiles written under {args.output}/{{original,jpg,webp}}/")


if __name__ == "__main__":
    main()
