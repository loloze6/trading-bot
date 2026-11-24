def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    # window lengths
    lens = []
    for c in bars:
        for w in bars[c]:
            lens.append(len(bars[c][w]))
    out["window length stats"] = pd.Series(lens).describe()

    def grid_cases(lb, h):
        rows = []
        for c in bars:
            for w, df in bars[c].items():
                cl = df["close"].values.astype(float)
                vol = df["volume"].values.astype(float)
                r1 = np.diff(np.log(cl))
                n = len(cl)
                for t in range(0, n - h, h):
                    if t < lb: continue
                    past = cl[t] / cl[t - lb] - 1
                    fwd = cl[t + h] / cl[t] - 1
                    rv = np.std(r1[max(0, t - lb):t]) if t - lb >= 0 else np.nan
                    vr = vol[t-14+1:t+1].mean() / vol[max(0,t-lb+1):t+1].mean() if t >= 14 else np.nan
                    rows.append((c, w, t, past, fwd, rv, vr))
        d = pd.DataFrame(rows, columns=["coin","w","t","past","fwd","rv","vr"])
        # coin drift from all windows grid
        drift = {}
        for c in bars:
            f = []
            for w, df in bars[c].items():
                cl = df["close"].values.astype(float)
                f += [cl[t+h]/cl[t]-1 for t in range(0, len(cl)-h, h)]
            drift[c] = np.mean(f); 
        d["ex"] = d["fwd"] - d["coin"].map(drift)
        # scale past by coin's std of past returns
        d["z"] = d.groupby("coin")["past"].transform(lambda s: s / s.abs().mean())
        return d

    res = []
    for lb in [7, 14, 30, 60]:
        for h in [3, 7, 14, 30]:
            d = grid_cases(lb, h)
            d = d.dropna(subset=["z","ex"])
            if len(d) < 30: continue
            sl = stats.linregress(d["z"], d["ex"])
            q = pd.qcut(d["z"], 5, labels=False, duplicates="drop")
            m = d.groupby(q)["ex"].mean()
            res.append(dict(lb=lb, h=h, n=len(d), slope=sl.slope, t=sl.slope/sl.stderr,
                            q1=m.iloc[0], q5=m.iloc[-1]))
    out["past return z vs future excess"] = pd.DataFrame(res)

    # volatility level vs forward 7d excess return and abs
    res = []
    for h in [7, 14]:
        d = grid_cases(30, h).dropna(subset=["rv","ex"])
        d["rvz"] = d.groupby("coin")["rv"].transform(lambda s: s / s.mean())
        q = pd.qcut(d["rvz"], 4, labels=False)
        g = d.groupby(q).agg(n=("ex","size"), mean_ex=("ex","mean"), sd=("ex","std"))
        g["t"] = g.mean_ex / (g.sd / np.sqrt(g.n))
        g["h"] = h
        res.append(g)
    out["vol quartile vs excess"] = pd.concat(res)

    # volume ratio (14 vs 30 lookback) vs forward
    res = []
    for h in [7, 14, 30]:
        d = grid_cases(30, h).dropna(subset=["vr","ex"])
        d["lvr"] = np.log(d["vr"])
        sl = stats.linregress(d["lvr"], d["ex"])
        # interaction with sign of past
        d2 = d[d.past > 0]; d3 = d[d.past <= 0]
        s2 = stats.linregress(d2["lvr"], d2["ex"]); s3 = stats.linregress(d3["lvr"], d3["ex"])
        res.append(dict(h=h, n=len(d), slope=sl.slope, t=sl.slope/sl.stderr,
                        t_up=s2.slope/s2.stderr, n_up=len(d2), t_dn=s3.slope/s3.stderr, n_dn=len(d3)))
    out["volume ratio vs future"] = pd.DataFrame(res)

    # weekday daily returns
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            ts = pd.to_datetime(df["timestamp"])
            r = df["close"].astype(float).pct_change()
            rows.append(pd.DataFrame({"wd": ts.dt.weekday, "r": r, "coin": c, "yr": ts.dt.year}))
    a = pd.concat(rows).dropna()
    g = a.groupby("wd")["r"].agg(["mean","std","size"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["size"]))
    out["weekday returns"] = g
    # big daily move reversal next day
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            r = df["close"].astype(float).pct_change()
            sd = r.rolling(30).std().shift(1)
            z = r / sd
            f1 = df["close"].astype(float).shift(-3)/df["close"].astype(float)-1
            rows.append(pd.DataFrame({"z": z, "f3": f1}).iloc[::3])
    b = pd.concat(rows).dropna()
    q = pd.qcut(b["z"], 5, labels=False)
    g = b.groupby(q)["f3"].agg(["mean","std","size"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["size"]))
    out["daily z quintile vs next 3d"] = g
    # book trades
    tr = pd.concat([df.assign(coin=c) for c in data["trades"] for df in data["trades"][c].values()])
    out["trades by coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
