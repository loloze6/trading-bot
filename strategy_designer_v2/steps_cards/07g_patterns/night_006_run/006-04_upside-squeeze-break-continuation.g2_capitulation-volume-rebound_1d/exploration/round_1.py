def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            hi = b["high"].astype(float); lo = b["low"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "w": w,
                "ret5": c / c.shift(5) - 1,
                "ret1": r1,
                "ret20": c / c.shift(20) - 1,
                "vr": v.rolling(5).mean() / v.rolling(30).mean(),
                "rng": (hi.rolling(5).max() - lo.rolling(5).min()) / (hi.rolling(30).max() - lo.rolling(30).min()),
                "vol20": r1.rolling(20).std(),
                "fwd3": c.shift(-3) / c - 1,
                "fwd3abs": (c.shift(-3) / c - 1).abs(),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "pos": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
            })
            df = df.iloc[::3]
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["fwd3"])
    cm = d.groupby("coin")["fwd3"].transform("mean")
    d["ex3"] = d["fwd3"] - cm
    out = {}
    def qtab(col, sub=None, q=5):
        x = d if sub is None else sub
        x = x.dropna(subset=[col])
        g = pd.qcut(x[col].rank(method="first"), q, labels=False)
        t = x.groupby(g).agg(mean_x=(col, "mean"), ex3=("ex3", "mean"), absmove=("fwd3abs", "mean"), n=("ex3", "size"))
        t["t"] = x.groupby(g)["ex3"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
        return t
    out["ret5 quintiles all"] = qtab("ret5")
    out["ret20 quintiles all"] = qtab("ret20")
    out["vr quintiles all"] = qtab("vr")
    out["vr quintiles up5"] = qtab("vr", d[d.ret5 > 0])
    out["vr quintiles down5"] = qtab("vr", d[d.ret5 < 0])
    out["range compression quintiles"] = qtab("rng")
    out["vol20 quintiles"] = qtab("vol20")
    wt = d.groupby("wd").agg(ex3=("ex3", "mean"), n=("ex3", "size"))
    out["weekday ex3"] = wt
    # per coin: ret5 slope
    pc = {}
    for coin, x in d.dropna(subset=["ret5"]).groupby("coin"):
        s = stats.linregress(x["ret5"], x["ex3"])
        s2 = stats.linregress(x["ret20"].fillna(0), x["ex3"])
        pc[coin] = {"slope_ret5": s.slope, "t_ret5": s.slope / s.stderr, "slope_ret20": s2.slope, "t_ret20": s2.slope / s2.stderr, "n": len(x)}
    out["per coin ret5/ret20 slopes"] = pd.DataFrame(pc).T
    # book daily
    dd = pd.concat([df.assign(coin=c, w=w) for c in days for w, df in days[c].items()])
    bk = dd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book daily"] = pd.Series({"book_mean": bk.book_return.mean(), "hold_mean": bk.coin_return.mean(),
        "book_sh": bk.book_return.mean() / bk.book_return.std() * np.sqrt(365),
        "hold_sh": bk.coin_return.mean() / bk.coin_return.std() * np.sqrt(365), "n": len(bk)})
    bw = bk.reset_index().groupby("w")[["book_return", "coin_return"]].sum()
    out["book by window sums"] = bw
    return out
