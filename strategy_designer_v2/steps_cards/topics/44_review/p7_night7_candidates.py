"""Topic 44, P7 for night 7 (runs/NIGHT7_RUN.md): every confirmed book of the 8 runs (4 new code, 4 control) as a portfolio
candidate by P1's rule, as p7_night6_candidates.py does for night 6, and the comparison at equal spend.
Each run is read from its own branch (`origin/night7-<name>`, `origin/night7c-<name>`), so the control runs need not be
merged. P1's rule: a confirmed book with a size above 0 (step 5's size.json) and step 6's Sharpe above 0; one book per
family (the run and its brief idea), the closest to the idea; it enters if its daily returns (the register's returns
chart file, as P7 night 6) correlate under 0.5 in size with each of the portfolio's 20 books and each book already in.
The equal-spend cut (fixed before the runs): a new-code run counts only the ideas whose turn began before 25 USD
(`loop.jsonl`, `spent_before`).
  python3 topics/44_review/p7_night7_candidates.py"""
import io, json, pathlib, subprocess, sys, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
HERE = pathlib.Path(__file__).resolve().parent; STEPS = HERE.parents[1]; REPO = STEPS.parents[1]
sys.path.insert(0, str(STEPS / "common")); sys.path.insert(0, str(HERE.parent / "47_review"))
from lib import idea_code                  # noqa: E402
import streaks as st                       # noqa: E402

SC = "strategy_designer_v2/steps_cards"
NAMES = ("rangefail", "chopreversal", "steadydecline", "panic")
CUT = 25.0


def show(ref, path, binary=False):
    p = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=REPO, capture_output=True)
    return p.stdout if binary else p.stdout.decode()


def returns(ref, run, bid):
    """The book's daily returns as P7 night 6 reads them (`47_review/streaks.per_coin` on the committed chart file, the
    mean over coins), from the run's branch."""
    import tempfile
    raw = show(ref, f"{SC}/04_backtest/{run}/backtests/{bid}/chart_bars.csv.gz", binary=True)
    if not raw:
        return None
    with tempfile.TemporaryDirectory() as d:
        (pathlib.Path(d) / "chart_bars.csv.gz").write_bytes(raw)
        ret, _ = st.per_coin(pathlib.Path(d))
    return ret.mean(axis=1).fillna(0.0)


def measure(ref, run, bid, name, key):
    txt = show(ref, f"{SC}/{name}/{run}/{'checks' if 'profit' in name else 'verdicts'}/{bid}/{key}")
    return json.loads(txt) if txt.strip() else {}


port = pd.read_csv(HERE / "p1_returns_earning.csv.gz", index_col=["w", "day"], parse_dates=["day"])
base = {c.split("_")[0]: port[c] for c in port.columns}

rows, summary = [], []
for control in (False, True):
    for n in NAMES:
        run, ref = f"night7{'c' if control else ''}_{n}_run", f"origin/night7{'c' if control else ''}-{n}"
        loop = [json.loads(l) for l in show(ref, f"{SC}/orchestration/loop/{run}/loop.jsonl").splitlines() if l.strip()]
        in_cut = {t["idea"] for t in loop if "turn" in t and (control or t.get("spent_before", 0) < CUT)}
        table = json.loads(show(ref, f"{SC}/orchestration/run_idea/{run}/table.json") or "[]")
        books = [b for b in json.loads(show(ref, f"{SC}/orchestration/ideas_similarities_check/register/books.json") or "[]")
                 if b.get("run") == run]
        series = dict(base)
        cands = 0
        reps = {}
        for b in books:
            bid = b["id"]
            code = idea_code(bid.rsplit("_", 1)[0]) if bid.endswith(("_1d", "_1h", "_4h")) else idea_code(bid)
            if code.split("_")[0] not in {idea_code(i) for i in in_cut}:
                continue
            chk = measure(ref, run, bid, "06_profitability", "result.json")
            sharpe = next((m["value"] for m in chk.get("measures", []) if m["measure"] == "sharpe_min"), np.nan)
            size = measure(ref, run, bid, "05_verification", "size.json").get("unusual_move", np.nan)
            if not (sharpe > 0 and size > 0):
                continue
            fam = code.split(".")[0]
            gen = code.count(".")
            if fam not in reps or gen < reps[fam][0]:
                reps[fam] = (gen, bid, sharpe)
        for fam, (gen, bid, sharpe) in sorted(reps.items()):
            s = returns(ref, run, bid)
            if s is None:
                rows.append({"run": run, "family": fam, "id": bid, "status": "no returns file"}); continue
            cors = {k: abs(pd.concat([s, v], axis=1, join="inner").corr().iloc[0, 1]) for k, v in series.items()}
            worst = max(cors, key=cors.get)
            ok = cors[worst] < 0.5
            cands += ok
            rows.append({"run": run, "family": fam, "id": bid, "generation": gen, "sharpe": sharpe,
                         "largest_correlation": round(cors[worst], 3), "with": worst, "status": "candidate" if ok else "related"})
            if ok:
                series[f"{run}:{fam}"] = s
        tested = [r for r in table if r["idea"] in in_cut]
        summary.append({"run": run, "tested": len(tested),
                        "confirmed": sum(str(r.get("step5", "")).startswith("confirmed") for r in tested),
                        "profitable": sum(str(r.get("step6", "")).startswith("profitable") for r in tested),
                        "from the brief (032)": sum(r["idea"].startswith("032-") for r in tested),
                        "families admitted": len(reps), "candidates": cands,
                        "spent": round(sum(r.get("cost", 0.0) for r in tested), 2)})
out = pd.DataFrame(rows); out.to_csv(HERE / "p7_night7_candidates.csv", index=False, float_format="%.4g")
pd.set_option("display.width", 220)
print(pd.DataFrame(summary).to_string(index=False))
print()
print(out.drop(columns=["id"]).to_string(index=False))
