def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            absmove = c.diff().abs().rolling(30).sum()
            er = (c - c.shift(30)).abs() / absmove
            ret30 = c / c.shift(30) - 1
            ret7 = c / c.shift(7) - 1
            sd30 = r.rolling(30).std()
            mv7 = ret7 / (sd30 * np.sqrt(7))
            mv1 = r / sd30
            fwd1 = c.shift(-1) / c - 1
            fwd2 = c.shift(-2) / c - 1
            fwd7 = c.shift(-7) / c - 1
            sdrel = sd30 / sd30.rolling(90, min_periods=30).mean()
            alloc = b["postRebalance_current_allocation"].astype(float)
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "er": er, "ret30": ret30,
                               "mv7": mv7, "mv1": mv1, "fwd1": fwd1, "fwd2": fwd2, "fwd7": fwd7,
                               "sdrel": sdrel, "alloc": alloc,
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    def agg(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    def cl_t(df, col):
        s = df.groupby("day")[col].sum(); G = len(s)
        m = df[col].mean(); se = np.sqrt((s ** 2).sum() * G / (G - 1)) / len(df)
        return pd.Series({"cases": len(df), "days": G, "mean": m, "t_clustered": m / se})
    # down-day bounce, graded by mv1 deciles among down days, 1-day and 2-day grid
    d1 = D.dropna(subset=["fwd1", "mv1"]).copy()
    d1["u1"] = d1["fwd1"] - d1["coin"].map(d1.groupby("coin")["fwd1"].mean())
    dn = d1[d1["mv1"] < 0].copy()
    dn["dq"] = pd.qcut(dn["mv1"], 6, labels=["most1", "d2", "d3", "d4", "d5", "least6"])
    out["next-day unusual ret after down days by size sextile"] = dn.groupby("dq")["u1"].apply(agg).unstack()
    out["down-day bounce clustered t (all down days, signed by size)"] = cl_t(dn.assign(x=dn["u1"]), "x")
    top = dn[dn["dq"] == "most1"]
    out["largest-down bounce clustered"] = cl_t(top.assign(x=top["u1"]), "x")
    out["largest-down bounce by window"] = top.groupby("w")["u1"].apply(agg).unstack()
    top = top.copy(); top["volq"] = pd.qcut(top["sdrel"], 3, labels=["calm", "mid", "agit"])
    out["largest-down bounce by vol level"] = top.groupby("volq")["u1"].apply(agg).unstack()
    out["largest-down: book position held after bar"] = agg(top["alloc"])
    g2 = D[D["pos"] % 2 == 0].dropna(subset=["fwd2", "mv1"]).copy()
    g2["u2"] = g2["fwd2"] - g2["coin"].map(g2.groupby("coin")["fwd2"].mean())
    g2d = g2[g2["mv1"] < 0].copy()
    g2d["dq"] = pd.qcut(g2d["mv1"], 4, labels=["most", "b", "c", "least"])
    out["2-day grid after down days by size quartile"] = g2d.groupby("dq")["u2"].apply(agg).unstack()
    # chop aligned continuation by vol level (7d grid)
    g = D[D["pos"] % 7 == 0].dropna(subset=["fwd7", "mv7", "er", "ret30", "sdrel"]).copy()
    g["u7"] = g["fwd7"] - g["coin"].map(g.groupby("coin")["fwd7"].mean())
    s = np.sign(g["mv7"])
    ca = g[(g["er"] < 0.3) & (np.sign(g["ret30"]) == s)].copy()
    ca["ud"] = ca["u7"] * np.sign(ca["mv7"])
    ca["volq"] = pd.qcut(ca["sdrel"], 3, labels=["calm", "mid", "agit"])
    out["chop aligned continuation by vol level"] = ca.groupby("volq")["ud"].apply(agg).unstack()
    ca["mq"] = pd.qcut(ca["mv7"].abs(), 3, labels=["small", "mid", "large"])
    out["chop aligned: vol x size mean"] = ca.groupby(["volq", "mq"])["ud"].mean().unstack()
    return out
