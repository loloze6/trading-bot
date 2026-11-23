import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        # drift: non-overlapping 3-day returns over all windows
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
            df=pd.DataFrame({"coin":coin,"w":w,"wd":ts.dt.weekday,"yr":ts.dt.year,"r1":r1,"r20":r20,"vr":vr,"volr":volr,
                             "ex3":f3-drift,"ex3s":(f3-drift)/sd3,"f1":f1,"fc":b["forecast"]})
            rows.append(df)
    D=pd.concat(rows).dropna(subset=["r1","r20","ex3"])
    out={}
    def summ(g):
        x=g["ex3"]; n=len(x)
        sl=stats.linregress(g["r1"],g["ex3s"]) if n>10 else None
        return pd.Series({"n":n,"mean_ex3":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)),
                          "slope_r1":sl.slope if sl else np.nan,"t_slope":(sl.slope/sl.stderr) if sl else np.nan})
    fall=D[D.r1<0]
    out["fall_by_wd_downtrend"]=fall[fall.r20<0].groupby("wd").apply(summ)
    out["fall_by_wd_uptrend"]=fall[fall.r20>=0].groupby("wd").apply(summ)
    rise=D[D.r1>0]
    out["rise_by_wd_downtrend"]=rise[rise.r20<0].groupby("wd").apply(summ)
    S=fall[(fall.wd==6)&(fall.r20<0)].copy()
    S["vrq"]=pd.qcut(S.vr,4,labels=False); S["volq"]=pd.qcut(S.volr,4,labels=False); S["r1q"]=pd.qcut(S.r1,4,labels=False)
    S["r20q"]=pd.qcut(S.r20,4,labels=False)
    out["sun_down_by_vrq"]=S.groupby("vrq")["ex3"].agg(["count","mean"])
    out["sun_down_by_volq"]=S.groupby("volq")["ex3"].agg(["count","mean"])
    out["sun_down_by_r1q(0=biggest fall)"]=S.groupby("r1q")["ex3"].agg(["count","mean"])
    out["sun_down_by_r20q(0=deepest)"]=S.groupby("r20q")["ex3"].agg(["count","mean"])
    out["sun_down_by_year"]=S.groupby("yr")["ex3"].agg(["count","mean"])
    out["sun_down_next1_mean_f1"]=float(S.f1.mean())
    # all days, downtrend, fall size quartile across all weekdays
    A=fall[fall.r20<0].copy(); A["isSun"]=A.wd==6
    A["r1s"]=A.groupby("coin")["r1"].transform(lambda s:s/s.std())
    A["r1q"]=pd.qcut(A.r1s,5,labels=False)
    out["down_fall_size_q_x_sun"]=A.groupby(["r1q","isSun"])["ex3"].mean().unstack()
    # book daily
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; dd.append(d)
    DD=pd.concat(dd); DD["yr"]=pd.to_datetime(DD["day"]).dt.year
    bk=DD.groupby(["w","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).reset_index()
    bk["yr"]=pd.to_datetime(bk["day"]).dt.year
    out["book_by_year"]=bk.groupby("yr").agg(n=("br","count"),mean=("br","mean"),sd=("br","std"),hold=("cr","mean"))
    return out
