def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]

    def clustered_t(df, col):
        d = df.dropna(subset=[col])
        if len(d) < 5: return np.nan, len(d), 0
        dev = d[col] - d[col].mean()
        g = dev.groupby(d["ts"]).sum()
        G = len(g)
        se = np.sqrt((g**2).sum() * G / (G - 1)) / len(d)
        return d[col].mean() / se, len(d), G

    rows = {}
    for h in [7, 30]:
        recs = []
        for coin, ws in bars.items():
            per = []
            for w, b in ws.items():
                c = b["close"].values.astype(float)
                n = len(c)
                lr = np.log(c)
                r1 = np.r_[np.nan, np.diff(lr)]
                for p in range(0, n - h, h):
                    fwd = c[p + h] / c[p] - 1
                    past7 = c[p] / c[p - 7] - 1 if p >= 7 else np.nan
                    past30 = c[p] / c[p - 30] - 1 if p >= 30 else np.nan
                    vol30 = np.nanstd(r1[max(1, p - 29):p + 1]) * np.sqrt(30) if p >= 20 else np.nan
                    hi60 = c[max(0, p - 59):p + 1].max() if p >= 30 else np.nan
                    ret1 = c[p] / c[p - 1] - 1 if p >= 1 else np.nan
                    per.append(dict(coin=coin, w=w, ts=b["timestamp"].iloc[p], fwd=fwd,
                                    past7=past7, past30=past30, vol30=vol30,
                                    dd60=(c[p] / hi60 - 1) if p >= 30 else np.nan,
                                    ret1=ret1,
                                    regime=b["regime"].iloc[p], fc=b["forecast"].iloc[p],
                                    wd=pd.Timestamp(b["timestamp"].iloc[p]).weekday(),
                                    yr=pd.Timestamp(b["timestamp"].iloc[p]).year))
            if not per: continue
            d = pd.DataFrame(per)
            d["ex"] = d["fwd"] - d["fwd"].mean()
            d["usual"] = d["fwd"].std()
            d["exz"] = d["ex"] / d["usual"]
            recs.append(d)
        D = pd.concat(recs, ignore_index=True)
        # scale past moves by coin usual
        D["p30z"] = D.groupby("coin")["past30"].transform(lambda s: s / s.abs().mean())
        D["p7z"] = D.groupby("coin")["past7"].transform(lambda s: s / s.abs().mean())
        D["volz"] = D.groupby("coin")["vol30"].transform(lambda s: s / s.mean())
        res = []
        for sig in ["p7z", "p30z", "volz", "dd60", "ret1"]:
            dd = D.dropna(subset=[sig, "exz"]).copy()
            dd["q"] = pd.qcut(dd[sig].rank(method="first"), 5, labels=False)
            for q in range(5):
                s = dd[dd.q == q]
                t, n, G = clustered_t(s, "exz")
                res.append(dict(sig=sig, q=q, sigmean=s[sig].mean(), exz=s["exz"].mean(),
                                ex=s["ex"].mean(), t=t, n=n, days=G))
            rho, pv = stats.spearmanr(dd[sig], dd["exz"])
            res.append(dict(sig=sig, q="rho", sigmean=rho, exz=pv, n=len(dd)))
        out[f"h{h}_quintiles"] = pd.DataFrame(res)
        if h == 30:
            g = []
            for key in ["regime", "yr"]:
                for k, s in D.groupby(key):
                    t, n, G = clustered_t(s, "exz")
                    g.append(dict(by=key, k=k, exz=s["exz"].mean(), ex=s["ex"].mean(), t=t, n=n))
            out["h30_by_regime_year"] = pd.DataFrame(g)
        if h == 7:
            g = []
            for k, s in D.groupby("regime"):
                t, n, G = clustered_t(s, "exz")
                g.append(dict(k=k, exz=s["exz"].mean(), t=t, n=n))
            out["h7_by_regime"] = pd.DataFrame(g)

    # daily coin returns by weekday, regime
    allb = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            c = b["close"].astype(float)
            r = c.shift(-1) / c - 1
            allb.append(pd.DataFrame(dict(coin=coin, r=r, alloc=b["postRebalance_current_allocation"],
                                          wd=pd.to_datetime(b["timestamp"]).dt.weekday,
                                          regime=b["regime"], fc=b["forecast"])))
    A = pd.concat(allb).dropna(subset=["r"])
    A["rz"] = A.groupby("coin")["r"].transform(lambda s: (s - s.mean()) / s.std())
    out["daily_by_weekday"] = A.groupby("wd")["rz"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    out["daily_by_regime"] = A.groupby("regime")["rz"].agg(["mean", "count"])
    # trades
    T = []
    for coin, ws in trades.items():
        for w, t in ws.items():
            if len(t): T.append(t.assign(coin=coin, w=w))
    if T:
        T = pd.concat(T)
        T["q"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
        out["trades_by_fc_quartile"] = T.groupby("q").agg(n=("net_profit_loss_percent", "size"),
                                                         fc=("entry_forecast", "mean"),
                                                         pl=("net_profit_loss_percent", "mean"),
                                                         med=("net_profit_loss_percent", "median"),
                                                         dur_d=("duration_minutes", lambda s: s.mean() / 1440))
        T["yr"] = pd.to_datetime(T["entry_time"]).dt.year
        out["trades_by_year"] = T.groupby("yr")["net_profit_loss_percent"].agg(["count", "mean", "median"])
        out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
