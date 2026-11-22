"""Code shared by the steps' helpers, in one place: the closed-book model call, atomic writes, a file's --- header, the
idea fields step 3 reads, and the shared definitions. A helper imports it with
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common")); from lib import ...
"""
import json, os, re, subprocess, sys, tempfile, time
from pathlib import Path

COMMON = Path(__file__).resolve().parent
# The calling session's variables that must not reach a closed-book model call.
DROP_ENV = {"CLAUDE_ADDITIONAL_DIRECTORIES", "CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD", "CLAUDE_EFFORT",
            "CLAUDE_CODE_USER_EMAIL", "CLAUDE_CODE_REMOTE_SESSION_ID", "CLAUDE_CODE_SESSION_ID"}


TIMEOUT = 900          # seconds; a call still running then is killed
SERVICE_REFUSED = 75   # a helper's exit code when the model service refused a call (it never ran: a usage limit, an
                       # outage): not a fault of the idea or the step; run_idea and the loop stop and retry later


def call_line(d, seconds):
    """The line a model call prints: its time, its tokens and its USD (visibility only)."""
    u = d.get("usage") or {}
    thinking = (u.get("output_tokens_details") or {}).get("thinking_tokens", 0)
    return (f"model call: {seconds:.1f} s; tokens: input {u.get('input_tokens', 0)}, cache read "
            f"{u.get('cache_read_input_tokens', 0)}, cache write {u.get('cache_creation_input_tokens', 0)}, output "
            f"{u.get('output_tokens', 0)} (thinking {thinking}); {d.get('total_cost_usd', 0.0):.4f} USD; "
            f"stop: {d.get('stop_reason')}")


ARG_BYTES = 120_000   # under the 131,072-byte cap on one argument (Linux MAX_ARG_STRLEN)


def call(model, system, request):
    """One model call, closed book: no tools, no files, no settings; the request on standard input. Returns (text,
    cost in USD). Prints one line per call on standard error (time, tokens, USD); a call killed at the timeout says
    so, its cost unknown, and stops the helper."""
    # One argument is capped at 128 KB on Linux; step 3's prompt (its component catalogue) passed it on 2026-11-22
    # ("Argument list too long"). A longer prompt is cut at a line end: the head as the system prompt, the rest
    # appended to it (a prompt file is not the same: the model read its text as the user's, tested that night).
    head, rest = system, ""
    if len(system.encode()) > ARG_BYTES:
        cut = system.encode()[:ARG_BYTES].decode(errors="ignore").rfind("\n") + 1
        head, rest = system[:cut], system[cut:]
    cmd = ["claude", "-p", "--model", model, "--system-prompt", head, "--tools", "",
           "--strict-mcp-config", "--disable-slash-commands", "--no-session-persistence", "--setting-sources", "",
           "--settings", '{"attribution":{"commit":"","pr":""},"includeCoAuthoredBy":false}', "--output-format", "json"]
    if rest:
        cmd += ["--append-system-prompt", rest]
    env = {k: v for k, v in os.environ.items() if k not in DROP_ENV}
    t0 = time.time()
    with tempfile.TemporaryDirectory() as empty:
        try:
            p = subprocess.run(cmd, input=request, cwd=empty, env=env, capture_output=True, text=True, timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            print(f"model call: killed after {TIMEOUT} s; cost unknown", file=sys.stderr, flush=True)
            sys.exit(f"model call killed after {TIMEOUT} s (cost unknown)")
    try:
        d = json.loads(p.stdout)
    except ValueError:
        print(f"model call refused by the service: no answer ({(p.stderr or p.stdout)[-300:].strip()})", file=sys.stderr, flush=True)
        sys.exit(SERVICE_REFUSED)
    print(call_line(d, time.time() - t0), file=sys.stderr, flush=True)
    if d.get("is_error") and not d.get("total_cost_usd"):
        print(f"model call refused by the service: {d.get('result')}", file=sys.stderr, flush=True)
        sys.exit(SERVICE_REFUSED)
    if d.get("is_error"):
        sys.exit(f"model call failed: {d.get('result')}")
    return d["result"], d["total_cost_usd"]


CATALOGUE = COMMON.parent / "03_test_plan" / "helper" / "reference" / "component_catalogue.md"


def catalogue_version(path=CATALOGUE):
    """The component catalogue's version: the first 12 hex digits of its SHA-256. Step 3 writes it in each plan's
    header; the components step compares it to tell a refusal written before a component was added."""
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:12]


def utc_now():
    """The time a record line is written: a full UTC timestamp, YYYY-MM-DDTHH:MM:SSZ (the journals' "at"; operator,
    2026-11-17: a run's dates come from its record, not from git)."""
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_atomic(path, text):
    """Write a file whole or not at all."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
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
    return (COMMON / f"{name}.md").read_text(encoding="utf-8")


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
