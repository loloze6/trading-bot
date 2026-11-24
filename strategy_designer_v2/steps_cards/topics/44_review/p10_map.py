"""Topic 44, P10 pilot (the operator, 2026-11-24: "strategies exploit a market profile and a side: see which are taken and
which are not"; "a pilot, and use proven results to see if it helps").

1. The market profile, one rule fixed before any strategy is read (no result enters it): the market is the mean daily
   return of the six core coins (BTC, ETH, LTC, XMR, XRP, ZEC; those with a price that day). At each day's close:
   trend = the market's compounded return over the last 60 days: rising above +10 %, falling below -10 %, else choppy;
   volatility = the standard deviation of its last 30 daily returns against its own median so far (from at least 365
   days): agitated above, calm at or below. Six profiles. A day carries the profile known at the previous day's close.
   Why this can't leak: each label uses closes up to the day before the one it labels.
2. The map: for each candidate strategy (P1's 20, P7's 2), its days in a position by (profile, side): long when its
   coins' mean position that day is above 0, short below. Its home cells: those holding 25 % or more of its days in a
   position (at least its largest).
3. The portfolio from the map, without results: for each filled cell, the strategy most concentrated in it (the largest
   share of its days there); equal risk per profile: each filled profile 1/P of the capital, split equally among its
   filled cells. A strategy chosen for several cells adds its weights.
4. Proven results, as a check: the map's portfolio against P4's (the 20, equal capital) and against the 22 at equal
   capital, on the folds (chained as step 6) and on the two unseen periods (already seen for P4: a check, not a verdict).
Writes p10_map.csv (shares by cell), p10_portfolio.csv (weights), p10_results.csv.
  python3 topics/44_review/p10_map.py"""
import json, pathlib, sys, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
HERE = pathlib.Path(__file__).resolve().parent; STEPS = HERE.parents[1]
DATA = STEPS.parents[1] / "trading-bot" / "local_data"
SP = pathlib.Path("/tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/p10_unseen")
sys.path.insert(0, str(STEPS / "orchestration" / "ideas_similarities_check" / "helper"))
from book_returns import book_returns   # noqa: E402
from p2_weights import calmar, sharpe     # noqa: E402

COINS = ["BTC", "ETH", "LTC", "XMR", "XRP", "ZEC"]
HOME_SHARE = 0.25

# 1. the market profile
px = {}
for c in COINS:
    d = pd.read_csv(DATA / f"kraken_{c}USD_1d.csv", usecols=["timestamp", "close"])
    d["timestamp"] = pd.to_datetime(d.timestamp, format="ISO8601")
    px[c] = d.drop_duplicates("timestamp").set_index("timestamp").close
m = pd.DataFrame(px).sort_index().pct_change().mean(axis=1, skipna=True).dropna()
trend = (1 + m).rolling(60).apply(np.prod, raw=True) - 1
vol = m.rolling(30).std()
vol_med = vol.expanding(min_periods=365).median()
lab_t = np.where(trend > 0.10, "rising", np.where(trend < -0.10, "falling", "choppy"))
lab_v = np.where(vol > vol_med, "agitated", "calm")
prof = pd.Series([f"{a}, {b}" for a, b in zip(lab_t, lab_v)], index=m.index)
prof[trend.isna() | vol_med.isna()] = None
prof = prof.shift(1)                                  # a day carries the profile known at the previous close
prof.index = prof.index.normalize()
PROFILES = [f"{a}, {b}" for a in ("rising", "choppy", "falling") for b in ("calm", "agitated")]

# the candidates
c1 = pd.read_csv(HERE / "p1_candidates_earning.csv"); c1 = c1[c1.status == "candidate"][["family", "run", "id"]]
c7 = pd.read_csv(HERE / "p7_night6_candidates.csv"); c7 = c7[c7.status == "candidate"]
c7 = pd.DataFrame({"family": c7.family.str.split(":").str[0].str.replace("_run", "") + ":" + c7.family.str.split(":").str[1],
                   "run": c7.family.str.split(":").str[0], "id": c7.id})
cand = pd.concat([c1, c7], ignore_index=True)


def daily_side(rec):
    b = pd.read_csv(rec / "chart_bars.csv.gz", usecols=["coin", "window", "timestamp", "position"])
    b["day"] = pd.to_datetime(b.timestamp, format="ISO8601", utc=True).dt.tz_localize(None).dt.normalize()
    p = b.groupby("day").position.mean()
    return np.sign(p.where(p.abs() > 1e-9, 0.0))


def returns(rec):
    br = book_returns(rec, "1d")
    br["day"] = pd.to_datetime(br.period, utc=True).dt.tz_localize(None).dt.normalize() if "period" in br else None
    return br


# 2. the map
share_rows, ret_in = [], {}
for r in cand.itertuples():
    rec = STEPS / "04_backtest" / r.run / "backtests" / r.id
    side = daily_side(rec)
    lab = prof.reindex(side.index)
    x = pd.DataFrame({"side": side, "profile": lab}).dropna()
    x = x[x.side != 0]
    n = len(x)
    for (pf, sd), g in x.groupby(["profile", "side"]):
        share_rows.append({"family": r.family, "profile": pf, "side": "long" if sd > 0 else "short", "share": len(g) / n, "days": len(g)})
    br = returns(rec); ret_in[r.family] = br.set_index(["window", "period"]).book
shares = pd.DataFrame(share_rows)
shares["cell"] = shares.profile + " / " + shares.side
shares.to_csv(HERE / "p10_map.csv", index=False, float_format="%.4g")
wide = shares.pivot_table(index="family", columns="cell", values="share", fill_value=0.0)
cells = [f"{p} / {s}" for p in PROFILES for s in ("long", "short")]
wide = wide.reindex(columns=cells, fill_value=0.0)
home = wide.ge(HOME_SHARE) | wide.eq(wide.max(axis=1), axis=0)

# 3. the portfolio from the map
chosen = {}
for cell in cells:
    homed = wide.index[home[cell]]
    if len(homed):
        chosen[cell] = wide.loc[homed, cell].idxmax()
filled_profiles = sorted({c.split(" / ")[0] for c in chosen})
weights = {}
for pf in filled_profiles:
    cs = [c for c in chosen if c.startswith(pf + " / ")]
    for c in cs:
        weights[chosen[c]] = weights.get(chosen[c], 0.0) + 1 / len(filled_profiles) / len(cs)
w = pd.Series(weights); w = w / w.sum()
pd.DataFrame([{"cell": c, "strategy": chosen.get(c, "-")} for c in cells]).to_csv(HERE / "p10_portfolio.csv", index=False)

pd.set_option("display.width", 250)
print("days per profile (the six coins, 2018-2025 folds and the unseen periods together):")
print(prof.dropna().value_counts().reindex(PROFILES).to_string())
print("\nthe map: each strategy's share of its days in a position, by profile and side (percent):")
short = {c: c.replace("rising", "R").replace("choppy", "C").replace("falling", "F").replace(", calm", "c").replace(", agitated", "a").replace(" / long", "+").replace(" / short", "-") for c in cells}
print((100 * wide.rename(columns=short)).round(0).astype(int).to_string())
print("\ncells and the strategy chosen (- = empty: no strategy has it as home):")
for c in cells: print(f"  {c:28s} {chosen.get(c, '-')}")
print("\nweights:", w.round(3).to_dict())

# 4. proven results, as a check
def unseen_returns(r, period):
    for rec in (STEPS / "04_backtest" / r.run / period / "backtests" / r.id, SP / r.run / period / r.id):
        try:
            return book_returns(rec, "1d").set_index(["window", "period"]).book
        except Exception:
            continue
    return None


def evaluate(series_by_family, weights, label):
    R = pd.DataFrame(series_by_family).fillna(0.0).sort_index()
    ww = pd.Series(weights).reindex(R.columns).fillna(0.0); ww = ww / ww.sum()
    p = (R * ww).sum(axis=1).to_numpy()
    c, a, f = calmar(p)
    return {"portfolio": label, "days": len(p), "sharpe": sharpe(p), "calmar": c, "yearly_pct": 100 * a, "worst_fall_pct": 100 * f}


rows = []
fold = lambda idx: (np.asarray(idx.get_level_values(0)).astype(str).astype(object))
eq20 = {f: 1.0 for f in c1.family}; eq22 = {f: 1.0 for f in cand.family}
for label, ws in (("P4: the 20, equal capital", eq20), ("the 22, equal capital", eq22), ("the map: one per cell, equal risk per profile", dict(w))):
    allr = {k: v for k, v in ret_in.items() if k in ws}
    R = pd.DataFrame(allr).fillna(0.0).sort_index()
    wn = pd.Series(ws).reindex(R.columns).fillna(0.0); wn = wn / wn.sum()
    p = (R * wn).sum(axis=1)
    win = R.index.get_level_values(0).astype(str).str.lstrip("w").astype(int)
    for f in (1, 2, 3, 4, "all"):
        x = p.to_numpy() if f == "all" else p[((win - 1) // 6 + 1) == f].to_numpy()
        c, a, fall = calmar(x)
        rows.append({"portfolio": label, "period": f"fold {f}" if f != "all" else "folds, all", "sharpe": sharpe(x), "calmar": c,
                     "yearly_pct": 100 * a, "worst_fall_pct": 100 * fall})
    for period in ("unseen_2016_2017", "unseen_2026"):
        u = {}
        for r in cand.itertuples():
            if r.family in ws:
                s = unseen_returns(r, period)
                if s is not None: u[r.family] = s
        res = evaluate(u, {k: v for k, v in ws.items() if k in u}, label)
        res["period"] = period; res["strategies_with_data"] = f"{len(u)} of {len(ws)}"
        rows.append(res)
out = pd.DataFrame(rows); out.to_csv(HERE / "p10_results.csv", index=False, float_format="%.4g")
print("\nproven results (a check: the unseen periods are already seen for P4):")
print(out.pivot_table(index="period", columns="portfolio", values="sharpe").round(2).to_string())
print("\nCalmar:"); print(out.pivot_table(index="period", columns="portfolio", values="calmar").round(2).to_string())
print("\nworst fall %:"); print(out.pivot_table(index="period", columns="portfolio", values="worst_fall_pct").round(1).to_string())
