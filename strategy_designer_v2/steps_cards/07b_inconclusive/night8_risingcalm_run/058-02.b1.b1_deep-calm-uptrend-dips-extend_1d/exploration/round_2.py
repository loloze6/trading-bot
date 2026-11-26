def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [1, 2, 3, 4, 5]
    for coin, wd in bars.items():
        for w, df in wd.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=30).std()
            hi5 = c.rolling(5, min_periods=5).max()
            depth = (c - hi5) / hi5 / sd30
            ret60 = c / c.shift(60) - 1
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in H:
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(df), h):
                    if pd.isna(fwd.iloc[i]) or pd.isna(depth.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, year=int(yr.iloc[i]),
                                     day=str(df["timestamp"].iloc[i])[:10],
                                     reg=df["regime"].iloc[i], depth=depth.iloc[i],
                                     ret60=ret60.iloc[i], fwd=fwd.iloc[i],
                                     usual=sd30.iloc[i] * np.sqrt(h)))
    R = pd.DataFrame(rows)
    R["ex"] = R["fwd"] - R.groupby(["coin", "h"])["fwd"].transform("mean")

    def tday(x, col):
        n = len(x); m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / n
        return m, (m / se if se > 0 else np.nan)

    out = {}
    R["ctx"] = np.where(R.reg == "unknown", "risingcalm",
               np.where(R.ret60 > 0.10, "rising_agit",
               np.where(R.ret60 < -0.10, "falling", np.where(R.ret60.notna(), "choppy", "na"))))
    neg = R[R.depth < 0].copy()
    neg["prod"] = -neg.depth / 3 * neg.ex          # >0: deeper dip -> higher excess (recovery)
    neg["strength"] = neg.ex / neg.usual
    res = []
    for (h, ctx), x in neg.groupby(["h", "ctx"]):
        m, t = tday(x, "prod"); me, te = tday(x, "ex")
        q = pd.qcut(x.depth.rank(method="first"), 3, labels=["deep", "mid", "shallow"])
        tq = x.groupby(q)["ex"].mean()
        res.append(dict(h=h, ctx=ctx, prod=m, prod_t=t, ex=me, ex_t=te,
                        deep_ex=tq["deep"], shallow_ex=tq["shallow"], n=len(x), days=x.day.nunique()))
    out["by_h_ctx"] = pd.DataFrame(res)
    rc = neg[neg.ctx == "risingcalm"]
    res = []
    for (h, yv), x in rc[rc.h.isin([1, 2, 3])].groupby(["h", "year"]):
        m, t = tday(x, "prod")
        res.append(dict(h=h, year=yv, prod=m, prod_t=t, n=len(x)))
    out["rc_by_year"] = pd.DataFrame(res)
    res = []
    for (h, cn), x in rc[rc.h.isin([2, 3])].groupby(["h", "coin"]):
        res.append(dict(h=h, coin=cn, prod=x["prod"].mean(), ex=x.ex.mean(), n=len(x)))
    out["rc_by_coin"] = pd.DataFrame(res)
    res = []
    for h in [1, 2, 3]:
        x = rc[rc.h == h]
        q = pd.qcut(x.depth.rank(method="first"), 5, labels=False)
        g = x.groupby(q).agg(depth=("depth", "mean"), ex=("ex", "mean"), strength=("strength", "mean"), n=("ex", "size"))
        g["h"] = h
        res.append(g.reset_index())
    out["rc_quintiles"] = pd.concat(res)
    return out
