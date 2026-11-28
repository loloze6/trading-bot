def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20).std()
            H20 = h.rolling(20).max(); H60 = h.rolling(60, min_periods=40).max()
            d20 = ((c - H20) / H20) / sd
            d60 = ((c - H60) / H60) / sd
            since = h.rolling(20).apply(lambda x: 19 - int(np.argmax(x)), raw=True)
            ret5 = c / c.shift(5) - 1
            ret5s = ret5 / (sd * np.sqrt(5))
            ppvcol = "debug_info.components.peak_depth.post_pipeline_value"
            ppv = b[ppvcol] if ppvcol in b else pd.Series([np.nan]*len(b))
            n = len(b)
            for hz in [2, 3, 5, 7]:
                fwd = c.shift(-hz) / c - 1
                for i in range(0, n, hz):
                    if np.isnan(fwd.iloc[i]) or np.isnan(d20.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, win=w, hz=hz, d20=d20.iloc[i], d60=d60.iloc[i],
                                     since=since.iloc[i], ret5s=ret5s.iloc[i], ppv=ppv.iloc[i],
                                     ret=fwd.iloc[i], regime=b["regime"].iloc[i],
                                     day=str(b["timestamp"].iloc[i])[:10]))
    df = pd.DataFrame(rows)
    drift = df.groupby(["coin", "hz"])["ret"].mean().rename("drift")
    df = df.join(drift, on=["coin", "hz"]); df["ex"] = df["ret"] - df["drift"]
    def ct(d, x, y="ex"):
        d = d.dropna(subset=[x, y])
        if len(d) < 20: return np.nan, np.nan, len(d)
        X = d[x].values; Y = d[y].values
        xm = X - X.mean(); b1 = (xm * (Y - Y.mean())).sum() / (xm**2).sum()
        e = Y - Y.mean() - b1 * xm
        s = pd.Series(xm * e).groupby(d["day"].values).sum()
        G = len(s); v = (s**2).sum() / (xm**2).sum()**2 * G / (G - 1)
        return b1, b1 / np.sqrt(v), len(d)
    out = {}
    fc = df[df.regime == "unknown"]
    res = []
    for hz in [2, 3, 5, 7]:
        d = fc[fc.hz == hz]
        for x in ["d20", "d60", "ppv", "since", "ret5s"]:
            s, t, nn = ct(d, x)
            res.append(dict(hz=hz, x=x, n=nn, slope=s, t_cl=t))
    out["fc_slopes"] = pd.DataFrame(res)
    d3 = fc[fc.hz == 3].copy()
    out["corr_d20_ppv"] = float(d3[["d20", "ppv"]].dropna().corr().iloc[0, 1])
    d3["sinceq"] = pd.cut(d3["since"], [-1, 2, 6, 12, 19])
    out["fc3_by_since"] = d3.groupby("sinceq").agg(ex=("ex", "mean"), tot=("ret", "mean"), n=("ex", "size"))
    d3["r5q"] = pd.qcut(d3["ret5s"], 4, labels=False)
    out["fc3_by_ret5s"] = d3.groupby("r5q").agg(r5=("ret5s", "mean"), ex=("ex", "mean"), tot=("ret", "mean"), n=("ex", "size"))
    d5 = fc[fc.hz == 5].copy(); d5["q"] = pd.qcut(d5["d20"], 4, labels=False)
    out["fc5_by_d20"] = d5.groupby("q").agg(dep=("d20", "mean"), ex=("ex", "mean"), tot=("ret", "mean"), n=("ex", "size"))
    d3["dq"] = pd.cut(d3["d20"], [-99, -2, 0.01])
    out["fc3_deep_vs_near_high"] = d3.groupby("dq").agg(ex=("ex", "mean"), sd=("ex", "std"), n=("ex", "size"))
    # without near-high cases
    s, t, nn = ct(d3[d3.d20 < -2], "d20"); out["fc3_slope_excl_nearhigh"] = f"slope {s:.5f} t {t:.2f} n {nn}"
    d3["year"] = d3["day"].str[:4]
    out["fc3_mean_by_year"] = d3.groupby("year").agg(ex=("ex", "mean"), tot=("ret", "mean"), n=("ex", "size"))
    return out
