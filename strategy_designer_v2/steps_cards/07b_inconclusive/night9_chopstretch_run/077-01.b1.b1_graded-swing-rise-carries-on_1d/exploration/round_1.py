def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30).std()
            raw = (c / c.shift(14) - 1) / (sd * np.sqrt(14))
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in (3, 7, 14):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(df), h)
                for i in idx:
                    rows.append(dict(coin=coin, w=w, h=h, i=i, year=yr[i], regime=df["regime"].iloc[i],
                                     fc=df["forecast"].iloc[i], raw=raw.iloc[i], fwd=fwd.iloc[i],
                                     day=str(df["timestamp"].iloc[i])[:10]))
    g = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = g.groupby(["coin", "h"])["fwd"].mean().rename("drift")
    g = g.join(drift, on=["coin", "h"])
    g["u"] = g["fwd"] - g["drift"]
    ip = g[g.regime == "unknown"]
    out = {}
    def slope_t(d, x):
        d = d.dropna(subset=[x, "u"])
        if len(d) < 10: return (np.nan, np.nan, len(d))
        X = d[x].values; y = d["u"].values
        xm = X - X.mean(); b = (xm * (y - y.mean())).sum() / (xm ** 2).sum()
        res = y - y.mean() - b * xm
        s = pd.Series(res * xm).groupby(d["day"].values).sum()
        G = len(s); se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (xm ** 2).sum()
        return (b, b / se, len(d))
    tab = []
    for h in (3, 7, 14):
        d = ip[ip.h == h]
        b, t, n = slope_t(d, "raw"); tab.append(("raw_all", h, b, t, n))
        b, t, n = slope_t(d[d.raw > 0], "raw"); tab.append(("raw_pos", h, b, t, n))
        b, t, n = slope_t(d[d.raw < 0], "raw"); tab.append(("raw_neg", h, b, t, n))
        b, t, n = slope_t(d, "fc"); tab.append(("fc_all", h, b, t, n))
        dn = g[(g.h == h) & (g.regime != "unknown")]
        b, t, n = slope_t(dn, "raw"); tab.append(("raw_outprofile", h, b, t, n))
    out["slopes"] = pd.DataFrame(tab, columns=["set", "h", "slope", "t", "n"])
    d7 = ip[ip.h == 7].dropna(subset=["raw"]).copy()
    d7["q"] = pd.qcut(d7["raw"], 5, labels=False)
    out["quintiles_raw_h7"] = d7.groupby("q").agg(raw=("raw", "mean"), u=("u", "mean"), n=("u", "size"),
                                               up=("u", lambda s: (s > 0).mean()))
    out["by_coin_h7"] = d7.groupby("coin").apply(lambda x: pd.Series(dict(zip(["slope", "t", "n"], slope_t(x, "raw")))))
    out["by_year_h7"] = d7.groupby("year").apply(lambda x: pd.Series(dict(zip(["slope", "t", "n"], slope_t(x, "raw")))))
    d14 = ip[ip.h == 14].dropna(subset=["raw"]).copy()
    d14["q"] = pd.qcut(d14["raw"], 5, labels=False)
    out["quintiles_raw_h14"] = d14.groupby("q").agg(raw=("raw", "mean"), u=("u", "mean"), n=("u", "size"))
    out["share_inprofile"] = float((g[g.h == 7].regime == "unknown").mean())
    return out
