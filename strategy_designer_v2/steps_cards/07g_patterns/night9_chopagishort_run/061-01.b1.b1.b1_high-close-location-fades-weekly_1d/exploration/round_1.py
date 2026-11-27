def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 15: continue
            c = b["close"].values; h = b["high"].values; l = b["low"].values; o = b["open"].values
            rng = h - l
            cl = np.where(rng > 0, (c - l) / rng, np.nan)
            r1 = pd.Series(c).pct_change().values
            n = len(b)
            vol20 = pd.Series(r1).rolling(20).std().values
            ret5p = pd.Series(c).pct_change(5).values
            ret20p = pd.Series(c).pct_change(20).values
            relrng = rng / c
            relrng_z = relrng / pd.Series(relrng).rolling(20).mean().values
            ts = pd.to_datetime(b["timestamp"])
            for H in (2, 5):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, w=w, H=H, cl=cl[i], r1=r1[i], vol=vol20[i],
                                     p5=ret5p[i], p20=ret20p[i], rz=relrng_z[i],
                                     fwd=c[i + H] / c[i] - 1, wd=ts.iloc[i].weekday(),
                                     yr=ts.iloc[i].year, pos=b["postRebalance_current_allocation"].iloc[i],
                                     reg=b["regime"].iloc[i]))
    df = pd.DataFrame(rows)
    # drift per coin per H
    df["drift"] = df.groupby(["coin", "H"])["fwd"].transform("mean")
    df["un"] = df["fwd"] - df["drift"]
    def summ(g):
        x = g["un"].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    for H in (2, 5):
        d = df[df.H == H].copy()
        d["clq"] = pd.cut(d["cl"], [0, .2, .4, .6, .8, .9, 1.0001], include_lowest=True)
        out[f"H{H} unusual by close location (all bars)"] = d.groupby("clq").apply(summ)
        d["r1q"] = pd.qcut(d["r1"], 5)
        out[f"H{H} by prior 1d return quintile"] = d.groupby("r1q").apply(summ)
        d["p5q"] = pd.qcut(d["p5"], 5)
        out[f"H{H} by prior 5d return quintile"] = d.groupby("p5q").apply(summ)
        d["rzq"] = pd.qcut(d["rz"], 5)
        out[f"H{H} by range vs 20d avg quintile"] = d.groupby("rzq").apply(summ)
    d = df[df.H == 5].copy()
    out["H5 by weekday"] = d.groupby("wd").apply(summ)
    out["H5 by year"] = d.groupby("yr").apply(summ)
    d["volq"] = pd.qcut(d["vol"], 3)
    d["clhi"] = d["cl"] >= 0.8
    out["H5 by vol tercile x high close"] = d.groupby(["volq", "clhi"]).apply(summ)
    d["p20s"] = pd.cut(d["p20"], [-9, -0.1, 0.1, 9])
    out["H5 by 20d trend x high close"] = d.groupby(["p20s", "clhi"]).apply(summ)
    # book daily
    dd = []
    for coin, ws in data["days"].items():
        for w, x in ws.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    dd = pd.concat(dd)
    bk = dd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book daily by window"] = bk.groupby(level=0).agg(["mean", "std", "count"])
    # trades
    tr = []
    for coin, ws in data["trades"].items():
        for w, x in ws.items():
            if len(x): x = x.copy(); x["coin"] = coin; x["w"] = w; tr.append(x)
    tr = pd.concat(tr)
    out["trades by side"] = tr.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    tr["days"] = tr["duration_minutes"] / 1440
    tr["dq"] = pd.cut(tr["days"], [0, 3, 5, 6, 10, 1000])
    out["trades by duration"] = tr.groupby("dq")["net_profit_loss_percent"].agg(["count", "mean"])
    out["trades by coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    tr["efq"] = pd.qcut(tr["entry_forecast"], 3, duplicates="drop")
    out["trades by entry forecast"] = tr.groupby("efq")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
