"""Topic 44, P1 (the operator's option A, 2026-11-23): the portfolio's candidates, chosen without looking at any
result. From the similarity register's books (all step 5 confirmed) with a size above 0 (topic 47, size_past.csv):
  1. one book per family (the brief's idea it descends from): the one closest to that idea (fewest generations; then
     the earliest made);
  2. families in a fixed order (brief number, then idea number); a family's book enters if the correlation of its daily
     returns with every book already in is below 0.5 in size (one explains under a quarter of the other).
Not applied: the book's fidelity to its idea (topic 47 N3 holds from 2026-11-23; every book here was built before).
Variant --earning (2026-11-23, after the first P2 run: four hourly candidates lose 0.2 to 1.2 % a day after costs):
  before step 1, keep only the books that earn on their own in sample (step 6's Sharpe above 0; no bar on how much).
Writes p1_candidates[_earning].csv and the candidates' daily returns (p1_returns[_earning].csv.gz: index window, day).
  python3 topics/44_review/p1_candidates.py [--earning]"""
import json, pathlib, sys, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
HERE = pathlib.Path(__file__).resolve().parent; STEPS = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "47_review")); sys.path.insert(0, str(STEPS / "common"))
import streaks as st                      # noqa: E402  (per-coin daily returns in step 6's chain)
from lib import idea_code                  # noqa: E402

books = pd.DataFrame(json.load(open(STEPS / "orchestration/ideas_similarities_check/register/books.json")))
size = pd.read_csv(HERE.parent / "47_review" / "size_past.csv")[["run", "book", "size", "size_t"]].rename(columns={"book": "id"})
b = books.merge(size, on=["run", "id"], how="inner")
b = b[b["size"] > 0].copy()
EARNING = "--earning" in sys.argv; TAG = "_earning" if EARNING else ""


def step6_sharpe(run, bid):
    f = STEPS / "06_profitability" / run / "checks" / bid / "result.json"
    if not f.exists(): return np.nan
    return next((m["value"] for m in json.load(open(f))["measures"] if m["measure"] == "sharpe_min"), np.nan)


b["sharpe"] = [step6_sharpe(r, i) for r, i in zip(b.run, b.id)]
if EARNING:
    print(f"with a size above 0: {len(b)}; step 6's Sharpe above 0: {int((b.sharpe > 0).sum())}; no step 6 record: {int(b.sharpe.isna().sum())}")
    b = b[b.sharpe > 0].copy()
b["code"] = b.id.str.replace(r"_(1h|4h|1d)$", "", regex=True).map(idea_code)
b["family"] = b.code.str.split(".").str[0]; b["generation"] = b.code.str.count(r"\.")
reps = b.sort_values(["family", "generation", "made_utc"]).groupby("family").head(1).sort_values("family")
print(f"register books {len(books)}; with a size above 0 {len(b)}; families {len(reps)}")
series, chosen, rows = {}, [], []
for r in reps.itertuples():
    rec = STEPS / "04_backtest" / r.run / "backtests" / r.id
    try:
        ret, _ = st.per_coin(rec)
    except Exception as e:
        rows.append({"family": r.family, "run": r.run, "id": r.id, "status": f"no daily returns: {e}"}); continue
    s = ret.mean(axis=1).fillna(0.0)
    worst = max((abs(pd.concat([s, series[k]], axis=1, join="inner").corr().iloc[0, 1]) for k in chosen), default=0.0)
    ok = worst < 0.5
    rows.append({"family": r.family, "run": r.run, "id": r.id, "bar": r.bar, "kind": r.kind, "generation": r.generation,
                 "size_pct": 100 * r.size, "size_t": r.size_t, "step6_sharpe": r.sharpe, "largest_correlation_with_those_in": worst,
                 "status": "candidate" if ok else "related to a candidate"})
    if ok:
        series[r.id] = s; chosen.append(r.id)
out = pd.DataFrame(rows); out.to_csv(HERE / f"p1_candidates{TAG}.csv", index=False, float_format="%.4g")
pd.DataFrame(series).to_csv(HERE / f"p1_returns{TAG}.csv.gz", float_format="%.6g")
print(out.status.value_counts().to_dict())
c = out[out.status == "candidate"]
print(c[["family", "bar", "kind", "generation", "size_pct", "size_t", "step6_sharpe", "largest_correlation_with_those_in"]].round(3).to_string(index=False))
