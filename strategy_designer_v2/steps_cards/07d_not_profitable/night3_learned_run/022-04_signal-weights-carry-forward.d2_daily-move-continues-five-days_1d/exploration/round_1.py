def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        # coin mean 5-bar return over all windows
        g=[]
        for w,b in ws.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-5,5)
            g+=list(c[idx+5]/c[idx]-1)
        mu=np.mean(g)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]
            r1=c.pct_change()
            r20=c/c.shift(20)-1
            vol=r1.rolling(20).std()
            vol120=r1.rolling(120,min_periods=40).std()
            rng=(b["high"]-b["low"])/c
            yr=pd.to_datetime(b["timestamp"]).dt.year
            for i in range(0,len(b)-5,5):
                f=b["forecast"].iloc[i]
                if pd.isna(f) or f==0: continue
                fr=c.iloc[i+5]/c.iloc[i]-1
                s=np.sign(f)
                rows.append(dict(coin=coin,w=w,yr=yr.iloc[i],f=f,af=abs(f),s=s,
                    fr=fr,sig=s*(fr-mu),tot=s*fr,
                    agree=np.sign(r20.iloc[i])==s if not pd.isna(r20.iloc[i]) else np.nan,
                    r20s=s*r20.iloc[i] if not pd.isna(r20.iloc[i]) else np.nan,
                    vr=vol.iloc[i]/vol120.iloc[i] if not pd.isna(vol120.iloc[i]) else np.nan,
                    alloc=abs(b["postRebalance_current_allocation"].iloc[i])))
    d=pd.DataFrame(rows)
    def agg(x):
        return pd.Series(dict(n=len(x),sig_bps=x.sig.mean()*1e4,tot_bps=x.tot.mean()*1e4,
            t=x.sig.mean()/(x.sig.std()/np.sqrt(len(x)))))
    out={}
    d["afq"]=pd.qcut(d.af,5,labels=False)
    out["by_absforecast_quintile"]=d.groupby("afq").apply(agg)
    out["by_side"]=d.groupby("s").apply(agg)
    out["by_side_x_bigday"]=d.groupby(["s",d.af>=15]).apply(agg)
    dd=d.dropna(subset=["agree"])
    out["by_agree_20d_trend"]=dd.groupby("agree").apply(agg)
    out["by_agree_x_big"]=dd.groupby(["agree",dd.af>=15]).apply(agg)
    dv=d.dropna(subset=["vr"])
    dv["vq"]=pd.qcut(dv.vr,3,labels=False)
    out["by_volratio_tercile"]=dv.groupby("vq").apply(agg)
    out["by_coin"]=d.groupby("coin").apply(agg)
    out["by_year"]=d.groupby("yr").apply(agg)
    # book
    bk=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; bk.append(x)
    bk=pd.concat(bk)
    bk["yr"]=pd.to_datetime(bk["day"]).dt.year
    out["book_by_year"]=bk.groupby("yr").agg(book_bps=("book_return",lambda v:v.mean()*1e4),coin_bps=("coin_return",lambda v:v.mean()*1e4))
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items() if len(t)])
    out["trades"]=tr.groupby("side").agg(n=("side","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur_days=("duration_minutes",lambda v:v.mean()/1440))
    return out
