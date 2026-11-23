"""C. Diagnostics: costs, years, combination, step 6's mean-per-day bar, how much the coins move together."""
import math, numpy as np, pandas as pd
import sim
from sim import m, B, r, px, size, cost, START, END, H
sh = lambda x: x.mean() / x.std() * math.sqrt(365)
def gross(sig):
    pos = (sig * size).where(sig.notna()); g = (pos.shift(1) * r).where(pos.shift(1).notna()).loc[START:END]
    return g.mean(axis=1).dropna()
print("1. Costs: Sharpe before and after costs")
for k in ["reversal 1d, long and short", "buy after a fall > 2 usual moves, hold 1 day", "trend 10d, long only", "trend 30d, long only",
          "ACROSS COINS: long top third, short bottom third (30d)", "trend 30d, short only"]:
    print(f"   {k:60s} before {sh(gross(sim.S_[k])):5.2f}  after {sh(B[k]):5.2f}")
print("\n2. By year: Sharpe of the market (held), the long momentum book and three short books")
cols = {"market held": sim.hold, "trend 30d long only": B["trend 30d, long only"], "trend 30d short only": B["trend 30d, short only"],
        "200d short below only": B["200-day average: short below only"], "sell after a rise > 2 sd": B["sell after a rise > 2 usual moves, hold 1 day"],
        "buy after a fall > 2 sd": B["buy after a fall > 2 usual moves, hold 1 day"]}
t = pd.DataFrame({k: v.groupby(v.index.year).apply(sh) for k, v in cols.items()})
print(t.round(2).to_string())
print("\n3. Combining with the long momentum book (equal risk, weights from the whole period's swings)")
mom = B["trend 30d, long only"]
for k in ["buy after a fall > 2 usual moves, hold 1 day", "ACROSS COINS: long top third, short bottom third (30d)", "trend 30d, short only",
          "reversal 1d, long and short"]:
    x = pd.concat([mom, B[k]], axis=1).dropna(); w = 1 / x.std(); w = w / w.sum(); c = x @ w.values
    print(f"   momentum + {k:58s} corr {x.corr().iloc[0,1]:+.2f}  Sharpe alone {sh(x.iloc[:,0]):.2f} / {sh(x.iloc[:,1]):.2f}  together {sh(c):.2f}  (weights {w.iloc[0]:.2f}/{w.iloc[1]:.2f})")
print("\n4. Step 6's mean daily return bar (0.05 % a day, counted over every calendar day) against a rarely active book")
dip = sim.S_["buy after a fall > 2 usual moves, hold 1 day"]; active = (dip.loc[START:END] > 0).any(axis=1).mean()
b = B["buy after a fall > 2 usual moves, hold 1 day"]
print(f"   dip buying: in a position on {100*active:.0f} % of days; mean per calendar day {100*b.mean():.3f} %, Sharpe {sh(b):.2f}")
print(f"   to reach 0.05 % a day at this Sharpe it would need its swings x {0.0005/b.mean():.1f} (more size), Sharpe unchanged")
print("\n5. How much the coins move together (average correlation of daily returns between two coins)")
rr = r.loc[START:END]; c = rr.corr().values; n = len(c)
print(f"   {(c.sum() - n) / (n * (n - 1)):.2f} over {n} coins; share of a coin's daily moves the market explains (r squared): {np.nanmean([rr[k].corr(rr.mean(axis=1))**2 for k in rr.columns]):.2f}")
