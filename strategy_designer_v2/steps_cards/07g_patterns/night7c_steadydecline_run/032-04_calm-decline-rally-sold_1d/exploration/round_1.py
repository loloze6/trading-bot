def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        allf = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            rng = (b["high"] - b["low"]) / c
            r28 = c / c.shift(28) - 1
            r5p = c / c.shift(5) - 1
            r1 = c / c.shift(1) - 1
            rr = rng.rolling(28).mean() / rng.rolling(120, min_periods=40).mean()
            v = b["volume"].astype(float)
            vr = v.rolling(28).mean() / v.shift(28).rolling(92, min_periods=20).mean()
            vol20 = r1.rolling(20).std()
            fwd = c.shift(-H) / c - 1
            idx = np.arange(0, n - H, H)
            for i in idx:
                allf.append(fwd.iloc[i])
                rows.append(dict(coin=coin, w=w, i=i, fwd=fwd.iloc[i], r28=r28.iloc[i], r5p=r5p.iloc[i],
                                 r1=r1.iloc[i], rr=rr.iloc[i], vr=vr.iloc[i], vol20=vol20.iloc[i],
                                 wd=pd.Timestamp(b["timestamp"].iloc[i]).dayofweek,
                                 yr=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 fc=b["forecast"].iloc[i]))
        drift[coin] = np.nanmean(allf)
    df = pd.DataFrame(rows)
    df["un"] = df["fwd"] - df["coin"].map(drift)
    sd = df.groupby("coin")["fwd"].transform("std")
    df["z"] = df["un"] / sd
    def summ(g):
        x = g["un"].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              zmean=g["z"].mean()))
    out = {}
    d = df.dropna(subset=["r28"])
    d["q28"] = d.groupby("coin")["r28"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["by_r28_quintile"] = d.groupby("q28").apply(summ)
    d2 = d.dropna(subset=["rr"])
    d2["calm"] = (d2["rr"] <= 1).astype(int)
    d2["down"] = (d2["r28"] < 0).astype(int)
    d2["up"] = (d2["r1"] > 0).astype(int)
    out["down_calm_up"] = d2.groupby(["down", "calm", "up"]).apply(summ)
    dd = d2[d2.down == 1]
    out["down_only_by_r28q_calm"] = dd.groupby(["calm", "q28"]).apply(summ)
    d5 = df.dropna(subset=["r5p"])
    d5["q5"] = d5.groupby("coin")["r5p"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["by_past5_quintile"] = d5.groupby("q5").apply(summ)
    dv = df.dropna(subset=["vol20"])
    dv["qv"] = dv.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["by_vol_tercile"] = dv.groupby("qv").apply(summ)
    out["by_weekday"] = df.groupby("wd").apply(summ)
    out["by_year"] = df.groupby("yr").apply(summ)
    out["fc_active_vs_not"] = df.assign(act=(df.fc < 0).astype(int)).groupby("act").apply(summ)
    dvr = df.dropna(subset=["vr"])
    dvr["qvr"] = dvr.groupby("coin")["vr"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["by_volratio_tercile"] = dvr.groupby("qvr").apply(summ)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr)
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    T["fq"] = pd.qcut(T["entry_forecast"].abs().rank(method="first"), 3, labels=False)
    out["trades_by_fc_tercile"] = T.groupby("fq")["net_profit_loss_percent"].agg(["count", "mean"])
    out["drift"] = pd.Series(drift)
    return out
