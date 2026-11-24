"""Code shared by the steps' helpers, in one place: the closed-book model call, a child helper ending with its parent, atomic writes, a file's --- header, the
idea fields step 3 reads, and the shared definitions. A helper imports it with
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common")); from lib import ...
"""
import json, os, re, subprocess, sys, tempfile, time
from pathlib import Path

COMMON = Path(__file__).resolve().parent


def end_with_parent():
    """A helper started by another helper ends when that helper ends (killed by hand, by a time limit, or by a crash),
    so no orphan keeps writing into a step's files after its run was stopped (night 5: an orphan step 4 kept writing
    into the folder a resumed run was removing). How: a helper marks its children with its own process id
    (CARDS_PARENT_PID); a child that sees its parent's id there asks Linux to stop it when that parent ends. A helper
    started from a shell (the loop, run_idea or a step called by hand) is not marked, so it is never stopped this way.
    Elsewhere than Linux it does nothing."""
    if sys.platform.startswith("linux") and os.environ.get("CARDS_PARENT_PID") == str(os.getppid()):
        import ctypes, signal
        ctypes.CDLL(None, use_errno=True).prctl(1, signal.SIGTERM)       # 1 = PR_SET_PDEATHSIG
        if os.getppid() != int(os.environ["CARDS_PARENT_PID"]):           # the parent ended before the call above
            sys.exit("its parent ended")
    os.environ["CARDS_PARENT_PID"] = str(os.getpid())


end_with_parent()      # on import: every helper that imports lib takes part


# An idea's id (common/idea_created_from.md; topic 46, operator 2026-11-23): the lineage code (the brief's idea NNN-KK,
# then one .<line letter><number> per generation) and the idea's own short name: `022-04.b1.d2_strong-nearness`.
# Ids written before 2026-11-23 carry every ancestor's short name (`022-04_signal-weights.b1_power-turns.d2_strong-
# nearness`); both are read the same way, through their lineage code.
LINEAGE_STEP = re.compile(r"\.([a-g])(\d+)(?=[._]|$)")


def idea_code(idea_id):
    """The lineage code of an id, in either convention: '022-04_x.b1_y.d2_z' and '022-04.b1.d2_z' -> '022-04.b1.d2'."""
    head = idea_id.split(".", 1)[0].split("_", 1)[0]
    return head + "".join(f".{m.group(1)}{m.group(2)}" for m in LINEAGE_STEP.finditer(idea_id))


def child_id(parent_id, letter, number, name):
    """The id of the idea a step 7 line writes from parent_id: the parent's lineage code, the line's letter and the
    idea's number, and its short name. It grows by about 3 characters a generation, not by a whole name."""
    return f"{idea_code(parent_id)}.{letter}{number}_{name}"


def first_child_number(parent_id, letter, existing_ids):
    """The number a line's first new idea from parent_id takes: one after the highest number the same line already
    gave an idea of the same parent among existing_ids (the run's other analyses), so that a lineage code names one idea
    in a run (an idea tested on two bar sizes is analysed twice by the same line; before 2026-11-23 both analyses
    numbered from 1, which only the full names told apart)."""
    want = f"{idea_code(parent_id)}.{letter}"
    taken = [int(c[len(want):]) for c in map(idea_code, existing_ids) if c.startswith(want) and c[len(want):].isdigit()]
    return max(taken, default=0) + 1
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


def call(model, system, request):
    """One model call, closed book: no tools, no files, no settings; the request on standard input. Returns (text,
    cost in USD). Prints one line per call on standard error (time, tokens, USD); a call killed at the timeout says
    so, its cost unknown, and stops the helper."""
    cmd = ["claude", "-p", "--model", model, "--system-prompt-file", None, "--tools", "",
           "--strict-mcp-config", "--disable-slash-commands", "--no-session-persistence", "--setting-sources", "",
           "--settings", '{"attribution":{"commit":"","pr":""},"includeCoAuthoredBy":false}', "--output-format", "json"]
    env = {k: v for k, v in os.environ.items() if k not in DROP_ENV}
    t0 = time.time()
    # The system prompt goes in a file, not on the command line: one argument is capped at 128 KiB on Linux, and step
    # 3's prompt (with the component catalogue) passed it on 2026-11-22 ("Argument list too long"). Its own folder,
    # outside the call's empty working folder; the same text.
    with tempfile.TemporaryDirectory() as empty, tempfile.TemporaryDirectory() as sysdir:
        sysfile = Path(sysdir) / "system_prompt.md"
        sysfile.write_text(system, encoding="utf-8")
        cmd[cmd.index("--system-prompt-file") + 1] = str(sysfile)
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


def with_common(text):
    """A prompt with each {{NAME}} replaced by the shared file common/name.md (for example {{IDEA_DEFINITION}})."""
    return re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: common_text(m.group(1).lower()), text)


# The market profiles (common/market_profile.md; topic 49): the six names, and when a bar is in each. The trend is the
# coin's 60-day return in percent, the agitation the rank of its 30-day swing over the past 365 days (0 to 1).
PROFILE_TREND = {"rising": [("gt", 10)], "choppy": [("gte", -10), ("lte", 10)], "falling": [("lt", -10)]}
PROFILE_AGITATION = {"calm": [("lte", 0.5)], "agitated": [("gt", 0.5)]}
PROFILES = tuple(f"{t} {a}" for t in PROFILE_TREND for a in PROFILE_AGITATION)


def profile_name(text):
    """An idea's profile from a line such as "falling, agitated", "Choppy market" or "calm": its trend, its agitation, or
    both (trend first); None when the line names none ("none", empty) or names two trends or two agitations."""
    words = re.findall(r"[a-z]+", (text or "").lower())
    t = [w for w in words if w in PROFILE_TREND]
    a = [w for w in words if w in PROFILE_AGITATION]
    if len(t) > 1 or len(a) > 1 or not (t or a):
        return None
    return " ".join(t + a)


# What step 3 reads of an idea file (operator, 2026-11-14): the same subset whatever step wrote it (step 2 or step 7).
# Anything else (a step 7 idea's "Why", with numbers measured on the data; a source line) never reaches a model that
# plans or analyses the idea's test.
IDEA_HEADER_FIELDS = ("brief", "instruments", "bar", "period", "profile")
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


# Exploring and checking on different years (common/explore_and_check.md).
EXPLORATION_FOLDS = ("B", "C")      # 2018 to 2021: what step 7 explores
CHECK_FOLDS = ("A", "D")            # 2022 to 2025: step 5's direction check
FOLDS_FILE = COMMON.parents[2] / "trading-bot" / "config" / "folds.yaml"


def plan_folds(plan_text):
    """The plan's folds in its order ('data-period: folds A, B, C, D'); () when the plan names none."""
    m = re.search(r"^data-period:\s*folds?\s+([A-Z](?:\s*,\s*[A-Z])*)\s*$", plan_text, re.M)
    return tuple(f.strip() for f in m.group(1).split(",")) if m else ()


def fold_windows(plan_text, folds_file=FOLDS_FILE):
    """{fold: [window names]}: a record names its windows w1..wN in the plan's fold order (04_backtest/card.md), each
    fold holding its windows in folds.yaml's count. Reads the count only, never a date."""
    import yaml
    counts = {k: len(v) for k, v in yaml.safe_load(folds_file.read_text())["folds"].items()}
    out, n = {}, 0
    for f in plan_folds(plan_text):
        out[f] = [f"w{i}" for i in range(n + 1, n + counts.get(f, 0) + 1)]
        n += counts.get(f, 0)
    return out


def ran_on_folds(record):
    """True when the backtest ran on its plan's folds (a coin's `fold_<X>` folder), not on other windows (`--windows`,
    the unseen dates)."""
    return any(p.is_dir() for p in Path(record).glob("*/fold_*"))


def windows_of(plan_text, folds, record=None):
    """The window names of these folds in this plan; empty when the record did not run on its folds."""
    if record is not None and not ran_on_folds(record):
        return []
    fw = fold_windows(plan_text)
    return [w for f in folds for w in fw.get(f, [])]
