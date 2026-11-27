def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            s20 = r.rolling(20, min_periods=15).std().shift(0)
            nxt = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]).astype(float)
            cl = (c - b["low"]) / rng.replace(0, np.nan)
            ret5 = c / c.shift(5) - 1
            ret30 = c / c.shift(30) - 1
            vol5 = r.rolling(5).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "r": r, "z": r / s20, "absz": (r / s20).abs(),
                "nxt": nxt, "cl": cl, "rngz": (rng / c) / s20,
                "ret5z": ret5 / (s20 * np.sqrt(5)), "ret30": ret30,
                "volratio": vol5 / s20,
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "pos_gain": b["postRebalance_current_allocation"].astype(float) * nxt,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].transform("mean")
    d["adj"] = d["nxt"] - drift
    d = d.dropna(subset=["adj"])
    out = {}

    def tab(col, q=5):
        x = d.dropna(subset=[col]).copy()
        x["bin"] = pd.qcut(x[col], q, duplicates="drop")
        g = x.groupby("bin", observed=True)["adj"]
        t = g.agg(["count", "mean", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t[["count", "mean", "t"]]

    out["by signed z (r/s20)"] = tab("z", 7)
    out["by abs z"] = tab("absz", 5)
    out["by close location"] = tab("cl", 5)
    out["by range/s20"] = tab("rngz", 5)
    out["by 5d scaled ret"] = tab("ret5z", 5)
    out["by 30d ret"] = tab("ret30", 5)
    out["by vol5/vol20"] = tab("volratio", 5)
    g = d.groupby("wd")["adj"].agg(["count", "mean", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["by weekday"] = g[["count", "mean", "t"]]
    g = d.groupby("coin")["adj"].agg(["count", "mean"]); out["coins"] = g
    # spearman overall
    for col in ["z", "cl", "ret5z", "ret30", "rngz", "volratio"]:
        x = d.dropna(subset=[col])
        rho, p = stats.spearmanr(x[col], x["adj"])
        out[f"spearman {col}"] = f"rho {rho:.4f} p {p:.4f} n {len(x)}"
    # close location within flat days vs within big up days
    x = d.dropna(subset=["cl", "z"]).copy()
    x["zb"] = pd.cut(x["z"], [-99, -1, -0.25, 0.25, 1, 99])
    x["cb"] = pd.cut(x["cl"], [0, 0.33, 0.67, 1.0001], include_lowest=True)
    out["z x close loc mean adj"] = x.pivot_table(index="zb", columns="cb", values="adj", aggfunc="mean", observed=True)
    out["z x close loc count"] = x.pivot_table(index="zb", columns="cb", values="adj", aggfunc="count", observed=True)
    # 30d trend x close location
    x = x.dropna(subset=["ret30"])
    x["tb"] = pd.cut(x["ret30"], [-9, -0.1, 0.1, 9])
    out["trend30 x close loc mean adj"] = x.pivot_table(index="tb", columns="cb", values="adj", aggfunc="mean", observed=True)
    out["trend30 x close loc count"] = x.pivot_table(index="tb", columns="cb", values="adj", aggfunc="count", observed=True)
    # book days
    dl = []
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            dl.append(dd.assign(coin=coin, win=w))
    dd = pd.concat(dl).dropna(subset=["book_return"])
    out["book by year"] = dd.assign(year=pd.to_datetime(dd["day"]).dt.year).groupby("year")["book_return"].agg(["count", "mean", "sum"])
    return out
