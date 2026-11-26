def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 15: continue
            c = b["close"].values; h = b["high"].values; l = b["low"].values; o = b["open"].values
            rng = h - l
            cl = np.where(rng > 0, (c - l) / rng, np.nan)
            s = pd.Series(c)
            r1 = s.pct_change().values
            vol20 = s.pct_change().rolling(20).std().values
            p20 = s.pct_change(20).values
            p60 = s.pct_change(60).values
            relrng = rng / c
            rz = relrng / pd.Series(relrng).rolling(20).mean().shift(1).values
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for H in (2, 5):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, w=w, H=H, cl=cl[i], r1=r1[i], vol=vol20[i], p20=p20[i], p60=p60[i],
                                     rz=rz[i], fwd=c[i + H] / c[i] - 1, day=ts.iloc[i].normalize(), yr=ts.iloc[i].year))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby(["coin", "H"])["fwd"].transform("mean")
    df["un"] = df["fwd"] - df["drift"]
    def summ(g):
        x = g.dropna(subset=["un"])
        if len(x) < 3: return pd.Series(dict(n=len(x), days=0, mean=np.nan, t_day=np.nan))
        m = x["un"].mean()
        dev = (x["un"] - m).groupby(x["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(x)
        return pd.Series(dict(n=len(x), days=D, mean=m, t_day=m / se))
    for H in (2, 5):
        d = df[(df.H == H)].dropna(subset=["rz", "r1"]).copy()
        d["rzq"] = pd.qcut(d["rz"], 5, labels=False)
        d["up"] = d["r1"] > 0
        out[f"H{H} range-z quintile x day up"] = d.groupby(["rzq", "up"]).apply(summ)
        top = d[d.rzq == 4].copy()
        top["clq"] = pd.cut(top["cl"], [0, .33, .67, 1.0001], include_lowest=True, labels=["low", "mid", "high"])
        out[f"H{H} top range-z by close location"] = top.groupby("clq").apply(summ)
        out[f"H{H} top range-z down day by year"] = top[~top.up].groupby("yr").apply(summ)
        top["p20s"] = pd.cut(top["p20"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
        out[f"H{H} top range-z down day by 20d trend"] = top[~top.up].groupby("p20s").apply(summ)
    d = df[df.H == 5].dropna(subset=["p20", "cl"]).copy()
    d["hc"] = pd.cut(d["cl"], [0, .6, .8, .9, 1.0001], include_lowest=True)
    fall = d[d.p20 < -0.1].copy()
    out["H5 20d-fall by close location"] = fall.groupby("hc").apply(summ)
    hcf = fall[fall.cl >= 0.8].copy()
    out["H5 20d-fall high close by year"] = hcf.groupby("yr").apply(summ)
    hcf["volq"] = pd.qcut(hcf["vol"], 2, labels=["calmer", "wilder"])
    out["H5 20d-fall high close by vol half"] = hcf.groupby("volq").apply(summ)
    hcf["p20q"] = pd.qcut(hcf["p20"], 2, labels=["deeper", "milder"])
    out["H5 20d-fall high close by depth"] = hcf.groupby("p20q").apply(summ)
    d2 = df[df.H == 2].dropna(subset=["p20", "cl"])
    f2 = d2[d2.p20 < -0.1].copy()
    f2["hc"] = pd.cut(f2["cl"], [0, .6, .8, .9, 1.0001], include_lowest=True)
    out["H2 20d-fall by close location"] = f2.groupby("hc").apply(summ)
    p60 = d.dropna(subset=["p60"]).copy()
    p60["tr"] = pd.cut(p60["p60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    p60["hi"] = p60["cl"] >= 0.8
    out["H5 60d trend x high close (where known)"] = p60.groupby(["tr", "hi"]).apply(summ)
    return out
