"""Base-branch synthetic control verifier; never execute code from the PR head."""

import base64
import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request


REPO = os.environ["GH_REPOSITORY"]
HEAD = os.environ["PR_HEAD_SHA"]
TOKEN = os.environ["GH_TOKEN"]
API = f"https://api.github.com/repos/{REPO}"
CONTEXT = "trial/exact-head"


def request(path, method="GET", payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{API}/{path}",
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {TOKEN}",
            "X-GitHub-Api-Version": "2026-03-10",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)


def file_at_head(name):
    encoded = urllib.parse.quote(name, safe="")
    item = request(f"contents/{encoded}?ref={HEAD}")
    if item.get("type") != "file" or item.get("encoding") != "base64":
        raise ValueError(f"{name} is not a base64 file")
    return base64.b64decode(item["content"], validate=False)


state = "failure"
description = "synthetic witness invalid"
try:
    commit = request(f"commits/{HEAD}")
    parent = commit["parents"][0]["sha"]
    source = file_at_head("source.txt")
    witness = json.loads(file_at_head("witness.json"))
    valid = (
        witness.get("kind") == "synthetic-exact-head-v1"
        and witness.get("parent_sha") == parent
        and witness.get("source_sha256") == hashlib.sha256(source).hexdigest()
        and witness.get("verdict") == "PASS"
    )
    if valid:
        state = "success"
        description = "synthetic witness matches this head's parent and source"
    else:
        description = "synthetic witness failed parent/source/verdict binding"
except (KeyError, ValueError, IndexError, urllib.error.HTTPError) as exc:
    description = f"synthetic witness unreadable: {type(exc).__name__}"[:140]

request(
    f"statuses/{HEAD}",
    method="POST",
    payload={"state": state, "context": CONTEXT, "description": description},
)
print(json.dumps({"head": HEAD, "context": CONTEXT, "state": state, "description": description}))
if state != "success":
    raise SystemExit(1)
