def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # coin mean daily return over all windows
    rows = []
    daily_book = []
    for coin in bars:
        allc = pd.concat([d["coin_return"] for d in days[coin].values()]).dropna()
        mu = allc.mean()
        for w, b in bars[coin].items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            b["day"] = b["ts"].dt.floor("D")
            b["nxt"] = b["close"].shift(-1)/b["close"]-1
            b["pg"] = b["postRebalance_current_allocation"]*b["nxt"]
            b["mkt"] = b["postRebalance_current_allocation"]*mu
            g = b.groupby("day").agg(pg=("pg","sum"), mkt=("mkt","sum"), pos=("postRebalance_current_allocation","mean"))
            d = days[coin][w].set_index(pd.to_datetime(days[coin][w]["day"]).dt.floor("D"))
            g["book"] = d["book_return"].reindex(g.index)
            g["coin"] = coin; g["w"] = w; g["year"] = g.index.year
            rows.append(g)
    D = pd.concat(rows)
    D2 = D.dropna(subset=["book"])
    out["overall"] = pd.Series({"book_mean": D2.book.mean(), "pos_gain_mean": D2.pg.mean(), "market_part": D2.mkt.mean(),
                                "mean_pos": D2.pos.mean(), "share_days_in": (D2.pos.abs()>0.01).mean()})
    out["by_coin"] = D2.groupby("coin").agg(book=("book","mean"), mkt=("mkt","mean"), pos=("pos","mean"), n=("book","size"))
    out["by_year"] = D2.groupby("year").agg(book=("book","mean"), mkt=("mkt","mean"), pos=("pos","mean"), n=("book","size"))
    bw = D2.groupby("w").agg(book=("book","mean"), mkt=("mkt","mean"))
    out["by_window"] = bw
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values() if len(t)])
    pl = T["net_profit_loss_percent"].astype(float)
    s = pl.sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(pl), "mean": pl.mean(), "median": pl.median(), "win": (pl>0).mean(),
        "top10_sum": s.head(10).sum(), "total_sum": pl.sum(), "top5pct_sum": s.head(max(1,len(s)//20)).sum(),
        "dur_days_med": T["duration_minutes"].median()/1440})
    # forward returns after signal at different horizons; signal = first active-regime bar after not active
    res = []
    for coin in bars:
        for w, b in bars[coin].items():
            c = b["close"].values; act = (b["regime"]=="trending").values
            for h in [1,2,5,10,20,40]:
                pass
    # coin usual drift per horizon
    hs=[1,3,5,10,20,40]
    drift = {}
    for coin in bars:
        for h in hs:
            r=[]
            for w,b in bars[coin].items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                r.extend(c[idx+h]/c[idx]-1)
            drift[(coin,h)] = np.mean(r)
    recs=[]
    for coin in bars:
        for w,b in bars[coin].items():
            c=b["close"].values; f=b["forecast"].fillna(0).values
            sig = np.where((f>0)&(np.r_[0,f[:-1]]<=0))[0]
            for i in sig:
                for h in hs:
                    if i+h < len(c):
                        recs.append((coin,w,h,c[i+h]/c[i]-1-drift[(coin,h)], c[i+h]/c[i]-1, f[i]))
    R = pd.DataFrame(recs, columns=["coin","w","h","unus","tot","f"])
    def tt(x): return pd.Series({"n":len(x),"unus":x.unus.mean(),"t":x.unus.mean()/(x.unus.std()/np.sqrt(len(x))),"tot":x.tot.mean()})
    out["entry_by_h"] = R.groupby("h").apply(tt)
    out["entry_h5_by_coin"] = R[R.h==5].groupby("coin").apply(tt)
    out["entry_h20_by_coin"] = R[R.h==20].groupby("coin").apply(tt)
    # all bars in position: next-day return vs drift
    pos=[]
    for coin in bars:
        mu1 = drift[(coin,1)]
        for w,b in bars[coin].items():
            a=b["postRebalance_current_allocation"].values; c=b["close"].values
            r=np.r_[c[1:]/c[:-1]-1, np.nan]
            run20 = pd.Series(c).pct_change(20).values
            pos.append(pd.DataFrame({"coin":coin,"in":a>0.01,"r":r-mu1,"run20":run20}))
    P=pd.concat(pos).dropna()
    out["nextday_in_vs_out"] = P.groupby("in")["r"].agg(["mean","count"])
    P["runq"]=pd.qcut(P.run20,5,labels=False)
    out["nextday_by_run20_quint_all_bars"] = P.groupby("runq")["r"].agg(["mean","count"])
    return out
