"""Topic 47, 1h (the operator, 2026-11-24: "why do ideas drift?"). For every book of the similarity register (all step 5
confirmed), its closeness to the effects already held: the largest correlation of its daily returns with the 20 books of
the fixed portfolio (topics/44_review/p1_returns_earning.csv.gz), the books of its own family (the same brief idea) left
out; and which held effect is nearest: trend continuation (002-03 price far above its 200-day average, 003-02 heavy-volume
up days continue, 006-04 a volume surge before a rise, 013-03 near the 30-day high) or the next-day rebound after a fall
(011-01 sharp selloffs bounce, 005-02 a volatile day's move reverses, 025-03 bounces in a falling market). Read by
generation and by step 7's line. Writes drift.csv.  python3 topics/47_review/drift.py"""
import json, pathlib, re, sys, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
HERE = pathlib.Path(__file__).resolve().parent; STEPS = HERE.parents[1]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(STEPS / "common"))
import streaks as st                      # noqa: E402
from lib import idea_code                  # noqa: E402

SEG = re.compile(r"\.([a-g])(\d+)(?=[._]|$)")
TREND = {"002-03", "003-02", "006-04", "013-03"}; REBOUND = {"011-01", "005-02", "025-03"}
port = pd.read_csv(HERE.parent / "44_review" / "p1_returns_earning.csv.gz", index_col=["w", "day"], parse_dates=["day"])
port.columns = [c.split("_")[0] for c in port.columns]
books = pd.DataFrame(json.load(open(STEPS / "orchestration/ideas_similarities_check/register/books.json")))
rows = []
for b in books.itertuples():
    rec = STEPS / "04_backtest" / b.run / "backtests" / b.id
    try:
        ret, _ = st.per_coin(rec)
    except Exception:
        continue
    s = ret.mean(axis=1).fillna(0.0)
    code = idea_code(re.sub(r"_(1h|4h|1d)$", "", b.id)); fam = code.split(".")[0]
    segs = SEG.findall(code)
    cors = {k: abs(pd.concat([s, port[k]], axis=1, join="inner").corr().iloc[0, 1]) for k in port.columns
            if k != fam and not b.run.startswith("night6_") or (b.run.startswith("night6_") and True)}
    if not b.run.startswith("night6_"):
        cors.pop(fam, None)                     # its own family is not "already held" for itself
    near = max(cors, key=lambda k: -1 if np.isnan(cors[k]) else cors[k])
    rows.append({"run": b.run, "id": b.id, "bar": b.bar, "kind": b.kind, "generation": len(segs),
                 "line": segs[-1][0] if segs else "-", "nearest_held": near, "corr": cors[near],
                 "nearest_effect": "trend" if near in TREND else "rebound" if near in REBOUND else "other"})
d = pd.DataFrame(rows); d.to_csv(HERE / "drift.csv", index=False, float_format="%.4g")
d["gen"] = d.generation.clip(upper=4).astype(str).replace({"4": "4+"})
pd.set_option("display.width", 200)
print(f"register books measured: {len(d)} of {len(books)}")
agg = dict(n=("corr", "size"), median_corr=("corr", "median"), related=("corr", lambda c: (c >= 0.5).mean()),
           trend=("nearest_effect", lambda e: (e == "trend").mean()), rebound=("nearest_effect", lambda e: (e == "rebound").mean()))
print("\nby generation (closeness to the effects already held; related = correlation 0.5 or more):")
print(d.groupby("gen").agg(**agg).round(2).to_string())
print("\nby step 7's line (follow-ups):")
print(d[d.generation > 0].groupby("line").agg(**agg).round(2).to_string())
print("\nnight 6 alone, by generation:")
print(d[d.run.str.startswith("night6_")].groupby("gen").agg(**agg).round(2).to_string())
