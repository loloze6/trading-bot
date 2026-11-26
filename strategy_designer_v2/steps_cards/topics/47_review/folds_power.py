"""Topic 31 (the operator, 2026-11-24: "reconfirm the fold reduction's impact, with folds between 8 and 2 years").
For every step-5-confirmed book of the similarity register (its in-sample record's chart files), the idea's size per case
(common/idea_size.py's definition, as size_past.py: the move beyond the coin's drift at the plan's horizon, per bet) and
its t with cases clustered by day, on all four folds (8 years) and on every subset of 3, 2 and 1 folds (6, 4, 2 years;
a fold = 6 windows, 2 years). Per number of folds: the share of books with t >= 2 (the verdict's bar), the median t, and
the share of the books sure on 8 years that stay sure. Writes folds_power.csv.
  python3 topics/47_review/folds_power.py"""
import itertools, json, pathlib, re, sys, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
HERE = pathlib.Path(__file__).resolve().parent; STEPS = HERE.parents[1]
sys.path.insert(0, str(STEPS / "common"))
from idea_size import day_t            # noqa: E402
from bets import bets, band_of          # noqa: E402


def cases(rec, H):
    b = pd.read_csv(rec / "chart_bars.csv.gz", usecols=["coin", "window", "timestamp", "close", "forecast"])
    band = band_of(rec); out = []
    for coin, g in b.groupby("coin"):
        frames = [(w, x) for w, x in g.groupby("window", sort=False)]
        st = [x.close.to_numpy(float) for _, x in frames]
        r = np.concatenate([c[H::H] / c[:len(c[H::H]) * H:H] - 1 for c in st if len(c) > H]) if st else np.array([])
        if len(r) < 3 or not r.std(ddof=1) > 0: continue
        drift = r.mean()
        for w, x in frames:
            fold = (int(str(w)[1:]) - 1) // 6 + 1
            c = x.close.to_numpy(float); fc = x.forecast.fillna(0).to_numpy(float); day = x.timestamp.astype(str).str[:10].to_numpy(); seen = set()
            for t in bets(fc, band):
                if t + H >= len(c) or t // H in seen: continue
                seen.add(t // H); s = 1.0 if fc[t] > 0 else -1.0
                out.append((s * (c[t + H] / c[t] - 1 - drift), day[t], fold))
    return out


books = json.load(open(STEPS / "orchestration/ideas_similarities_check/register/books.json"))
rows = []
for bk in books:
    run, rid = bk["run"], bk["id"]
    rec = STEPS / "04_backtest" / run / "backtests" / rid; plan = STEPS / "03_test_plan" / run / "plans" / f"{rid}.md"
    v = STEPS / "05_verification" / run / "verdicts" / rid / "result.json"
    if not ((rec / "chart_bars.csv.gz").exists() and plan.exists() and v.exists()): continue
    if json.load(open(v)).get("status") != "confirmed": continue
    hz = re.search(r"Horizon:\s*(\d+)", plan.read_text())
    if not hz: continue
    cs = cases(rec, int(hz.group(1)))
    if len(cs) < 3: continue
    u = np.array([c[0] for c in cs]); dy = np.array([c[1] for c in cs]); fo = np.array([c[2] for c in cs])
    for k in (4, 3, 2, 1):
        for sub in itertools.combinations((1, 2, 3, 4), k):
            m = np.isin(fo, sub)
            t = day_t(u[m], dy[m]) if m.sum() >= 3 else None
            rows.append({"run": run, "book": rid, "bar": rid[-2:], "folds": k, "subset": "".join(map(str, sub)),
                         "cases": int(m.sum()), "t": t})
d = pd.DataFrame(rows); d.to_csv(HERE / "folds_power.csv", index=False, float_format="%.4g")
full = d[d.folds == 4].set_index(["run", "book"]).t
d["sure_on_8_years"] = [full.get((r, b), np.nan) >= 2 for r, b in zip(d.run, d.book)]
print(f"confirmed books measured: {d[d.folds == 4].shape[0]}; sure on 8 years (t >= 2): {int((full >= 2).sum())}")
pd.set_option("display.width", 200)
for bar in ("all", "1d", "1h"):
    x = d if bar == "all" else d[d.bar == bar]
    if x.empty: continue
    t = x.groupby("folds").agg(years=("folds", lambda f: 2 * f.iloc[0]), books=("book", lambda b: b.nunique()),
                               median_cases=("cases", "median"), median_t=("t", "median"),
                               share_t_ge_2=("t", lambda s: (s >= 2).mean()))
    keep = x[x.sure_on_8_years].groupby("folds").t.apply(lambda s: (s >= 2).mean())
    t["of_the_sure_on_8_years_stay_sure"] = keep
    print(f"\n{bar} (every subset of folds counted; a book counts once per subset):")
    print(t.sort_index(ascending=False).round(2).to_string())
