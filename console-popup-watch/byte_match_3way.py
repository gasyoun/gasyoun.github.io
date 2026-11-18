# MIT License — © 2026 Dr. Mārcis Gasūns — https://github.com/gasyoun/gasyoun.github.io
"""Three-place byte-match: prove a source fix did not revert in any copy.

Compares each file across three places:
  live   <live-dir>  — the deployed, running copy (may use CRLF)
  deploy <deploy-dir> — a second deploy chain, if any (optional)
  repo   <repo> HEAD:<file> — the canonical repo copy (git show)

CRLF is normalized before hashing (the EOL artifact is not a revert). Exit 0
when live == deploy (if given) and live == repo for every file; exit 1 on any
drift or error — a drifted file is named on stdout.

Usage:
  python byte_match_3way.py --live C:/path/live --deploy C:/path/deploy \
      --repo C:/path/repo --file plugin/foo.ts [--file plugin/bar.ts]

Dependencies: stdlib + git on PATH (for `git show`). MIT — reuse freely.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys


def sha_norm(path):
    with open(path, "rb") as f:
        data = f.read()
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def sha_norm_bytes(data):
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def git_show(repo, relpath):
    r = subprocess.run(["git", "-C", repo, "show", f"HEAD:{relpath.replace(os.sep, '/')}"],
                       capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--live", required=True, help="directory of the live copy")
    ap.add_argument("--deploy", default=None, help="directory of a second deploy copy (optional)")
    ap.add_argument("--repo", required=True, help="path to the canonical git repo")
    ap.add_argument("--file", action="append", required=True,
                    help="repo-relative file path (repeat per file)")
    a = ap.parse_args()

    report = {"live": a.live, "deploy": a.deploy, "repo": a.repo, "files": []}
    drift = False

    for rel in a.file:
        live_path = os.path.join(a.live, rel)
        entry = {"file": rel}
        try:
            live_sha = sha_norm(live_path)
            entry["live_sha256"] = live_sha
        except OSError as e:
            entry["error"] = f"live read failed: {e}"
            report["files"].append(entry)
            drift = True
            continue
        if a.deploy:
            try:
                dep_sha = sha_norm(os.path.join(a.deploy, rel))
                entry["deploy_sha256"] = dep_sha
                entry["live_equals_deploy"] = dep_sha == live_sha
                if dep_sha != live_sha:
                    drift = True
            except OSError as e:
                entry["error"] = f"deploy read failed: {e}"
                drift = True
        head = git_show(a.repo, rel)
        if head is None:
            entry["error"] = "git show failed (file absent at HEAD?)"
            drift = True
        else:
            head_sha = sha_norm_bytes(head)
            entry["repo_sha256"] = head_sha
            entry["live_equals_repo_normalized"] = head_sha == live_sha
            if head_sha != live_sha:
                drift = True
        report["files"].append(entry)

    report["all_equal_normalized"] = not drift
    print(json.dumps(report, indent=2))
    sys.exit(0 if not drift else 1)


if __name__ == "__main__":
    main()
