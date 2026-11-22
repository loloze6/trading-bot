def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]; allret=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values.astype(float); v=b["volume"].values.astype(float)
            n=len(c)
            for i in range(0,n-H,H): allret.append((coin,c[i+H]/c[i]-1))
            # failed breakout events from closes
            for t in range(24,n-H):
                if t%H: continue
                j=None
                for k in (1,2,3):
                    jj=t-k
                    if jj-20<0: continue
                    ph=c[jj-20:jj].max()
                    if c[jj]>ph: j=jj; hi=ph; break
                if j is None or c[t]>=hi: continue
                depth=hi/c[t]-1
                pre=c[j-1]/c[j-21]-1 if j-21>=0 else np.nan
                bo=c[j]/hi-1
                tr=c[t]/c[max(0,t-90)]-1 if t>=90 else np.nan
                vr=v[j]/np.nanmean(v[max(0,j-20):j]) if j>=20 else np.nan
                vol=np.std(np.diff(np.log(c[max(1,t-30):t+1])))
                rows.append(dict(coin=coin,w=w,yr=pd.Timestamp(b["timestamp"].iloc[t]).year,
                    fwd=c[t+H]/c[t]-1,depth=depth,pre=pre,bo=bo,tr90=tr,vr=vr,vol=vol,
                    alloc=b["postRebalance_current_allocation"].iloc[t]))
    ev=pd.DataFrame(rows)
    ar=pd.DataFrame(allret,columns=["coin","r"])
    drift=ar.groupby("coin")["r"].mean()
    ev["u"]=-(ev["fwd"]-ev["coin"].map(drift))  # short-direction unusual
    ev["tot"]=-ev["fwd"]
    def g(col,q=4):
        d=ev.dropna(subset=[col]).copy()
        d["b"]=pd.qcut(d[col],q,labels=False,duplicates="drop")
        r=d.groupby("b").agg(n=("u","size"),lo=(col,"min"),hi=(col,"max"),u=("u","mean"),tot=("tot","mean"))
        r["t"]=d.groupby("b")["u"].apply(lambda x:x.mean()/(x.std()/np.sqrt(len(x))))
        return r
    out={"overall":pd.Series({"n":len(ev),"u":ev.u.mean(),"tot":ev.tot.mean(),
          "t":ev.u.mean()/(ev.u.std()/np.sqrt(len(ev))),"drift_mean":ar.r.mean()})}
    for col in ["depth","pre","bo","tr90","vr","vol"]: out["by_"+col]=g(col)
    out["by_coin"]=ev.groupby("coin").agg(n=("u","size"),u=("u","mean"),tot=("tot","mean"))
    out["by_year"]=ev.groupby("yr").agg(n=("u","size"),u=("u","mean"),tot=("tot","mean"))
    # book
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            x=d.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    D=pd.concat(dd)
    D["yr"]=pd.to_datetime(D["day"]).dt.year
    D["inpos"]=D.groupby(["coin","w"])["book_return"].transform(lambda s:s.abs()>0)
    out["book_by_year"]=D.groupby("yr").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    out["book_by_coin"]=D.groupby("coin").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    # trades
    tr=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): tr.append(t)
    T=pd.concat(tr)
    out["trades"]=pd.Series({"n":len(T),"gross":T.profit_loss_percent.mean(),"net":T.net_profit_loss_percent.mean(),
        "win":(T.net_profit_loss_percent>0).mean(),"dur_days":T.duration_minutes.mean()/1440})
    return out
