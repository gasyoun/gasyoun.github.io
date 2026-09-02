"""Wrap a Claude Artifact fragment into a standalone HTML document for GitHub Pages.

Why this exists (Uprava FINDINGS §684)
--------------------------------------
A Claude Artifact is authored as a *fragment*: the Artifact host wraps it in
`<!doctype html><head>...</head><body>` at publish time, and that injected head
carries a small reset -- `color-scheme`, `body{margin:0}`, `img{max-width:100%}`
and, critically, `[hidden]{display:none!important}`.

The documented way to toggle visibility inside an Artifact is `el.hidden`, so any
tabbed or stepped page depends on that last rule without ever declaring it. Copy
the same bytes into a Pages repo and the dependency vanishes silently: an element
whose own CSS sets `display` overrides the UA default for `[hidden]`, so every
panel renders stacked. The file is byte-identical, the HTML validates, every link
resolves -- and the page is broken, visually only.

So: porting an Artifact to Pages is a format change, not a copy. Keep the fragment
as the single source of truth and run this wrapper.

Usage
-----
    python build_standalone.py <fragment.html> <output.html> [--description "..."]

Exits non-zero if any load-bearing property is missing from the result.
"""
import argparse
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

# The reset the Artifact host supplies and a standalone document must restate.
HOST_RESET = """  /* Reset the Artifact host normally supplies; the page depends on it. */
  :root{color-scheme:light dark}
  body{margin:0}
  img{max-width:100%}
  [hidden]{display:none!important}"""


def build(fragment: str, description: str) -> tuple[str, str]:
    """Return (standalone document, title) for one Artifact fragment."""
    match = re.search(r"<title>(.*?)</title>\s*", fragment, re.S)
    if not match:
        raise ValueError("no <title> found in the fragment")

    title = match.group(1).strip()
    body = fragment[: match.start()] + fragment[match.end() :]

    head = (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{title}</title>\n"
        f'<meta name="description" content="{description}">\n'
        f'<meta property="og:title" content="{title}">\n'
        f'<meta property="og:description" content="{description}">\n'
        '<meta property="og:type" content="article">\n'
        "<style>\n"
        f"{HOST_RESET}\n"
        "</style>\n"
        "</head>\n"
        "<body>\n"
    )
    return head + body.strip() + "\n</body>\n</html>\n", title


def verify(doc: str, title: str) -> dict:
    """The properties that would otherwise fail silently, visually only."""
    head, _, tail = doc.partition("</head>")
    return {
        "doctype first": doc.lstrip().startswith("<!DOCTYPE html>"),
        "hidden reset present": "[hidden]{display:none!important}" in doc,
        "body margin reset present": "body{margin:0}" in doc,
        "charset declared": '<meta charset="utf-8">' in head,
        "viewport declared": 'name="viewport"' in head,
        "title in head": f"<title>{title}</title>" in head,
        "no stray title in body": "<title>" not in tail,
        "no nested doctype": doc.count("<!DOCTYPE") == 1,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fragment", help="the Artifact fragment (.html)")
    parser.add_argument("output", help="standalone document to write")
    parser.add_argument("--description", default="", help="meta/og description")
    args = parser.parse_args()

    with open(args.fragment, encoding="utf-8") as fh:
        fragment = fh.read()

    try:
        doc, title = build(fragment, args.description)
    except ValueError as exc:
        print(f"FAIL - {exc}")
        return 1

    checks = verify(doc, title)
    for name, ok in checks.items():
        print(f"  {'ok  ' if ok else 'FAIL'}  {name}")

    if not all(checks.values()):
        print("\nFAIL - not written")
        return 1

    with open(args.output, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(doc)

    print(f"\nPASS - wrote {args.output} ({len(doc):,} bytes), title: {title}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
