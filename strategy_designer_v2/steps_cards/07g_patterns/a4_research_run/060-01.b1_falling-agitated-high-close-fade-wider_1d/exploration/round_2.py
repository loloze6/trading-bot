def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 30:
                continue
            o, h, l, c, v = b["open"], b["high"], b["low"], b["close"], b["volume"]
            rng = (h - l).replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "loc": (c - l) / rng,
                "ret0": c / c.shift(1) - 1,
                "range_rel": (h - l) / c.shift(1),
                "next": c.shift(-1) / c - 1,
                "next3": c.shift(-3) / c - 1,
                "regime": b["regime"],
                "volz": v / v.rolling(20, min_periods=10).median(),
                "year": pd.to_datetime(b["timestamp"]).dt.year,
            })
            d["vol20"] = d["ret0"].rolling(20, min_periods=10).std()
            d["ret60"] = c / c.shift(60) - 1
            d["inprof"] = d["regime"].isin(["mean_reversion", "unknown"])
            d["pos_idx"] = np.arange(len(d))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["next", "vol20"])
    D["ret0z"] = D["ret0"] / D["vol20"]
    D["absz"] = D["ret0z"].abs()
    D["rngz"] = D["range_rel"] / D["vol20"]

    def summ(g, col="next"):
        x = g[col].dropna(); n = len(x)
        m = x.mean(); t = m / (x.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean": m, "t": t})

    out = {}
    # quiet day fade: graded by |ret0z|
    D["aq"] = pd.qcut(D["absz"], 5, duplicates="drop")
    out["next by |ret0z|, all"] = D.groupby("aq", observed=True).apply(summ)
    out["next by |ret0z|, in profile"] = D[D.inprof].groupby("aq", observed=True).apply(summ)
    out["next by |ret0z|, outside"] = D[~D.inprof].groupby("aq", observed=True).apply(summ)
    D["rq"] = pd.qcut(D["rngz"], 5, duplicates="drop")
    out["next by range/vol, all"] = D.groupby("rq", observed=True).apply(summ)
    out["next by range/vol, in profile"] = D[D.inprof].groupby("rq", observed=True).apply(summ)
    quiet = D[D["absz"] <= D["absz"].quantile(0.4)]
    out["quiet days by coin"] = quiet.groupby("coin").apply(summ)
    out["quiet days by year"] = quiet.groupby("year").apply(summ)
    out["quiet days by win"] = quiet.groupby("win").apply(summ)
    out["quiet days next3 (grid)"] = summ(quiet[quiet.pos_idx % 3 == 0], "next3")
    # trend among quiet days
    quiet = quiet.copy()
    quiet["tr"] = pd.cut(quiet["ret60"], [-10, -0.1, 0.1, 100])
    out["quiet days by 60d trend"] = quiet.groupby("tr", observed=True).apply(summ)
    # in profile: down day rebound graded
    P = D[D.inprof].copy()
    P["zq"] = pd.qcut(P["ret0z"], 4, duplicates="drop")
    out["in profile next by ret0z quartile"] = P.groupby("zq", observed=True).apply(summ)
    out["in profile ret0z<0 by coin"] = P[P.ret0z < 0].groupby("coin").apply(summ)
    # correlation tests
    out["corr next vs absz all"] = float(D[["next", "absz"]].corr().iloc[0, 1])
    out["corr next vs ret0z all"] = float(D[["next", "ret0z"]].corr().iloc[0, 1])
    D["vq"] = pd.qcut(D["volz"], 5, duplicates="drop")
    out["next by volume z, all"] = D.groupby("vq", observed=True).apply(summ)
    return out
