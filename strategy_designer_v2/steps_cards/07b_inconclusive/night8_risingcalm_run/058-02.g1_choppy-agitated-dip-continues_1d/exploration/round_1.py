def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            mx = c.rolling(5, min_periods=5).max()
            depth = (c - mx) / mx / sd
            tr60 = c / c.shift(60) - 1
            yr = pd.to_datetime(b["timestamp"]).dt.year
            n = len(b)
            for h in (1, 3, 5, 10):
                fwd = c.shift(-h) / c - 1
                for i in range(0, n, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, depth=depth.iloc[i], fwd=fwd.iloc[i],
                                     prof=(b["regime"].iloc[i] != "chop"), fc=b["forecast"].iloc[i],
                                     tr=tr60.iloc[i], yr=yr.iloc[i]))
    df = pd.DataFrame(rows).dropna(subset=["fwd"])
    df["drift"] = df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["adj"] = df["fwd"] - df["drift"]
    def slope(g, x="depth"):
        g = g.dropna(subset=[x, "adj"])
        if len(g) < 10 or g[x].std() == 0: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, corr=np.nan))
        s = stats.linregress(g[x], g["adj"])
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr, corr=s.rvalue))
    out = {}
    out["by_h_profile"] = df.groupby(["h", "prof"]).apply(slope)
    p5 = df[(df.h == 5) & df.prof].copy()
    out["h5_prof_by_coin"] = p5.groupby("coin").apply(slope)
    out["h5_prof_by_year"] = p5.groupby("yr").apply(slope)
    p5d = p5.dropna(subset=["depth"]).copy()
    p5d["q"] = pd.qcut(p5d["depth"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    out["h5_prof_terciles"] = p5d.groupby("q")["adj"].agg(["count", "mean", "std"])
    a5 = df[(df.h == 5)].dropna(subset=["depth"]).copy()
    a5["trb"] = pd.cut(a5["tr"], [-10, -0.1, 0.1, 10], labels=["falling", "choppy", "rising"])
    out["h5_all_by_trend"] = a5.groupby(["trb", "prof"]).apply(slope)
    a5["q"] = pd.qcut(a5["depth"].rank(method="first"), 5, labels=False)
    out["h5_all_quintiles"] = a5.groupby("q")["adj"].agg(["count", "mean"])
    out["h5_prof_fc_slope"] = slope(p5, "fc")
    return out
