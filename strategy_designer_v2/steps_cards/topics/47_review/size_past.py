"""Topic 47, N2 on past runs: the idea's size and how sure it is (common/idea_size.py's definition), computed from each
record's chart files (close and forecast per bar), for every book of the similarity register and every idea tested
on the unseen dates. Then: does a sure size (t > 2) say more than step 5's verdict about paying (step 6) and about
holding on the unseen dates?  python3 topics/47_review/size_past.py"""
import json, pathlib, re, sys, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
STEPS = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(STEPS / "common"))
from idea_size import day_t            # noqa: E402
from bets import bets, band_of          # noqa: E402


def size_from_chart(rec, H):
    b = pd.read_csv(rec / "chart_bars.csv.gz", usecols=["coin", "window", "timestamp", "close", "forecast"])
    band = band_of(rec); un, days = [], []
    for coin, g in b.groupby("coin"):
        frames = [w for _, w in g.groupby("window", sort=False)]
        st = [w.close.to_numpy(float) for w in frames]
        r = np.concatenate([c[H::H] / c[:len(c[H::H]) * H:H] - 1 for c in st if len(c) > H]) if st else np.array([])
        if len(r) < 3 or not r.std(ddof=1) > 0: continue
        drift = r.mean()
        for w in frames:
            c = w.close.to_numpy(float); fc = w.forecast.fillna(0).to_numpy(float); day = w.timestamp.astype(str).str[:10].to_numpy(); seen = set()
            for t in bets(fc, band):
                if t + H >= len(c) or t // H in seen: continue
                seen.add(t // H); s = 1.0 if fc[t] > 0 else -1.0
                un.append(s * (c[t + H] / c[t] - 1 - drift)); days.append(day[t])
    if len(un) < 3: return None
    return {"cases": len(un), "size": float(np.mean(un)), "size_t": day_t(un, days)}


rows = []
books = json.load(open(STEPS / "orchestration/ideas_similarities_check/register/books.json"))
items = {(b["run"], b["id"]) for b in books}
items |= {(f.parent.name, f.stem) for f in (STEPS / "orchestration/unseen_test").glob("*_run/*.json")}
for run, rid in sorted(items):
    rec = STEPS / "04_backtest" / run / "backtests" / rid; plan = STEPS / "03_test_plan" / run / "plans" / f"{rid}.md"
    v = STEPS / "05_verification" / run / "verdicts" / rid / "result.json"; c = STEPS / "06_profitability" / run / "checks" / rid / "result.json"
    if not ((rec / "chart_bars.csv.gz").exists() and plan.exists() and v.exists()): continue
    hz = re.search(r"Horizon:\s*(\d+)", plan.read_text())
    if not hz: continue
    s = size_from_chart(rec, int(hz.group(1)))
    if not s: continue
    ver = json.load(open(v)); mm = ver.get("main_measure") or {}
    st = (mm.get("statistic") or {}).get("value") if isinstance(mm.get("statistic"), dict) else None
    u = STEPS / "orchestration/unseen_test" / run / f"{rid}.json"
    uj = json.load(open(u)) if u.exists() else None
    hold = None
    if uj:
        h = [p.get("holds") for p in uj["periods"].values() if p.get("holds") is not None]
        hold = all(h) if h else None
    rows.append({"run": run, "book": rid, "bar": rid[-2:], "step5": ver.get("status"), "step5_t": st,
                 "pays": bool(c.exists() and json.load(open(c)).get("status", "").startswith("profitable")), **s,
                 "unseen_tested": uj is not None, "holds_all_unseen": hold})
d = pd.DataFrame(rows); d.to_csv(pathlib.Path(__file__).with_name("size_past.csv"), index=False, float_format="%.4g")
d["sure"] = d.size_t > 2
conf = d[d.step5 == "confirmed"]
print(f"books measured: {len(d)}; confirmed by step 5: {len(conf)}")
print(f"confirmed books whose size is sure (t > 2): {int(conf.sure.sum())} of {len(conf)}; size below 0: {int((conf['size'] < 0).sum())}")
print("\nconfirmed books, does step 6 pass?")
print(conf.groupby("sure").pays.agg(["size", "sum", "mean"]).rename(index={True: "size sure (t > 2)", False: "size not sure"}).round(2))
u = d[d.unseen_tested & d.holds_all_unseen.notna()]
print(f"\nideas tested on the unseen dates: {len(u)}")
print(u.groupby(u.size_t > 2).holds_all_unseen.agg(["size", "sum", "mean"]).rename(index={True: "size sure (t > 2)", False: "size not sure"}).round(2))
u2 = u.dropna(subset=["step5_t"])
print("\npredicting 'holds on every unseen period' (share of pairs ordered right, 0.5 = no information):")
from scipy.stats import mannwhitneyu
for col in ("size_t", "size", "step5_t"):
    x = u2[[col, "holds_all_unseen"]].dropna()
    a, b = x[x.holds_all_unseen][col], x[~x.holds_all_unseen.astype(bool)][col]
    if len(a) and len(b):
        auc = mannwhitneyu(a, b).statistic / (len(a) * len(b))
        print(f"  {col:8s}: {auc:.2f} (holds {len(a)}, does not {len(b)})")
print("\ncorrelation over confirmed books: size_t with step 5's statistic:", round(conf[["size_t", "step5_t"]].dropna().corr().iloc[0, 1], 2))
