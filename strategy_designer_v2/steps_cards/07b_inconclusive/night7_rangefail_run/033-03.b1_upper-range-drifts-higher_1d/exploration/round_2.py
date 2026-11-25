def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).values
            ah = df["debug_info.components.above_high.last_history_value"].astype(float).values
            rp = df["debug_info.components.range_pos.last_history_value"].astype(float).values
            tr = pd.Series(c).pct_change(min(60, len(c)-1)).values
            tr30 = pd.Series(c).pct_change(30).values
            for h in (3, 5, 10):
                for i in range(0, len(df) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, day=str(df["timestamp"].iloc[i])[:10],
                                     f=f[i], ah=ah[i], rp=rp[i], ret=c[i+h]/c[i]-1, tr30=tr30[i]))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby(["coin", "h"])["ret"].transform("mean")
    def clt(g, x="f"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 15 or g[x].std() == 0:
            return pd.Series(dict(n=len(g), days=np.nan, slope=np.nan, t_cl=np.nan))
        X = g[x].values; y = g["ex"].values
        Xm = X - X.mean(); b = (Xm*(y-y.mean())).sum()/(Xm**2).sum()
        a = y.mean() - b*X.mean(); e = y - a - b*X
        s = pd.Series(Xm*e).groupby(g["day"].values).sum()
        G = len(s); n = len(g)
        v = (s**2).sum()/((Xm**2).sum()**2) * G/(G-1) * (n-1)/(n-2)
        return pd.Series(dict(n=n, days=G, slope=b, t_cl=b/np.sqrt(v)))
    out = {}
    out["clustered_by_h"] = d.groupby("h").apply(clt)
    out["long_side_f>0"] = d[d.f > 0].groupby("h").apply(clt)
    out["short_side_f<0"] = d[d.f < 0].groupby("h").apply(clt)
    for h in (5, 10):
        dh = d[d.h == h].copy()
        dh["side"] = np.where(dh["ah"] > 0, "above_high", np.where(dh["f"] > 0, "upper", "lower"))
        out[f"h{h}_side"] = dh.groupby("side").agg(n=("ex", "size"), ex_mean=("ex", "mean"),
            ex_t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
        a = dh[dh.ah > 0].copy()
        if len(a) >= 10:
            a["aq"] = pd.qcut(a["ah"], 3, labels=False, duplicates="drop")
            out[f"h{h}_abovehigh_terciles"] = a.groupby("aq").agg(n=("ex", "size"), ah=("ah", "mean"), ex_mean=("ex", "mean"))
        dh["t30"] = np.where(dh.tr30 > 0.05, "up30", np.where(dh.tr30 < -0.05, "down30", np.where(dh.tr30.notna(), "flat30", "na")))
        out[f"h{h}_by_trend30"] = dh.groupby("t30").apply(clt)
        out[f"h{h}_by_coin_cl"] = dh.groupby("coin").apply(clt)
    d5 = d[d.h == 5]
    out["h5_by_window_cl"] = d5.groupby("w").apply(clt)
    return out
