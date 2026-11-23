import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        d3=[]
        for w,b in ws.items():
            c=b["close"].values
            d3+= [c[i+3]/c[i]-1 for i in range(0,len(c)-3,3)]
        drift=np.mean(d3); sd3=np.std(d3,ddof=1)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; ts=pd.to_datetime(b["timestamp"])
            r1=c.pct_change(); r20=c/c.shift(20)-1
            lr=np.log(c).diff()
            vr=lr.rolling(20).std()/lr.rolling(60).std()
            vol=b["volume"]; volr=vol/vol.rolling(30).mean()
            f3=c.shift(-3)/c-1; f1=c.shift(-1)/c-1
            f13=c.shift(-3)/c.shift(-1)-1
            sd20=lr.rolling(20).std()
            df=pd.DataFrame({"coin":coin,"w":w,"wd":ts.dt.weekday,"yr":ts.dt.year,"r1":r1,"r20":r20,"vr":vr,"volr":volr,
                             "ex3":f3-drift,"ex3s":(f3-drift)/sd3,"f1":f1,"f13":f13,"z1":r1/sd20,"fc":b["forecast"],
                             "alloc":b["postRebalance_current_allocation"]})
            rows.append(df)
    D=pd.concat(rows).dropna(subset=["r1","r20","ex3","vr"])
    out={}
    def tt(x):
        x=x.dropna(); n=len(x); return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    R=D[(D.wd==6)&(D.r1>0)&(D.r20<0)].copy()
    R["vrq"]=pd.qcut(R.vr,4,labels=False); R["r1q"]=pd.qcut(R.z1,4,labels=False); R["r20q"]=pd.qcut(R.r20,4,labels=False)
    out["sunrise_down_by_vrq"]=R.groupby("vrq")["ex3"].apply(tt).unstack()
    out["sunrise_down_by_z1q(3=biggest)"]=R.groupby("r1q")["ex3"].apply(tt).unstack()
    out["sunrise_down_by_r20q(0=deepest)"]=R.groupby("r20q")["ex3"].apply(tt).unstack()
    out["sunrise_down_by_year"]=R.groupby("yr")["ex3"].apply(tt).unstack()
    out["sunrise_down_mon_vs_tuewed"]=pd.DataFrame({"mon":tt(R.f1),"tue_wed":tt(R.f13)})
    S=D[(D.wd==6)&(D.r1<0)&(D.r20<0)].copy()
    S["vrq"]=pd.qcut(S.vr,4,labels=False)
    out["sunfall_down_by_vrq_t"]=S.groupby("vrq")["ex3"].apply(tt).unstack()
    out["sunfall_down_mon_vs_tuewed"]=pd.DataFrame({"mon":tt(S.f1),"tue_wed":tt(S.f13)})
    # signed sunday move in downtrend: regression of ex3s on z1, all sunday downtrend
    SD=D[(D.wd==6)&(D.r20<0)]
    sl=stats.linregress(SD.z1,SD.ex3s); out["sun_down_all_slope_z1"]=pd.Series({"n":len(SD),"slope":sl.slope,"t":sl.slope/sl.stderr})
    # vr effect on any day in downtrend falls (non-Sunday) - is vr generic?
    N=D[(D.wd!=6)&(D.r1<0)&(D.r20<0)].copy(); N["vrq"]=pd.qcut(N.vr,4,labels=False)
    out["nonsun_fall_down_by_vrq"]=N.groupby("vrq")["ex3"].apply(tt).unstack()
    # deep 20d downtrend any day (non-overlap: use every 3rd row approx via wd==6 only? use all weekdays separately)
    D["r20q"]=D.groupby("coin")["r20"].transform(lambda s:pd.qcut(s,5,labels=False))
    out["ex3_by_r20q_x_wd(mean)"]=D.groupby(["r20q","wd"])["ex3"].mean().unstack()
    # book: largest gain/loss days by weekday
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; dd.append(d)
    DD=pd.concat(dd)
    bk=DD.groupby(["w","day"]).agg(br=("book_return","mean")).reset_index().dropna()
    bk["wd"]=pd.to_datetime(bk["day"]).dt.weekday
    out["book_by_weekday"]=bk.groupby("wd")["br"].apply(tt).unstack()
    q=bk.br.quantile([0.02,0.98]).values
    out["book_extreme_days_wd"]=pd.DataFrame({"worst2pct":bk[bk.br<=q[0]].wd.value_counts(),"best2pct":bk[bk.br>=q[1]].wd.value_counts()})
    return out
