def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; o = b["open"]; h = b["high"]; l = b["low"]
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            sd20 = r.rolling(20).std()
            hh = h.rolling(20).max()
            depth = (c - hh) / hh / sd20
            rng = (h - l) / c
            df = pd.DataFrame({
                "coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]),
                "regime": b["regime"], "ret": r, "nxt": nxt, "nxt2": nxt2, "z1": r / sd20,
                "depth": depth, "rngz": rng / rng.rolling(20).mean(),
                "rngsd": rng / sd20,
                "clpos": (c - l) / (h - l),
                "tr60": c / c.shift(60) - 1,
                "up": (c > o).astype(int)})
            df["pos2"] = np.arange(len(df)) % 2
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["ex"] = d["nxt"] - d.groupby("coin")["nxt"].transform("mean")
    d["ex2"] = d["nxt2"] - d.groupby("coin")["nxt2"].transform("mean")
    d["day"] = d["ts"].dt.floor("D")
    d["yr"] = d["ts"].dt.year
    d["choppy"] = (d["regime"] == "unknown").astype(int)
    d = d.dropna(subset=["ex"])
    def ct(g, col="ex"):
        g = g.dropna(subset=[col])
        x = g[col]; n = len(x)
        if n < 5: return pd.Series({"n": n})
        dev = (x - x.mean()).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / n
        return pd.Series({"n": n, "days": g["day"].nunique(), "mean_%": 100 * x.mean(), "t_day": x.mean() / se})
    out = {}
    # wide range up day fade: graded?
    dr = d.dropna(subset=["rngz"]).copy()
    dr["q"] = pd.qcut(dr["rngz"], 5, labels=False)
    up = dr[dr["up"] == 1]
    out["up days: range-width quintile (day-clustered t)"] = up.groupby("q").apply(ct)
    out["up days: range-width quintile, 2-day ex"] = up.groupby("q").apply(lambda g: ct(g, "ex2"))
    top = up[up["q"] == 4].copy()
    top["tr"] = pd.cut(top["tr60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    out["wide up days by 60d trend"] = top.groupby("tr").apply(ct)
    out["wide up days by year"] = top.groupby("yr").apply(ct)
    top["cp"] = pd.cut(top["clpos"], [-0.01, 0.5, 0.8, 1.01])
    out["wide up days by close position in bar"] = top.groupby("cp").apply(ct)
    out["wide up days by coin"] = top.groupby("coin").apply(ct)
    # slope of ex on rngz within up days
    u = up.dropna(subset=["rngz"])
    X = u["rngz"] - u["rngz"].mean(); y = u["ex"] - u["ex"].mean()
    beta = (X * y).sum() / (X ** 2).sum()
    res = y - beta * X
    s = (X * res).groupby(u["day"]).sum()
    se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
    out["up days: slope ex on range width"] = pd.Series({"beta_%": 100 * beta, "t_day": beta / se, "n": len(u)})
    # same for down days
    dn = dr[dr["up"] == 0].dropna(subset=["rngz"])
    X = dn["rngz"] - dn["rngz"].mean(); y = dn["ex"] - dn["ex"].mean()
    beta = (X * y).sum() / (X ** 2).sum(); res = y - beta * X
    s = (X * res).groupby(dn["day"]).sum(); se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
    out["down days: slope ex on range width"] = pd.Series({"beta_%": 100 * beta, "t_day": beta / se, "n": len(dn)})
    # choppy deepest quintile by up/down and year
    ch = d[(d["choppy"] == 1)].dropna(subset=["depth"]).copy()
    ch["dq"] = pd.qcut(ch["depth"].rank(method="first"), 5, labels=False)
    out["choppy depth quintile x up (t_day)"] = ch.groupby(["up", "dq"]).apply(ct)
    out["choppy deepest quintile by year"] = ch[ch["dq"] == 0].groupby("yr").apply(ct)
    # trending markets: near-high continuation by trend side
    nc = d[d["choppy"] == 0].dropna(subset=["depth", "tr60"]).copy()
    nc["dq"] = pd.qcut(nc["depth"].rank(method="first"), 5, labels=False)
    nc["tr"] = np.where(nc["tr60"] > 0.1, "rising", np.where(nc["tr60"] < -0.1, "falling", "other"))
    out["non-choppy depth quintile x trend"] = nc.groupby(["tr", "dq"]).apply(ct)
    return out
