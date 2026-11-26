def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allret = []
        for w, b in wins.items():
            c = b["close"].values
            allret.append(pd.Series(c).pct_change().dropna().values)
        mu = np.concatenate(allret).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            ts = pd.to_datetime(b["timestamp"])
            d = b.get("debug_info.components.depth.last_history_value")
            for h in (1, 3, 5, 10):
                fwd = c.shift(-h) / c - 1
                df = pd.DataFrame({
                    "coin": coin, "w": w, "h": h, "pos": np.arange(len(b)),
                    "day": ts.dt.normalize(), "year": ts.dt.year,
                    "depth": -d if d is not None else np.nan,
                    "chop": b["regime"] == "unknown",
                    "up": b["close"] > b["open"],
                    "ex": fwd - ((1 + mu) ** h - 1),
                    "ret1d": c.pct_change(),
                })
                rows.append(df)
    D = pd.concat(rows)
    D = D[D["chop"] & D["depth"].notna() & D["ex"].notna() & (D["depth"] > 0)]

    def slope(g):
        if len(g) < 30:
            return pd.Series({"n": len(g)})
        r = stats.linregress(g["depth"], g["ex"])
        return pd.Series({"n": len(g), "slope_bp": r.slope * 1e4, "t": r.slope / r.stderr,
                          "mean_ex_%": g["ex"].mean() * 100})
    out = {}
    out["by horizon (non-overlap grid)"] = D[D["pos"] % D["h"] == 0].groupby("h").apply(slope)
    D1 = D[D["h"] == 1].copy()
    out["h1 by coin"] = D1.groupby("coin").apply(slope)
    out["h1 by year"] = D1.groupby("year").apply(slope)
    out["h1 by up/down"] = D1.groupby("up").apply(slope)
    D1["q"] = pd.qcut(D1["depth"], 5, labels=False)
    out["h1 depth quintile"] = D1.groupby("q").agg(n=("ex", "size"), depth=("depth", "mean"),
                                                   mean_ex_pct=("ex", lambda x: x.mean() * 100),
                                                   t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    D3 = D[(D["h"] == 3) & (D["pos"] % 3 == 0)].copy()
    D3["q"] = pd.qcut(D3["depth"], 5, labels=False)
    out["h3 depth quintile"] = D3.groupby("q").agg(n=("ex", "size"), mean_ex_pct=("ex", lambda x: x.mean() * 100),
                                                   t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    D5 = D[(D["h"] == 5) & (D["pos"] % 5 == 0)].copy()
    out["h5 by up/down"] = D5.groupby("up").apply(slope)
    out["h5 by coin"] = D5.groupby("coin").apply(slope)
    return out
