def explore(data):
    import numpy as np, pandas as pd
    out={}
    rows=[]; drift={}
    for coin,ws in data["bars"].items():
        for h in (12,24,48):
            vals=[]
            for w,b in ws.items():
                c=b["close"].values; idx=np.arange(0,len(c)-h,h); vals.extend(c[idx+h]/c[idx]-1)
            drift[(coin,h)]=np.mean(vals)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]); c=b["close"].values; v=b["volume"].values
            hr=ts.dt.hour.values; wd=ts.dt.weekday.values
            al=b["postRebalance_current_allocation"].values; f=b["forecast"].values
            for i in np.where(hr==23)[0]:
                if i<168 or i+48>=len(c): continue
                past=c[i]/c[i-48]-1
                lo=max(1,i-720); hv=np.std(np.diff(np.log(c[lo:i+1])))
                d={"coin":coin,"wd":wd[i],"year":ts.iloc[i].year,"side":"up" if past>0 else "down",
                   "s":np.sign(past),"z":abs(past)/(hv*np.sqrt(48)) if hv>0 else np.nan,
                   "vr":v[i-47:i+1].mean()/max(v[i-167:i-47].mean(),1e-12),"alloc":abs(al[i]),"f":abs(f[i]),
                   "held12":np.mean(np.abs(al[i:i+12])>0),"held_after":np.mean(np.abs(al[i+12:i+48])>0)}
                for h in (12,24,48):
                    d[f"x{h}"]=np.sign(past)*(c[i+h]/c[i]-1-drift[(coin,h)])
                    d[f"raw{h}"]=c[i+h]/c[i]-1-drift[(coin,h)]
                rows.append(d)
    df=pd.DataFrame(rows)
    def summ(x):
        r={"n":len(x)}
        for k in ("x12","x24","x48","raw12","raw48"):
            m=x[k].mean(); r[k+"%"]=m*100; r["t_"+k]=m/(x[k].std()/np.sqrt(len(x)))
        r["alloc"]=x["alloc"].mean(); r["held_after"]=x["held_after"].mean()
        return pd.Series(r)
    df["q_vr"]=df.groupby("wd")["vr"].transform(lambda s: pd.qcut(s,10,labels=False))
    sun=df[df.wd==6].copy()
    out["sun_by_vr_decile"]=sun.groupby("q_vr").apply(summ)
    top=sun[sun.q_vr>=8].copy()
    out["sun_topvr_by_side"]=top.groupby("side").apply(summ)
    top["q_z"]=pd.qcut(top["z"],3,labels=False)
    out["sun_topvr_by_movetercile"]=top.groupby("q_z").apply(summ)
    out["sun_topvr_by_year"]=top.groupby("year").apply(summ)
    out["other_days_topvr"]=df[(df.wd!=6)&(df.q_vr>=8)].groupby("wd").apply(summ)
    # allocation vs vr: where does the book put size on Sunday
    sun["alloc_pos"]=sun["alloc"]>0
    out["sun_alloc_share_by_vrdecile"]=sun.groupby("q_vr")[["alloc_pos","alloc","held_after"]].mean()
    # book daily returns on Mondays vs alloc bucket; deepest falls: which weekday
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items(): dd.append(d.assign(coin=coin,w=w))
    D=pd.concat(dd); D["day"]=pd.to_datetime(D["day"]); D["wd"]=D["day"].dt.weekday
    worst=D.nsmallest(40,"book_return")
    out["worst40_coinday_by_wd"]=worst.groupby("wd")["book_return"].agg(["count","sum"])
    out["worst40_coinday_by_coin"]=worst.groupby("coin")["book_return"].agg(["count","sum"])
    out["book_sum_by_wd"]=D.groupby("wd")["book_return"].sum()
    return out
