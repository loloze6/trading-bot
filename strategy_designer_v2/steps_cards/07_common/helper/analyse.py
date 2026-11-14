"""Step 7, one analysis line. The same script for every line (7.a to 7.g); a line is its folder's helper/line.yaml
(id, name, entry condition) and helper/line_prompt.md (its objective, what it looks for, what it proposes).

  python analyse.py LINE_DIR RECORD --plan PLAN.md --briefs-dir DIR --verdicts-dir DIR --checks-dir DIR --python VENV_PY
Options: --out-dir (default: LINE_DIR/analyses), --rounds (default 3), --split (an analyst writes the findings, then a
separate deducer, who does not see the data, writes the ideas), --model (default: the strongest).

How it runs:
1. The entry condition: the line runs only when step 5's verdict and step 6's check on this backtest meet it.
2. Rounds: a closed-book model call reads the brief, the plan, the verdict, the check and a description of the data
   (no rows), and either writes `explore(data)` or gives its answer. The function runs on the record in a separate,
   isolated process with the venv's Python; its results (aggregates, at most 40 rows each, dates hidden) go back to the
   next call. At most --rounds explorations, then the answer.
3. The answer: findings (each with its numbers), then ideas (each naming the findings it rests on), or "no-ideas".
   Code refuses only a major deviation and sends it back, up to three times.
4. Saves the analysis, one file per idea in step 2's format (with its origin and its why), every exploration and its
   result, and the index line.
"""
import argparse, json, os, re, subprocess, sys, tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
STEPS = HERE.parents[1]
sys.path.insert(0, str(STEPS / "03_test_plan" / "helper"))
from make_test_plan import call, write_atomic   # noqa: E402  (the same closed-book call as steps 3 and 5)

ATTEMPTS, MAX_WORDS, ROW_CAP, CHAR_CAP = 3, 300, 40, 15000
DATE = re.compile(r"\b(19|20)\d\d-\d\d(-\d\d)?([ T]\d\d:\d\d(:\d\d)?(\.\d+)?([+-]\d\d:\d\d|Z)?)?\b")

RUNNER = r'''
import glob, gzip, json, os, re, sys
import numpy as np, pandas as pd
record, script, cap_rows, cap_chars = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
data = {"bars": {}, "trades": {}, "days": {}}
for coin in sorted(d for d in os.listdir(record) if os.path.isdir(os.path.join(record, d))):
    for f in sorted(glob.glob(os.path.join(record, coin, "w*", "bars.csv.gz")), key=lambda p: int(p.split(os.sep)[-2][1:])):
        w = f.split(os.sep)[-2]
        b = pd.read_csv(f, low_memory=False)
        b["timestamp"] = pd.to_datetime(b["timestamp"], utc=True)
        data["bars"].setdefault(coin, {})[w] = b
        tf = os.path.join(os.path.dirname(f), "trades.json.gz")
        t = pd.DataFrame(json.load(gzip.open(tf, "rt")) if os.path.exists(tf) else [])
        for c in ("entry_time", "exit_time"):
            if c in t:
                t[c] = pd.to_datetime(t[c], utc=True)
        data["trades"].setdefault(coin, {})[w] = t
        s = b.set_index("timestamp")
        day = s.index.floor("D")
        dd = pd.DataFrame({"book_value": s["postRebalance_total_value"].groupby(day).last(), "close": s["close"].groupby(day).last()})
        dd["book_return"] = dd["book_value"].pct_change(); dd["coin_return"] = dd["close"].pct_change()
        data["days"].setdefault(coin, {})[w] = dd.reset_index(names="day")
ns = {}
exec(compile(open(script).read(), script, "exec"), ns)
out = ns["explore"](data)
if not isinstance(out, dict):
    raise SystemExit("explore(data) must return a dict")
parts = []
with pd.option_context("display.max_rows", cap_rows, "display.max_columns", 14, "display.width", 160):
    for k, v in out.items():
        if isinstance(v, (pd.DataFrame, pd.Series)):
            txt = v.head(cap_rows).to_string() + (f"\n... ({len(v)} rows, first {cap_rows} shown)" if len(v) > cap_rows else "")
        else:
            txt = str(v)[:600]
        parts.append(f"## {k}\n{txt}")
print("\n\n".join(parts)[:cap_chars])
'''


def header(text):
    m = re.match(r"\s*---\n(.*?)---\n", text, re.S)
    return {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)} if m else {}


def status_of(folder, rid):
    f = folder / rid / "result.json" if folder else None
    return json.loads(f.read_text())["status"] if f and f.exists() else "none"


def entry_met(entry, s5, s6):
    entry = entry or {}
    return ((not entry.get("step5_in") or s5 in entry["step5_in"]) and (s5 not in entry.get("step5_not_in", []))
            and (not entry.get("step6_in") or s6 in entry["step6_in"]))


def data_summary(record):
    """Coins, windows and rows of this record, and the bars' columns (names only, no values)."""
    import gzip
    lines, cols = [], None
    for coin in sorted(p for p in record.iterdir() if p.is_dir()):
        ws = sorted(coin.glob("w*/bars.csv.gz"), key=lambda p: int(p.parent.name[1:]))
        if not ws:
            continue
        rows = []
        for w in ws:
            with gzip.open(w, "rt") as f:
                h = f.readline().strip().split(",")
                rows.append(sum(1 for _ in f))
            cols = cols or h
        lines.append(f"{coin}: {len(ws)} windows ({', '.join(w.parent.name for w in ws)}), {sum(rows)} bars")
    keep = [c for c in (cols or []) if not re.match(r"(balances\.|postRebalance_balances\.|debug_approve|debug_execute|confidence|strategy)", c)]
    return "\n".join(lines) + "\nBars columns: " + ", ".join(keep)


def run_explore(python, record, code):
    with tempfile.TemporaryDirectory() as tmp:
        script, runner = Path(tmp) / "explore.py", Path(tmp) / "runner.py"
        script.write_text(code)
        runner.write_text(RUNNER)
        r = subprocess.run([python, "-I", str(runner), str(record), str(script), str(ROW_CAP), str(CHAR_CAP)], cwd=tmp,
                           capture_output=True, text=True, timeout=1200)
    out = r.stdout if r.returncode == 0 else "The function failed: " + (r.stderr.strip().splitlines() or ["no output"])[-1][:500]
    out = re.sub(r"(/[\w.\-]+)+/([\w.\-]+)", r"\2", out.replace(str(record), "<record>"))   # no folder names reach the model
    return DATE.sub("<date>", out.strip() or "(no output)")


def code_of(text):
    m = re.search(r"```(?:python)?\n(.*?)```", text, re.S)
    return m.group(1) if m and "def explore(" in m.group(1) else None


MONTH_YEAR = re.compile(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\b[^.\n]{0,40}\b(19|20)\d\d\b|\b(19|20)\d\d\b[^.\n]{0,10}\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\b|\bQ[1-4][ -]?(19|20)\d\d\b|\b(19|20)\d\d-(0[1-9]|1[0-2])\b")


def no_dates(text):
    if MONTH_YEAR.search(text):
        raise ValueError("a period is named by its months and year; name periods by window (w1, w2, ...) or by year only")


def parse_findings(text):
    no_dates(text)
    f = dict(re.findall(r"^F(\d+):\s*(.+)$", text, re.M))
    if not f:
        raise ValueError("no findings: write them as lines 'F1: ...', each with its numbers")
    for k, v in f.items():
        if len(v.split()) > MAX_WORDS:
            raise ValueError(f"finding F{k} is over {MAX_WORDS} words")
    return {f"F{k}": v.strip() for k, v in f.items()}


COMMON = HERE.parents[1] / "common"   # the workflow's shared definitions (measures, what an idea is)
IDEA_DEFINITION = (COMMON / "idea_definition.md").read_text()
MEASURES = (COMMON / "measures.md").read_text()


def parse_ideas(text, findings):
    no_dates(text)
    m = re.search(r"^no-ideas:\s*(.+)$", text, re.M)
    start = re.search(r"(?m)^idea:", text)
    blocks = re.split(r"(?m)^(?=idea:)", text[start.start():]) if start else []
    ideas = []
    for b in blocks:
        g = {k: v.strip() for k, v in re.findall(r"^(idea|consequence|name|from|data):\s*(.+)$", b, re.M)}
        if not g:
            continue
        for k in ("idea", "consequence", "from"):
            if not g.get(k):
                raise ValueError(f"an idea block has no '{k}' line")
            if len(g[k].split()) > MAX_WORDS:
                raise ValueError(f"an idea's '{k}' is over {MAX_WORDS} words")
        refs = re.findall(r"F\d+", g["from"])
        if not refs:
            raise ValueError("every idea names the findings it rests on, in 'from: F1, F3'")
        missing = [r for r in refs if r not in findings]
        if missing:
            raise ValueError(f"an idea rests on findings that do not exist: {', '.join(missing)}")
        g["refs"] = refs
        ideas.append(g)
    if not ideas and not m:
        raise ValueError("give the ideas, or one line 'no-ideas: <why>'")
    return ideas, (m.group(1).strip() if m and not ideas else None)


def slug(s, n=8):
    w = re.findall(r"[a-z0-9]+", s.lower())[:n]
    return "-".join(w) or "idea"


def main():
    a = argparse.ArgumentParser()
    a.add_argument("line_dir", type=Path)
    a.add_argument("record", type=Path)
    a.add_argument("--plan", type=Path, required=True)
    a.add_argument("--briefs-dir", type=Path, required=True)
    a.add_argument("--verdicts-dir", type=Path, required=True)
    a.add_argument("--checks-dir", type=Path, required=True)
    a.add_argument("--python", required=True)
    a.add_argument("--out-dir", type=Path)
    a.add_argument("--rounds", type=int, default=3)
    a.add_argument("--split", action="store_true")
    a.add_argument("--model", default="claude-opus-5-5")
    args = a.parse_args()

    line_dir, record = args.line_dir.resolve(), args.record.resolve()
    line = yaml.safe_load((line_dir / "helper" / "line.yaml").read_text())
    rid = record.name
    out_dir = (args.out_dir or line_dir / "analyses").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    index_path = out_dir / "INDEX.md"

    def index_line(text):
        lines = [l for l in (index_path.read_text().splitlines() if index_path.exists() else []) if not l.startswith(rid + ":")]
        write_atomic(index_path, "".join(l + "\n" for l in sorted(lines + [text])))

    s5, s6 = status_of(args.verdicts_dir.resolve(), rid), status_of(args.checks_dir.resolve(), rid)
    if not entry_met(line.get("entry"), s5, s6):
        index_line(f"{rid}: not run: entry condition not met (step 5: {s5}; step 6: {s6})")
        print(f"{line['id']} {rid}: not run (step 5: {s5}; step 6: {s6})")
        return

    plan_text = args.plan.read_text()
    h = header(plan_text)
    brief_file = args.briefs_dir / f"{h.get('brief', '')}.md"
    brief = brief_file.read_text() if brief_file.exists() else "(not found)"
    config = args.plan.with_name(args.plan.stem + "_config.json")
    verdict = (args.verdicts_dir / rid / "verdict.md")
    check = (args.checks_dir / rid / "check.md")
    no_paths = lambda f: "".join(l for l in f.read_text().splitlines(True) if not re.match(r"(Plan|Record|Measure|Rule):", l))
    context = (f"[THE BRIEF]\n{brief}\n[THE TEST PLAN]\n{plan_text}\n[ITS CONFIG]\n{config.read_text() if config.exists() else '(none)'}\n"
               f"[THE VERDICT ON THE IDEA (step 5)]\n{no_paths(verdict) if verdict.exists() else s5}\n"
               f"[THE CHECK OF THE BOOK (step 6)]\n{no_paths(check) if check.exists() else s6}\n"
               f"[THE DATA]\n{(HERE / 'data_description.md').read_text()}\nThis backtest holds:\n{data_summary(record)}\n")
    line_prompt = (line_dir / "helper" / "line_prompt.md").read_text()
    system = ((HERE / "common_rules.md").read_text() + "\n[HOW THE WORKFLOW MEASURES]\n" + MEASURES + "\n" + line_prompt + "\n"
              + (HERE / ("output_analyst.md" if args.split else "output_one_call.md")).read_text()
              ).replace("{{IDEA_DEFINITION}}", IDEA_DEFINITION)

    d = out_dir / rid
    (d / "exploration").mkdir(parents=True, exist_ok=True)
    cost, transcript, rounds_used, retry = 0.0, "", 0, ""
    for step in range(1, args.rounds + 1 + ATTEMPTS):
        last = rounds_used >= args.rounds
        ask = ("Give your answer now: no more exploration." if last else
               f"Round {rounds_used + 1} of at most {args.rounds}: explore, or give your answer.")
        text, c = call(args.model, system, context + transcript + "\n" + ask + retry)
        cost += c
        code = code_of(text)
        if code and not last:
            rounds_used += 1
            result = run_explore(args.python, record, code)
            write_atomic(d / "exploration" / f"round_{rounds_used}.py", code)
            write_atomic(d / "exploration" / f"round_{rounds_used}_result.txt", result + "\n")
            transcript += f"\n[EXPLORATION, ROUND {rounds_used}]\n```python\n{code}```\n[ITS RESULT]\n{result}\n"
            retry = ""
            continue
        try:
            findings = parse_findings(text)
            if args.split:
                ideas, none_why = None, None
            else:
                ideas, none_why = parse_ideas(text, findings)
            break
        except ValueError as e:
            print(f"answer refused: {e}")
            retry = f"\n\nYour previous answer was refused: {e}. Give your answer again, in the format."
    else:
        sys.exit(f"no valid answer; cost {cost:.4f} USD")

    if args.split:
        deducer_system = (HERE / "deducer.md").read_text().replace("{{IDEA_DEFINITION}}", IDEA_DEFINITION) + "\n" + line_prompt
        fl = "\n".join(f"{k}: {v}" for k, v in findings.items())
        req = context.split("[THE DATA]")[0] + f"[THE FINDINGS]\n{fl}\n\nWrite the ideas your line asks for."
        retry = ""
        for attempt in range(ATTEMPTS):
            text2, c = call(args.model, deducer_system, req + retry)
            cost += c
            try:
                ideas, none_why = parse_ideas(text2, findings)
                break
            except ValueError as e:
                print(f"deducer answer refused: {e}")
                retry = f"\n\nYour previous answer was refused: {e}. Give your answer again, in the format."
        else:
            sys.exit(f"no valid deducer answer; cost {cost:.4f} USD")

    # Save: the analysis, one file per idea, the index line.
    market = {k: h[f"data-{k}"] for k in ("instruments", "bar", "period") if h.get(f"data-{k}")}
    letter = line["id"].split(".")[1]
    (d / "ideas").mkdir(exist_ok=True)
    names = []
    for i, g in enumerate(ideas or [], 1):
        mk = dict(market)
        for k, v in re.findall(r"(instruments|bar|period)\s*:\s*([^;]+)", g.get("data", "")):
            mk[k] = v.strip()
        iid = f"{h.get('idea', rid)}.{letter}{i}_{slug(g.get('name') or g['idea'])}"
        why = "".join(f"\n- {r}: {findings[r]}" for r in g["refs"])
        body = ("---\n" + f"brief: {h.get('brief', '')}\nsource-idea: {h.get('idea', '')}\nline: {line['id']} {line['name']}\n"
                f"backtest: {rid}\n" + "".join(f"{k}: {v}\n" for k, v in mk.items()) + "---\n"
                f"Idea: {g['idea']}\nConsequence: {g['consequence']}\nWhy:{why}\n")
        write_atomic(d / "ideas" / f"{iid}.md", DATE.sub("<date>", body))
        names.append(iid)
    fl = "\n".join(f"- **{k}:** {v}" for k, v in findings.items())
    il = "\n".join(f"- `{n}` (from {', '.join(g['refs'])}): {g['idea']}" for n, g in zip(names, ideas or [])) or f"- No ideas: {none_why}"
    md = (f"---\nline: {line['id']} {line['name']}\nbacktest: {rid}\nidea tested: {h.get('idea', '')}\n"
          f"step 5: {s5}\nstep 6: {s6}\nmode: {'analyst then deducer' if args.split else 'one call'}\n"
          f"explorations: {rounds_used}\ncost: {cost:.4f} USD\n---\n## Findings\n{fl}\n\n## Ideas\n{il}\n\n"
          f"Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.\n")
    write_atomic(d / "analysis.md", DATE.sub("<date>", md))
    write_atomic(d / "result.json", DATE.sub("<date>", json.dumps({"line": line["id"], "backtest": rid, "step5": s5, "step6": s6,
                                                "split": args.split, "explorations": rounds_used, "cost": cost,
                                                "findings": findings, "ideas": [{k: v for k, v in g.items()} for g in ideas or []],
                                                "idea_ids": names, "no_ideas": none_why}, indent=2)) + "\n")
    index_line(f"{rid}: {len(names)} ideas ({rounds_used} explorations)" if names else f"{rid}: no ideas: {none_why}")
    print(f"{line['id']} {rid}: {len(findings)} findings, {len(names)} ideas, {rounds_used} explorations; cost {cost:.4f} USD")


if __name__ == "__main__":
    main()
