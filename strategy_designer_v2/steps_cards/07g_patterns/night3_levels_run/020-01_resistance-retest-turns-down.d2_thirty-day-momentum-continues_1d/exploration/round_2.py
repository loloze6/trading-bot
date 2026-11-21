def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    H = 5
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            if n < 40: continue
            s = pd.Series(c)
            lr = np.log(s).diff()
            r30 = s.pct_change(30)
            vol20 = lr.rolling(20).std()
            def pos(L):
                hi = s.rolling(L, min_periods=L).max(); lo = s.rolling(L, min_periods=L).min()
                return (s - lo) / (hi - lo)
            p20, p30, p60 = pos(20), pos(30), pos(60)
            dist30 = s / s.rolling(30).max() - 1
            f = b["forecast"].astype(float)
            al = b["postRebalance_current_allocation"].astype(float)
            wn = int(w[1:])
            for t in range(0, n - H, H):
                rows.append(dict(coin=coin, wn=wn, f=f.iloc[t], al=al.iloc[t], r30=r30.iloc[t],
                    vol=vol20.iloc[t], p20=p20.iloc[t], p30=p30.iloc[t], p60=p60.iloc[t], d30=dist30.iloc[t],
                    fwd=c[t+H]/c[t]-1, fwd10=(c[t+10]/c[t]-1) if t+10 < n else np.nan))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    df["ex10"] = df["fwd10"] - df.groupby("coin")["fwd10"].transform("mean")
    out = {}
    def slope(col, tg="ex", d=None):
        d = (df if d is None else d).dropna(subset=[col, tg])
        z = d.groupby("coin")[col].transform(lambda x: (x - x.mean()) / x.std())
        r = stats.linregress(z, d[tg]); return (round(r.slope, 5), round(r.slope / r.stderr, 2), len(d))
    sl = {}
    for col in ["p20", "p30", "p60", "d30", "r30"]:
        for tg in ["ex", "ex10"]:
            sl[f"{col}->{tg}"] = slope(col, tg)
            sl[f"{col}->{tg} early"] = slope(col, tg, df[df.wn <= 12])
            sl[f"{col}->{tg} late"] = slope(col, tg, df[df.wn > 12])
    out["slopes"] = pd.DataFrame(sl, index=["slope", "t", "n"]).T
    pc = {}
    for coin, g in df.groupby("coin"):
        pc[coin + " p30 ex10"] = slope("p30", "ex10", g)
        pc[coin + " p30 ex5"] = slope("p30", "ex", g)
    out["p30 per coin"] = pd.DataFrame(pc, index=["slope", "t", "n"]).T
    # joint regression p30 + r30 on ex10
    d = df.dropna(subset=["p30", "r30", "ex10"]).copy()
    X = np.column_stack([np.ones(len(d)),
        d.groupby("coin")["p30"].transform(lambda x: (x-x.mean())/x.std()),
        d.groupby("coin")["r30"].transform(lambda x: (x-x.mean())/x.std())])
    y = d["ex10"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta; s2 = res @ res / (len(y) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["joint ex10 ~ p30 + r30 (beta,t)"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["c", "p30", "r30"]).round(5)
    # within-side slopes: forecast positive vs negative
    out["f slope, f>0"] = str(slope("f", "ex", df[df.f > 0]))
    out["f slope, f<0"] = str(slope("f", "ex", df[df.f < 0]))
    # p30 by vol regime
    df["hv"] = df.groupby("coin")["vol"].transform(lambda x: x > x.median())
    out["p30 ex10 low vol"] = str(slope("p30", "ex10", df[df.hv == False]))
    out["p30 ex10 high vol"] = str(slope("p30", "ex10", df[df.hv == True]))
    # deciles of p30 -> ex10
    dd = df.dropna(subset=["p30", "ex10"]).copy()
    dd["q"] = dd.groupby("coin")["p30"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    g = dd.groupby("q")["ex10"].agg(["mean", "count", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["p30 quintile -> ex10"] = g.round(5)
    # book long-only vs actual, daily
    L = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            a = b["postRebalance_current_allocation"].astype(float)
            r = b["close"].astype(float).pct_change().shift(-1)
            L.append(pd.DataFrame({"w": w, "long": (a.clip(lower=0) * r), "short": (a.clip(upper=0) * r), "all": a * r}))
    L = pd.concat(L).dropna()
    m = L[["long", "short", "all"]].mean(); sd = L[["long", "short", "all"]].std()
    out["bar gain by side before costs (mean, t)"] = pd.DataFrame({"mean": m, "t": m / (sd / np.sqrt(len(L)))}).round(6)
    return out
