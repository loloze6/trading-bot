def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd5": c.shift(-5) / c - 1,
                "ret28": c / c.shift(28) - 1,
                "ret5": c / c.shift(5) - 1,
                "ret1": r1,
                "prox": c / c.rolling(28).max(),
                "vol20": r1.rolling(20).std(),
                "rng": ((b["high"] - b["low"]) / c).rolling(5).mean() / ((b["high"] - b["low"]) / c).rolling(60, min_periods=20).mean(),
                "vrat": b["volume"].rolling(5).mean() / b["volume"].rolling(60, min_periods=20).mean(),
                "fc": b["forecast"], "reg": b["regime"],
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            df["pos"] = np.arange(len(df))
            rows.append(df[df["pos"] % 5 == 0])
    g = pd.concat(rows).dropna(subset=["fwd5"])
    g["ex"] = g["fwd5"] - g.groupby("coin")["fwd5"].transform("mean")

    def grp(col, q=5, sub=None):
        d = g if sub is None else sub
        d = d.dropna(subset=[col])
        k = pd.qcut(d[col].rank(method="first"), q, labels=False)
        o = d.groupby(k)["ex"].agg(["count", "mean", "std"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        o["xmean"] = d.groupby(k)[col].mean()
        return o.round(4)

    def slope(col, sub=None):
        d = (g if sub is None else sub).dropna(subset=[col, "ex"])
        s = stats.linregress(d[col], d["ex"])
        return pd.Series({"n": len(d), "slope": s.slope, "t": s.slope / s.stderr})

    up = g[g["ret28"] > 0]; dn = g[g["ret28"] <= 0]
    out = {}
    out["regime_ex"] = g.groupby(g["ret28"] > 0)["ex"].agg(["count", "mean"]).round(4)
    out["ret28_q_all"] = grp("ret28")
    out["prox_q_up"] = grp("prox", sub=up)
    out["prox_q_down"] = grp("prox", sub=dn)
    out["ret5_q"] = grp("ret5")
    out["ret1_q"] = grp("ret1")
    out["vol20_q"] = grp("vol20")
    out["rng_q"] = grp("rng")
    out["vrat_q"] = grp("vrat")
    out["slopes"] = pd.DataFrame({k: slope(k) for k in ["ret28", "ret5", "ret1", "prox", "vol20", "rng", "vrat"]}).T.round(4)
    out["slopes_down"] = pd.DataFrame({k: slope(k, dn) for k in ["ret28", "ret5", "prox", "rng", "vrat"]}).T.round(4)
    out["weekday"] = g.groupby("wd")["ex"].agg(["count", "mean"]).round(4)
    out["coin_up_prox_t"] = pd.DataFrame({c: slope("prox", up[up.coin == c]) for c in up.coin.unique()}).T.round(3)
    out["win_up_prox_t"] = pd.DataFrame({w: slope("prox", up[up.win == w]) for w in up.win.unique()}).T.round(3)
    # book days
    dd = pd.concat([d.assign(coin=c, win=w) for c, ws in data["days"].items() for w, d in ws.items()])
    bk = dd.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_by_win"] = bk.groupby(level=0).agg(["count", "mean", "std"]).round(5)
    return out
