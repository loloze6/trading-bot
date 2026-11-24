def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 45
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c)
            raw = df["debug_info.components.fall90.last_history_value"].values
            fc = df["forecast"].values
            ts = df["timestamp"].astype(str).str[:10].values
            for t in range(0, n - H):
                rows.append(dict(coin=coin, win=w, t=t, off=t % H, day=ts[t], year=ts[t][:4],
                                 ret=c[t+H]/c[t]-1, fc=fc[t], raw=raw[t],
                                 r10=(c[t]/c[t-10]-1) if t >= 10 else np.nan,
                                 r20=(c[t]/c[t-20]-1) if t >= 20 else np.nan))
    d = pd.DataFrame(rows)
    grid0 = d[d.off == 0]
    mu = grid0.groupby("coin")["ret"].mean()
    d["ex"] = d["ret"] - d["coin"].map(mu)
    def cs(g, x="fc"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 10 or g[x].std() == 0:
            return pd.Series(dict(n=len(g), days=np.nan, slope=np.nan, t=np.nan))
        X = g[x].values - g[x].mean(); Y = g["ex"].values
        b = (X*Y).sum()/(X*X).sum(); a = Y.mean()-b*g[x].mean()
        e = Y-a-b*g[x].values
        s = pd.Series(X*e).groupby(g["day"].values).sum(); G = len(s)
        v = (s**2).sum()/(X*X).sum()**2*G/max(G-1, 1)
        return pd.Series(dict(n=len(g), days=G, slope=b, t=b/np.sqrt(v)))
    out = {}
    offs = pd.DataFrame({o: cs(d[d.off == o]) for o in range(0, H, 3)}).T
    out["slope by grid offset (every 3rd)"] = offs
    allo = pd.DataFrame({o: cs(d[d.off == o]) for o in range(H)}).T
    out["offset t summary"] = allo["t"].describe()
    out["offset slope summary"] = allo["slope"].describe()
    pos = d[d.fc > 0].copy()
    pos["fcq"] = pd.qcut(pos["fc"], 4, duplicates="drop")
    out["all offsets fc>0: excess by fc quartile"] = pos.groupby("fcq")["ex"].agg(["count", "mean", "median"])
    pos["r10s"] = np.where(pos.r10 > 0, "last10 up", "last10 down")
    out["all offsets fc>0 by last10 sign"] = pos.groupby("r10s").apply(cs)
    pos["grp"] = np.where(pos.coin.isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"]), "default6", "others")
    out["all offsets fc>0 by coin group"] = pos.groupby("grp").apply(cs)
    out["all offsets fc>0 by year (slope)"] = pos.groupby("year").apply(cs)
    out["all offsets fc>0 by year mean ex"] = pos.groupby("year")["ex"].mean()
    return out
