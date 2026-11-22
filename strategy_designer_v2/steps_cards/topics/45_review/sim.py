"""B. Quick strategy families outside the bot, fold years 2018-2025, daily bars, Kraken futures costs per coin.
No lookahead: the position set at day t's close (from closes up to t) earns day t+1's return. Size: target 40 %/year
per coin from the 60-day volatility, capped at 2 (as the plans' vol_target sizing). Book: each day, the mean over the
coins that have a position defined. Measures as step 6: Sharpe, Sharpe minus holding's (equal-weight coins, unsized),
mean daily return, Calmar; plus the correlation with the long momentum book (30-day, long only)."""
import sys, math, numpy as np, pandas as pd
from data import closes, CORE, ALL, START, END, cost_bps
UNI = CORE if len(sys.argv) < 2 or sys.argv[1] == "core" else ALL
px = closes(UNI); r = px.pct_change(fill_method=None)
vol = r.rolling(60).std() * math.sqrt(365)
size = (0.40 / vol).clip(upper=2.0)
cost = pd.Series({c: cost_bps(c) / 1e4 for c in UNI})

def book(sig):
    """sig: DataFrame of desired direction/weight in [-1, 1] at day t's close. Returns the book's daily net returns."""
    pos = (sig * size).where(sig.notna())
    gross = pos.shift(1) * r
    turn = pos.fillna(0).diff().abs() * cost
    net = (gross - turn.shift(0) * 0 - turn).where(pos.shift(1).notna())   # cost charged on the day the trade is made
    net = net.loc[START:END]
    return net.mean(axis=1).dropna()

def m(x):
    x = x.dropna(); sd = x.std()
    c = (1 + x).cumprod(); fall = float((1 - c / c.cummax()).max()); yrs = len(x) / 365
    ann = c.iloc[-1] ** (1 / yrs) - 1 if c.iloc[-1] > 0 else -1
    return {"sharpe": x.mean() / sd * math.sqrt(365) if sd > 0 else 0, "mean": x.mean(), "calmar": ann / fall if fall > 0 else 9.99, "ann": ann, "fall": fall}

hold = r.loc[START:END].mean(axis=1).dropna(); H = m(hold)["sharpe"]
ret = lambda n: px / px.shift(n) - 1
ma = lambda n: px.rolling(n).mean()
S_ = {}
for n in (10, 30, 90):
    s = np.sign(ret(n)); S_[f"trend {n}d, long and short"] = s; S_[f"trend {n}d, long only"] = s.clip(lower=0); S_[f"trend {n}d, short only"] = s.clip(upper=0)
for n in (1, 3, 5):
    s = -np.sign(ret(n)); S_[f"reversal {n}d, long and short"] = s; S_[f"reversal {n}d, short only (sell rises)"] = s.clip(upper=0)
z1 = r / r.rolling(60).std()
S_["buy after a fall > 2 usual moves, hold 1 day"] = (z1 < -2).astype(float).where(z1.notna())
S_["sell after a rise > 2 usual moves, hold 1 day"] = -(z1 > 2).astype(float).where(z1.notna())
S_["200-day average: long above, short below"] = np.sign(px - ma(200))
S_["200-day average: short below only"] = np.sign(px - ma(200)).clip(upper=0)
S_["short only in a deep downtrend (below 200d and 30d < -20 %)"] = -((px < ma(200)) & (ret(30) < -0.2)).astype(float).where(ma(200).notna())
S_["holding, risk-sized (vol targeting)"] = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(vol.notna())
# cross-sectional (several coins at once: not expressible in the workflow): long the top third by 30-day
# risk-adjusted return, short the bottom third, each day; market neutral in count
score = ret(30) / (r.rolling(30).std() * math.sqrt(30))
rk = score.rank(axis=1, pct=True)
S_["ACROSS COINS: long top third, short bottom third (30d)"] = ((rk > 2 / 3).astype(float) - (rk <= 1 / 3).astype(float)).where(score.notna())
rk5 = (ret(5)).rank(axis=1, pct=True)
S_["ACROSS COINS: reversal, long 5-day losers, short winners"] = ((rk5 <= 1 / 3).astype(float) - (rk5 > 2 / 3).astype(float)).where(ret(5).notna())
B = {k: book(v) for k, v in S_.items()}
mom = B["trend 30d, long only"]
rows = []
for k, b in B.items():
    x = m(b); both = pd.concat([b, mom], axis=1).dropna()
    passes = x["sharpe"] > 0 and x["sharpe"] - H > 0 and x["mean"] >= 0.0005 and x["calmar"] > 0.75
    rows.append({"family": k, "Sharpe": x["sharpe"], "minus holding": x["sharpe"] - H, "mean %/day": 100 * x["mean"],
                 "yearly %": 100 * x["ann"], "deepest fall %": 100 * x["fall"], "Calmar": x["calmar"],
                 "corr. with long momentum": both.iloc[:, 0].corr(both.iloc[:, 1]), "step 6 (4 of 6 checks)": "pass" if passes else "fail"})
t = pd.DataFrame(rows).set_index("family")
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 60)
print(f"universe {len(UNI)} coins; holding (equal weight, unsized) Sharpe {H:.2f}\n")
print(t.round(2).to_string())
pd.to_pickle(B, f"books_{'core' if UNI is CORE else 'all'}.pkl")
