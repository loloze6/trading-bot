import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for H in [6, 18]:
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
                if len(b) < 60: continue
                ph = hi.shift(1).rolling(12).max(); pl = lo.shift(1).rolling(12).min()
                rng = (hi - lo) / c
                quiet = rng.rolling(360, min_periods=180).mean() / rng.rolling(42).mean()
                ts = pd.to_datetime(b["timestamp"])
                df = pd.DataFrame({"H": H, "coin": coin, "w": w, "year": ts.dt.year,
                    "up": (c > ph).astype(float), "dn": (c < pl).astype(float),
                    "quiet": quiet, "r42": c.pct_change(42), "fwd": c.shift(-H) / c - 1})
                df.loc[ph.isna(), ["up", "dn"]] = np.nan
                rows.append(df.iloc[::H])
    G = pd.concat(rows, ignore_index=True).dropna(subset=["fwd", "quiet"])
    G["u"] = G["fwd"] - G.groupby(["H", "coin"])["fwd"].transform("mean")
    G["s"] = G["u"] / G.groupby(["H", "coin"])["fwd"].transform("std")
    G["lq"] = -np.log(G["quiet"])  # busier week = larger
    out = {}
    def summ(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    g = G[G.H == 18].copy()
    g["qq"] = g.groupby("coin")["quiet"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["all_busy_q0_by_coin"] = g[g.qq == 0].groupby("coin")["u"].apply(summ).unstack()
    out["all_busy_q0_by_year"] = g[g.qq == 0].groupby("year")["u"].apply(summ).unstack()
    out["all_quiet_q4_by_coin"] = g[g.qq == 4].groupby("coin")["u"].apply(summ).unstack()
    # graded: correlation of busyness with u, per coin
    out["corr_busy_u_by_coin"] = g.groupby("coin").apply(lambda d: pd.Series({"n": len(d), "rho": stats.spearmanr(d["lq"], d["u"])[0], "p": stats.spearmanr(d["lq"], d["u"])[1]}))
    # busy week split by direction of 7-day return
    g["r42s"] = np.sign(g["r42"])
    out["busy_q0_by_r42sign"] = g[g.qq == 0].groupby("r42s")["u"].apply(summ).unstack()
    out["busy_q4_by_r42sign"] = g[g.qq == 4].groupby("r42s")["u"].apply(summ).unstack()
    # downward breakouts, busy half vs quiet half, by coin and year
    d = g[g.dn == 1].copy()
    med = d["quiet"].median(); d["busy"] = (d["quiet"] < med).astype(int)
    out["dn_busy_by_coin"] = d[d.busy == 1].groupby("coin")["u"].apply(summ).unstack()
    out["dn_busy_by_year"] = d[d.busy == 1].groupby("year")["u"].apply(summ).unstack()
    out["dn_spearman_busy_u"] = pd.Series({"rho": stats.spearmanr(d["lq"], d["u"])[0], "p": stats.spearmanr(d["lq"], d["u"])[1], "n": len(d)})
    # one-day horizon
    g6 = G[G.H == 6].copy()
    g6["qq"] = g6.groupby("coin")["quiet"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["h6_by_quiet_q"] = g6.groupby("qq")["u"].apply(summ).unstack()
    out["h6_dn_by_quiet_q"] = g6[g6.dn == 1].assign(q=lambda x: pd.qcut(x["quiet"].rank(method="first"), 4, labels=False)).groupby("q")["u"].apply(summ).unstack()
    # strength by quintile at 18
    out["s_by_quiet_q18"] = g.groupby("qq")["s"].apply(summ).unstack()
    return out
