"""A. What the market data offers, per coin, fold years 2018-2025: drift, swings, persistence, reversal, asymmetry."""
import numpy as np, pandas as pd
from data import closes, CORE, ALL, START, END
px = closes(ALL); r = px.pct_change().loc[START:END]
rows = []
for c in ALL:
    x = r[c].dropna()
    if len(x) < 400: continue
    w = (1 + x).resample("W").prod() - 1; m = (1 + x).resample("ME").prod() - 1
    up = x[x.shift(1) > 2 * x.rolling(60).std().shift(1)]; dn = x[x.shift(1) < -2 * x.rolling(60).std().shift(1)]
    rows.append({"coin": c, "years": round(len(x) / 365, 1), "mean %/day": 100 * x.mean(), "vol %/day": 100 * x.std(),
                 "hold Sharpe": x.mean() / x.std() * 365 ** .5, "share up days": (x > 0).mean(),
                 "ac1 day": x.autocorr(1), "ac1 week": w.autocorr(1), "ac1 month": m.autocorr(1),
                 "next day after +2sd": 100 * up.mean(), "next day after -2sd": 100 * dn.mean(),
                 "ac |r| (vol clustering)": x.abs().autocorr(1), "skew": x.skew(),
                 "worst fall %": 100 * (1 - ((1 + x).cumprod() / (1 + x).cumprod().cummax()).min())})
t = pd.DataFrame(rows).set_index("coin")
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(t.round(3).to_string())
core = t.loc[[c for c in CORE if c in t.index]]
print("\nCORE 6 mean:"); print(core.mean().round(3).to_string())
# market regimes: share of days the equal-weight core market is above its 200-day average, and its return in each
mk = px[CORE].pct_change().mean(axis=1); lvl = (1 + mk.fillna(0)).cumprod()
above = (lvl > lvl.rolling(200).mean()).shift(1).loc[START:END]; mr = mk.loc[START:END]
print(f"\ncore market: days above its 200-day average {above.mean():.2f}; mean %/day above {100*mr[above==True].mean():+.3f}, below {100*mr[above==False].mean():+.3f}")
yr = (1 + mr).groupby(mr.index.year).prod() - 1
print("core market return by year %:", (100 * yr).round(0).to_dict())
