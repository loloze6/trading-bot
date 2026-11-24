def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = 14
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            v = df["volume"].astype(float)
            n = len(c)
            if n < H + 2: continue
            cs = pd.Series(c)
            r14 = cs / cs.shift(14) - 1
            r60 = cs / cs.shift(60) - 1
            r90 = cs / cs.shift(90) - 1
            r1 = cs.pct_change()
            vol30 = r1.rolling(30).std()
            vr = v.rolling(14).mean() / v.rolling(30).mean() - 1
            fwd = cs.shift(-H) / cs - 1
            alloc = df["postRebalance_current_allocation"].astype(float)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, r14=r14[i], r60=r60[i], r90=r90[i],
                                 vol30=vol30[i], vr=vr[i], fwd=fwd[i], alloc=alloc[i],
                                 regime=df["regime"].iloc[i], dow=ts.iloc[i].dayofweek,
                                 year=ts.iloc[i].year, r1=r1[i]))
    g = pd.DataFrame(rows)
    drift = g.groupby("coin")["fwd"].transform("mean")
    sd = g.groupby("coin")["fwd"].transform("std")
    g["ex"] = g["fwd"] - drift
    g["z"] = g["ex"] / sd
    out = {}
    def tab(col, q=5):
        s = g.dropna(subset=[col])
        s = s.assign(b=s.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False)))
        t = s.groupby("b")["ex"].agg(["mean", "count"])
        t["t"] = s.groupby("b")["ex"].apply(lambda x: x.mean() / x.std() * np.sqrt(len(x)))
        t["zmean"] = s.groupby("b")["z"].mean()
        return t
    for col in ["r14", "r60", "r90", "vr", "vol30", "r1"]:
        out["fwd14 excess by coin-quintile of " + col] = tab(col)
    # slope of z on standardized signal
    sl = {}
    for col in ["r14", "r60", "r90", "vr", "vol30"]:
        s = g.dropna(subset=[col, "z"])
        x = s.groupby("coin")[col].transform(lambda x: (x - x.mean()) / x.std())
        r = stats.pearsonr(x, s["z"])
        sl[col] = f"corr {r[0]:.3f} p {r[1]:.3f} n {len(s)}"
    out["corr of z fwd with signal"] = pd.Series(sl)
    # interaction r14 sign x vr sign
    s = g.dropna(subset=["r14", "vr"])
    s = s.assign(k=np.sign(s.r14).astype(int).astype(str) + "/" + np.sign(s.vr).astype(int).astype(str))
    out["r14sign/vrsign"] = s.groupby("k")["ex"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["by regime"] = g.groupby("regime")["ex"].agg(["mean", "count"])
    out["by year"] = g.groupby("year")["ex"].agg(["mean", "count"])
    # book: long vs short contribution daily
    br = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float)
            ret = c.shift(-1) / c - 1
            a = df["postRebalance_current_allocation"].astype(float)
            gain = a * ret
            br.append(pd.DataFrame(dict(gain=gain, side=np.sign(a), regime=df["regime"],
                                        dow=pd.to_datetime(df["timestamp"]).dt.dayofweek)))
    b = pd.concat(br).dropna()
    out["bar gain by side"] = b.groupby("side")["gain"].agg(["mean", "count", "sum", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["bar gain by dow"] = b.groupby("dow")["gain"].agg(["mean", "count"])
    # daily coin return by weekday
    dd = []
    for coin, wins in days.items():
        for w, df in wins.items():
            dd.append(pd.DataFrame(dict(r=df["coin_return"], dow=pd.to_datetime(df["day"]).dt.dayofweek)))
    d = pd.concat(dd).dropna()
    out["coin daily ret by dow"] = d.groupby("dow")["r"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t)
    T = pd.concat(tr)
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["mean", "median", "count"])
    out["trades by regime"] = T.groupby("entry_regime")["net_profit_loss_percent"].agg(["mean", "count"])
    return out
