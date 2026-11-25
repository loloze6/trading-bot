def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r28 = c / c.shift(28) - 1
            hi28 = c.rolling(28, min_periods=28).max()
            dist = c / hi28 - 1
            r28z = (r28 - r28.rolling(60, min_periods=20).mean()) / r28.rolling(60, min_periods=20).std()
            vol = c.pct_change().rolling(28, min_periods=20).std()
            n = len(c); h = 5
            for i in range(0, n - h, h):
                rows.append(dict(coin=coin, win=w, fwd=c.iloc[i + h] / c.iloc[i] - 1,
                                 r28=r28.iloc[i], r28z=r28z.iloc[i], dist=dist.iloc[i],
                                 vol=vol.iloc[i], fc=b["forecast"].iloc[i], reg=b["regime"].iloc[i],
                                 runup_raw=b.get("debug_info.components.runup.last_history_value", pd.Series(np.nan, index=b.index)).iloc[i]))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    out = {}
    def summ(g):
        return pd.Series({"n": len(g), "mean_ex": g["ex"].mean(),
                          "t": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    def sl(x, y):
        m = x.notna() & y.notna()
        s = stats.linregress(x[m], y[m]); return f"slope {s.slope:.4f}, t {s.slope/s.stderr:.2f}, n {m.sum()}"
    tr = d[d.reg == "trending"].copy()
    out["trending cases"] = summ(tr)
    out["slope ex on forecast (trending)"] = sl(tr["fc"], tr["ex"])
    out["slope ex on raw r28 (trending)"] = sl(tr["r28"], tr["ex"])
    out["slope ex on r28z (trending)"] = sl(tr["r28z"], tr["ex"])
    out["slope ex on r28/vol (trending)"] = sl(tr["r28"] / (tr["vol"] * np.sqrt(28)), tr["ex"])
    out["corr forecast vs raw r28 (trending)"] = float(tr[["fc", "r28"]].corr().iloc[0, 1])
    out["corr forecast vs r28z"] = float(tr[["fc", "r28z"]].corr().iloc[0, 1])
    tr["fq"] = pd.qcut(tr["fc"].rank(method="first"), 4, labels=False)
    out["trending by forecast quartile"] = tr.groupby("fq").apply(summ).join(tr.groupby("fq")[["fc", "r28"]].mean())
    tr["vq"] = pd.qcut((tr["r28"] / (tr["vol"] * np.sqrt(28))).rank(method="first"), 4, labels=False)
    out["trending by r28/vol quartile"] = tr.groupby("vq").apply(summ)
    a = d.dropna(subset=["dist"]).copy()
    out["all bars slope ex on dist"] = sl(a["dist"], a["ex"])
    near = a[a.dist > -0.1]
    out["dist>-10% slope ex on dist"] = sl(near["dist"], near["ex"])
    a["dq"] = pd.qcut(a["dist"].rank(method="first"), 10, labels=False)
    out["all bars by dist decile"] = a.groupby("dq").apply(summ).join(a.groupby("dq")["dist"].mean())
    top = tr[tr.r28 > tr.r28.quantile(0.75)]
    out["top r28 quartile at high by coin"] = top.groupby("coin").apply(summ)
    out["top r28 quartile by window"] = top.groupby("win").apply(summ)
    return out
