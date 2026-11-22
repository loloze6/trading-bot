def explore(data):
    import numpy as np, pandas as pd
    rows=[]; drift_rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]); c=b["close"].values
            n=len(b)
            idx=np.arange(0,n-48,48)
            r=c[idx+48]/c[idx]-1
            ok=(ts.values[idx+48]-ts.values[idx])==np.timedelta64(48,'h')
            for v in r[ok]: drift_rows.append((coin,v))
            hc=np.log(c[1:]/c[:-1])
            close_t=ts+pd.Timedelta(hours=1)
            for i in range(168,n-48):
                ct=close_t.iloc[i]
                if ct.hour!=0: continue
                if (ts.iloc[i+48]-ts.iloc[i])!=pd.Timedelta(hours=48) or (ts.iloc[i]-ts.iloc[i-168])!=pd.Timedelta(hours=168): continue
                past=c[i]/c[i-48]-1; fwd=c[i+48]/c[i]-1; fwd24=c[i+24]/c[i]-1
                vol48=np.std(hc[i-48:i]); vol168=np.std(hc[i-168:i])
                pre5=c[i-48]/c[i-168]-1
                rows.append(dict(coin=coin,window=w,year=ct.year,wd=ct.weekday(),past=past,fwd=fwd,fwd24=fwd24,
                                 vr=vol48/vol168 if vol168>0 else np.nan,pre=pre5,
                                 alloc=b["postRebalance_current_allocation"].iloc[i]))
    d=pd.DataFrame(rows)
    dr=pd.DataFrame(drift_rows,columns=["coin","r"])
    dm=dr.groupby("coin")["r"].mean(); sd=dr.groupby("coin")["r"].std()
    d["unus"]=d["fwd"]-d["coin"].map(dm)
    d["z"]=d["past"]/d["coin"].map(sd)
    out={}
    def st(x):
        return pd.Series(dict(n=len(x),past=x.past.mean(),unus=x.unus.mean(),t=x.unus.mean()/(x.unus.std()/np.sqrt(len(x))),fwd24=x.fwd24.mean()))
    fall=d[d.past<0].copy()
    bins=[-10,-1.5,-1,-0.5,-0.25,0]
    fall["zb"]=pd.cut(fall.z,bins)
    out["fall_by_zbin_wd"]=fall[fall.wd.isin([0,2,3])].groupby(["wd","zb"]).apply(st)
    mon=d[d.wd==0].copy()
    mon["vrq"]=pd.qcut(mon.vr,3,labels=False)
    out["mon_fall_by_volratio"]=mon[mon.past<0].groupby("vrq").apply(st)
    mon["pres"]=np.where(mon.pre<0,"pre_down","pre_up")
    out["mon_fall_by_prior5d"]=mon[mon.past<0].groupby("pres").apply(st)
    # momentum: unusual move signed by past direction, per weekday
    d["mom"]=np.sign(d.past)*d.unus
    out["mom_by_wd"]=d.groupby("wd").apply(lambda x: pd.Series(dict(n=len(x),mom=x.mom.mean(),t=x.mom.mean()/(x.mom.std()/np.sqrt(len(x))))))
    d["mom_z"]=d.z*d.unus/d["coin"].map(sd)
    out["fri_sat_rise_by_year"]=d[(d.wd==4)&(d.past>0)].groupby("year").apply(st)
    # book on Mon signals: allocation vs outcome
    act=mon[mon.alloc.abs()>0]
    out["active_mon"]=pd.Series(dict(n=len(act),mean_alloc=act.alloc.mean(),gain=(act.alloc*act.fwd).mean(),unus=act.unus.mean()))
    return out
