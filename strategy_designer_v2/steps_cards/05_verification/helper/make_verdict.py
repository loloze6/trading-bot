"""Verification helper, step 5. One closed-book model call reads a test plan and a description of its backtest record,
and writes a Python function, measure(bars), that applies the plan's criterion to the record. A small runner executes it
on the record and saves the verdict.

  python make_verdict.py path/to/PLAN.md --python path/to/venv/bin/python
Options: --records-root (default: ../../04_backtest/backtests), --verdicts-dir (default: ../verdicts next to this folder),
--model (default: the strongest).

The model sees only the system prompt and the request (the plan, the config, the record description, and the coins,
windows and columns of this record): no data, no tools, no files, an empty working folder. The runner executes the
model's function on the record, in a separate process, with the venv's Python. Saved per plan, in verdicts/<plan id>/:
verdict.md (status and evidence), measure.py (the function), result.json (what it returned). One line in INDEX.md.
"""
import argparse, gzip, json, os, re, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP3_HELPER = HERE.parents[1] / "03_test_plan" / "helper"
sys.path.insert(0, str(STEP3_HELPER))
from make_test_plan import call, write_atomic   # noqa: E402  (the same closed-book call as step 3)

ATTEMPTS = 3
STATUSES = ("confirmed", "rejected", "inconclusive", "not observable", "mismatch")

RUNNER = r'''
import glob, json, os, sys
import pandas as pd
record, script = sys.argv[1], sys.argv[2]
bars = {}
for coin in sorted(d for d in os.listdir(record) if os.path.isdir(os.path.join(record, d))):
    for w in sorted(glob.glob(os.path.join(record, coin, "w*", "bars.csv.gz")), key=lambda p: int(p.split(os.sep)[-2][1:])):
        df = pd.read_csv(w, low_memory=False)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        bars.setdefault(coin, {})[w.split(os.sep)[-2]] = df
ns = {}
exec(compile(open(script).read(), script, "exec"), ns)
out = ns["measure"](bars)
print("RESULT_JSON=" + json.dumps(out, default=float))
'''


def plan_header(text):
    m = re.match(r"\s*---\n(.*?)---\n", text, re.S)
    return {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)} if m else {}


def record_summary(record):
    """Coins, windows, rows per window and the columns of this record, for the request (no values)."""
    lines, columns = [], None
    for coin in sorted(p for p in record.iterdir() if p.is_dir()):
        ws = sorted(coin.glob("w*/bars.csv.gz"), key=lambda p: int(p.parent.name[1:]))
        rows = []
        for w in ws:
            with gzip.open(w, "rt") as f:
                header = f.readline().strip().split(",")
                rows.append(f"{w.parent.name}: {sum(1 for _ in f)} bars")
            columns = columns or header
        lines.append(f"{coin}: " + ", ".join(rows))
    usable = [c for c in (columns or []) if not re.match(r"(confidence|strategy|balances\.|postRebalance_balances\.|debug_approve|debug_execute|debug_info\.(regime_|forecast_delta|bars_in))", c)]
    return "\n".join(lines), usable


def extract_code(text):
    m = re.search(r"```(?:python)?\n(.*?)```", text, re.S)
    code = m.group(1) if m else text
    if "def measure(" not in code:
        raise ValueError("the answer has no function measure(bars)")
    return code


def check_result(out):
    """Refuse only a major deviation: not a dict, no valid status, no main measure, no case count."""
    if not isinstance(out, dict):
        raise ValueError("measure(bars) did not return a dict")
    if out.get("status") not in STATUSES:
        raise ValueError(f"status must be one of {STATUSES}, got {out.get('status')!r}")
    sc = out.get("situation_check")
    if not isinstance(sc, dict) or not isinstance(sc.get("agreement"), (int, float)) or not isinstance(sc.get("passed"), bool):
        raise ValueError("situation_check must be a dict with a numeric agreement and a true/false passed")
    if (out["status"] == "mismatch") == sc["passed"]:
        raise ValueError("the status must be mismatch exactly when the situation check has not passed")
    if out["status"] == "mismatch":
        for k in ("decided_by", "reading"):
            if not isinstance(out.get(k), str) or not out[k].strip():
                raise ValueError(f"{k} must be a sentence")
        return
    mm = out.get("main_measure")
    if not isinstance(mm, dict) or "value" not in mm:
        raise ValueError("main_measure must be a dict with a value")
    st = mm.get("statistic")
    if st is not None and not (isinstance(st, dict) and "value" in st):
        raise ValueError("main_measure.statistic must be null or a dict with a value")
    if not isinstance(out.get("counts"), dict) or not out["counts"] or not all(isinstance(v, (int, float)) for v in out["counts"].values()):
        raise ValueError("counts must be a non-empty dict of numbers, one per count the plan's minimums refer to")
    for k in ("decided_by", "reading"):
        if not isinstance(out.get(k), str) or not out[k].strip():
            raise ValueError(f"{k} must be a sentence")


def fmt(v):
    return f"{v:.6g}" if isinstance(v, float) else str(v)


def render(d, plan_id, h, out, plan_path, record):
    """verdict.md, from what the function returned."""
    chk = out.get("situation_check") or {}
    if out["status"] == "mismatch":
        lines = ["---", f"plan: {plan_id}", f"idea: {h.get('idea', '')}", f"fit: {h.get('fit', 'not given')}", "status: mismatch", "---",
                 f"Situation check: {fmt(chk.get('agreement'))} of the active bars are bars of the plan's situation on its side (90 % needed).",
                 f"- Decided by: {out['decided_by']}", f"- Reading: {out['reading']}",
                 f"Plan: `steps_cards/{os.path.relpath(plan_path, HERE.parents[1])}`",
                 f"Record: `steps_cards/{os.path.relpath(record, HERE.parents[1])}`", "Measure: `measure.py`"]
        write_atomic(d / "verdict.md", "\n".join(lines) + "\n")
        return
    mm, sc = out["main_measure"], out.get("supporting_check")
    stat = f"; {mm['statistic'].get('name', 'statistic')}: {fmt(mm['statistic'].get('value'))}" if isinstance(mm.get("statistic"), dict) else ""
    lines = ["---", f"plan: {plan_id}", f"idea: {h.get('idea', '')}", f"fit: {h.get('fit', 'not given')}", f"status: {out['status']}", "---",
             f"Situation check: {fmt(chk.get('agreement'))} of the active bars match the plan's situation and side",
             "Evidence:",
             f"- Main measure: {mm.get('name', '')}: {fmt(mm.get('value'))}{stat} (threshold: {mm.get('threshold', '')})",
             (f"- Supporting check: {sc.get('name', '')}: {fmt(sc.get('value'))}, passed: {sc.get('passed')}" if isinstance(sc, dict) else "- Supporting check: none"),
             "- Counts: " + ", ".join(f"{k}: {fmt(v)}" for k, v in out["counts"].items()),
             f"- Decided by: {out['decided_by']}",
             f"- Reading: {out['reading']}",
             f"Plan: `steps_cards/{os.path.relpath(plan_path, HERE.parents[1])}`",
             f"Record: `steps_cards/{os.path.relpath(record, HERE.parents[1])}`",
             "Measure: `measure.py`"]
    write_atomic(d / "verdict.md", "\n".join(lines) + "\n")


def main():
    a = argparse.ArgumentParser()
    a.add_argument("plan", type=Path)
    a.add_argument("--python", required=True, help="the interpreter of a venv with trading-bot/requirements.txt")
    a.add_argument("--records-root", type=Path, default=HERE.parents[1] / "04_backtest" / "backtests")
    a.add_argument("--verdicts-dir", type=Path, default=HERE.parent / "verdicts")
    a.add_argument("--model", default="claude-opus-5-5")
    args = a.parse_args()

    plan_path = args.plan.resolve()
    plan_id, plan_text = plan_path.stem, plan_path.read_text()
    h = plan_header(plan_text)
    record = args.records_root.resolve() / plan_id
    index_path = args.verdicts_dir / "INDEX.md"
    args.verdicts_dir.mkdir(parents=True, exist_ok=True)

    def index_line(line):
        lines = [l for l in (index_path.read_text().splitlines() if index_path.exists() else []) if not l.startswith(plan_id + ":")]
        write_atomic(index_path, "".join(l + "\n" for l in sorted(lines + [line])))

    if h.get("outcome", "plan") != "plan" or not list(record.glob("*/w*/bars.csv.gz")):
        why = f"the plan is {h['outcome']}" if h.get("outcome", "plan") != "plan" else "no backtest record"
        index_line(f"{plan_id}: no verdict: {why}")
        print(f"no verdict ({why}): {plan_id}")
        return

    config = (plan_path.with_name(plan_id + "_config.json")).read_text()
    windows, columns = record_summary(record)
    system = (HERE / "system_prompt.md").read_text()
    request = (f"[TEST PLAN]\n{plan_text}\n[CONFIG]\n{config}\n"
               f"[THE RECORD]\n{(HERE / 'record_description.md').read_text()}\n"
               f"This record holds:\n{windows}\nColumns: {', '.join(columns)}\n\n"
               f"Write measure(bars) for this plan.")

    cost, retry = 0.0, ""
    for attempt in range(1, ATTEMPTS + 1):
        text, c = call(args.model, system, request + retry)
        cost += c
        try:
            code = extract_code(text)
            with tempfile.TemporaryDirectory() as tmp:
                script = Path(tmp) / "measure.py"
                script.write_text(code)
                runner = Path(tmp) / "runner.py"
                runner.write_text(RUNNER)
                r = subprocess.run([args.python, "-I", str(runner), str(record), str(script)], cwd=tmp,
                                   capture_output=True, text=True, timeout=1800)
            m = re.search(r"^RESULT_JSON=(.*)$", r.stdout, re.M)
            if r.returncode or not m:
                raise ValueError("the function failed when run on the record: " + (r.stderr.strip().splitlines() or ["no output"])[-1][:400])
            out = json.loads(m.group(1))
            check_result(out)
            break
        except ValueError as e:
            print(f"attempt {attempt} refused: {e}")
            retry = f"\n\nYour previous function was refused: {e}. Write measure(bars) again."
    else:
        sys.exit(f"no valid function after {ATTEMPTS} attempts; cost {cost:.4f} USD")

    d = args.verdicts_dir / plan_id
    d.mkdir(parents=True, exist_ok=True)
    write_atomic(d / "measure.py", code)
    write_atomic(d / "result.json", json.dumps(out, indent=2) + "\n")
    render(d, plan_id, h, out, plan_path, record)
    fit = h.get("fit", "not given")
    if out["status"] == "mismatch":
        index_line(f"{plan_id}: mismatch: the test does not match its plan (agreement {fmt(out['situation_check']['agreement'])}) (fit: {fit})")
        print(f"{plan_id}: mismatch (agreement {fmt(out['situation_check']['agreement'])}); cost {cost:.4f} USD, attempts {attempt}")
        return
    mm = out["main_measure"]
    stat = f"; {mm['statistic'].get('name', 'statistic')} {fmt(mm['statistic'].get('value'))}" if isinstance(mm.get("statistic"), dict) else ""
    counts = ", ".join(f"{k} {fmt(v)}" for k, v in out["counts"].items())
    index_line(f"{plan_id}: {out['status']} (fit: {fit}) [main: {fmt(mm.get('value'))}{stat}; {counts}]")
    print(f"{plan_id}: {out['status']} (main {fmt(mm.get('value'))}{stat}; {counts}); cost {cost:.4f} USD, attempts {attempt}")


if __name__ == "__main__":
    main()
