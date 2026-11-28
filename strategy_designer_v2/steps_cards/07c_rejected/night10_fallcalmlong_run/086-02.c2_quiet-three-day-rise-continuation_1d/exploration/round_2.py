def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].values; v = b["volume"].values.astype(float)
            n = len(b)
            vs = pd.Series(v)
            vr1 = np.log(vs / vs.shift(1).rolling(20).mean())
            cs = pd.Series(c)
            r1 = cs.pct_change(1)
            fc = b["regime"].isin(["trending", "unknown"])
            year = pd.to_datetime(b["timestamp"]).dt.year
            for h in [2, 3, 5, 7, 10]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=year[i], fc=bool(fc[i]),
                                     ret=c[i+h]/c[i]-1, vr1=vr1[i], r1=r1[i]))
    df = pd.DataFrame(rows)
    mu = df.groupby(["coin", "h"])["ret"].mean().rename("mu")
    df = df.join(mu, on=["coin", "h"]); df["ex"] = df["ret"] - df["mu"]
    f = df[df.fc].dropna(subset=["vr1", "r1"])
    def reg(g, x="vr1"):
        if len(g) < 8: return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        s = stats.linregress(g[x], g.ex)
        return pd.Series({"n": len(g), "slope": s.slope, "t": s.slope / s.stderr})
    up = f[f.r1 > 0]; dn = f[f.r1 < 0]
    out["up_vr1_slope_by_h"] = up.groupby("h").apply(reg)
    out["down_vr1_slope_by_h"] = dn.groupby("h").apply(reg)
    # signed: volume times direction of day
    f = f.copy(); f["sv"] = -np.sign(f.r1) * f.vr1  # high when light up day or heavy down day
    out["signed_slope_by_h"] = f.groupby("h").apply(lambda g: reg(g, "sv"))
    d5 = dn[dn.h.isin([5])]
    out["down5_by_coin"] = d5.groupby("coin").apply(reg)
    out["down5_by_year"] = d5.groupby("year").apply(reg)
    u5 = up[up.h == 5]
    out["up5_by_coin"] = u5.groupby("coin").apply(reg)
    out["up5_by_year"] = u5.groupby("year").apply(reg)
    def summ(g):
        return pd.Series({"n": len(g), "mean_ex": g.ex.mean(), "t": g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g) > 2 else np.nan})
    dnh = dn.copy(); dnh["q"] = dnh.groupby("h")["vr1"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["down_by_vol_tercile_h"] = dnh.groupby(["h", "q"]).apply(summ)
    # heavy down day sized by fall size too
    dnh["big"] = dnh.groupby("h")["r1"].transform(lambda s: s < s.median())
    out["down_5_vol_tercile_by_bigfall"] = dnh[dnh.h == 5].groupby(["big", "q"]).apply(summ)
    return out
