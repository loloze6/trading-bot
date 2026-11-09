"""Ideas helper, step 2. One closed-book model call reads one brief and writes the ideas it gives;
this script checks their shape, saves each as NNN-KK_short-name.md in the ideas folder, with the
brief's name and header lines copied into its header, and adds its line to INDEX.md.

  python make_ideas.py path/to/NNN_brief-name.md
Options: --ideas-dir (default: ../ideas next to this folder), --model (default: the strongest).

The model sees only the system prompt, the index and the brief: no tools, no files, no web, no
repository, an empty working folder. This script reads no market data.
"""
import argparse, json, os, re, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAX_FIELD_WORDS, ATTEMPTS = 300, 3   # 300 words: a guard against a runaway answer, not a length rule
MARKET_KEYS = {"venue", "instruments", "bar", "period", "side"}
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


def brief_header(text):
    """The brief's header lines, word for word."""
    m = re.match(r"\s*---\n(.*?)---\n", text, re.S)
    if not m:
        sys.exit("the brief does not start with a --- header")
    return [l.strip() for l in m.group(1).splitlines() if l.strip()]


def slug(text, max_words=8):
    """A file-safe name: lowercase words joined by hyphens, at most max_words words."""
    words = re.sub(r"[^a-z0-9]+", " ", text.lower()).split()
    return "-".join(words[:max_words]) or "idea"


def parse(text):
    """Split the answer into idea blocks and the already-indexed line.
    Refuse only a major deviation: a block without its idea or consequence, or a runaway field.
    Minor ones are fixed here: markup is stripped, the name is made file-safe, a missing index line
    falls back to the idea, a missing already-indexed line is recorded as not given."""
    text = re.sub(r"\*\*|__", "", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.M)
    m = re.search(r"^already-indexed:\s*(.*)$", text, re.M | re.I)
    already, body = (m.group(1).strip(), text[:m.start()]) if m else ("not given", text)
    ideas = []
    for raw in re.split(r"^\s*---\s*$", body, flags=re.M):
        fields = dict((k.lower(), " ".join(v.split())) for k, v in
                      re.findall(r"^(idea|consequence|short-name|index-line):\s*(.*?)(?=^(?:idea|consequence|short-name|index-line):|\Z)",
                                 raw, re.M | re.S | re.I))
        if not fields:
            continue
        if not fields.get("idea") or not fields.get("consequence"):
            raise ValueError(f"a block has no idea or no consequence: {' '.join(raw.split())[:80]}")
        for k, v in fields.items():
            if len(v.split()) > MAX_FIELD_WORDS:
                raise ValueError(f"the {k} field has {len(v.split())} words; write one or two sentences")
        idea, consequence = fields["idea"], fields["consequence"]
        ideas.append((idea, consequence, slug(fields.get("short-name") or idea), fields.get("index-line") or idea))
    if not ideas and not m:
        raise ValueError("the answer has no idea block and no already-indexed line")
    return ideas, already


def write_atomic(path, text):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("brief", type=Path)
    a.add_argument("--ideas-dir", type=Path, default=HERE.parent / "ideas")
    a.add_argument("--model", default="claude-opus-5-5")
    args = a.parse_args()

    brief_text, brief_name = args.brief.read_text(), args.brief.stem
    header = brief_header(brief_text)
    ideas_dir, index_path = args.ideas_dir, args.ideas_dir / "INDEX.md"
    ideas_dir.mkdir(parents=True, exist_ok=True)
    index = index_path.read_text() if index_path.exists() else ""
    system = (HERE / "system_prompt.md").read_text()
    request = (f"[INDEX OF IDEAS ALREADY WRITTEN]\n{index.strip() or '(empty)'}\n\n"
               f"Write the ideas this research brief gives.\n\n[BRIEF]\n{brief_text}")

    cost, refusal = 0.0, ""
    for attempt in range(1, ATTEMPTS + 1):
        text, c = call(args.model, system, request + refusal)
        cost += c
        try:
            ideas, already = parse(text)
            break
        except ValueError as e:
            print(f"attempt {attempt} refused: {e}")
            refusal = f"\n\nYour previous answer was refused: {e}. Write the ideas again."
    else:
        sys.exit(f"no valid answer after {ATTEMPTS} attempts; cost {cost:.4f} USD")

    nnn = brief_name[:3]
    taken = [int(p.name[4:6]) for p in ideas_dir.glob(f"{nnn}-[0-9][0-9]_*.md")]
    kk = max(taken, default=0)
    file_header = "---\n" + f"brief: {brief_name}\n" + "".join(l + "\n" for l in header) + "---\n"
    market = [l for l in header if l.split(":", 1)[0].strip() in MARKET_KEYS]
    bracket = "[" + ", ".join(market) + "]" if market else ""
    lines = []
    for idea, consequence, short, line in ideas:
        kk += 1
        name = f"{nnn}-{kk:02d}_{short}"
        write_atomic(ideas_dir / f"{name}.md", file_header + f"Idea: {idea}\nConsequence: {consequence}\n")
        lines.append(f"{name}: {line} {bracket}".rstrip())
        print(f"idea: {ideas_dir / (name + '.md')}")
    write_atomic(index_path, index + "".join(l + "\n" for l in lines))
    print(f"ideas written: {len(ideas)}")
    print(f"already-indexed: {already}")
    print(f"cost: {cost:.4f} USD, attempts: {attempt}")


if __name__ == "__main__":
    main()
