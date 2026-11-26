def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    rows = []; d1 = []
    for coin, wins in bars.items():
        # coin mean 7-bar return over all windows (grid)
        g7 = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - 7, 7):
                g7.append(c[i+7]/c[i]-1)
        m7 = np.mean(g7) if g7 else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; r = c.pct_change()
            sd30 = r.rolling(30).std()
            r7 = c / c.shift(7) - 1
            z7 = r7 / (sd30 * np.sqrt(7))
            net = (c - c.shift(30)).abs(); path = c.diff().abs().rolling(30).sum()
            er = net / path
            r30 = c / c.shift(30) - 1
            z30 = r30 / (sd30*np.sqrt(30))
            sdrank = sd30.rank(pct=True)  # within-window, rough
            fwd7 = c.shift(-7) / c - 1
            rng = (df["high"]-df["low"])/c
            for i in range(0, len(c) - 7, 7):
                if np.isnan(z7[i]) or np.isnan(er[i]): continue
                rows.append(dict(coin=coin, w=w, i=i, z7=z7[i], er=er[i], z30=z30[i],
                                 sd=sd30[i], fx=fwd7[i]-m7, f=fwd7[i], reg=df["regime"][i],
                                 fc=df["forecast"][i], day=str(df["timestamp"][i])[:10]))
            fw1 = c.shift(-1)/c - 1
            for i in range(30, len(c)-1):
                d1.append(dict(coin=coin, r=r[i], z1=r[i]/sd30[i] if sd30[i]>0 else np.nan,
                               f1=fw1[i], wd=pd.Timestamp(df["timestamp"][i]).dayofweek,
                               er=er[i], rng=rng[i]/sd30[i] if sd30[i]>0 else np.nan))
    X = pd.DataFrame(rows); D = pd.DataFrame(d1).dropna()
    def summ(g):
        return pd.Series(dict(n=len(g), mean=g["fx"].mean(),
                              t=g["fx"].mean()/(g["fx"].std()/np.sqrt(len(g))) if len(g)>2 else np.nan))
    out = {}
    X["zq"] = pd.qcut(X["z7"], 5, labels=False)
    X["erq"] = pd.qcut(X["er"], 3, labels=False)
    out["fwd7x_by_z7quint"] = X.groupby("zq").apply(summ)
    out["fwd7x_by_er_tercile_x_z7quint"] = X.groupby(["erq","zq"]).apply(summ)
    X["z30q"] = pd.qcut(X["z30"], 5, labels=False)
    out["fwd7x_by_z30quint"] = X.groupby("z30q").apply(summ)
    out["fwd7x_by_er_x_z30quint"] = X.groupby(["erq","z30q"]).apply(summ)
    out["fwd7x_by_regime"] = X.groupby("reg").apply(summ)
    # slope corr
    for lab, sub in [("all", X), ("lowER", X[X.erq==0]), ("highER", X[X.erq==2])]:
        rr = stats.pearsonr(sub["z7"], sub["fx"]); out[f"corr_z7_fx_{lab}"] = f"r={rr[0]:.3f} p={rr[1]:.3f} n={len(sub)}"
        rr = stats.pearsonr(sub["z30"], sub["fx"]); out[f"corr_z30_fx_{lab}"] = f"r={rr[0]:.3f} p={rr[1]:.3f} n={len(sub)}"
    # daily
    D["zq"] = pd.qcut(D["z1"], 5, labels=False)
    out["fwd1_by_z1quint"] = D.groupby("zq")["f1"].agg(["count","mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    out["fwd1_by_weekday"] = D.groupby("wd")["f1"].agg(["count","mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    D["rq"] = pd.qcut(D["rng"], 5, labels=False)
    out["fwd1_by_rangequint"] = D.groupby("rq")["f1"].agg(["count","mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in trades.items() for t in ws.values() if len(t)], ignore_index=True)
    T["fq"] = pd.qcut(T["entry_forecast"], 4, labels=False, duplicates="drop")
    out["trades_by_entryfc_q"] = T.groupby("fq")["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean"])
    return out
