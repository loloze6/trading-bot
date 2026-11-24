def explore(data):
    import pandas as pd, numpy as np
    H = 20
    allr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); r = c.pct_change()
            vol = r.rolling(30).std()
            dfw = pd.DataFrame({"coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]), "r1": r,
                                "r30": c / c.shift(30) - 1, "r60": c / c.shift(60) - 1,
                                "vol": vol, "volrel": vol / vol.expanding(60).mean(),
                                "f20": c.shift(-H) / c - 1, "f5": c.shift(-5) / c - 1, "f1": c.shift(-1) / c - 1,
                                "z": r / r.rolling(60, min_periods=20).std(),
                                "pos": b["postRebalance_current_allocation"].astype(float),
                                "reg": b["regime"], "i": np.arange(len(b))})
            allr.append(dfw)
    D = pd.concat(allr, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    def cl(df, key, col):
        res = {}
        for k, g in df.dropna(subset=[col]).groupby(key):
            m = g[col].mean(); n = len(g)
            s = (g[col] - m).groupby(g["day"]).sum()
            se = np.sqrt((s ** 2).sum()) / n
            res[k] = {"mean": round(m, 5), "n": n, "days": s.size, "t_cl": round(m / se, 2) if se > 0 else np.nan}
        return pd.DataFrame(res).T
    out = {}
    D["r1u"] = D["r1"] - D.groupby("coin")["r1"].transform("mean")
    D["wd"] = D["ts"].dt.weekday
    out["daily unusual return by weekday, day-clustered"] = cl(D, "wd", "r1u")
    for y, g in D.dropna(subset=["r1u"]).groupby(D["ts"].dt.year):
        pass
    D["yr"] = D["ts"].dt.year
    thu = D[D.wd == 3]; sat = D[D.wd == 5]
    out["thursday by year clustered"] = cl(thu, "yr", "r1u")
    out["saturday by year clustered"] = cl(sat, "yr", "r1u")
    # 20-bar grid
    G = D[(D.i % H) == 0].dropna(subset=["f20"]).copy()
    G["u"] = G["f20"] - G.groupby("coin")["f20"].transform("mean")
    Gv = G.dropna(subset=["volrel"]).copy()
    Gv["vq"] = pd.qcut(Gv["volrel"], 4, labels=False)
    out["fwd20 unusual by 30d vol vs own past (quartile), clustered"] = cl(Gv, "vq", "u")
    Gv["trend"] = np.where((Gv.r30 > 0) & (Gv.r60 > 0), "up", "other")
    out["fwd20 by vol quartile x trend"] = cl(Gv, ["trend", "vq"], "u")
    # 5-bar grid: after large moves
    G5 = D[(D.i % 5) == 0].dropna(subset=["f5", "z"]).copy()
    G5["u"] = G5["f5"] - G5.groupby("coin")["f5"].transform("mean")
    G5["zb"] = pd.cut(G5["z"], [-99, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 99])
    out["fwd5 by last-day z, clustered"] = cl(G5, "zb", "u")
    G5["zs"] = G5["z"].clip(-4, 4)
    G5u = G5.dropna(subset=["u"])
    out["fwd5 slope on z"] = round(np.polyfit(G5u["zs"], G5u["u"], 1)[0], 5)
    # book: in position, by regime state
    D["gain"] = D["pos"] * D.groupby(["coin", "w"])["r1"].shift(-1)
    D["st"] = np.where(D["reg"] == "trending", "regime_on", "regime_off")
    inpos = D[D.pos.abs() > 1e-9]
    out["position gain per in-position bar by regime state, clustered"] = cl(inpos, "st", "gain")
    D["r60q"] = pd.qcut(D["r60"], 5, labels=False)
    out["position gain in position by r60 quintile"] = cl(D[D.pos.abs() > 1e-9], "r60q", "gain")
    # graded r60 inside up regime on 20-grid
    Gu = G[(G.r30 > 0) & (G.r60 > 0)].copy()
    Gu["r60q"] = pd.qcut(Gu["r60"], 4, labels=False)
    out["fwd20 by r60 quartile inside both-up, clustered"] = cl(Gu, "r60q", "u")
    return out
