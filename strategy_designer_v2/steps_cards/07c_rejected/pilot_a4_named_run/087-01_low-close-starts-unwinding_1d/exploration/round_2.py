def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            if len(b) < 15: continue
            c = b["close"].values; hi = b["high"].values; lo = b["low"].values; op = b["open"].values
            rng = hi - lo
            cl = np.where(rng > 0, (hi - c) / np.where(rng > 0, rng, 1), np.nan)
            ol = np.where(rng > 0, (hi - op) / np.where(rng > 0, rng, 1), np.nan)
            reg = b["regime"].astype(str).values
            ret1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            prevc = np.r_[np.nan, c[:-1]]
            upwick = np.where(np.isfinite(prevc), (hi - np.maximum(prevc, op)) / np.where(rng > 0, rng, 1), np.nan)
            rngpct = rng / c
            for h in [1, 2, 3, 5]:
                for i in range(0, len(b) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, cl=cl[i], ol=ol[i], reg=reg[i],
                                     r=c[i + h] / c[i] - 1, r1=ret1[i], up=upwick[i], rp=rngpct[i],
                                     yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
    df = pd.DataFrame(rows)
    df = df.join(df.groupby(["coin", "h"])["r"].mean().rename("drift"), on=["coin", "h"])
    df["u"] = -(df["r"] - df["drift"])
    def summ(g):
        x = g["u"].dropna(); n = len(x)
        return pd.Series(dict(n=n, mean_short=x.mean(), t=x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan))
    ip = df[df.reg.isin(["mean_reversion", "unknown"])].dropna(subset=["cl", "r1"])
    low = ip[ip.cl >= 0.8].copy()
    # own day return sign
    low["daysign"] = np.where(low.r1 >= 0, "up day", "down day")
    out["low close in profile, by day sign and h"] = low.groupby(["h", "daysign"]).apply(summ).round(4)
    low["open_loc"] = pd.cut(low.ol, [-0.01, 0.33, 0.66, 1.01], labels=["open near high", "open mid", "open near low"])
    out["low close in profile, by open location and h"] = low.groupby(["h", "open_loc"]).apply(summ).round(4)
    # all in-profile days: graded by r1 among low closes -> correlation
    for h in [2, 3, 5]:
        g = low[low.h == h]
        out[f"spearman r1 vs u among low closes h{h}"] = pd.Series(stats.spearmanr(g.r1, g.u), index=["rho", "p"]).round(4)
        g2 = ip[ip.h == h]
        out[f"spearman cl vs u all in-profile h{h}"] = pd.Series(stats.spearmanr(g2.cl, g2.u), index=["rho", "p"]).round(4)
    # rejection strength = cl minus own-day fall: reversal days (up-day yet low close) graded by cl
    ip2 = ip.copy()
    ip2["rej"] = ip2.cl * (ip2.r1 >= 0)
    for h in [3, 5]:
        g = ip2[(ip2.h == h) & (ip2.r1 >= 0)]
        out[f"up days in profile h{h}: by close location"] = g.groupby(pd.cut(g.cl, [-0.01, 0.33, 0.66, 1.01])).apply(summ).round(4)
    out["low close up-day h3 by coin"] = low[(low.h == 3) & (low.r1 >= 0)].groupby("coin").apply(summ).round(4)
    out["low close down-day h3 by coin"] = low[(low.h == 3) & (low.r1 < 0)].groupby("coin").apply(summ).round(4)
    # range size
    low3 = low[low.h == 3]
    out["low close h3 by range size tercile"] = low3.groupby(pd.qcut(low3.rp, 3, labels=["narrow", "mid", "wide"])).apply(summ).round(4)
    # strategy bars: actual short bars in mean_reversion, forward 3 bars every signal
    sr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True); c = b["close"].values
            for i in range(len(b) - 3):
                if str(b["regime"].iloc[i]) == "mean_reversion":
                    sr.append(dict(coin=coin, r3=c[i + 3] / c[i] - 1))
    sr = pd.DataFrame(sr)
    out["all mean_reversion bars, raw 3-day return (overlapping)"] = sr.groupby("coin")["r3"].agg(["count", "mean"]).round(4)
    return out
