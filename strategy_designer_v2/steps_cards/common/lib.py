"""Code shared by the steps' helpers, in one place: the closed-book model call, atomic writes, a file's --- header, the
idea fields step 3 reads, and the shared definitions. A helper imports it with
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common")); from lib import ...
"""
import json, os, re, subprocess, sys, tempfile
from pathlib import Path

COMMON = Path(__file__).resolve().parent
# The calling session's variables that must not reach a closed-book model call.
DROP_ENV = {"CLAUDE_ADDITIONAL_DIRECTORIES", "CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD", "CLAUDE_EFFORT",
            "CLAUDE_CODE_USER_EMAIL", "CLAUDE_CODE_REMOTE_SESSION_ID", "CLAUDE_CODE_SESSION_ID"}


def call(model, system, request):
    """One model call, closed book: no tools, no files, no settings; the request on standard input. Returns (text,
    cost in USD)."""
    cmd = ["claude", "-p", "--model", model, "--system-prompt", system, "--tools", "",
           "--strict-mcp-config", "--disable-slash-commands", "--no-session-persistence", "--setting-sources", "",
           "--settings", '{"attribution":{"commit":"","pr":""},"includeCoAuthoredBy":false}', "--output-format", "json"]
    env = {k: v for k, v in os.environ.items() if k not in DROP_ENV}
    with tempfile.TemporaryDirectory() as empty:
        p = subprocess.run(cmd, input=request, cwd=empty, env=env, capture_output=True, text=True, timeout=900)
    d = json.loads(p.stdout)
    if d.get("is_error"):
        sys.exit(f"model call failed: {d.get('result')}")
    return d["result"], d["total_cost_usd"]


def write_atomic(path, text):
    """Write a file whole or not at all."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)


def header(text):
    """The --- header lines of a Markdown file, word for word, and the body."""
    m = re.match(r"\s*---\n(.*?)---\n(.*)", text, re.S)
    if not m:
        sys.exit("the file does not start with a --- header")
    return [l.strip() for l in m.group(1).splitlines() if l.strip()], m.group(2)


def header_fields(text):
    """The --- header of a Markdown file as a dict (empty when it has none)."""
    m = re.match(r"\s*---\n(.*?)---\n", text, re.S)
    return {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)} if m else {}


def common_text(name):
    """A shared definition, common/<name>.md."""
    return (COMMON / f"{name}.md").read_text()


# What step 3 reads of an idea file (operator, 2026-11-14): the same subset whatever step wrote it (step 2 or step 7).
# Anything else (a step 7 idea's "Why", with numbers measured on the data; a source line) never reaches a model that
# plans or analyses the idea's test.
IDEA_HEADER_FIELDS = ("brief", "instruments", "bar", "period")
IDEA_BODY_FIELDS = ("Idea", "Consequence")


def idea_fields(text):
    """An idea file reduced to the fields step 3 reads: its brief and data lines, then Idea and Consequence."""
    head, body = header(text)
    kept = [l for l in head if l.split(":", 1)[0].strip() in IDEA_HEADER_FIELDS]
    lines = []
    for f in IDEA_BODY_FIELDS:
        m = re.search(rf"^{f}:\s*(.+)$", body, re.M)
        if not m:
            sys.exit(f"the idea file has no '{f}:' line")
        lines.append(f"{f}: {m.group(1).strip()}")
    return "---\n" + "".join(l + "\n" for l in kept) + "---\n" + "".join(l + "\n" for l in lines)
