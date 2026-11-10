"""Brief helper, step 1. One closed-book model call writes one brief; this script checks its shape,
saves it as NNN_short-name.md in the briefs folder and adds its line to INDEX.md.

  python make_brief.py                          no theme: a theory of the helper's choice
  python make_brief.py --theme "..."            a theme in the operator's words
  python make_brief.py --source page.txt        a source pasted into a text file
A request that can only be met by a theory about several coins together gets "not researchable", with the reason:
no brief is written.
Options: --briefs-dir (default: ../briefs next to this folder), --model (default: the strongest).

The model sees only the system prompt, the index and the request: no tools, no files, no web, no
repository, an empty working folder. This script reads no market data.
"""
import argparse, json, os, re, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
KEYS = {"venue", "instruments", "bar", "period", "side", "source"}
MAX_THEORY_WORDS, MAX_INDEX_WORDS, ATTEMPTS = 900, 100, 3   # guards against a runaway answer, not length rules
DROP_ENV = {"CLAUDE_ADDITIONAL_DIRECTORIES", "CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD", "CLAUDE_EFFORT",
            "CLAUDE_CODE_USER_EMAIL", "CLAUDE_CODE_REMOTE_SESSION_ID", "CLAUDE_CODE_SESSION_ID"}


def call(model, system, request):
    """One model call, closed book. Returns (text, cost in USD)."""
    cmd = ["claude", "-p", request, "--model", model, "--system-prompt", system, "--tools", "",
           "--strict-mcp-config", "--disable-slash-commands", "--no-session-persistence", "--setting-sources", "",
           "--settings", '{"attribution":{"commit":"","pr":""},"includeCoAuthoredBy":false}', "--output-format", "json"]
    env = {k: v for k, v in os.environ.items() if k not in DROP_ENV}
    with tempfile.TemporaryDirectory() as empty:
        p = subprocess.run(cmd, cwd=empty, env=env, capture_output=True, text=True, timeout=600)
    d = json.loads(p.stdout)
    if d.get("is_error"):
        sys.exit(f"model call failed: {d.get('result')}")
    return d["result"], d["total_cost_usd"]


def slug(text, max_words=8):
    """A file-safe name: lowercase words joined by hyphens, at most max_words words."""
    words = re.sub(r"[^a-z0-9]+", " ", text.lower()).split()
    return "-".join(words[:max_words]) or "brief"


def parse(text, with_source):
    """Split the answer into header lines, theory, short-name, index summary, other theories.
    Refuse only a major deviation: no header, a header key outside the list, no theory, a runaway answer.
    Minor ones are fixed here: markup is stripped, the name is made file-safe, a missing index line
    falls back to the theory's first words, a missing other-theories line is recorded as not given."""
    m = re.match(r"\s*---\n(.*?)---\n(.*)", text, re.S)
    if not m:
        raise ValueError("the answer does not start with the --- header")
    header = [l.strip() for l in m.group(1).splitlines() if l.strip()]
    for l in header:
        if l.split(":", 1)[0].strip() not in KEYS:
            raise ValueError(f"header line outside the list: {l}")
    rest = re.sub(r"\*\*|__", "", m.group(2))
    rest = re.sub(r"^#+\s*", "", rest, flags=re.M)
    body = re.split(r"^(?:short-name|index-line|other-theories):", rest, flags=re.M)[0].strip()
    fields = dict(re.findall(r"^(short-name|index-line|other-theories):\s*(.*)$", rest, re.M))
    words = len(body.split())
    if not body or words > MAX_THEORY_WORDS:
        raise ValueError(f"the theory has {words} words; the limit is {MAX_THEORY_WORDS}")
    summary = fields.get("index-line", "").split("[")[0].strip() or " ".join(body.split()[:25])
    if len(summary.split()) > MAX_INDEX_WORDS:
        raise ValueError(f"the index-line has {len(summary.split())} words; write one or two short sentences")
    short = slug(fields.get("short-name") or summary)
    others = fields.get("other-theories", "not given") if with_source else None
    bracket = "[" + ", ".join(header) + "]"
    return header, body, short, summary, bracket, others


def write_atomic(path, text):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)


def main():
    a = argparse.ArgumentParser()
    g = a.add_mutually_exclusive_group()
    g.add_argument("--theme")
    g.add_argument("--source", type=Path)
    a.add_argument("--briefs-dir", type=Path, default=HERE.parent / "briefs")
    a.add_argument("--model", default="claude-opus-5-5")
    args = a.parse_args()

    briefs, index_path = args.briefs_dir, args.briefs_dir / "INDEX.md"
    briefs.mkdir(parents=True, exist_ok=True)
    index = index_path.read_text() if index_path.exists() else ""
    system = (HERE / "system_prompt.md").read_text()
    if args.theme:
        ask = f"Write one research brief on this theme, given by the operator in their own words:\n\n{args.theme}"
    elif args.source:
        ask = f"Write one research brief from the source below, pasted by the operator.\n\n[SOURCE]\n{args.source.read_text()}"
    else:
        ask = "Write one research brief on a trading theory of your choice."
    request = f"[INDEX OF BRIEFS ALREADY WRITTEN]\n{index.strip() or '(empty)'}\n\n{ask}"

    cost, refusal = 0.0, ""
    for attempt in range(1, ATTEMPTS + 1):
        text, c = call(args.model, system, request + refusal)
        cost += c
        nr = re.search(r"^not-researchable:\s*(.+)", text, re.M | re.S)
        if nr and not re.match(r"\s*---", text):
            print(f"not researchable: {' '.join(nr.group(1).split())}")
            print(f"cost: {cost:.4f} USD, attempts: {attempt}")
            return
        try:
            header, body, short, summary, bracket, others = parse(text, bool(args.source))
            break
        except ValueError as e:
            print(f"attempt {attempt} refused: {e}")
            refusal = f"\n\nYour previous answer was refused: {e}. Write the brief again."
    else:
        sys.exit(f"no valid brief after {ATTEMPTS} attempts; cost {cost:.4f} USD")

    numbers = [int(p.name[:3]) for p in briefs.glob("[0-9][0-9][0-9]_*.md")]
    name = f"{max(numbers, default=0) + 1:03d}_{short}"
    write_atomic(briefs / f"{name}.md", "---\n" + "".join(l + "\n" for l in header) + "---\n" + body + "\n")
    write_atomic(index_path, index + f"{name}: {summary} {bracket}\n")
    print(f"brief: {briefs / (name + '.md')}")
    print(f"index: {name}: {summary} {bracket}")
    if others:
        print(f"other theories in the source: {others}")
    print(f"cost: {cost:.4f} USD, attempts: {attempt}")


if __name__ == "__main__":
    main()
