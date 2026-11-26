def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = pd.Series(df["close"].astype(float).values)
            n = len(c)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r3 = c / c.shift(3) - 1
            s3 = r3 / (sd30 * np.sqrt(3))
            tr60 = c / c.shift(60) - 1
            prof = (df["regime"] == "unknown").values
            fc = df["forecast"].astype(float).values
            al = df["postRebalance_current_allocation"].astype(float).values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").astype("int64").values
            for h in (3, 7, 15):
                for i in range(n - h):
                    rows.append(dict(coin=coin, w=w, h=h, off=i % h, s3=s3[i], prof=prof[i], fc=fc[i], al=al[i],
                                     tr=tr60[i], fwd=c[i+h]/c[i]-1, day=day[i], year=pd.Timestamp(day[i]).year))
    R = pd.DataFrame(rows).dropna(subset=["s3"])
    def drift(Rh):
        g = Rh[Rh.off == 0].groupby("coin").fwd.mean()
        return Rh.fwd - Rh.coin.map(g)
    def ct(sub, x="s3"):
        # day-clustered slope t via residual sums per day
        X = sub[x].values; Y = sub.ex.values
        if len(sub) < 10: return (np.nan, np.nan, len(sub))
        b = np.cov(X, Y)[0,1] / np.var(X, ddof=1); a = Y.mean() - b * X.mean()
        e = Y - a - b * X; xc = X - X.mean()
        s = pd.Series(xc * e).groupby(sub.day.values).sum()
        se = np.sqrt((s**2).sum()) / (xc**2).sum()
        return (round(b,4), round(b/se,2), len(sub))
    for h in (3, 7, 15):
        Rh = R[R.h == h].copy(); Rh["ex"] = drift(Rh)
        # stability over grid offsets, in profile
        res = []
        for o in range(h):
            sub = Rh[(Rh.off == o) & Rh.prof]
            b, t, k = ct(sub)
            res.append(dict(off=o, slope=b, t=t, n=k))
        res = pd.DataFrame(res)
        out[f"h{h} in-profile slope ex~s3 by grid offset (summary)"] = pd.Series(dict(mean_slope=res.slope.mean(), mean_t=res.t.mean(), min_t=res.t.min(), max_t=res.t.max(), share_neg=(res.slope<0).mean()))
        P = Rh[Rh.prof & (Rh.off == 0)]
        # rises only vs falls only in profile
        for side, sub in (("rises", P[P.s3 > 0]), ("falls", P[P.s3 < 0])):
            b, t, k = ct(sub); out[f"h{h} in-profile {side} slope"] = f"slope {b} t {t} n {k} mean ex {sub.ex.mean():.4f}"
        # forecast-based (book's signal) on all offsets pooled, in profile, forecast<0
        Q = Rh[Rh.prof]
        out[f"h{h} in-profile pooled offsets: ex by s3 bin"] = Q.groupby(pd.cut(Q.s3, [-9,-1.5,-0.75,0,0.75,1.5,9])).ex.agg(["count","mean"]).round(4)
        # out of profile by trend bucket (60d trend known), off 0
        O = Rh[(~Rh.prof) & (Rh.off == 0)].dropna(subset=["tr"])
        O = O.assign(tb=pd.cut(O.tr, [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"]))
        tab = []
        for tb, sub in O.groupby("tb"):
            b, t, k = ct(sub)
            fl = sub[sub.s3 < -0.75]; ri = sub[sub.s3 > 0.75]
            tab.append(dict(tb=tb, slope=b, t=t, n=k, ex_after_fall=fl.ex.mean(), n_fall=len(fl), ex_after_rise=ri.ex.mean(), n_rise=len(ri)))
        out[f"h{h} out-of-profile by 60d trend (off 0)"] = pd.DataFrame(tab).round(4)
    # book: forecast vs s3 in profile, and what the book held
    Rb = R[(R.h == 15) & R.prof]
    out["in-profile corr(forecast, s3)"] = round(Rb.fc.corr(Rb.s3), 3)
    out["in-profile share forecast<0 / alloc<0"] = f"{(Rb.fc<0).mean():.3f} / {(Rb.al<0).mean():.3f}"
    Rb2 = R[(R.h == 1) ] if False else None
    # book's daily return when in position vs not
    D = []
    for coin, ws in data["days"].items():
        for w, df in ws.items():
            d = df.copy(); d["coin"] = coin; D.append(d)
    D = pd.concat(D)
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    out["book & coin daily mean by year"] = D.groupby("yr")[["book_return", "coin_return"]].mean().round(5)
    return out
