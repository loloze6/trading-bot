def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","close","volume","forecast"]].copy().reset_index(drop=True)
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            c = d["close"].values
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            d["r1"] = r1
            d["vol24"] = pd.Series(r1).rolling(24).std().values
            d["shock"] = d["r1"]/d["vol24"]
            d["r24p"] = d["close"]/d["close"].shift(24)-1
            d["r72p"] = d["close"]/d["close"].shift(72)-1
            d["r168p"] = d["close"]/d["close"].shift(168)-1
            d["vol72"] = pd.Series(r1).rolling(72).std().values
            for h in (24, 72):
                d[f"f{h}"] = d["close"].shift(-h)/d["close"]-1
            d["coin"] = coin; d["win"] = w; d["pos"] = np.arange(len(d))
            d["hour"] = d["timestamp"].dt.hour; d["wd"] = d["timestamp"].dt.weekday
            d["year"] = d["timestamp"].dt.year
            d["vrel"] = d["volume"]/d["volume"].rolling(168).mean()
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    # drifts
    for h in (24, 72):
        g = A[A["pos"] % h == 0]
        mu = g.groupby("coin")[f"f{h}"].mean()
        A[f"x{h}"] = A[f"f{h}"] - A["coin"].map(mu)
    G24 = A[A["pos"] % 24 == 0].dropna(subset=["x24","shock"])
    # shock buckets incl extremes
    G24 = G24.assign(sb=pd.cut(G24["shock"], [-99,-4,-3,-2,-1,0,1,2,3,4,99]))
    def summ(g, col):
        return pd.Series({"n": len(g), "mean": g[col].mean(), "t": g[col].mean()/(g[col].std()/np.sqrt(len(g))) if len(g)>2 else np.nan})
    out["x24 by shock bucket (grid pos 0)"] = G24.groupby("sb", observed=True).apply(lambda g: summ(g,"x24"))
    # all grid offsets for shock: use every hour but report by hour of signal, nonoverlapping per offset
    A["fade24"] = -np.sign(A["shock"]) * A["x24"]
    H = []
    for hr in range(24):
        g = A[(A["hour"]==hr) & A["shock"].abs().between(1,3)].dropna(subset=["fade24"])
        # one per day per coin at that hour -> non-overlapping 24h
        H.append(pd.Series({"hour": hr, **summ(g,"fade24")}))
    out["fade of |shock| 1-3 over 24h by UTC hour"] = pd.DataFrame(H).set_index("hour")
    # past multi-day return -> next 72h
    G72 = A[A["pos"] % 72 == 0].dropna(subset=["x72","r72p","vol72"])
    G72 = G72.assign(z=G72["r72p"]/(G72["vol72"]*np.sqrt(72)))
    G72 = G72.assign(zb=pd.qcut(G72["z"], 5))
    out["x72 by past 72h z quintile"] = G72.groupby("zb", observed=True).apply(lambda g: summ(g,"x72"))
    G72b = G72.dropna(subset=["r168p"]).copy()
    G72b["zb7"] = pd.qcut(G72b["r168p"]/(G72b["vol72"]*np.sqrt(168)), 5)
    out["x72 by past 7d z quintile"] = G72b.groupby("zb7", observed=True).apply(lambda g: summ(g,"x72"))
    # vol level
    G24b = G24.dropna(subset=["vol24"]).copy()
    G24b["vq"] = G24b.groupby("coin")["vol24"].transform(lambda s: pd.qcut(s, 5, labels=False))
    G24b["fade"] = -np.sign(G24b["shock"])*G24b["x24"]
    out["fade24 by vol quintile (per coin)"] = G24b.groupby("vq").apply(lambda g: summ(g,"fade"))
    out["fade24 by coin"] = G24b.groupby("coin").apply(lambda g: summ(g,"fade"))
    out["fade24 by year"] = G24b.groupby("year").apply(lambda g: summ(g,"fade"))
    # volume shock
    G24c = G24b.dropna(subset=["vrel"]).copy()
    G24c["vrq"] = pd.qcut(G24c["vrel"], 5, labels=False)
    out["fade24 by relative volume quintile"] = G24c.groupby("vrq").apply(lambda g: summ(g,"fade"))
    # book per window
    bw = []
    for coin, wins in days.items():
        for w, dd in wins.items():
            bw.append({"win": w, "coin": coin, "book": dd["book_return"].mean(), "coin_r": dd["coin_return"].mean()})
    bw = pd.DataFrame(bw)
    out["book vs coin mean daily ret by window"] = bw.groupby("win")[["book","coin_r"]].mean()
    return out
