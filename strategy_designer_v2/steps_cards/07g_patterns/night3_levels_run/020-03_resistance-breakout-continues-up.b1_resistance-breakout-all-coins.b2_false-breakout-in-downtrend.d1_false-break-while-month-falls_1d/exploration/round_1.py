def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            n = len(c)
            if n < 40: continue
            r1 = c.pct_change()
            r7 = c / c.shift(7) - 1
            r30 = c / c.shift(30) - 1
            vol30 = r1.rolling(30).std()
            hi90 = c.rolling(90, min_periods=30).max()
            prevhi = c.shift(1).rolling(89, min_periods=29).max()
            dist = c / hi90 - 1
            lo90 = c.rolling(90, min_periods=30).min()
            dlo = c / lo90 - 1
            brk = (c > prevhi).astype(float)
            # swing highs (2 bars each side), count of past swing highs within 2% of close below it
            sh = (c > c.shift(1)) & (c > c.shift(2)) & (c >= c.shift(-1)) & (c >= c.shift(-2))
            shv = c.where(sh)
            # known at t: swing high at t-2 confirmed
            shk = shv.shift(2)
            cnt = np.full(n, np.nan)
            vals = shk.values; cv = c.values
            for t in range(n):
                lo = max(0, t - 88)
                s = vals[lo:t+1]; s = s[~np.isnan(s)]
                cnt[t] = np.sum(np.abs(s / cv[t] - 1) < 0.02) if t >= 30 else np.nan
            fwd = c.shift(-H) / c - 1
            wd = pd.to_datetime(df["timestamp"]).dt.weekday.reset_index(drop=True)
            nxt = c.shift(-1) / c - 1
            for i in range(0, n - H, H):
                recs.append(dict(coin=coin, w=w, fwd=fwd[i], r1=r1[i], r7=r7[i], r30=r30[i],
                                 vol=vol30[i], dist=dist[i], dlo=dlo[i], brk=brk[i], cnt=cnt[i]))
            daily.append(pd.DataFrame({"coin": coin, "wd": wd, "nxt": nxt, "r1": r1, "vol": vol30}))
        if recs:
            d = pd.DataFrame(recs)
            d["drift"] = d["fwd"].mean(); d["sd"] = d["fwd"].std()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["ex"] = D["fwd"] - D["drift"]; D["st"] = D["ex"] / D["sd"]
    D["volz"] = D.groupby("coin")["vol"].rank(pct=True)
    def summ(g):
        x = g["ex"].dropna(); s = g["st"].dropna()
        return pd.Series({"n": len(x), "mean_ex": x.mean(), "strength": s.mean(),
                          "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out = {}
    for v in ["r1", "r7", "r30", "dist", "dlo", "volz"]:
        q = D.groupby("coin")[v].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False) if x.notna().sum() > 10 else np.nan)
        out["q5_" + v] = D.assign(q=q).dropna(subset=["q"]).groupby("q").apply(summ)
    out["brk90"] = D.dropna(subset=["brk"]).groupby("brk").apply(summ)
    D["cntb"] = pd.cut(D["cnt"], [-1, 0, 1, 2, 3, 100])
    out["swing_count_near"] = D.dropna(subset=["cnt"]).groupby("cntb").apply(summ)
    out["brk_x_r30neg"] = D.dropna(subset=["brk", "r30"]).assign(neg=lambda x: x.r30 < 0).groupby(["brk", "neg"]).apply(summ)
    out["by_window"] = D.groupby("w").apply(summ)
    Y = pd.concat(daily, ignore_index=True)
    Y["dm"] = Y.groupby("coin")["nxt"].transform("mean")
    Y["ex"] = Y["nxt"] - Y["dm"]
    out["weekday_next"] = Y.dropna().groupby("wd")["ex"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    # spearman rank IC per variable
    ic = {}
    for v in ["r1", "r7", "r30", "dist", "dlo", "volz"]:
        z = D[[v, "st"]].dropna()
        rho, p = stats.spearmanr(z[v], z["st"]); ic[v] = (rho, p, len(z))
    out["spearman"] = pd.DataFrame(ic, index=["rho", "p", "n"]).T
    # book
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    if tr:
        T = pd.concat(tr)
        out["trades"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median", "std"])
    return out
