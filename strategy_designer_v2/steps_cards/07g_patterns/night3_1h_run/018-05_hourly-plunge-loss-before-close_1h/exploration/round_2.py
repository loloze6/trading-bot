def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    rows = []
    for coin, wins in bars.items():
        usual = {}; drift = {}
        for h in [24, 72, 168]:
            allr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr.append(c[idx + h] / c[idx] - 1)
            allr = np.concatenate(allr); drift[h] = allr.mean(); usual[h] = allr.std()
        for w, b in wins.items():
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            r24 = c / c.shift(24) - 1
            z = r24 / r24.abs().rolling(720, min_periods=120).mean().shift(1)
            r7 = c / c.shift(168) - 1
            z7 = r7 / r7.abs().rolling(720, min_periods=120).mean().shift(1)
            cv = c.values
            for h in [24, 72, 168]:
                idx = np.arange(0, len(cv) - h, h)
                fr = cv[idx + h] / cv[idx] - 1
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "year": ts.dt.year.values[idx],
                                          "wn": int(w[1:]), "z": z.values[idx], "z7": z7.values[idx],
                                          "ex": fr - drift[h], "st": (fr - drift[h]) / usual[h], "tot": fr}))
    df = pd.concat(rows).dropna()
    def agg(g):
        return pd.Series({"n": len(g), "ex_bps": g.ex.mean() * 1e4, "tot_bps": g.tot.mean() * 1e4,
                          "strength": g.st.mean(), "t": g.ex.mean() / (g.ex.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    d24 = df[df.h == 24]
    big = d24[d24.z <= -2.5]
    out["drop z<=-2.5, 24h, by coin"] = big.groupby("coin").apply(agg)
    out["drop z<=-2.5, 24h, by year"] = big.groupby("year").apply(agg)
    big["half"] = np.where(big.wn <= 12, "w1-12", "w13-24")
    out["drop z<=-2.5, 24h, by half"] = big.groupby("half").apply(agg)
    d24["zb"] = pd.cut(d24.z, [-99, -4, -3, -2.5, -2, -1.5, -1, 99])
    out["24h fine grade of drop"] = d24.groupby("zb").apply(agg)
    # rise z7 continuation, 168h
    d168 = df[df.h == 168]
    up = d168[d168.z7 >= 1.5]
    out["z7>=1.5, 168h, by coin"] = up.groupby("coin").apply(agg)
    up = up.assign(half=np.where(up.wn <= 12, "w1-12", "w13-24"))
    out["z7>=1.5, 168h, by half"] = up.groupby("half").apply(agg)
    d72 = df[df.h == 72]
    up72 = d72[d72.z7 >= 1.5].assign(half=lambda x: np.where(x.wn <= 12, "w1-12", "w13-24"))
    out["z7>=1.5, 72h, by coin"] = up72.groupby("coin").apply(agg)
    out["z7>=1.5, 72h, by half"] = up72.groupby("half").apply(agg)
    return out
