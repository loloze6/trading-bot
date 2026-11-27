def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r1 = cl.pct_change()
            hi20 = b["high"].rolling(20).max()
            sd20 = r1.rolling(20).std()
            depth = (hi20 - cl) / hi20 / sd20
            ret60 = cl / cl.shift(60) - 1
            sd30 = r1.rolling(30).std()
            n = len(b)
            for h in (1, 10):
                fwd = cl.shift(-h) / cl - 1
                idx = np.arange(0, n, h)
                d = pd.DataFrame({"coin": c, "w": w, "h": h, "depth": depth.iloc[idx].values,
                                  "up": (r1.iloc[idx] > 0).values, "r1": r1.iloc[idx].values,
                                  "ret60": ret60.iloc[idx].values, "sd30": sd30.iloc[idx].values,
                                  "fwd": fwd.iloc[idx].values,
                                  "alloc": b["postRebalance_current_allocation"].iloc[idx].values,
                                  "wd": pd.to_datetime(b["timestamp"].iloc[idx]).dt.weekday.values})
                rows.append(d)
    D = pd.concat(rows).dropna(subset=["fwd", "depth", "r1"])
    # normal drift per coin & h
    D["drift"] = D.groupby(["coin", "h"])["fwd"].transform("mean")
    D["un"] = D["fwd"] - D["drift"]
    D["prof"] = np.where(D["ret60"] > .1, "rising", np.where(D["ret60"] < -.1, "falling", "choppy"))
    D.loc[D["ret60"].isna(), "prof"] = "na"
    D["dq"] = D.groupby(["coin", "h"])["depth"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    def tab(g):
        return pd.Series({"n": len(g), "mean_un": g["un"].mean(), "t": g["un"].mean() / (g["un"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    for h in (1, 10):
        Dh = D[D.h == h]
        out[f"h{h} by profile x depthQ (unusual move)"] = Dh.groupby(["prof", "dq"]).apply(tab).unstack("dq")["t"].round(2)
        out[f"h{h} choppy by up x depthQ mean"] = Dh[Dh.prof == "choppy"].groupby(["up", "dq"]).apply(tab).round(4)
    D10 = D[D.h == 10].copy()
    D10["volq"] = D10.groupby("coin")["sd30"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    D10["moveq"] = D10.groupby("coin")["r1"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["h10 all by prior-day move quintile"] = D10.groupby("moveq").apply(tab).round(4)
    out["h10 all by vol tercile x prof"] = D10.groupby(["prof", "volq"]).apply(tab).round(4)
    D1 = D[D.h == 1]
    out["h1 by weekday"] = D1.groupby("wd").apply(tab).round(4)
    # book
    br = []
    for c in days:
        for w, d in days[c].items():
            br.append(d.assign(coin=c, w=w))
    B = pd.concat(br)
    B["lev"] = np.nan
    out["book daily by coin"] = B.groupby("coin")["book_return"].agg(["mean", "std", "min", "max", "count"]).round(4)
    out["book daily by window"] = B.groupby("w")["book_return"].agg(["mean", "std", "min"]).round(4)
    # allocation stats
    al = pd.concat([b["postRebalance_current_allocation"] for c in bars for b in bars[c].values()])
    out["alloc abs when nonzero"] = al[al != 0].abs().describe().round(3)
    # trades
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values() if len(t)])
    out["trades"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median", "min", "max"]).round(3)
    return out
