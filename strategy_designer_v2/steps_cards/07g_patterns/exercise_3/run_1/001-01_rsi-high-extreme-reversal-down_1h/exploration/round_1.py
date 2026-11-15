def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    H = 12
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            # past returns
            def past(k):
                p = np.full(n, np.nan); p[k:] = c[k:]/c[:-k]-1; return p
            p12 = past(12); p24 = past(24); p72 = past(72)
            vol24 = pd.Series(r1).rolling(24).std().values
            vol168 = pd.Series(r1).rolling(168).std().values
            fwd = np.full(n, np.nan); fwd[:-H] = c[H:]/c[:-H]-1
            fc = df["forecast"].astype(float).values
            alloc = df["postRebalance_current_allocation"].astype(float).values
            for i in range(0, n-H, H):
                rows.append(dict(coin=coin, w=w, fwd=fwd[i], p12=p12[i], p24=p24[i], p72=p72[i],
                                 vol24=vol24[i], vol168=vol168[i], fc=fc[i], alloc=alloc[i],
                                 hour=ts.iloc[i].hour, wd=ts.iloc[i].weekday(), year=ts.iloc[i].year))
    g = pd.DataFrame(rows)
    # demean by coin mean over all windows
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    def summ(grp):
        x = grp["ex"].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    for col in ["p12","p24","p72"]:
        g[col+"_q"] = g.groupby("coin")[col].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        out["fwd12 ex by "+col+" quintile"] = g.groupby(["coin", col+"_q"]).apply(summ)
    g["vr"] = g["vol24"]/g["vol168"]
    for col in ["vol168","vr"]:
        g[col+"_q"] = g.groupby("coin")[col].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        out["fwd12 ex by "+col+" quintile"] = g.groupby(["coin", col+"_q"]).apply(summ)
    out["fwd12 ex by grid hour"] = g.groupby(["hour"]).apply(summ)
    out["fwd12 ex by weekday"] = g.groupby(["wd"]).apply(summ)
    out["fwd12 ex by window"] = g.groupby(["coin","w"]).apply(summ)
    # corr p12 with fwd within vol regime
    out["corr p24-fwd by vol168 q"] = g.dropna(subset=["p24","fwd","vol168_q"]).groupby(["coin","vol168_q"]).apply(lambda d: pd.Series(dict(n=len(d), corr=stats.spearmanr(d.p24, d.fwd)[0])))
    # forecast deciles
    g["fz"] = g["fc"]==0
    nz = g[~g.fz].copy()
    nz["fq"] = pd.qcut(nz["fc"].abs(), 5, labels=False, duplicates="drop")
    out["fwd12 ex by |fc| quintile (nonzero)"] = nz.groupby("fq").apply(summ)
    out["fwd12 ex zero fc"] = summ(g[g.fz])
    # book daily
    drows = []
    for coin in days:
        for w, d in days[coin].items():
            d = d.copy(); d["coin"]=coin; d["w"]=w; drows.append(d)
    D = pd.concat(drows)
    out["book daily by coin"] = D.groupby("coin")[["book_return","coin_return"]].agg(["mean","std","count"])
    out["book daily by window"] = D.groupby(["coin","w"])["book_return"].mean().unstack()
    # trades
    trs = []
    for coin in trades:
        for w, t in trades[coin].items():
            t = t.copy(); t["coin"]=coin; trs.append(t)
    T = pd.concat(trs)
    out["trades summary"] = T.groupby("coin").agg(n=("side","size"), gross=("profit_loss_percent","mean"),
        net=("net_profit_loss_percent","mean"), dur=("duration_minutes","median"))
    # gross pos pnl vs fees
    prow=[]
    for coin in bars:
        for w, df in bars[coin].items():
            c = df["close"].astype(float).values; a = df["postRebalance_current_allocation"].astype(float).values
            v = df["postRebalance_total_value"].astype(float).values
            r = np.r_[c[1:]/c[:-1]-1, np.nan]
            gp = a*r
            vr = np.r_[v[1:]/v[:-1]-1, np.nan]
            prow.append(dict(coin=coin,w=w,gross_mean=np.nanmean(gp),net_mean=np.nanmean(vr), mean_alloc=np.nanmean(a), turnover=np.nanmean(np.abs(np.diff(a)))))
    out["hourly gross vs net"] = pd.DataFrame(prow).groupby("coin").mean(numeric_only=True)
    return out
