import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; h=b["high"]; l=b["low"]
            r1=c.pct_change()
            hh=h.rolling(20).max(); ll=l.rolling(20).min()
            pos=(c-ll)/(hh-ll)
            nxt=c.shift(-1)/c-1
            nxt2=c.shift(-2)/c-1
            vol30=r1.rolling(30).std()
            tr60=c/c.shift(60)-1
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"day":ts.dt.floor("D"),"wd":ts.dt.weekday,
                "r1":r1,"pos":pos,"nxt":nxt,"nxt2":nxt2,"z":r1/vol30,"tr60":tr60,
                "alloc":b["postRebalance_current_allocation"],"fc":b["forecast"]})
            rows.append(df)
    d=pd.concat(rows)
    mu=d.groupby("coin")["nxt"].transform("mean")
    d["ex"]=d["nxt"]-mu
    d=d.dropna(subset=["r1","pos","ex"])
    def tday(g):
        s=g.groupby("day")["ex"].sum(); n=g.groupby("day").size()
        m=g["ex"].mean(); dev=(g["ex"]-m).groupby(g["day"]).sum()
        G=len(s); se=np.sqrt((dev**2).sum()*G/(G-1))/len(g)
        return pd.Series({"n":len(g),"days":G,"mean_ex%":m*100,"t":m/se})
    out={}
    up=d[d.r1>0].copy(); dn=d[d.r1<0].copy()
    up["q"]=pd.qcut(up.pos,5,labels=False); dn["q"]=pd.qcut(dn.pos,5,labels=False)
    out["up_by_pos_quint"]=up.groupby("q").apply(tday)
    out["down_by_pos_quint"]=dn.groupby("q").apply(tday)
    d["zq"]=pd.qcut(d.z,10,labels=False)
    out["all_by_z_decile"]=d.groupby("zq").apply(tday)
    d["prof"]=np.where(d.tr60>0.1,"rising",np.where(d.tr60<-0.1,"falling","choppy"))
    lowup=up[up.q<=1].copy(); lowup["prof"]=np.where(lowup.tr60>0.1,"rising",np.where(lowup.tr60<-0.1,"falling","choppy"))
    out["lowup_by_trend"]=lowup.groupby("prof").apply(tday)
    out["lowup_by_window"]=lowup.groupby("w").apply(tday)
    out["all_by_wd"]=d.groupby("wd").apply(tday)
    pq=pd.qcut(d.pos,5,labels=False); d["pq"]=pq
    out["all_by_pos_quint"]=d.groupby("pq").apply(tday)
    out["book_short_days_share"]=float((d.alloc<0).mean())
    return out
