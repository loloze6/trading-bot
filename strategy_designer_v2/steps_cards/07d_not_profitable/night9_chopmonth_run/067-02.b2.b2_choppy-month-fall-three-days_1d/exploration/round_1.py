def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    # coin mean h-return over all windows (grid)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            r7 = pd.Series(c).pct_change(7).values
            vol10 = pd.Series(c).pct_change().rolling(10).std().values
            vol30 = pd.Series(c).pct_change().rolling(30).std().values
            r30 = pd.Series(c).pct_change(30).values
            for h in (3, 5, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, ts=df["timestamp"].iloc[i],
                                     ret=c[i+h]/c[i]-1, fc=df["forecast"].iloc[i],
                                     reg=df["regime"].iloc[i], r7=r7[i], r30=r30[i],
                                     vr=vol10[i]/vol30[i] if vol30[i] else np.nan))
    g = pd.DataFrame(rows)
    g["mu"] = g.groupby(["coin","h"])["ret"].transform("mean")
    g["ex"] = g["ret"] - g["mu"]
    g["day"] = pd.to_datetime(g["ts"]).dt.floor("D")
    out = {}
    def summ(d):
        if len(d) < 5: return pd.Series(dict(n=len(d)))
        return pd.Series(dict(n=len(d), raw_short=-d["ret"].mean(), ex_short=-d["ex"].mean(),
                              t_raw=-d["ret"].mean()/(d["ret"].std()/np.sqrt(len(d))),
                              t_ex=-d["ex"].mean()/(d["ex"].std()/np.sqrt(len(d)))))
    sig = g[g["fc"] < 0].copy()
    out["signal by horizon"] = sig.groupby("h").apply(summ)
    chop_nosig = g[(g["reg"]=="unknown") & (g["fc"]==0)]
    out["choppy no signal by h (short gain)"] = chop_nosig.groupby("h").apply(summ)
    out["all bars by h"] = g.groupby("h").apply(summ)
    s3 = sig[sig.h==3].copy()
    s3["terc"] = pd.qcut(s3["fc"].rank(method="first"), 3, labels=["deep","mid","shallow"])
    out["h3 by tercile"] = s3.groupby("terc").apply(summ)
    sig_all = sig.copy()
    sig_all["terc"] = sig_all.groupby("h")["fc"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    out["by h and tercile (0 deep)"] = sig_all.groupby(["h","terc"]).apply(summ)
    s3["r7pos"] = np.where(s3["r7"]>0, "r7 up", "r7 down")
    out["h3 by 7d return sign"] = s3.groupby("r7pos").apply(summ)
    s3["vrh"] = np.where(s3["vr"]>1, "vol rising", "vol falling")
    out["h3 by vol10/vol30"] = s3.groupby("vrh").apply(summ)
    out["h3 by window"] = s3.groupby("w").apply(summ)
    out["h3 by coin"] = s3.groupby("coin").apply(summ)
    # condition alone: r30<0 outside choppy / r7 down without signal
    g3 = g[g.h==3]
    out["h3 r30<0 non-choppy (short gain)"] = summ(g3[(g3.reg!="unknown") & (g3.r30<0)])
    out["h3 r7 down, choppy, no signal"] = summ(chop_nosig[(chop_nosig.h==3)&(chop_nosig.r7<=0)])
    out["h3 r7 up, choppy, no signal"] = summ(chop_nosig[(chop_nosig.h==3)&(chop_nosig.r7>0)])
    # book
    bd = []
    for coin, wins in days.items():
        for w, df in wins.items():
            d = df.dropna(subset=["book_return"])
            bd.append(pd.DataFrame(dict(w=w, coin=coin, br=d["book_return"].values, cr=d["coin_return"].values)))
    bd = pd.concat(bd)
    out["book by window"] = bd.groupby("w").agg(mean_book=("br","mean"), mean_coin=("cr","mean"), n=("br","size"))
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, df in wins.items():
            if len(df): tr.append(df.assign(w=w))
    tr = pd.concat(tr)
    tr["dur_d"] = tr["duration_minutes"]/1440
    out["trades"] = tr.groupby("side").agg(n=("net_profit_loss_percent","size"), gross=("profit_loss_percent","mean"),
                                           net=("net_profit_loss_percent","mean"), dur=("dur_d","mean"),
                                           win=("net_profit_loss_percent", lambda x:(x>0).mean()))
    return out
