def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float).values
            r=np.r_[np.nan, c[1:]/c[:-1]-1]
            nxt=np.r_[r[1:], np.nan]
            ar=pd.Series(np.abs(r)).rolling(30,min_periods=20).mean().shift(1).values
            ts=pd.to_datetime(b["timestamp"])
            n=len(c)
            for t in range(2,n):
                # run before t of down closes
                k=0; loss=0.0; j=t-1
                while j>=1 and r[j]<0:
                    k+=1; loss+= -r[j]; j-=1
                # up-run before t
                ku=0; gain=0.0; j=t-1
                while j>=1 and r[j]>0:
                    ku+=1; gain+=r[j]; j-=1
                rows.append(dict(coin=coin,w=w,t=t,day=ts[t].normalize(),wd=ts[t].dayofweek,
                    r=r[t],nxt=nxt[t],usual=ar[t],downk=k,downloss=loss,upk=ku,upgain=gain,
                    regime=b["regime"].iloc[t],alloc=b["postRebalance_current_allocation"].iloc[t]))
    d=pd.DataFrame(rows).dropna(subset=["nxt","r","usual"])
    drift=d.groupby("coin")["nxt"].transform("mean")
    d["ex"]=d["nxt"]-drift
    d["prof"]=np.where(d["regime"]=="chop","outside","fallcalm")
    d["depth"]=d["downloss"]/d["usual"]
    d["zr"]=d["r"]/d["usual"]
    def summ(g):
        x=g["ex"]
        dd=g.groupby("day")["ex"].sum()
        t=dd.mean()/(dd.std(ddof=1)/np.sqrt(len(dd))) if len(dd)>2 else np.nan
        return pd.Series(dict(n=len(x),days=len(dd),mean_ex=x.mean(),t_day=t))
    out={}
    up=d[d["r"]>0].copy()
    up["dbin"]=pd.cut(up["depth"],[-0.01,0.001,1,2,3,5,100])
    out["upday_after_downrun_by_depth_prof"]=up.groupby(["prof","dbin"]).apply(summ)
    dn=d[d["r"]<0].copy()
    dn["gain_u"]=dn["upgain"]/dn["usual"]
    dn["gbin"]=pd.cut(dn["gain_u"],[-0.01,0.001,1,2,3,5,100])
    out["downday_after_uprun_by_depth_prof"]=dn.groupby(["prof","gbin"]).apply(summ)
    d["zbin"]=pd.cut(d["zr"],[-100,-3,-2,-1,0,1,2,3,100])
    out["nextday_by_todaymove_prof"]=d.groupby(["prof","zbin"]).apply(summ)
    out["nextday_by_weekday_prof"]=d.groupby(["prof","wd"]).apply(summ)
    # book days
    bd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; bd.append(x)
    bd=pd.concat(bd)
    bd["year"]=pd.to_datetime(bd["day"]).dt.year
    out["book_by_window"]=bd.groupby("w")["book_return"].agg(["mean","count","sum"])
    # trades
    tr=[]
    for coin,ws in data["trades"].items():
        for w,x in ws.items():
            if len(x): x=x.copy(); x["coin"]=coin; x["w"]=w; tr.append(x)
    tr=pd.concat(tr)
    out["trades_by_coin"]=tr.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"])
    tr["et"]=pd.to_datetime(tr["entry_time"])
    out["trades_by_weekday"]=tr.groupby(tr["et"].dt.dayofweek)["net_profit_loss_percent"].agg(["count","mean"])
    out["trades_by_year"]=tr.groupby(tr["et"].dt.year)["net_profit_loss_percent"].agg(["count","mean"])
    out["regime_share"]=d["regime"].value_counts(normalize=True)
    return out
