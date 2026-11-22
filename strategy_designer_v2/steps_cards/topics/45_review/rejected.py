"""D. The confirmed books step 6 rejected only on its size-dependent bars: how related are they to the paying books
(the similarity register, day by day), and what would they add combined with momentum?"""
import json, glob, math, os, sys, numpy as np, pandas as pd
from pathlib import Path
ST = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ST / "06_profitability/helper")); sys.path.insert(0, str(ST / "orchestration/ideas_similarities_check/helper"))
import check_profitability as cp, ideas_similarities_check as isc
SIZE = {"avg_daily_return_min", "calmar_min"}
def daily_book(rec):
    rec = Path(rec)
    if list(rec.glob("*/w*/bars.csv.gz")):
        book, *_ = cp.load(rec)
    elif (rec / "chart_bars.csv.gz").exists():
        c = pd.read_csv(rec / "chart_bars.csv.gz", usecols=["coin", "window", "timestamp", "value"]); book = {}
        for (coin, w), g in c.groupby(["coin", "window"]): book.setdefault(int(w[1:]), []).append(cp.daily(g["value"], g["timestamp"]).rename(coin))
        book = {w: pd.concat(v, axis=1, sort=True).mean(axis=1) for w, v in book.items()}
    else: return None
    s = pd.concat([book[w] for w in sorted(book)]); s.index = pd.to_datetime(s.index, utc=True); return s.groupby(level=0).last()
reg = {b["key"]: isc.series(b["key"], "1d") for b in isc.books()}
mom = reg["paying_rerun_run__022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d"]
sh = lambda x: x.mean() / x.std() * math.sqrt(365)
rows = []
for f in glob.glob(str(ST / "06_profitability/*/checks/*/result.json")):
    run, rid = f.split("/")[-4], f.split("/")[-2]
    v = ST / f"05_verification/{run}/verdicts/{rid}/result.json"
    if not v.exists() or json.loads(v.read_text()).get("status") != "confirmed": continue
    c = json.loads(open(f).read())
    if c["status"] == "profitable enough": continue
    failed = {x["measure"] for x in c["measures"] if not x["passed"]}
    if not failed or not failed <= SIZE: continue
    b = daily_book(ST / f"04_backtest/{run}/backtests/{rid}")
    if b is None: rows.append({"book": f"{run}/{rid}", "source": "none"}); continue
    best = max(((isc.compare(b, s, 24).get("share_explained") or 0, k) for k, s in reg.items()), default=(0, ""))
    x = pd.concat([mom, b], axis=1, join="inner").dropna()
    w = 1 / x.std(); w = w / w.sum(); comb = x @ w.values
    rows.append({"book": rid[:64], "run": run, "Sharpe": sh(b), "share explained by nearest paying book": best[0],
                 "corr. with momentum 022-03": x.iloc[:, 0].corr(x.iloc[:, 1]), "momentum alone": sh(x.iloc[:, 0]),
                 "momentum + it, equal risk": sh(comb), "days": len(x)})
t = pd.DataFrame(rows)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 64)
print(f"{len(t)} books; without bars or chart file: {(t.get('source') == 'none').sum() if 'source' in t else 0}")
t = t.dropna(subset=["Sharpe"]).sort_values("share explained by nearest paying book")
print(t.round(2).to_string(index=False))
t.to_csv("rejected_books.csv", index=False)
