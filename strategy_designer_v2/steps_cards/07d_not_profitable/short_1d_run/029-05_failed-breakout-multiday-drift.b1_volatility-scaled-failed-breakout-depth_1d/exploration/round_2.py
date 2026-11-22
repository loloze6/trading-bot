def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=8
    rows=[]; drift={}
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            allr+=list(c[idx+H]/c[idx]-1)
        drift[coin]=np.mean(allr)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values; n=len(c)
            r1=np.r_[np.nan,c[1:]/c[:-1]-1]
            seen=set()
            for t in range(3,n-15):
                if f[t]<=-2 and f[t-1]-f[t]>=2:
                    cell=t//H
                    if cell in seen: continue
                    seen.add(cell)
                    d=dict(coin=coin,w=w,absf=-f[t],year=pd.Timestamp(b["timestamp"].iloc[t]).year)
                    # returns from failure bar (t-2) and from signal bar t
                    for h in [1,2,3,5,8,12]:
                        d["fail_h%d"%h]=-(c[t-2+h]/c[t-2]-1)
                        d["sig_h%d"%h]=-(c[t+h]/c[t]-1)
                    d["tot"]=-(c[t+H]/c[t]-1)
                    ma50=np.mean(c[max(0,t-49):t+1]) if t>=49 else np.nan
                    d["below_ma50"]=(c[t]/ma50-1) if t>=49 else np.nan
                    d["ret60"]=c[t]/c[t-60]-1 if t>=60 else np.nan
                    hi60=np.max(c[max(0,t-59):t+1]) if t>=59 else np.nan
                    d["dd60"]=c[t]/hi60-1 if t>=59 else np.nan
                    rows.append(d)
    R=pd.DataFrame(rows)
    out={}
    out["n"]=len(R)
    hz=[k for k in R.columns if k.startswith("fail_h") or k.startswith("sig_h")]
    m=R[hz].mean(); s=R[hz].std(); out["horizons_short_total"]=pd.DataFrame(dict(mean=m,t=m/(s/np.sqrt(len(R)))))
    def summ(g):
        return pd.Series(dict(n=len(g),tot=g.tot.mean(),t=g.tot.mean()/(g.tot.std()/np.sqrt(len(g))),f1=g.fail_h1.mean(),f3=g.fail_h3.mean()))
    for k in ["below_ma50","ret60","dd60"]:
        q=R.dropna(subset=[k]).copy()
        q["q"]=pd.qcut(q[k],4,labels=False,duplicates="drop")
        g=q.groupby("q").apply(summ); g["mid"]=q.groupby("q")[k].median(); out["by_"+k]=g
    R["cap"]=(R.absf>=19.9).astype(int)
    q=R.dropna(subset=["below_ma50"]).copy(); q["trend"]=(q.below_ma50>0).astype(int)
    out["cap_x_trend"]=q.groupby(["cap","trend"]).apply(summ)
    # trades
    T=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; T.append(t)
    T=pd.concat(T)
    T["ef"]=pd.cut(-T.entry_forecast,[-1,2,6,12,19.9,21])
    out["trades_by_entryf"]=T.groupby("ef").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur=("duration_minutes",lambda x:x.mean()/1440))
    T["dur_b"]=pd.cut(T.duration_minutes/1440,[0,1.5,4,8.5,20,1000])
    out["trades_by_dur"]=T.groupby("dur_b").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"))
    # book daily by market state: coin above/below 50d mean
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd=d.copy(); c=dd.close.values
            dd["trend"]=pd.Series(c).rolling(50).mean().values
            dd["trend"]=(dd.close>dd.trend).astype(float).where(~np.isnan(dd.trend))
            dd["coin"]=coin; D.append(dd)
    D=pd.concat(D)
    out["book_by_trend"]=D.groupby("trend").agg(n=("book_return","size"),br=("book_return","mean"),cr=("coin_return","mean"))
    return out
