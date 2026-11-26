def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; h = b["high"].values; l = b["low"].values; o = b["open"].values
            n = len(b)
            r1 = pd.Series(c).pct_change().values
            absr = pd.Series(np.abs(r1)).rolling(30, min_periods=20).mean().values
            sd30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            sdw = np.nanmedian(sd30) if np.isfinite(sd30).any() else np.nan
            tr60 = pd.Series(c).pct_change(60).values
            r3 = pd.Series(c).pct_change(3).values
            ts = pd.to_datetime(b["timestamp"])
            for t in range(0, n - 5, 5):
                rng = h[t] - l[t]
                cl = (c[t] - l[t]) / rng if rng > 0 else np.nan
                rows.append(dict(coin=coin, w=w, day=str(ts[t].date()), wd=ts[t].weekday(), yr=ts[t].year,
                                 cl=cl, r1=r1[t], sr=r1[t] / absr[t] if absr[t] > 0 else np.nan,
                                 volr=sd30[t] / sdw if sdw > 0 else np.nan, tr60=tr60[t],
                                 r3s=r3[t] / (absr[t] * np.sqrt(3)) if absr[t] > 0 else np.nan,
                                 body=(c[t] - o[t]) / rng if rng > 0 else np.nan,
                                 rngs=(rng / c[t]) / absr[t] if absr[t] > 0 else np.nan,
                                 f5=c[t + 5] / c[t] - 1))
    df = pd.DataFrame(rows)
    drift = df.groupby("coin")["f5"].mean(); usual = df.groupby("coin")["f5"].std()
    df["u"] = df["f5"] - df["coin"].map(drift)
    df["s"] = df["u"] / df["coin"].map(usual)

    def tday(x):
        x = x.dropna(subset=["u"])
        N = len(x); D = x["day"].nunique()
        if N < 5 or D < 3: return pd.Series(dict(n=N, mean_u=np.nan, strength=np.nan, t=np.nan))
        m = x["u"].mean(); rd = (x["u"] - m).groupby(x["day"]).sum()
        se = np.sqrt((rd ** 2).sum() * D / (D - 1)) / N
        return pd.Series(dict(n=N, days=D, mean_u=m, strength=x["s"].mean(), t=m / se))

    out = {}
    out["by_close_loc"] = df.groupby(pd.cut(df["cl"], [-.01, .2, .4, .6, .8, 1.01])).apply(tday)
    out["by_scaled_ret"] = df.groupby(pd.qcut(df["sr"], 5)).apply(tday)
    out["by_3d_scaled"] = df.groupby(pd.qcut(df["r3s"], 5)).apply(tday)
    out["by_range_size"] = df.groupby(pd.qcut(df["rngs"], 5)).apply(tday)
    out["by_vol_ratio"] = df.groupby(pd.qcut(df["volr"], 4)).apply(tday)
    out["by_trend60"] = df.groupby(pd.cut(df["tr60"], [-5, -.1, .1, 50])).apply(tday)
    out["by_weekday"] = df.groupby("wd").apply(tday)
    out["by_year"] = df.groupby("yr").apply(tday)
    hc = df[df["cl"] >= .8]
    out["hiclose_by_trend"] = hc.groupby(pd.cut(hc["tr60"], [-5, -.1, .1, 50])).apply(tday)
    out["hiclose_by_volr"] = hc.groupby(pd.qcut(hc["volr"], 3)).apply(tday)
    out["hiclose_by_sr"] = hc.groupby(pd.qcut(hc["sr"], 3)).apply(tday)
    lc = df[df["cl"] <= .2]
    out["loclose_by_trend"] = lc.groupby(pd.cut(lc["tr60"], [-5, -.1, .1, 50])).apply(tday)
    # trades
    tr = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): tr.append(t.assign(coin=coin))
    if tr:
        T = pd.concat(tr)
        out["trades"] = pd.Series(dict(n=len(T), mean_net=T["net_profit_loss_percent"].mean(),
                                       win=(T["net_profit_loss_percent"] > 0).mean(),
                                       med_days=T["duration_minutes"].median() / 1440))
        out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
