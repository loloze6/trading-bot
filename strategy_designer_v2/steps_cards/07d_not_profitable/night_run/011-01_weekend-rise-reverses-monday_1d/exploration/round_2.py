def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            ts=pd.to_datetime(b["timestamp"]); wd=ts.dt.weekday.values
            c=b["close"].values; n=len(b)
            r=np.full(n,np.nan); r[1:]=c[1:]/c[:-1]-1
            s=pd.Series(r).abs().rolling(60,min_periods=20).mean().shift(0).values
            z=r/s
            mon=np.full(n,np.nan); mon[:-1]=c[1:]/c[:-1]-1
            tue=np.full(n,np.nan); tue[:-2]=c[2:]/c[1:-1]-1
            wed=np.full(n,np.nan); wed[:-3]=c[3:]/c[2:-1]-1
            r3d=np.full(n,np.nan); r3d[3:]=c[3:]/c[:-3]-1  # fri..sun 3-day
            vol=pd.Series(r).rolling(60,min_periods=20).std().values
            df=pd.DataFrame({"coin":coin,"w":w,"wd":wd,"z":z,"rs":r,"mon":mon,"tue":tue,"wed":wed,"r3d":r3d,"vol":vol,"fc":b["forecast"].values,"pos":b["postRebalance_current_allocation"].values})
            rows.append(df[df.wd==6])
    d=pd.concat(rows,ignore_index=True).dropna(subset=["z","mon"])
    d["zc"]=d.z.clip(-20,20)
    out={}
    def tt(x):
        x=pd.Series(x).dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    d["zbin"]=pd.qcut(d.z,6,labels=False)
    out["sunday z sextile: z, mon, tue, wed"]=d.groupby("zbin").agg(n=("mon","size"),z=("z","mean"),mon=("mon","mean"),tue=("tue","mean"),wed=("wed","mean"))
    # vol-scaled hypothetical gains: pos = -z/10 * 0.38/(vol*sqrt365) capped 2
    sc=(0.382/(d.vol*np.sqrt(365))).clip(upper=2)
    pos_short=(-d.zc.clip(lower=0)/10)*sc
    pos_sym=(-d.zc/10)*sc
    out["hyp gains per sunday"]=pd.DataFrame({
        "short_mon":tt(pos_short*d.mon),
        "short_montue":tt(pos_short*(d.mon+d.tue)),
        "sym_mon":tt(pos_sym*d.mon),
        "sym_montue":tt(pos_sym*(d.mon+d.tue)),
        "actual_short_mon":tt(d.pos*d.mon)})
    d["g"]=pos_sym*(d.mon+d.tue)
    d["ga"]=d.pos*d.mon
    out["by window: actual vs sym2d"]=d.groupby("w")[["ga","g"]].mean().agg(["mean","min"]).T.assign(share_pos=[ (d.groupby("w").ga.mean()>0).mean(),(d.groupby("w").g.mean()>0).mean()])
    out["by coin sym2d"]=d.groupby("coin").g.apply(lambda x: tt(x)).unstack()
    out["mean abs pos actual active"]=d.loc[d.fc<0,"pos"].abs().mean()
    # down weekend: grading
    dn=d[d.z<0]
    out["down sundays: corr z vs mon+tue"]=pd.Series({"n":len(dn),"corr":np.corrcoef(dn.z,(dn.mon+dn.tue).fillna(0))[0,1]})
    return out
