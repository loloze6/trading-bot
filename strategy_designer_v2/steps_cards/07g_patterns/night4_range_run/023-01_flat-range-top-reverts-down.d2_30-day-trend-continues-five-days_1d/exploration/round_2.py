def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    out = {}
    rows = []; daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            daily.append(pd.DataFrame(dict(coin=coin, w=w, ts=ts.values, r=r1.values,
                                           alloc=b["postRebalance_current_allocation"].shift(1).values)))
            if n < 40: continue
            hh = hi.rolling(30).max(); ll = lo.rolling(30).min()
            nmr = (c - c.shift(30)).abs() / (hh - ll)
            pos = (c - (hh + ll) / 2) / (hh - ll)
            fwd = c.shift(-H) / c - 1
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, nmr=nmr[i], pos=pos[i],
                                 z1=r1[i] / vol20[i] if vol20[i] > 0 else np.nan,
                                 fwd=fwd[i], year=ts[i].year))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df["coin"].map(df.groupby("coin")["fwd"].mean())
    df["exs"] = df["ex"] / df["coin"].map(df.groupby("coin")["fwd"].std())
    df = df.dropna(subset=["exs"])
    tf = lambda x: x.mean() / x.std() * np.sqrt(len(x))
    # A: weekday, cross-coin day average (removes coin co-movement)
    dd = pd.concat(daily).dropna(subset=["r"])
    dd["rx"] = dd["r"] - dd["coin"].map(dd.groupby("coin")["r"].mean())
    dd["wd"] = pd.to_datetime(dd["ts"]).dt.weekday
    dd["year"] = pd.to_datetime(dd["ts"]).dt.year
    day = dd.groupby(["w", "ts"]).agg(rx=("rx", "mean"), wd=("wd", "first"), year=("year", "first")).reset_index()
    out["weekday, coin-avg day ex ret"] = day.groupby("wd")["rx"].agg(["mean", "count", tf])
    sat = dd[dd.wd == 5]
    out["saturday ex ret by coin"] = sat.groupby("coin")["rx"].agg(["mean", "count", tf])
    out["saturday coin-avg by year"] = day[day.wd == 5].groupby("year")["rx"].agg(["mean", "count", tf])
    # A2: Saturday graded by prior volatility? sat ex ret by vol tercile
    # B: flat regime, range bottom continuation, by coin and year
    f = df.dropna(subset=["nmr", "pos"])
    f = f[f.nmr < 0.5].copy()
    f["bot"] = f["pos"] <= -0.3
    out["flat bottom (pos<=-0.3) by coin"] = f[f.bot].groupby("coin")["exs"].agg(["mean", "count", tf])
    out["flat bottom by year"] = f[f.bot].groupby("year")["exs"].agg(["mean", "count", tf])
    f["pq"] = pd.qcut(f["pos"], 6, labels=False)
    out["flat pos sextile"] = f.groupby("pq")[["pos", "exs"]].agg(["mean"]).join(f.groupby("pq")["exs"].agg(["count", tf]))
    # C: 1-day shock z continuation, by coin and year, and correlation
    e = df.dropna(subset=["z1"]).copy()
    r, p = stats.pearsonr(e["z1"].clip(-4, 4), e["exs"])
    out["z1 vs exs corr r,n,t"] = pd.Series([r, len(e), r * np.sqrt((len(e) - 2) / (1 - r * r))], index=["r", "n", "t"])
    up = e[e.z1 > 1]
    out["z1>1 by coin"] = up.groupby("coin")["exs"].agg(["mean", "count", tf])
    out["z1>1 by year"] = up.groupby("year")["exs"].agg(["mean", "count", tf])
    dn = e[e.z1 < -1]
    out["z1<-1 by coin"] = dn.groupby("coin")["exs"].agg(["mean", "count", tf])
    # D: book long vs short contribution, coin-avg per day
    dd["g"] = dd["alloc"] * dd["r"]
    dd["side"] = np.sign(dd["alloc"].fillna(0))
    out["bar gain by side (per coin-bar)"] = dd.groupby("side")["g"].agg(["mean", "sum", "count", tf])
    out["bar gain by side and coin"] = dd.groupby(["coin", "side"])["g"].agg(["mean", "count"]).unstack()
    # E: trades long winsorised
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    tr["pl"] = tr["profit_loss_percent"].clip(-50, 50)
    out["trades clipped by side"] = tr.groupby("side")["pl"].agg(["mean", "median", "count", tf])
    out["trades by side and regime"] = tr.groupby(["side", "entry_regime"])["profit_loss_percent"].agg(["median", "count"])
    return out
