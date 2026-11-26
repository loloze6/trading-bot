def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r28 = c / c.shift(28) - 1
            rng = ((b["high"] - b["low"]) / b["close"]).astype(float)
            rr = rng.rolling(28).mean() / rng.rolling(360, min_periods=100).mean()
            vr = b["volume"].rolling(28).mean() / b["volume"].rolling(360, min_periods=100).mean()
            z = (r28 - r28.rolling(60, min_periods=20).mean()) / r28.rolling(60, min_periods=20).std()
            n = len(b)
            for h in [3, 5, 10]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, day=str(b["timestamp"][i])[:10],
                                     fwd=c[i + h] / c[i] - 1, r28=r28[i], rr=rr[i], vr=vr[i], z=z[i],
                                     regime=b["regime"][i], fc=b["forecast"][i]))
    d = pd.DataFrame(rows)
    d["mu"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["mu"]
    d["calm"] = d["regime"] == "trending"
    out = {}
    def clslope(x, xc, yc="ex"):
        x = x[[xc, yc, "day"]].dropna()
        if len(x) < 15: return dict(n=len(x), slope=np.nan, t=np.nan, days=0)
        X = x[xc] - x[xc].mean(); Y = x[yc] - x[yc].mean()
        b = (X * Y).sum() / (X * X).sum()
        e = Y - b * X
        s = (X * e).groupby(x["day"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (X * X).sum()
        return dict(n=len(x), slope=b, t=b / se, days=G)
    res = []
    for h in [3, 5, 10]:
        for nm, m in [("calm_fall", lambda q: q.calm & (q.r28 < 0)),
                      ("all_fall", lambda q: q.r28 < 0),
                      ("quiet_fall_rr<1", lambda q: (q.rr < 1) & (q.r28 < 0)),
                      ("loud_fall_rr>1", lambda q: (q.rr >= 1) & (q.r28 < 0)),
                      ("quiet_fall_rr<1_vr<1", lambda q: (q.rr < 1) & (q.vr < 1) & (q.r28 < 0))]:
            x = d[(d.h == h) & m(d)]
            for xc in ["r28", "z", "rr"]:
                r = clslope(x, xc); r.update(h=h, set=nm, x=xc, mean_ex=x["ex"].mean())
                res.append(r)
    out["slopes"] = pd.DataFrame(res)[["h", "set", "x", "n", "days", "slope", "t", "mean_ex"]].round(4)
    # graded interaction: ex on r28*(quietness) among falls
    f = d[(d.r28 < 0)].copy()
    f["quiet_depth"] = f["r28"] * (1 / f["rr"])
    res2 = []
    for h in [3, 5, 10]:
        r = clslope(f[f.h == h], "quiet_depth"); r.update(h=h); res2.append(r)
    out["falls_ex_on_r28_over_rr"] = pd.DataFrame(res2).round(4)
    # falls h10 by rr tercile and depth half
    f10 = f[f.h == 10].dropna(subset=["rr"]).copy()
    f10["rrq"] = pd.qcut(f10["rr"], 3, labels=["quiet", "mid", "loud"])
    f10["dq"] = pd.qcut(f10["r28"], 2, labels=["deep", "shallow"])
    out["falls_h10_rr_x_depth"] = f10.groupby(["rrq", "dq"])["ex"].agg(["mean", "count"]).round(4)
    out["share_calm_bars"] = float(d[d.h == 3]["calm"].mean())
    return out
