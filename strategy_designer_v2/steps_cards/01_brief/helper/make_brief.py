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
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))
from lib import call, write_atomic, with_common  # noqa: E402  (shared helpers, common/lib.py)
import target_box  # noqa: E402  (a run's target box, part of the brief's theme: common/target_box.md)
import coins  # noqa: E402  (a run's data use and the coin groups: common/data_use.md, common/coins.md)

HERE = Path(__file__).resolve().parent
KEYS = {"venue", "instruments", "bar", "period", "side", "source", "profile"}   # profile: a boxed run's brief (B2.1)
MAX_THEORY_WORDS, MAX_INDEX_WORDS, ATTEMPTS = 900, 100, 3   # guards against a runaway answer, not length rules
INSTRUMENTS_KEY = "- instruments: the coins or pairs\n"      # the header key step 1 is not asked for in the new data use


def coins_note():
    """In a run in the new data use (common/data_use.md), the run's coins are drawn by rule: the brief's instruments
    line is written by code, and the model is told so, in place of being asked for it."""
    return ("\n[THE COINS OF THIS RESEARCH]\nThe coins this research runs on are chosen by the workflow, not by the brief: "
            "write no `instruments:` line (it is written for you), and name no coin in the theory.\n")


def final_coins_named(text):
    """The final group's coins (common/coins.md) a text names, as tickers: they are used by no step before the final
    test, so no file step 1 writes in the new data use may name one."""
    return [c for c in coins.FINAL if re.search(rf"\b{c}\b", text)]


def with_research_coins(header, research_coins):
    """The brief's header with its instruments line written by code: the run's research coins, whatever the answer
    named."""
    return [f"instruments: {', '.join(research_coins)}"] + [l for l in header if l.split(":", 1)[0].strip() != "instruments"]


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


def main():
    a = argparse.ArgumentParser()
    g = a.add_mutually_exclusive_group()
    g.add_argument("--theme")
    g.add_argument("--source", type=Path)
    a.add_argument("--briefs-dir", type=Path, default=HERE.parent / "briefs")
    a.add_argument("--model", default="claude-opus-5-5")
    a.add_argument("--run", help="the run the brief is for: in a run with a target box, the box is part of its theme; "
                   "in a run in the new data use (its data_use.json), the brief's instruments are its research coins")
    args = a.parse_args()

    briefs, index_path = args.briefs_dir, args.briefs_dir / "INDEX.md"
    briefs.mkdir(parents=True, exist_ok=True)
    index = index_path.read_text() if index_path.exists() else ""
    system = with_common((HERE / "system_prompt.md").read_text())
    du = coins.data_use(args.run) if args.run else None      # the run's data use (None: the old one, step 1 as before)
    if du:
        system = system.replace(INSTRUMENTS_KEY, "")
    if args.theme:
        ask = f"Write one research brief on this theme, given by the operator in their own words:\n\n{args.theme}"
    elif args.source:
        ask = f"Write one research brief from the source below, pasted by the operator.\n\n[SOURCE]\n{args.source.read_text()}"
    else:
        ask = "Write one research brief on a trading theory of your choice."
    request = f"[INDEX OF BRIEFS ALREADY WRITTEN]\n{index.strip() or '(empty)'}\n\n{ask}"
    request += target_box.theme_note(args.run) if args.run else ""       # the run's box (empty without one)
    request += coins_note() if du else ""

    cost, refusal = 0.0, ""
    for attempt in range(1, ATTEMPTS + 1):
        text, c = call(args.model, system, request + refusal)
        cost += c
        nr = re.search(r"^not-researchable:\s*(.+)", text, re.M | re.S)
        if nr and not re.match(r"\s*---", text):
            print(f"not researchable: {' '.join(nr.group(1).split())}")
            print(f"cost: {cost:.4f} USD, attempts: {attempt}")
            return
        # A source whose only theory is already in the index (2026-11-24, topic 50: a discovery found again in another
        # backtest): no brief, the existing one named, rather than another theory the source does not state.
        ai = re.search(r"^already-indexed:\s*(\S+)", text, re.M)
        if ai and not re.match(r"\s*---", text):
            print(f"already indexed: {ai.group(1).strip()}")
            print(f"cost: {cost:.4f} USD, attempts: {attempt}")
            return
        try:
            header, body, short, summary, bracket, others = parse(text, bool(args.source))
            if du:      # the new data use: the instruments by code; no final coin in what is written
                header = with_research_coins(header, du["research_coins"])
                bracket = "[" + ", ".join(header) + "]"
                named = final_coins_named("\n".join(header + [body, short, summary]))
                if named:
                    raise ValueError(f"the brief names {', '.join(named)}: name no coin")
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
