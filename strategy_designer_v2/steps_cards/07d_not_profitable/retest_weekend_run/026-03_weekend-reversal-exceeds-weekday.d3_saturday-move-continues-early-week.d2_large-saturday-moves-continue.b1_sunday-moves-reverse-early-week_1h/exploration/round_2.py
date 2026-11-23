def explore(data):
    import numpy as np, pandas as pd
    rows=[]; hold=[]
    for coin,ws in data["bars"].items():
        rr=[]
        for w,b in ws.items():
            c=b["close"].values.astype(float); idx=np.arange(0,len(c)-48,48); rr.append(c[idx+48]/c[idx]-1)
        dr=np.nanmean(np.concatenate(rr))
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"])+pd.Timedelta(hours=1)
            c=b["close"].values.astype(float); n=len(c)
            ret1=np.append(c[1:]/c[:-1]-1,np.nan)
            r24=pd.Series(c).pct_change(24); z=(r24/r24.abs().rolling(720,min_periods=200).mean()).values
            vol=pd.Series(c).pct_change().rolling(720,min_periods=200).std().values
            fc=b["forecast"].values; al=b["postRebalance_current_allocation"].fillna(0).values
            prev=b["previous_allocation"].fillna(0).values
            hrs=ts.dt.hour.values; wds=ts.dt.weekday.values
            hold.append(pd.DataFrame({"wd":wds,"held":np.abs(al)>1e-6,"gain":al*ret1,"turn":np.abs(al-prev)}))
            for i in np.where(hrs==0)[0]:
                if np.isnan(z[i]) or i+48>=n: continue
                d={"coin":coin,"wd":wds[i],"z":z[i],"fc":fc[i],"al":al[i],"vol":vol[i],
                   "r48":c[i+48]/c[i]-1-dr,"raw48":c[i+48]/c[i]-1,
                   "book48":np.nansum(al[i:i+48]*ret1[i:i+48]),
                   "al_after48":al[i+48] if i+48<n else np.nan}
                rows.append(d)
    df=pd.DataFrame(rows)
    df["vq"]=df.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    def summ(g,col="r48"):
        x=(-np.sign(g["z"])*g[col]).dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x))})
    def bk(g):
        x=g["book48"].dropna()
        return pd.Series({"n":len(x),"book48":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)),"abs_al":g.al.abs().mean()})
    out={}
    mon=df[df.wd==0].copy()
    mon["agree"]=np.sign(mon.fc)==-np.sign(mon.z)
    out["mon_sign_agree_share"]=float(mon.agree.mean())
    out["mon_fc_zero_share"]=float((mon.fc==0).mean())
    out["mon_by_agree"]=mon.groupby("agree").apply(lambda g: pd.concat([summ(g),bk(g)]))
    mon["fq"]=pd.qcut(mon.fc.abs(),5,labels=False,duplicates="drop")
    out["mon_by_absfc_quint"]=mon.groupby("fq").apply(lambda g: pd.concat([summ(g),bk(g),pd.Series({"absfc":g.fc.abs().mean(),"absz":g.z.abs().mean()})]))
    out["mon_by_vq"]=mon.groupby("vq").apply(lambda g: pd.concat([summ(g),bk(g),pd.Series({"absraw48":g.raw48.abs().mean()})]))
    out["mon_by_vq_side"]=mon.groupby(["vq",np.where(mon.z>0,"short","long")]).apply(summ)
    out["mon_share_still_held_at_48"]=float((mon.al_after48.abs()>1e-6).mean())
    oth=df[df.wd.isin([1,2,3,4,5])]
    out["otherdays_by_vq_condition_alone"]=oth.groupby("vq").apply(summ)
    H=pd.concat(hold)
    out["held_share_and_gain_by_weekday"]=H.groupby("wd").agg(held=("held","mean"),gain=("gain","mean"),turn=("turn","mean"))
    return out
