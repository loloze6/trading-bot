def explore(data):
    import numpy as np, pandas as pd
    rows=[]; blocks=[]
    # market proxy: average 20-bar forward return across coins, keyed by timestamp
    fw={}
    for coin,ws in data["bars"].items():
        rs=[]
        for w,df in ws.items():
            c=df["close"].astype(float).values; rs.append(np.diff(c)/c[:-1])
        mu=np.nanmean(np.concatenate(rs))
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float).values; n=len(c)
            fwd=np.full(n,np.nan)
            if n>20: fwd[:-20]=c[20:]/c[:-20]-1
            f=df["forecast"].astype(float).values
            a=df["postRebalance_current_allocation"].astype(float).values
            on=f>0
            since=np.zeros(n); k=0
            for i in range(n):
                k=k+1 if on[i] else 0; since[i]=k
            ts=pd.to_datetime(df["timestamp"]).values
            for i in range(n):
                rows.append((coin,w,ts[i],f[i],a[i],fwd[i],fwd[i]-20*mu,since[i]))
            ex=fwd-20*mu; v=~np.isnan(ex)
            for b in range(0,n,20):
                m=v[b:b+20]
                if m.sum()==0: continue
                aa=a[b:b+20][m]; ee=ex[b:b+20][m]
                if (aa!=0).any(): blocks.append((coin,w,(aa*ee).sum(),np.mean(f[b:b+20])))
    d=pd.DataFrame(rows,columns=["coin","w","ts","f","a","fwd","ex","since"]).dropna(subset=["ex"])
    d["mkt"]=d.groupby("ts")["fwd"].transform("mean")
    d["ncoin"]=d.groupby("ts")["fwd"].transform("size")
    d["rel"]=d["fwd"]-d["mkt"]
    B=pd.DataFrame(blocks,columns=["coin","w","pnl","fm"])
    def t(x): x=np.asarray(x); return x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))
    out={}
    s=B.pnl.sort_values()
    out["trim"]=pd.Series({"all_mean":s.mean(),"all_t":t(s),"drop_top5_mean":s.iloc[:-5].mean(),"drop_top5_t":t(s.iloc[:-5]),
        "drop_top10_t":t(s.iloc[:-10]),"share_pos":(s>0).mean(),"top10_sum_share":s.iloc[-10:].sum()/s.sum(),
        "winsor_1pct_t":t(s.clip(s.quantile(.01),s.quantile(.99)))})
    act=d[d.f>0].copy()
    act["sq"]=pd.cut(act.since,[0,20,60,120,250,10000])
    out["by_days_since_cross"]=act.groupby("sq").agg(n=("ex","size"),ex=("ex","mean"),med=("ex","median"),hit=("ex",lambda x:(x>0).mean()),rel=("rel","mean"))
    act["fq"]=pd.qcut(act.f,5,labels=False)
    m=act[act.ncoin>=4]
    out["rel_by_fq"]=m.groupby("fq").agg(n=("rel","size"),rel=("rel","mean"),relmed=("rel","median"),relhit=("rel",lambda x:(x>0).mean()),ex=("ex","mean"))
    d2=d[d.ncoin>=4]
    out["rel_on_off"]=d2.groupby(d2.f>0)["rel"].agg(["size","mean","median",lambda x:(x>0).mean()])
    out["top_fq_by_coin"]=act[act.fq==4].groupby("coin").agg(n=("ex","size"),ex=("ex","mean"),med=("ex","median"),hit=("ex",lambda x:(x>0).mean()))
    out["top_fq_by_year"]=act[act.fq==4].groupby(pd.to_datetime(act[act.fq==4].ts).dt.year).agg(n=("ex","size"),ex=("ex","mean"),med=("ex","median"))
    B["fmq"]=pd.qcut(B.fm,3,labels=False)
    out["blocks_by_fmean"]=B.groupby("fmq")["pnl"].agg(["count","mean","median",t])
    return out
