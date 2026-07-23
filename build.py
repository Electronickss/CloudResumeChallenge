#!/usr/bin/env python3
"""Build script: converts resume/resume.md to frontend/index.html."""

import os
import re
import markdown
import yaml
from jinja2 import Template

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESUME_PATH = os.path.join(SCRIPT_DIR, "resume", "resume.md")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "frontend", "index.html")

HTML_TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ name }} — {{ title }}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="header">
    <h1>{{ name }}</h1>
    <div class="contact">{{ location }} &bull; {{ phone }} &bull; {{ email }}</div>
  </div>

  <div class="visitor-counter">
    Views: <span id="visitor-count">...</span>
  </div>

  {{ content | safe }}

  <script src="counter.js"></script>
</body>
</html>
""")


def parse_resume(path):
    with open(path, "r") as f:
        raw = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", raw, re.DOTALL)
    if not match:
        raise ValueError("No YAML front matter found in resume.md")

    meta = yaml.safe_load(match.group(1))
    body = match.group(2)
    return meta, body


def render_body(body):
    extensions = ["fenced_code", "tables", "sane_lists"]
    html = markdown.markdown(body, extensions=extensions)
    return html


def build():
    meta, body = parse_resume(RESUME_PATH)
    content = render_body(body)
    html = HTML_TEMPLATE.render(
        name=meta["name"],
        title=meta["title"],
        location=meta["location"],
        phone=meta["phone"],
        email=meta["email"],
        content=content,
    )
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write(html)
    print(f"Built {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
