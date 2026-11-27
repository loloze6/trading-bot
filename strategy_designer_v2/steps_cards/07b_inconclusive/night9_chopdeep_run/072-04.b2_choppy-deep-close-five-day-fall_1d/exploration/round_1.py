def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    H = [1, 2, 5, 10]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            f = b["forecast"].values
            reg = b["regime"].values
            hi20 = pd.Series(c).rolling(20, min_periods=20).max().values
            r = pd.Series(c).pct_change()
            sd20 = r.rolling(20, min_periods=20).std().values
            raw = (c / hi20 - 1) / sd20
            upday = (r > 0).values
            ret60 = (pd.Series(c) / pd.Series(c).shift(60) - 1).values
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, f=f[i], reg=reg[i], raw=raw[i],
                                     up=upday[i], fr=c[i + h] / c[i] - 1, r60=ret60[i]))
    df = pd.DataFrame(rows)
    drift = df.groupby(["coin", "h"])["fr"].mean().rename("drift")
    df = df.join(drift, on=["coin", "h"])
    df["ex"] = df["fr"] - df["drift"]
    sig = df[(df.f < 0)]
    # buckets of forecast by horizon
    sig = sig.copy()
    sig["fb"] = pd.cut(sig.f, [-21, -15, -10, -5, -2, 0])
    t = sig.groupby(["h", "fb"])["ex"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    t.columns = ["n", "mean_ex", "t"]
    out["ex by forecast bucket and horizon"] = t.round(4)
    # flat choppy (forecast 0 in unknown) vs signals
    ch = df[df.reg == "unknown"].copy()
    ch["isig"] = ch.f < 0
    out["choppy: signal vs flat, by h"] = ch.groupby(["h", "isig"])["ex"].agg(["count", "mean"]).round(4)
    # raw depth buckets in choppy regime
    ch["rb"] = pd.qcut(ch.raw, 5, duplicates="drop")
    out["choppy raw depth quintile by h"] = ch.groupby(["h", "rb"])["ex"].agg(["count", "mean"]).round(4)
    s5 = sig[sig.h == 5]
    out["h5 by coin"] = s5.groupby("coin")["ex"].agg(["count", "mean", lambda x: np.corrcoef(x, s5.loc[x.index, "f"])[0, 1]]).round(4)
    out["h5 by window"] = s5.groupby("w")["ex"].agg(["count", "mean"]).round(4)
    out["h5 by upday"] = s5.groupby("up")["ex"].agg(["count", "mean"]).round(4)
    s5b = s5.copy(); s5b["r60b"] = pd.cut(s5b.r60, [-0.11, -0.03, 0.03, 0.11])
    out["h5 by 60d return"] = s5b.groupby("r60b")["ex"].agg(["count", "mean"]).round(4)
    # slope by horizon
    sl = {}
    for h in H:
        s = sig[sig.h == h]
        res = stats.linregress(s.f, s.ex)
        sl[h] = (len(s), res.slope, res.slope / res.stderr, s.ex.mean())
    out["slope by h (n, slope, t, mean ex)"] = pd.DataFrame(sl, index=["n", "slope", "t", "mean_ex"]).T.round(5)
    return out
