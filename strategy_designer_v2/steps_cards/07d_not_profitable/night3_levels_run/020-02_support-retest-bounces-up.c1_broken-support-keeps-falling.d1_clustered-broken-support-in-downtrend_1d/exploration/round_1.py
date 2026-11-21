def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]; drift={}
    bk=[]
    for coin,ws in data["bars"].items():
        allf=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(c)
            s=pd.Series(c)
            ma=s.rolling(50).mean().values
            r5p=s.pct_change(5).values; r20p=s.pct_change(20).values
            vol=s.pct_change().rolling(20).std().values
            raw=b.get("debug_info.components.low_cluster.last_history_value")
            raw=raw.values if raw is not None else np.full(n,np.nan)
            for i in range(0,n-5,5):
                f=c[i+5]/c[i]-1; allf.append(f)
                rows.append(dict(coin=coin,w=w,f=f,reg=b["regime"].iloc[i],raw=raw[i],
                    fc=b["forecast"].iloc[i],alloc=b["postRebalance_current_allocation"].iloc[i],
                    dma=c[i]/ma[i]-1 if not np.isnan(ma[i]) else np.nan,r5=r5p[i],r20=r20p[i],vol=vol[i],
                    year=pd.Timestamp(b["timestamp"].iloc[i]).year))
        drift[coin]=np.mean(allf)
    d=pd.DataFrame(rows); d["u"]=d["f"]-d["coin"].map(drift)
    mr=d[d.reg=="mean_reversion"].copy()
    def g(df,col,q=5):
        x=df.dropna(subset=[col]).copy()
        x["b"]=pd.qcut(x[col].rank(method="first"),q,labels=False)
        return x.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("u","size"),u_long=("u","mean"),
            t=("u",lambda v: v.mean()/(v.std()/np.sqrt(len(v)))))
    out={}
    out["regime_u_long"]=d.groupby("reg")["u"].agg(["size","mean"])
    act=mr[mr.raw>0]
    out["active_raw_q"]=g(act,"raw")
    out["mr_dma_q"]=g(mr,"dma")
    out["mr_r5_q"]=g(mr,"r5")
    out["mr_r20_q"]=g(mr,"r20")
    out["mr_vol_q"]=g(mr,"vol")
    out["mr_raw0_vs_pos"]=mr.assign(p=mr.raw>0).groupby("p")["u"].agg(["size","mean"])
    out["all_dma_q"]=g(d,"dma",6)
    out["act_year"]=act.groupby("year")["u"].agg(["size","mean"])
    # book
    bd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            bd.append(x.assign(coin=coin,w=w))
    bd=pd.concat(bd)
    bd["year"]=pd.to_datetime(bd["day"]).dt.year
    out["book_year"]=bd.groupby("year")[["book_return","coin_return"]].mean()
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
    out["trades"]=tr.groupby("side")[["profit_loss_percent","net_profit_loss_percent"]].agg(["count","mean"])
    return out
