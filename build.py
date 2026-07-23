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
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;700;800;900&display=swap" rel="stylesheet">
</head>
<body>
  <div class="page-header">
    <h1 class="header-name">{{ name }}</h1>

    <div class="title-bar">
      <h2 class="header-title">{{ title }}</h2>
      <ul class="social-links">
        {% if github %}<li><a href="{{ github }}" target="_blank"><svg viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg> GitHub</a></li>{% endif %}
        {% if linkedin %}<li><a href="{{ linkedin }}" target="_blank"><svg viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg> LinkedIn</a></li>{% endif %}
        {% if twitter %}<li><a href="{{ twitter }}" target="_blank"><svg viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg> Twitter</a></li>{% endif %}
      </ul>
    </div>

    <div class="header-contact-info">
      {{ location }} &bull; {{ phone }} &bull; <a href="mailto:{{ email }}">{{ email }}</a>
    </div>
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
        github=meta.get("github", ""),
        linkedin=meta.get("linkedin", ""),
        twitter=meta.get("twitter", ""),
        content=content,
    )
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write(html)
    print(f"Built {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
