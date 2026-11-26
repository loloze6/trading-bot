def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            up = np.zeros(n); dn = np.zeros(n)
            for i in range(1, n):
                if r1[i] > 0: up[i] = up[i-1] + 1
                if r1[i] < 0: dn[i] = dn[i-1] + 1
            ts = pd.to_datetime(b["timestamp"])
            vol30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            ret20 = pd.Series(c).pct_change(20).values
            ret10 = pd.Series(c).pct_change(10).values
            ret60 = pd.Series(c).pct_change(60).values
            pos = b["postRebalance_current_allocation"].astype(float).values
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, day=ts.iloc[i].normalize(), yr=ts.iloc[i].year,
                                 fwd=c[i+H]/c[i]-1, up=up[i], dn=dn[i], vol30=vol30[i],
                                 ret10=ret10[i], ret20=ret20[i], ret60=ret60[i], pos=pos[i]))
    df = pd.DataFrame(rows)
    df["unu"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    df["z"] = df["unu"] / df.groupby("coin")["fwd"].transform("std")
    df["r20s"] = df["ret20"] / (df["vol30"] * np.sqrt(20))
    df["r10s"] = df["ret10"] / (df["vol30"] * np.sqrt(10))
    df["vrank"] = df.groupby("coin")["vol30"].rank(pct=True)
    df["agit"] = np.where(df["vrank"] > 0.5, "agit", "calm")
    def ctt(g, x):
        g = g.dropna(subset=[x, "z"])
        if len(g) < 10: return pd.Series(dtype=float)
        xs = (g[x] - g[x].mean()) / g[x].std()
        prod = xs * g["z"]
        s = prod.groupby(g["day"]).sum(); G = len(s)
        m = prod.sum() / len(g)
        se = np.sqrt(G / (G - 1) * (s ** 2).sum() / len(g) ** 2)
        return pd.Series(dict(n=len(g), days=G, corr=m, t_day=m / se))
    out = {}
    cal = df[df.agit == "calm"]; ag = df[df.agit == "agit"]
    out["calm vs agit momentum"] = pd.DataFrame({"calm r20": ctt(cal, "r20s"), "calm r10": ctt(cal, "r10s"),
                                                 "agit r20": ctt(ag, "r20s"), "agit r10": ctt(ag, "r10s")}).T
    out["calm r20 by window"] = cal.groupby("win").apply(lambda g: ctt(g, "r20s"))
    out["calm r20 by coin"] = cal.groupby("coin").apply(lambda g: ctt(g, "r20s"))
    cal = cal.dropna(subset=["r20s"]).copy()
    cal["q"] = pd.qcut(cal["r20s"], 5, labels=False)
    out["calm r20 quintiles"] = cal.groupby("q").agg(n=("z", "size"), mean_unu=("unu", "mean"), mean_z=("z", "mean"))
    # streak length in calm vs agit
    u = df[df.up > 0].copy(); u["upl"] = u["up"].clip(upper=6)
    out["up streak len by agit"] = u.groupby("agit").apply(lambda g: ctt(g, "upl"))
    d = df[df.dn > 0].copy(); d["dnl"] = -d["dn"].clip(upper=6)
    out["down streak len (signed) by agit"] = d.groupby("agit").apply(lambda g: ctt(g, "dnl"))
    # book: drift vs timing
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; dd.append(x)
    dd = pd.concat(dd)
    out["book mean daily, coin mean daily"] = pd.Series(dict(book=dd["book_return"].mean(), coin=dd["coin_return"].mean(),
                                                            mean_pos=df["pos"].mean()))
    return out
