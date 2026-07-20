---
sidebar_position: 3
---

# optimize_images.py

Standalone script: pass it one or more image URLs (e.g. ones PageSpeed
Insights flags as oversized) and it downloads + re-saves each as
optimized JPEG and WebP, organized into `original/`/`jpg/`/`webp/`
folders.

It doesn't resize — only recompresses/reformats — so the output is safe
to reuse anywhere the original was used (mobile, desktop, any
breakpoint).

## Requirements

```bash
pip3 install --user Pillow
```

## Usage

```bash
python3 optimize_images.py --output findings/image-optimization \
    https://their-domain.org/wp-content/uploads/2024/big-photo.png \
    https://their-domain.org/wp-content/uploads/2024/other.jpg
```

## Behavior

- Detects real alpha-channel transparency before converting — if an
  image genuinely uses transparency, it's left alone (converting to JPEG
  would silently destroy it) rather than corrupting the output.
- Reports a before/after size summary, including total savings across
  all images passed in.
- Typical results: 80-95% smaller file size at the same visual quality,
  since most flagged images are unnecessarily large PNGs where a JPEG or
  WebP re-encode loses nothing visible.

## Handoff tip

Lead with the `.webp` folder when handing files to a non-technical org —
it's the smallest and supported by every modern browser. Keep `.jpg` as
the fallback only if they have a specific reason to need it.
