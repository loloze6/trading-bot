def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 30: continue
            rng = (b.high - b.low)
            loc = (b.close - b.low) / rng.replace(0, np.nan)
            ret5 = b.close / b.close.shift(5) - 1
            ret20 = b.close / b.close.shift(20) - 1
            ret60 = b.close / b.close.shift(60) - 1
            r1 = b.close.pct_change()
            vol10 = r1.rolling(10).std()
            vol30 = r1.rolling(30).std()
            fwd = b.close.shift(-H) / b.close - 1
            fwd2 = b.close.shift(-2) / b.close - 1
            ts = pd.to_datetime(b.timestamp)
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                              "loc": loc, "ret5": ret5, "ret20": ret20, "ret60": ret60,
                              "vr": vol10 / vol30, "fwd": fwd, "fwd2": fwd2,
                              "regime": b.regime.astype(str), "day": ts.dt.floor("D"),
                              "year": ts.dt.year})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A.pos % H == 0) & A.fwd.notna()].copy()
    drift = G.groupby("coin").fwd.mean()
    G["unu"] = G.fwd - G.coin.map(drift)
    G["inprof"] = G.regime != "chop"

    def ct(s, days):
        df = pd.DataFrame({"v": s.values, "d": days.values}).dropna()
        n = len(df)
        if n < 5: return (n, np.nan, np.nan)
        m = df.v.mean()
        g = (df.v - m).groupby(df.d).sum()
        k = len(g)
        se = np.sqrt((g ** 2).sum() * k / max(k - 1, 1)) / n
        return (n, m, m / se if se > 0 else np.nan)

    def tab(df, by):
        out = []
        for key, g in df.groupby(by, observed=True):
            n, m, t = ct(g.unu, g.day)
            out.append({"key": str(key), "n": n, "days": g.day.nunique(), "mean_unu": m, "t": t})
        return pd.DataFrame(out)

    res = {}
    P = G[G.inprof].copy()
    n, m, t = ct(P.unu, P.day)
    res["in profile all"] = pd.Series({"n": n, "days": P.day.nunique(), "mean_unu": m, "t": t})
    n, m, t = ct(G[~G.inprof].unu, G[~G.inprof].day)
    res["out profile all"] = pd.Series({"n": n, "mean_unu": m, "t": t})
    res["in profile by window"] = tab(P, "win")
    res["in profile by coin"] = tab(P, "coin")
    res["in profile by year"] = tab(P, "year")
    P["locq"] = pd.qcut(P["loc"], 3, duplicates="drop")
    res["in profile loc tercile"] = tab(P, "locq")
    P["r20q"] = pd.qcut(P.ret20, 3, duplicates="drop")
    res["in profile ret20 tercile"] = tab(P, "r20q")
    P["vrq"] = pd.qcut(P.vr, 3, duplicates="drop")
    res["in profile vol10/vol30 tercile"] = tab(P, "vrq")
    # own trend classes over all grid bars where ret60 known
    Q = G[G.ret60.notna()].copy()
    Q["trend"] = np.where(Q.ret60 > 0.10, "rising", np.where(Q.ret60 < -0.10, "falling", "choppy"))
    Q["ag"] = np.where(Q.inprof, "chopagi", "other")
    Q["locq"] = pd.cut(Q["loc"], [0, 1/3, 2/3, 1.0001], include_lowest=True)
    res["trend x loc (ret60 known)"] = tab(Q, ["trend", "ag", "locq"])
    # correlation of loc with unu in profile
    res["in profile spearman loc vs unu"] = float(P[["loc", "unu"]].corr(method="spearman").iloc[0, 1])
    res["in profile spearman ret20 vs unu"] = float(P[["ret20", "unu"]].dropna().corr(method="spearman").iloc[0, 1])
    return res
