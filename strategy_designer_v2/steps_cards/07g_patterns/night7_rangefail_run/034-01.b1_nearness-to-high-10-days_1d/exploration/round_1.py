def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi = c.shift(1).rolling(20, min_periods=20).max()
            vol = r1.rolling(20, min_periods=15).std()
            dist = (c / hi - 1) / vol
            ret20 = c / c.shift(20) - 1
            ret5 = c / c.shift(5) - 1
            for h in (5, 10, 20):
                b[f"f{h}"] = c.shift(-h) / c - 1
            b["dist"] = dist; b["vol"] = vol; b["r1"] = r1; b["ret20"] = ret20; b["ret5"] = ret5
            b["rising"] = (b["regime"] == "unknown").astype(int)
            b["coin"] = coin; b["win"] = w; b["pos"] = np.arange(len(b))
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["alloc"] = b["postRebalance_current_allocation"]
            b["nh_raw"] = b.get("debug_info.components.near_high.last_history_value")
            rows.append(b[["timestamp","coin","win","pos","close","forecast","alloc","dist","vol","r1","ret20","ret5","f5","f10","f20","rising","wd","year","nh_raw"]])
    D = pd.concat(rows, ignore_index=True)
    # coin mean returns per horizon on grid over all windows
    for h in (5, 10, 20):
        g = D[D["pos"] % h == 0]
        m = g.groupby("coin")[f"f{h}"].mean()
        D[f"x{h}"] = D[f"f{h}"] - D["coin"].map(m)
    out["check raw vs recomputed dist corr"] = float(D[["dist","nh_raw"]].dropna().corr().iloc[0,1]) if D["nh_raw"].notna().any() else "na"

    def slope(df, xcol, ycol):
        d = df[[xcol, ycol, "timestamp"]].dropna()
        if len(d) < 30: return (np.nan, np.nan, len(d))
        s = stats.linregress(d[xcol], d[ycol])
        return (round(s.slope, 5), round(s.slope / s.stderr, 2), len(d))

    G10 = D[D["pos"] % 10 == 0].copy()
    res = {}
    for prof in (1, 0):
        sub = G10[G10["rising"] == prof]
        res[f"rising={prof} dist->x10"] = slope(sub, "dist", "x10")
        res[f"rising={prof} ret20->x10"] = slope(sub, "ret20", "x10")
        res[f"rising={prof} ret5->x10"] = slope(sub, "ret5", "x10")
        res[f"rising={prof} r1/vol->x10"] = slope(sub.assign(z=sub["r1"]/sub["vol"]), "z", "x10")
    for h in (5, 20):
        Gh = D[D["pos"] % h == 0]
        for prof in (1, 0):
            res[f"h{h} rising={prof} dist"] = slope(Gh[Gh["rising"] == prof], "dist", f"x{h}")
    out["slopes (slope,t,n)"] = pd.DataFrame(res, index=["slope","t","n"]).T

    # dist bins by profile
    G10["dbin"] = pd.cut(G10["dist"], [-99, -6, -4, -2.5, -1.5, -0.5, 0.0001, 99])
    out["x10 by dist bin & rising"] = G10.groupby(["rising","dbin"], observed=True)["x10"].agg(["mean","count"]).round(4)

    # vol level (coin-relative tercile of 20d vol) in rising
    D["vrank"] = D.groupby("coin")["vol"].rank(pct=True)
    G10 = D[D["pos"] % 10 == 0].copy()
    G10["vt"] = pd.cut(G10["vrank"], [0, 1/3, 2/3, 1], labels=["low","mid","high"])
    tab = {}
    for prof in (1, 0):
        for v in ["low","mid","high"]:
            tab[f"r{prof}_{v}"] = slope(G10[(G10["rising"]==prof)&(G10["vt"]==v)], "dist", "x10")
    out["dist slope by vol tercile"] = pd.DataFrame(tab, index=["slope","t","n"]).T

    # large 1-day moves -> next 5d (overlap avoided via grid 5)
    G5 = D[D["pos"] % 5 == 0].copy()
    G5["z"] = G5["r1"] / G5["vol"]
    G5["zb"] = pd.cut(G5["z"], [-99, -2, -1, 0, 1, 2, 99])
    out["x5 after 1d move (z) by rising"] = G5.groupby(["rising","zb"], observed=True)["x5"].agg(["mean","count"]).round(4)

    # weekday of daily returns
    out["daily ret by weekday"] = D.groupby("wd")["r1"].agg(["mean","count", lambda s: s.mean()/s.std()*np.sqrt(len(s))]).round(4)

    # book: daily returns
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    DD = pd.concat(dd, ignore_index=True)
    bk = DD.groupby("day")["book_return"].mean().dropna()
    out["book mean daily by year"] = bk.groupby(pd.to_datetime(bk.index).year).agg(["mean","std","count"]).round(5)
    # positions by profile side
    D["side"] = np.sign(D["alloc"].fillna(0))
    out["alloc side share by rising"] = D.groupby(["rising","side"]).size().unstack(fill_value=0)
    # gain before costs by side
    D["nxt"] = D.groupby(["coin","win"])["close"].shift(-1) / D["close"] - 1
    D["gain"] = D["alloc"] * D["nxt"]
    out["gain per bar by side"] = D.groupby("side")["gain"].agg(["mean","sum","count"]).round(5)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    T = pd.concat(tr, ignore_index=True)
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["mean","median","count"]).round(3)
    T["dur_d"] = T["duration_minutes"]/1440
    T["db"] = pd.cut(T["dur_d"], [0, 10, 20, 40, 400])
    out["trades by duration"] = T.groupby(["side","db"], observed=True)["net_profit_loss_percent"].agg(["mean","count"]).round(3)
    return out
