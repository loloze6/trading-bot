"""Topic 44, P7: night 6's books as portfolio candidates, by P1's rule (the operator's decision of 2026-11-23), against the
fixed portfolio (p1_candidates_earning.csv, its 20 books). From the register's night-6 books (all step 5 confirmed):
  1. size above 0 (step 5's size.json, `unusual_move`: the same measure as P1's size) and earning on its own in sample
     (step 6's Sharpe above 0);
  2. one book per family, the one closest to the idea (fewest generations, then the earliest made). The family is the
     brief and its idea number: tonight's four briefs all carry the number 031 (each branch numbered from the briefs it
     had), so the brief's name is part of the family here (topic NEXT_STEPS 3e);
  3. families in a fixed order (run name, then idea number); a family's book enters if its daily returns correlate
     under 0.5 in size with every book of the fixed portfolio and every night-6 book already in.
Reports each family's representative, its largest correlation and with which book, and whether it enters.
  python3 topics/44_review/p7_night6_candidates.py"""
import json, pathlib, sys, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
HERE = pathlib.Path(__file__).resolve().parent; STEPS = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "47_review")); sys.path.insert(0, str(STEPS / "common"))
import streaks as st                      # noqa: E402
from lib import idea_code                  # noqa: E402

books = pd.DataFrame(json.load(open(STEPS / "orchestration/ideas_similarities_check/register/books.json")))
n6 = books[books.run.str.startswith("night6_")].copy()


def step6_sharpe(run, bid):
    f = STEPS / "06_profitability" / run / "checks" / bid / "result.json"
    return next((m["value"] for m in json.load(open(f))["measures"] if m["measure"] == "sharpe_min"), np.nan) if f.exists() else np.nan


def size_of(run, bid):
    f = STEPS / "05_verification" / run / "verdicts" / bid / "size.json"
    if not f.exists(): return np.nan, np.nan
    d = json.load(open(f)); return d.get("unusual_move", np.nan), d.get("unusual_move_t", np.nan)


n6["sharpe"] = [step6_sharpe(r, i) for r, i in zip(n6.run, n6.id)]
n6[["size", "size_t"]] = [size_of(r, i) for r, i in zip(n6.run, n6.id)]
n6["code"] = n6.id.str.replace(r"_(1h|4h|1d)$", "", regex=True).map(idea_code)
n6["family"] = n6.run + ":" + n6.code.str.split(".").str[0]
n6["generation"] = n6.code.str.count(r"\.")
print(f"night-6 books in the register: {len(n6)}; size above 0: {int((n6['size'] > 0).sum())}; "
      f"step 6's Sharpe above 0: {int((n6.sharpe > 0).sum())}; both: {int(((n6['size'] > 0) & (n6.sharpe > 0)).sum())}")
adm = n6[(n6["size"] > 0) & (n6.sharpe > 0)]
reps = adm.sort_values(["family", "generation", "made_utc"]).groupby("family").head(1).sort_values("family")
print(f"families admitted: {len(reps)} (of {n6.family.nunique()} with a confirmed book)")

port = pd.read_csv(HERE / "p1_returns_earning.csv.gz", index_col=["w", "day"], parse_dates=["day"])
port.columns = [c.split("_")[0] for c in port.columns]
series = {c: port[c] for c in port.columns}
rows = []
for r in reps.itertuples():
    ret, _ = st.per_coin(STEPS / "04_backtest" / r.run / "backtests" / r.id)
    s = ret.mean(axis=1).fillna(0.0)
    cors = {k: abs(pd.concat([s, v], axis=1, join="inner").corr().iloc[0, 1]) for k, v in series.items()}
    worst = max(cors, key=cors.get)
    ok = cors[worst] < 0.5
    rows.append({"family": r.family, "id": r.id, "kind": r.kind, "generation": r.generation, "sharpe": r.sharpe,
                 "size_pct": 100 * r.size, "size_t": r.size_t, "largest_correlation": cors[worst], "with": worst,
                 "status": "candidate" if ok else "related"})
    if ok:
        series[r.family + ":" + r.id.split("_")[0]] = s
out = pd.DataFrame(rows); out.to_csv(HERE / "p7_night6_candidates.csv", index=False, float_format="%.4g")
pd.set_option("display.width", 220)
print(out.drop(columns=["id"]).round(3).to_string(index=False))
print(out.status.value_counts().to_dict())
