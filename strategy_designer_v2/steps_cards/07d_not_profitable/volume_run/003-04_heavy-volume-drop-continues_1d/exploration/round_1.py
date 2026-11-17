def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # book daily returns
    br=[];cr=[]
    for c in data["days"]:
        for w,d in data["days"][c].items():
            br.append(d["book_return"].dropna()); cr.append(d["coin_return"].dropna())
    br=pd.concat(br); cr=pd.concat(cr)
    out["book_daily"]=pd.Series({"mean":br.mean(),"std":br.std(),"n":len(br),"share_nonzero":(br.abs()>1e-12).mean(),"coin_mean":cr.mean()})
    # trades
    tr=[]
    for c in data["trades"]:
        for w,t in data["trades"][c].items():
            if len(t): tt=t.copy(); tt["coin"]=c; tr.append(tt)
    tr=pd.concat(tr)
    out["trades"]=pd.Series({"n":len(tr),"mean_pl":tr["profit_loss_percent"].mean(),"mean_net":tr["net_profit_loss_percent"].mean(),
        "median_dur_days":tr["duration_minutes"].median()/1440,"mean_dur_days":tr["duration_minutes"].mean()/1440,"win":(tr["net_profit_loss_percent"]>0).mean()})
    # events: forward returns per horizon, coin-mean adjusted, and splits
    rows=[]
    cm={}
    for c in data["bars"]:
        for h in [1,2,3,5,10]:
            r=[]
            for w,b in data["bars"][c].items():
                cl=b["close"].values
                idx=np.arange(0,len(cl)-h,h)
                r+=list(cl[idx+h]/cl[idx]-1)
            cm[(c,h)]=np.mean(r)
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            cl=b["close"].values; f=b["forecast"].fillna(0).values
            al=b["postRebalance_current_allocation"].fillna(0).values
            ret=pd.Series(cl).pct_change()
            vol=ret.rolling(20).std()
            r20=pd.Series(cl).pct_change(20).values
            r60=pd.Series(cl).pct_change(60).values
            last=-99
            for i in range(len(cl)):
                if f[i]<0 and i-last>=5:
                    last=i
                    d={"coin":c,"f":f[i],"r1":ret.iloc[i],"r20":r20[i],"r60":r60[i],"alloc":al[i]}
                    for h in [1,2,3,5,10]:
                        d[f"x{h}"]=cl[i+h]/cl[i]-1-cm[(c,h)] if i+h<len(cl) else np.nan
                    rows.append(d)
    ev=pd.DataFrame(rows)
    def summ(g):
        s={}
        for h in [1,2,3,5,10]:
            x=g[f"x{h}"].dropna(); s[f"m{h}"]=x.mean(); s[f"t{h}"]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        s["n"]=len(g); return pd.Series(s)
    out["all_events"]=summ(ev)
    out["by_coin"]=ev.groupby("coin").apply(summ)
    ev["r20q"]=pd.qcut(ev["r20"],3,labels=["down","mid","up"])
    out["by_prior20d"]=ev.groupby("r20q").apply(summ)
    ev["r60q"]=pd.qcut(ev["r60"],3,labels=["down","mid","up"])
    out["by_prior60d"]=ev.groupby("r60q").apply(summ)
    ev["fq"]=pd.qcut(ev["f"].rank(method="first"),3,labels=["strong","midf","weak"])
    out["by_forecast"]=ev.groupby("fq").apply(summ)
    out["alloc_on_event"]=ev["alloc"].describe()
    return out
