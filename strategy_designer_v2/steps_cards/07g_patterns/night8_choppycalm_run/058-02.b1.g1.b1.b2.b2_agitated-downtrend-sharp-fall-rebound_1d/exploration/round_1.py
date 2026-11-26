def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20, min_periods=20).std()
            z = r / sd
            rng = (b["high"] - b["low"]).astype(float)
            clv = ((c - b["low"]) / rng.replace(0, np.nan))
            n1 = c.shift(-1) / c - 1
            n3 = c.shift(-3) / c - 1
            tr60 = c / c.shift(60) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "day": ts.dt.floor("D"), "wd": ts.dt.dayofweek,
                               "z": z, "clv": clv, "x1": n1 - mu, "x3": n3 - 3 * mu,
                               "fa": (b["regime"] == "unknown").astype(int), "tr60": tr60,
                               "pos": b["postRebalance_current_allocation"].astype(float),
                               "pos3": (np.arange(len(b)) % 3 == 0), "sd": sd})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)

    def ct(x, day):
        m = x.notna()
        x = x[m]; day = day[m]
        if len(x) < 10: return np.nan
        mean = x.mean()
        g = (x - mean).groupby(day).sum()
        se = np.sqrt((g ** 2).sum()) / len(x)
        return mean / se if se > 0 else np.nan

    def tab(sub, key, col="x1"):
        out = []
        for k, g in sub.groupby(key, observed=True):
            out.append({"bucket": str(k), "n": len(g.dropna(subset=[col])), "mean%": 100 * g[col].mean(),
                        "t_day": ct(g[col], g["day"])})
        return pd.DataFrame(out)

    d["zb"] = pd.cut(d["z"], [-99, -2.5, -1.5, -0.75, 0, 0.75, 1.5, 2.5, 99])
    d["cb"] = pd.cut(d["clv"], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    res = {}
    res["share_fa"] = d["fa"].mean()
    res["z_in_FA_next1"] = tab(d[d.fa == 1], "zb")
    res["z_out_FA_next1"] = tab(d[d.fa == 0], "zb")
    s3 = d[d.pos3]
    res["z_in_FA_next3_grid"] = tab(s3[s3.fa == 1], "zb", "x3")
    res["z_out_FA_next3_grid"] = tab(s3[s3.fa == 0], "zb", "x3")
    res["clv_in_FA_next1"] = tab(d[d.fa == 1], "cb")
    res["clv_out_FA_next1"] = tab(d[d.fa == 0], "cb")
    o = d[d.fa == 0].copy()
    o["trb"] = pd.cut(o["tr60"], [-9, -0.1, 0.1, 99])
    o["k"] = o["trb"].astype(str) + "|" + o["zb"].astype(str)
    res["out_by_trend_z"] = tab(o, "k")
    res["wd_all_next1"] = tab(d, "wd")
    res["wd_FA_next1"] = tab(d[d.fa == 1], "wd")
    return res
