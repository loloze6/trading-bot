def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r14 = c / c.shift(14) - 1
            z = (r14 - r14.rolling(60, min_periods=20).mean()) / r14.rolling(60, min_periods=20).std()
            r1 = c.pct_change()
            vr = r1.rolling(20).std() / r1.rolling(20).std().rolling(60, min_periods=20).mean()
            for h in (1, 2, 5, 10):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(b), h)
                for i in idx:
                    if i + h >= len(b):
                        continue
                    rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b["timestamp"].iloc[i]).year, h=h,
                                     calm=b["regime"].iloc[i] == "trending", fc=b["forecast"].iloc[i],
                                     z=z.iloc[i], vr=vr.iloc[i], fwd=fwd.iloc[i]))
    df = pd.DataFrame(rows)
    df["dfwd"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")
    def slope(g, x="z"):
        g = g.dropna(subset=[x, "dfwd"])
        if len(g) < 30:
            return pd.Series(dict(n=len(g), b=np.nan, t=np.nan))
        r = stats.linregress(g[x], g["dfwd"])
        return pd.Series(dict(n=len(g), b=r.slope * 1e4, t=r.slope / r.stderr))
    out = {}
    out["by h & calm (z, slope bp per z)"] = df.groupby(["h", "calm"]).apply(slope)
    d2 = df[df.h == 2]
    out["h2 calm: fc vs z corr"] = float(d2[d2.calm][["fc", "z"]].corr().iloc[0, 1])
    out["h2 by coin & calm"] = d2.groupby(["coin", "calm"]).apply(slope).unstack()
    out["h2 by year & calm"] = d2.groupby(["year", "calm"]).apply(slope).unstack()
    d2 = d2.copy()
    d2["vrq"] = pd.qcut(d2["vr"], 5, labels=False)
    out["h2 by vr quintile"] = d2.groupby("vrq").apply(slope)
    d2["zq"] = pd.qcut(d2["z"], 10, labels=False)
    out["h2 mean dfwd % by z decile"] = d2.groupby("zq")["dfwd"].agg(["count", "mean"]).assign(mean=lambda x: x["mean"] * 100)
    d2["side"] = np.sign(d2["z"])
    out["h2 by side & calm"] = d2.groupby(["side", "calm"]).apply(slope).unstack()
    for h in (5, 10):
        dh = df[df.h == h].copy()
        dh["side"] = np.sign(dh["z"])
        out[f"h{h} by side"] = dh.groupby("side").apply(slope)
    return out
