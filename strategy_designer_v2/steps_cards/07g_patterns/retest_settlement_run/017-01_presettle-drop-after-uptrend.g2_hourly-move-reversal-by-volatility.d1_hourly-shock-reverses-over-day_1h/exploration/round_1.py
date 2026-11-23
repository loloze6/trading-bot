def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","close","volume"]].copy().reset_index(drop=True)
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            c = d["close"]
            r1 = c.pct_change()
            v24 = r1.rolling(24).std()
            d["z1"] = r1 / v24
            d["z4"] = (c/c.shift(4)-1)/(v24*2)
            d["z24"] = (c/c.shift(24)-1)/(v24*np.sqrt(24))
            d["z72"] = (c/c.shift(72)-1)/(r1.rolling(72).std()*np.sqrt(72))
            d["volr"] = d["volume"]/d["volume"].rolling(168).median()
            d["vlev"] = v24 / r1.rolling(720, min_periods=200).std()
            for h in (1,8,24,72):
                d[f"f{h}"] = c.shift(-h)/c - 1
            d["hour"] = d["ts"].dt.hour; d["wd"] = d["ts"].dt.weekday; d["year"] = d["ts"].dt.year
            d["pos"] = np.arange(len(d)); d["coin"] = coin; d["win"] = w
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def grid(h):
        G = A[A["pos"] % h == 0].copy()
        drift = G.groupby("coin")[f"f{h}"].transform("mean")
        G["ex"] = G[f"f{h}"] - drift
        G["usual"] = G.groupby("coin")[f"f{h}"].transform("std")
        return G
    def slope(G, x):
        s = G[[x,"ex"]].dropna()
        r = stats.linregress(s[x], s["ex"])
        return r.slope, r.slope/r.stderr, len(s)
    res = []
    for h in (24,72):
        G = grid(h)
        for x in ("z1","z4","z24","z72","volr"):
            b, t, n = slope(G, x); res.append([h, x, b*100, t, n])
    out["slope ex fwd (%/unit) on feature"] = pd.DataFrame(res, columns=["h","feat","slope_pct","t","n"])
    # bins of z1 and z24: signed reversal move
    for h, x in ((24,"z1"),(24,"z24"),(72,"z72"),(72,"z24")):
        G = grid(h).dropna(subset=[x,"ex"])
        G["bin"] = pd.qcut(G[x], 10, labels=False)
        g = G.groupby("bin").agg(xmean=(x,"mean"), ex_pct=("ex", lambda s: s.mean()*100),
                                  t=("ex", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))), n=("ex","size"))
        out[f"decile {x} -> ex fwd {h}h"] = g.round(3)
    # z1 effect by volatility level (vlev tercile), h=24
    G = grid(24).dropna(subset=["z1","ex","vlev"])
    G["vb"] = pd.qcut(G["vlev"], 3, labels=["lowvol","mid","highvol"])
    rr = []
    for k, s in G.groupby("vb"):
        r = stats.linregress(s["z1"], s["ex"]); rr.append([k, r.slope*100, r.slope/r.stderr, len(s)])
    out["z1 slope by vol level h24"] = pd.DataFrame(rr, columns=["vb","slope_pct","t","n"])
    # z1 effect by hour of signal bar (pooled all bars counted at h=24 grid shifted by hour: use all bars but per hour non-overlapping since each hour appears once per day)
    rr = []
    for hr, s in A.dropna(subset=["z1","f24"]).groupby("hour"):
        ex = s["f24"] - s.groupby("coin")["f24"].transform("mean")
        r = stats.linregress(s["z1"], ex); rr.append([hr, r.slope*100, r.slope/r.stderr, len(s)])
    out["z1 slope by hour (f24)"] = pd.DataFrame(rr, columns=["hour","slope_pct","t","n"]).round(3)
    # 1h return by hour, signed against 24h trend (brief), and volume ratio by hour
    B = A.dropna(subset=["z24","f1","volr"]).copy()
    B["against"] = -np.sign(B["z24"]) * B["f1"]
    hh = B.groupby("hour").agg(against_bp=("against", lambda s: s.mean()*1e4),
                               t=("against", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))),
                               raw_bp=("f1", lambda s: s.mean()*1e4),
                               volr=("volr","median"))
    out["by hour: 1h ret against 24h trend, volume"] = hh.round(3)
    # weekday 24h forward
    G = grid(24)
    out["weekday ex f24"] = G.groupby("wd")["ex"].agg(lambda s: s.mean()*100).to_frame("ex_pct").join(
        G.groupby("wd")["ex"].agg(lambda s: s.mean()/(s.std()/np.sqrt(len(s)))).rename("t"))
    # book by year
    D = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df.copy(); x["coin"]=coin; x["win"]=w; D.append(x)
    D = pd.concat(D)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book by year"] = D.groupby("year").agg(book_pct=("book_return", lambda s: s.mean()*100),
                                               coin_pct=("coin_return", lambda s: s.mean()*100), n=("book_return","count")).round(4)
    out["book by coin"] = D.groupby("coin").agg(book_pct=("book_return", lambda s: s.mean()*100),
                                               coin_pct=("coin_return", lambda s: s.mean()*100)).round(4)
    return out
