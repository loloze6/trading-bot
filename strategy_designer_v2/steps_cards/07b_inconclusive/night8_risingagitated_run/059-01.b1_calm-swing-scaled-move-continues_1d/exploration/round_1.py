def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            ret20 = c / c.shift(20) - 1
            sd20 = r.rolling(20).std()
            sm = ret20 / sd20
            tr60 = c / c.shift(60) - 1
            year = pd.to_datetime(b["timestamp"]).dt.year
            n = len(b)
            for h in (2, 5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, sm=sm.iloc[i],
                                     fc=b["forecast"].iloc[i], calm=b["regime"].iloc[i] != "chop",
                                     fwd=c.iloc[i + h] / c.iloc[i] - 1, tr=tr60.iloc[i], yr=year.iloc[i],
                                     day=str(b["timestamp"].iloc[i])[:10]))
    d = pd.DataFrame(rows).dropna(subset=["sm", "fwd"])
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]

    def reg(g, x="sm"):
        g = g.dropna(subset=[x])
        if len(g) < 30:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        X = g[x].values; y = g["ex"].values
        Xm = X - X.mean()
        b1 = (Xm * (y - y.mean())).sum() / (Xm ** 2).sum()
        e = y - y.mean() - b1 * Xm
        s = pd.Series(Xm * e).groupby(g["day"].values).sum()
        se = np.sqrt((s ** 2).sum()) / (Xm ** 2).sum()
        return pd.Series(dict(n=len(g), slope=b1, t=b1 / se))

    out = {}
    out["by_h_calm"] = d.groupby(["h", "calm"]).apply(reg)
    d5 = d[d.h == 5]
    out["h5_by_coin_calm"] = d5.groupby(["coin", "calm"]).apply(reg)
    out["h5_by_year_calm"] = d5.groupby(["yr", "calm"]).apply(reg)
    d5 = d5.copy()
    d5["trend"] = pd.cut(d5["tr"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    out["h5_by_trend_calm"] = d5.groupby(["trend", "calm"]).apply(reg)
    d5["side"] = np.where(d5["sm"] > 0, "up", "down")
    d5["dirmove"] = np.sign(d5["sm"]) * d5["ex"]
    d5["q"] = pd.qcut(d5["sm"].abs(), 5, labels=False)
    out["h5_dirmove_side_q_calm"] = d5.groupby(["calm", "side", "q"])["dirmove"].agg(["count", "mean"])
    d10 = d[d.h == 10].copy()
    d10["trend"] = pd.cut(d10["tr"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    out["h10_by_trend_calm"] = d10.groupby(["trend", "calm"]).apply(reg)
    return out
