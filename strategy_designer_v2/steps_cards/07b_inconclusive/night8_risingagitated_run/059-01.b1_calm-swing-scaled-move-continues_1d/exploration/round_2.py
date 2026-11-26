def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sm = (c / c.shift(20) - 1) / r.rolling(20).std()
            tr60 = c / c.shift(60) - 1
            n = len(b)
            for h in (5, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, sm=sm.iloc[i], fc=b["forecast"].iloc[i],
                                     calm=b["regime"].iloc[i] != "chop", fwd=c.iloc[i + h] / c.iloc[i] - 1,
                                     tr=tr60.iloc[i], day=str(b["timestamp"].iloc[i])[:10]))
    d = pd.DataFrame(rows).dropna(subset=["fwd"])
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    d["trend"] = pd.cut(d["tr"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])

    def reg(g, x):
        g = g.dropna(subset=[x])
        g = g[g[x] != 0]
        if len(g) < 30:
            return pd.Series(dict(n=len(g), days=g["day"].nunique(), slope=np.nan, t=np.nan))
        X = g[x].values; y = g["ex"].values
        Xm = X - X.mean()
        b1 = (Xm * (y - y.mean())).sum() / (Xm ** 2).sum()
        e = y - y.mean() - b1 * Xm
        s = pd.Series(Xm * e).groupby(g["day"].values).sum()
        se = np.sqrt((s ** 2).sum()) / (Xm ** 2).sum()
        return pd.Series(dict(n=len(g), days=g["day"].nunique(), slope=b1, t=b1 / se))

    out = {}
    cal = d[d.calm]
    out["calm_fc_vs_sm"] = pd.concat({"fc": cal.groupby("h").apply(lambda g: reg(g, "fc")),
                                      "sm": cal.groupby("h").apply(lambda g: reg(g, "sm"))})
    out["calm_trend_fc"] = cal.groupby(["h", "trend"]).apply(lambda g: reg(g, "fc"))
    out["corr_fc_sm_calm"] = float(cal[["fc", "sm"]].dropna().corr().iloc[0, 1])
    c5 = cal[(cal.h == 5) & cal.sm.notna()].copy()
    c5["dirmove"] = np.sign(c5["sm"]) * c5["ex"]
    out["calm_h5_dirmove_by_trend"] = c5.groupby("trend")["dirmove"].agg(["count", "mean", "std"])
    out["choppy_calm_by_coin_h5_sm"] = c5[c5.trend == "choppy"].groupby("coin").apply(lambda g: reg(g, "sm"))
    return out
