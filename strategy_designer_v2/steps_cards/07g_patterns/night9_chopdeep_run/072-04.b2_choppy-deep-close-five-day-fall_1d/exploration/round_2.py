def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); n = len(b)
            r1 = c.pct_change()
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            sd20 = r1.rolling(20).std()
            hi20 = c.rolling(20).max(); lo20 = c.rolling(20).min()
            depth = (c / hi20 - 1) / sd20
            rngpos = (c - lo20) / (hi20 - lo20)
            ret60 = c / c.shift(60) - 1
            sd30 = r1.rolling(30).std()
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(n), "regime": b["regime"].values,
                "fc": b["forecast"].values, "raw": b.get("debug_info.components.depth.last_history_value", pd.Series(np.nan, index=b.index)).values,
                "r1": r1, "f1": f1, "f5": f5, "depth": depth, "rngpos": rngpos, "ret60": ret60,
                "sd30": sd30, "year": ts.dt.year.values, "day": ts.dt.floor("D").values}))
    D = pd.concat(rows, ignore_index=True)
    out = {}
    g = D[D.pos % 5 == 0].dropna(subset=["f5"])
    drift5 = g.groupby("coin")["f5"].mean()
    D["x5"] = D["f5"] - D.coin.map(drift5)
    D["choppy"] = D.regime == "unknown"
    D["calm"] = D.sd30 <= D.groupby(["coin", "w"])["sd30"].transform("median")
    def ttab(s, by, y="x5"):
        s = s.dropna(subset=[y])
        t = s.groupby(by)[y].agg(["mean", "std", "size"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["size"]))
        return t.drop(columns="std")
    G = D[D.pos % 5 == 0].dropna(subset=["x5", "depth"]).copy()
    C = G[G.choppy].copy()
    C["q"] = pd.qcut(C.depth, 5, labels=False)
    out["choppy corr depth vs forecast"] = float(C[["depth", "fc"]].corr().iloc[0, 1])
    C["fq"] = pd.qcut(C.fc.rank(method="first"), 5, labels=False)
    out["choppy forecast quintile -> x5"] = ttab(C, "fq")
    out["choppy deepest q by year"] = ttab(C[C.q == 0], "year")
    out["choppy deepest q by coin"] = ttab(C[C.q == 0], "coin")
    out["choppy deep(q0,1) up vs down day"] = ttab(C[C.q <= 1].assign(up=lambda x: x.r1 > 0), "up")
    out["choppy q by calm"] = ttab(C, ["calm", "q"])
    # non choppy: trend split, rngpos
    N = G[~G.choppy & G.ret60.notna()].copy()
    N["tr"] = np.where(N.ret60 > 0.1, "rising", np.where(N.ret60 < -0.1, "falling", "other"))
    N["rq"] = pd.qcut(N.rngpos, 3, labels=False)
    out["nonchoppy trend x rngpos tercile"] = ttab(N, ["tr", "rq"])
    G["rq"] = pd.qcut(G.rngpos, 5, labels=False)
    out["all rngpos quint by year"] = G.groupby(["year", "rq"])["x5"].mean().unstack()
    # all: depth continuous slope t, clustered by day approx: per-day mean
    G["dz"] = G.depth
    dm = G.groupby("day")[["dz", "x5"]].mean()
    out["depth-x5 corr all, days"] = pd.Series({"corr": dm.corr().iloc[0, 1], "ndays": len(dm)})
    return out
