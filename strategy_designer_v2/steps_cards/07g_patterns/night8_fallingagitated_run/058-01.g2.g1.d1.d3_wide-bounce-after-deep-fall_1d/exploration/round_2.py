def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r = c.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            n = len(b)
            d = pd.DataFrame({"coin": coin, "w": w, "wn": int(w[1:]),
                              "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                              "regime": b["regime"].astype(str), "vol": vol,
                              "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                              "r1": r})
            for k in (2, 3, 5):
                d[f"z{k}"] = (c / c.shift(k) - 1) / (vol * np.sqrt(k))
            for h in (1, 2, 3, 5):
                d[f"f{h}"] = c.shift(-h) / c - 1
                d[f"g{h}"] = (np.arange(n) % h == 0)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["inprof"] = D["regime"].isin(["mean_reversion", "unknown"])
    for h in (1, 2, 3, 5):
        m = D[D[f"g{h}"]].groupby("coin")[f"f{h}"].mean()
        sd = D[D[f"g{h}"]].groupby("coin")[f"f{h}"].std()
        D[f"x{h}"] = D[f"f{h}"] - D["coin"].map(m)
        D[f"s{h}"] = D[f"x{h}"] / D["coin"].map(sd)
    def clt(S, col):
        g = S.groupby("day")[col].sum()
        n = len(S)
        if n < 3: return np.nan
        return S[col].mean() / (g.std() * np.sqrt(len(g)) / n)
    out = {}
    res = []
    for k in (2, 3, 5):
        for h in (1, 2, 3, 5):
            S = D[D.inprof & D[f"g{h}"]].dropna(subset=[f"z{k}", f"x{h}"])
            rho, p = stats.spearmanr(S[f"z{k}"], S[f"x{h}"])
            top = S[S[f"z{k}"] >= S[f"z{k}"].quantile(0.8)]
            up = S[S[f"z{k}"] > 0]
            res.append({"k": k, "h": h, "n": len(S), "rho": rho, "p": p,
                        "top20_n": len(top), "top20_short%": -100 * top[f"x{h}"].mean(),
                        "top20_t_dayclust": -clt(top, f"x{h}"),
                        "up_rho": stats.spearmanr(up[f"z{k}"], up[f"x{h}"])[0], "up_n": len(up),
                        "up_strength": -(up[f"s{h}"] * np.sign(up[f"z{k}"])).mean()})
    out["inprof: past k-day z vs next h excess"] = pd.DataFrame(res)
    # outside profile same for contrast
    res = []
    for k in (3, 5):
        for h in (3, 5):
            S = D[~D.inprof & D[f"g{h}"]].dropna(subset=[f"z{k}", f"x{h}"])
            top = S[S[f"z{k}"] >= S[f"z{k}"].quantile(0.8)]
            res.append({"k": k, "h": h, "n": len(S), "rho": stats.spearmanr(S[f"z{k}"], S[f"x{h}"])[0],
                        "top20_short%": -100 * top[f"x{h}"].mean(), "t": -clt(top, f"x{h}")})
    out["outprof contrast"] = pd.DataFrame(res)
    # robustness of k=3,h=3 rises in profile: by window half and coin
    S = D[D.inprof & D["g3"]].dropna(subset=["z3", "x3"])
    up = S[S.z3 > 0].copy()
    up["q"] = pd.qcut(up.z3, 3, labels=False)
    out["inprof 3d rises by tercile, next3 short%"] = up.groupby("q").apply(
        lambda g: pd.Series({"n": len(g), "zmean": g.z3.mean(), "short%": -100 * g.x3.mean(), "t": -clt(g, "x3")}))
    up["half"] = np.where(up.wn <= 12, "w7-12", "w13-18")
    out["inprof 3d rises: rho by half"] = up.groupby("half").apply(
        lambda g: pd.Series({"n": len(g), "rho": stats.spearmanr(g.z3, g.x3)[0], "short%": -100 * g.x3.mean()}))
    out["inprof 3d rises: by coin"] = up.groupby("coin").apply(
        lambda g: pd.Series({"n": len(g), "rho": stats.spearmanr(g.z3, g.x3)[0], "short%": -100 * g.x3.mean()}))
    # 5-day rises next 5, by coin and half
    S5 = D[D.inprof & D["g5"]].dropna(subset=["z5", "x5"])
    u5 = S5[S5.z5 > 0].copy(); u5["half"] = np.where(u5.wn <= 12, "w7-12", "w13-18")
    out["inprof 5d rises next5 by half"] = u5.groupby("half").apply(
        lambda g: pd.Series({"n": len(g), "rho": stats.spearmanr(g.z5, g.x5)[0], "short%": -100 * g.x5.mean(), "t": -clt(g, "x5")}))
    # up day with high close in profile, next1 by z1 among up days
    S1 = D[D.inprof & (D.r1 > 0)].dropna(subset=["z2", "x1", "clv"]).copy()
    z1 = S1.r1 / S1.vol
    S1["q"] = pd.qcut(z1, 3, labels=False)
    out["inprof up days next1 by z1 tercile"] = S1.groupby("q").apply(
        lambda g: pd.Series({"n": len(g), "short%": -100 * g.x1.mean(), "t": -clt(g, "x1")}))
    return out
