def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r1.rolling(20).std()
            stretch = (c / sma - 1) / sd
            ret60 = c / c.shift(60) - 1
            ret20 = c / c.shift(20) - 1
            vol20 = sd
            volrank = vol20.rolling(60, min_periods=30).rank(pct=True)
            rng = (b["high"] - b["low"]) / c
            for h in (1, 3, 10):
                pass
            f10 = c.shift(-10) / c - 1
            f3 = c.shift(-3) / c - 1
            f1 = c.shift(-1) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "year": pd.to_datetime(b["timestamp"]).dt.year,
                               "stretch": stretch, "ret60": ret60, "ret20": ret20, "r1": r1,
                               "r1z": r1 / sd.shift(1), "volrank": volrank, "rng": rng / sd,
                               "f10": f10, "f3": f3, "f1": f1,
                               "fc": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    # drift per coin over 10 bars on grid
    g10 = D[D.pos % 10 == 0]
    drift10 = g10.groupby("coin")["f10"].mean()
    D["u10"] = D["f10"] - D["coin"].map(drift10)
    g3 = D[D.pos % 3 == 0]
    drift3 = g3.groupby("coin")["f3"].mean()
    D["u3"] = D["f3"] - D["coin"].map(drift3)
    D["u1"] = D["f1"] - D["coin"].map(D.groupby("coin")["f1"].mean())
    D["trend"] = np.where(D.ret60 > .1, "rising", np.where(D.ret60 < -.1, "falling", np.where(D.ret60.notna(), "choppy", "na")))
    out = {}
    G = D[(D.pos % 10 == 0)].dropna(subset=["stretch", "u10"])
    def tab(df, key, val):
        a = df.groupby(key)[val].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.drop(columns="std")
    G = G.copy(); G["sq"] = pd.qcut(G.stretch, 5, labels=False)
    out["10d unusual by stretch quintile, all"] = tab(G, "sq", "u10")
    out["10d unusual by trend x stretch quintile"] = tab(G, ["trend", "sq"], "u10")
    G3 = D[(D.pos % 3 == 0)].dropna(subset=["r1z", "u3"]).copy()
    G3["zq"] = pd.qcut(G3.r1z, 5, labels=False)
    out["3d unusual by 1d move z quintile x trend"] = tab(G3, ["trend", "zq"], "u3")
    G3["rq"] = pd.qcut(G3.rng, 5, labels=False, duplicates="drop")
    out["3d unusual by range/sd quintile"] = tab(G3, "rq", "u3")
    G1 = D.dropna(subset=["u1"])
    out["1d unusual by weekday"] = tab(G1, "wd", "u1")
    G3["vq"] = pd.qcut(G3.volrank, 3, labels=False, duplicates="drop")
    out["3d unusual by 20d return sign x volrank"] = tab(G3.assign(s=np.sign(G3.ret20)), ["vq", "s"], "u3")
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    DD = pd.concat(dd)
    out["book by window"] = DD.groupby("w")[["book_return", "coin_return"]].mean()
    out["book by coin"] = DD.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "count"])
    return out
