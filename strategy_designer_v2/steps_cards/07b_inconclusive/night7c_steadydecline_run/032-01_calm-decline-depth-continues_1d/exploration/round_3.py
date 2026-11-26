def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r28 = c / c.shift(28) - 1
            rng = ((b["high"] - b["low"]) / b["close"]).astype(float)
            rr = rng.rolling(28).mean() / rng.rolling(90, min_periods=60).mean()
            vr = b["volume"].rolling(28).mean() / b["volume"].rolling(90, min_periods=60).mean()
            n = len(b)
            for h in [5, 10]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, day=str(b["timestamp"][i])[:10],
                                     fwd=c[i + h] / c[i] - 1, r28=r28[i], rr=rr[i], vr=vr[i]))
    d = pd.DataFrame(rows)
    d["mu"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["mu"]
    def clslope(x, xc, yc="ex"):
        x = x[[xc, yc, "day"]].dropna()
        if len(x) < 15: return dict(n=len(x), slope=np.nan, t=np.nan, days=0)
        X = x[xc] - x[xc].mean(); Y = x[yc] - x[yc].mean()
        bb = (X * Y).sum() / (X * X).sum()
        e = Y - bb * X
        s = (X * e).groupby(x["day"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (X * X).sum()
        return dict(n=len(x), slope=bb, t=bb / se, days=G)
    def clmean(x):
        x = x[["ex", "day"]].dropna()
        dev = (x["ex"] - x["ex"].mean()).groupby(x["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(x)
        return x["ex"].mean(), x["ex"].mean() / se, G
    out = {}
    f = d[(d.r28 < 0) & d.rr.notna()].copy()
    res = []
    for h in [5, 10]:
        fh = f[f.h == h].copy()
        fh["rrq"] = pd.qcut(fh["rr"], 3, labels=["quiet", "mid", "loud"])
        for q in ["quiet", "mid", "loud"]:
            x = fh[fh.rrq == q]
            r = clslope(x, "r28"); m, tm, G = clmean(x)
            r.update(h=h, rrq=q, mean_ex=m, t_mean=tm, rr_lo=x.rr.min(), rr_hi=x.rr.max())
            res.append(r)
        r = clslope(fh, "rr"); m, tm, G = clmean(fh); r.update(h=h, rrq="all_on_rr", mean_ex=m, t_mean=tm); res.append(r)
        fh["depthxrr"] = fh["r28"] * fh["rr"]
        r = clslope(fh, "depthxrr"); r.update(h=h, rrq="all_on_r28xrr"); res.append(r)
        fh["depthxquiet"] = fh["r28"] / fh["rr"]
        r = clslope(fh, "depthxquiet"); r.update(h=h, rrq="all_on_r28/rr"); res.append(r)
    out["falls_by_rr90"] = pd.DataFrame(res).round(4)
    f10 = f[f.h == 10].copy()
    f10["rrq"] = pd.qcut(f10["rr"], 3, labels=["quiet", "mid", "loud"])
    f10["dq"] = pd.qcut(f10["r28"], 3, labels=["deep", "mid", "shallow"])
    out["h10_rr_x_depth"] = f10.groupby(["rrq", "dq"])["ex"].agg(["mean", "count"]).round(4)
    loud = f10[f10.rrq == "loud"]
    out["h10_loud_by_coin"] = loud.groupby("coin")["ex"].agg(["mean", "count"]).round(4)
    out["h10_loud_by_window"] = loud.groupby("w")["ex"].agg(["mean", "count"]).round(4)
    return out
