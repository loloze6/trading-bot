"""Rerun existing plans with the holding period (topic 30; runs/HOLDING_NIGHT_RUN.md): each plan unchanged except
strategies.min_holding_bars = its own horizon (the line "Horizon: N bars"), through step 4, step 5 with the idea's saved
measure (--measure; without one, step 5 as usual), step 6, and the unseen-dates test for a confirmed and profitable idea.

  python3 hold_rerun.py LIST --run OUT_run --python VENV_PYTHON [--standardise WINDOW MIN_PERIODS]

--standardise (topic 36's pilot): every standardise op of the config gets this window and min_periods (in bars), so
the forecast is scaled on the same span of time as on daily bars.

LIST: one line per plan, "ROOT|RUN|PLAN_ID" (ROOT: a steps_cards folder holding RUN's plans and verdicts). A step whose
output exists is skipped, so a cut run resumes. One line per plan on stdout: its result.
"""
import argparse, json, re, shutil, subprocess, sys
from pathlib import Path

STEPS = Path(__file__).resolve().parents[2]


def call(cmd):
    r = subprocess.run([sys.executable] + [str(c) for c in cmd], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def main():
    a = argparse.ArgumentParser()
    a.add_argument("list", type=Path)
    a.add_argument("--run", required=True)
    a.add_argument("--python", required=True)
    a.add_argument("--standardise", nargs=2, type=int, metavar=("WINDOW", "MIN_PERIODS"))
    args = a.parse_args()
    plans = STEPS / "03_test_plan" / args.run / "plans"
    bt, vd, ck = (STEPS / "04_backtest" / args.run / "backtests", STEPS / "05_verification" / args.run / "verdicts",
                  STEPS / "06_profitability" / args.run / "checks")
    plans.mkdir(parents=True, exist_ok=True)
    for line in args.list.read_text().split("\n"):
        if not line.strip():
            continue
        root, run, pid = line.strip().split("|")
        src = Path(root) / "03_test_plan" / run / "plans"
        plan = plans / f"{pid}.md"
        text = (src / f"{pid}.md").read_text()
        m = re.search(r"Horizon:\s*(\d+)", text)
        if not m:
            print(json.dumps({"plan": pid, "error": "no horizon line"}), flush=True)
            continue
        if not plan.exists():
            shutil.copy(src / f"{pid}.md", plan)
            cfg = json.loads((src / f"{pid}_config.json").read_text())
            cfg["strategies"]["min_holding_bars"] = int(m.group(1))
            if args.standardise:
                def walk(x):
                    if isinstance(x, dict):
                        if x.get("op") == "standardise":
                            x.setdefault("params", {}).update(window=args.standardise[0], min_periods=args.standardise[1])
                        for v in x.values(): walk(v)
                    elif isinstance(x, list):
                        for v in x: walk(v)
                walk(cfg)
            (plans / f"{pid}_config.json").write_text(json.dumps(cfg, indent=2) + "\n")
        if not (bt / pid / "run.md").exists():
            if (bt / pid).exists():
                shutil.rmtree(bt / pid)                    # a backtest cut short: started again
            call([STEPS / "04_backtest/helper/run_backtest.py", plan, "--python", args.python, "--out-root", bt])
        measure = Path(root) / "05_verification" / run / "verdicts" / pid / "measure.py"
        if (bt / pid / "run.md").exists() and not (vd / pid / "result.json").exists():
            cmd = [STEPS / "05_verification/helper/make_verdict.py", plan, "--python", args.python, "--records-root", bt,
                   "--verdicts-dir", vd]
            call(cmd + (["--measure", measure] if measure.exists() else []))
        if (bt / pid / "run.md").exists() and not (ck / pid / "result.json").exists():
            call([STEPS / "06_profitability/helper/check_profitability.py", bt / pid, "--checks-dir", ck])
        v = json.loads((vd / pid / "result.json").read_text()) if (vd / pid / "result.json").exists() else {}
        c = json.loads((ck / pid / "result.json").read_text()) if (ck / pid / "result.json").exists() else {}
        unseen = None
        if v.get("status") == "confirmed" and c.get("status") == "profitable enough":
            out = STEPS / "orchestration" / "unseen_test" / args.run / f"{pid}.json"
            if not out.exists():
                call([STEPS / "orchestration/unseen_test/helper/unseen_test.py", plan, "--run", args.run, "--python", args.python])
            unseen = json.loads(out.read_text())["periods"] if out.exists() else "failed"
        sh = {x["measure"]: round(x["value"], 3) for x in c.get("measures", [])}
        print(json.dumps({"plan": pid, "from": run, "hold": int(m.group(1)), "step5": v.get("status"),
                          "step6": c.get("status"), "sharpe": sh.get("sharpe_min"), "vs_hold": sh.get("sharpe_vs_hold_min"),
                          "calmar": sh.get("calmar_min"), "measure": "saved" if measure.exists() else "new",
                          "unseen": unseen}), flush=True)


if __name__ == "__main__":
    main()
