def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    bookrows = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            if n < H + 25: continue
            lr = np.log(c)
            r1 = np.r_[np.nan, np.diff(lr)]
            vol20 = pd.Series(r1).rolling(20).std().values
            ret10 = pd.Series(c).pct_change(10).values
            ret20 = pd.Series(c).pct_change(20).values
            hi20 = pd.Series(c).rolling(20).max().values
            lo20 = pd.Series(c).rolling(20).min().values
            raw = b.get("debug_info.components.res_break.last_history_value", pd.Series(np.nan, index=b.index)).values
            fc = b["forecast"].values
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                recs.append(dict(coin=coin, w=w, fwd=c[i+H]/c[i]-1, ret10=ret10[i], ret20=ret20[i],
                                 vol20=vol20[i], near=(c[i]-lo20[i])/(hi20[i]-lo20[i]) if hi20[i]>lo20[i] else np.nan,
                                 ret1=r1[i], raw=raw[i], fc=fc[i], wd=ts[i].dayofweek, yr=ts[i].year,
                                 # any breakout in grid cell's past 3 bars
                                 ))
        if not recs: continue
        df = pd.DataFrame(recs)
        mu = df["fwd"].mean(); sd = df["fwd"].std()
        df["unu"] = df["fwd"] - mu
        df["str"] = df["unu"] / sd
        # rank vol within coin
        df["volq"] = pd.qcut(df["vol20"].rank(method="first"), 3, labels=["lo","mid","hi"]) if df["vol20"].notna().sum()>30 else np.nan
        rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    def summ(g):
        x = g["unu"].dropna()
        return pd.Series({"n": len(x), "mean_unu": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, "strength": g["str"].mean()})
    out = {}
    A["ret10q"] = A.groupby("coin")["ret10"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    A["ret20q"] = A.groupby("coin")["ret20"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    A["nearq"] = pd.cut(A["near"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=False)
    A["ret1q"] = A.groupby("coin")["ret1"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["by_ret10_quintile"] = A.groupby("ret10q").apply(summ)
    out["by_ret20_quintile"] = A.groupby("ret20q").apply(summ)
    out["by_near20"] = A.groupby("nearq").apply(summ)
    out["by_ret1_quintile"] = A.groupby("ret1q").apply(summ)
    out["by_vol"] = A.groupby("volq").apply(summ)
    out["by_vol_x_ret20top_bottom"] = A[A["ret20q"].isin([0,4])].groupby(["volq","ret20q"]).apply(summ)
    out["by_weekday"] = A.groupby("wd").apply(summ)
    out["by_year"] = A.groupby("yr").apply(summ)
    A["fcpos"] = np.where(A["fc"] > 0, "fc>0", "fc=0")
    out["by_forecast_state"] = A.groupby("fcpos").apply(summ)
    # corr ranks
    for k in ["ret10","ret20","near","ret1"]:
        s = A[[k,"str"]].dropna()
        rho, p = stats.spearmanr(s[k], s["str"])
        out[f"spearman_{k}_vs_strength"] = f"rho={rho:.4f} p={p:.4g} n={len(s)}"
    # book daily
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"]=coin; d["w"]=w; D.append(d)
    D = pd.concat(D)
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    bd = D.groupby(["w","day"]).agg(book=("book_return","mean"), hold=("coin_return","mean")).dropna().reset_index()
    bd["yr"] = pd.to_datetime(bd["day"]).dt.year
    out["book_by_year"] = bd.groupby("yr").agg(n=("book","size"), book_mean=("book","mean"), hold_mean=("hold","mean"),
                                                book_sh=("book", lambda x: x.mean()/x.std()*np.sqrt(365)),
                                                hold_sh=("hold", lambda x: x.mean()/x.std()*np.sqrt(365)))
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t=t.copy(); t["coin"]=coin; T.append(t)
    T = pd.concat(T)
    T["days"] = T["duration_minutes"]/1440
    T["dq"] = pd.cut(T["days"], [0,5,9.5,11,20,60,1e9])
    out["trades_by_duration"] = T.groupby("dq").agg(n=("net_profit_loss_percent","size"), mean_net=("net_profit_loss_percent","mean"), med=("net_profit_loss_percent","median"))
    out["trades_n"] = len(T)
    return out
