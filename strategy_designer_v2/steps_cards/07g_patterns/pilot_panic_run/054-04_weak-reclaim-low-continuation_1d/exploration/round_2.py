import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; lo=b["low"].values; hi=b["high"].values
            n=len(b)
            low30=pd.Series(lo).shift(1).rolling(30).min().values
            ret60=pd.Series(c).pct_change(60).values
            r1=pd.Series(c).pct_change().values
            fwd={}
            for h in (5,10):
                f=np.full(n,np.nan); f[:n-h]=c[h:]/c[:n-h]-1; fwd[h]=f
            rng=hi-lo
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(n),
                "pierce":(lo<low30)&(c>low30),
                "near":np.where(rng>0,1-(c-low30)/rng,np.nan),
                "depth":np.where(low30>0,(low30-lo)/low30,np.nan),
                "r1":r1,"ret60":ret60,"fa":(b["regime"].values!="chop"),
                "year":ts.dt.year.values,"day":ts.dt.floor("D").values,
                "f5":fwd[5],"f10":fwd[10]}))
    d=pd.concat(rows,ignore_index=True)
    out={}
    drift={h:d[d.pos%h==0].groupby("coin")["f%d"%h].mean() for h in (5,10)}
    def cases(sub,h):
        s=sub[sub.pierce].assign(cell=lambda x:x.pos//h)
        s=s.groupby(["coin","w","cell"]).head(1).copy()
        s["u"]=s["f%d"%h]-s.coin.map(drift[h])
        return s.dropna(subset=["u"])
    def dayt(s):
        g=s.groupby("day")["u"].sum(); D=len(g)
        if D<3: return [len(s),D,s.u.mean() if len(s) else np.nan,np.nan]
        se=np.sqrt((g-g.mean()*0).pow(2).sum()*0+((g - s.u.mean()*s.groupby("day").size())**2).sum()*D/(D-1))/len(s)
        return [len(s),D,s.u.mean(),s.u.mean()/se]
    res=[]
    for h in (5,10):
        for lab,sub in [("all",d),("fa",d[d.fa]),("notfa",d[~d.fa])]:
            res.append([h,lab]+dayt(cases(sub,h)))
    out["daycluster"]=pd.DataFrame(res,columns=["h","prof","n","days","mean","t_day"])
    s=cases(d[~d.fa],5)
    f=lambda x: pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out["notfa_by_window"]=s.groupby("w")["u"].apply(f).unstack()
    out["notfa_by_coin"]=s.groupby("coin")["u"].apply(f).unstack()
    out["notfa_by_year"]=s.groupby("year")["u"].apply(f).unstack()
    s["trend"]=pd.cut(s.ret60,[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    out["notfa_by_trend"]=s.groupby("trend")["u"].apply(f).unstack()
    out["notfa_trend_missing"]=int(s.ret60.isna().sum())
    ss=s.dropna(subset=["near"])
    lr=stats.linregress(ss.near,-ss.u)
    out["notfa_slope_short_u_on_near"]=f"slope {lr.slope:.4f} t {lr.slope/lr.stderr:.2f} n {len(ss)}"
    ss["nq"]=pd.qcut(ss.near,3,labels=False)
    out["notfa_by_near_tercile"]=ss.groupby("nq")["u"].apply(f).unstack()
    sd=s.dropna(subset=["depth"]); sd["dq"]=pd.qcut(sd.depth,3,labels=False)
    out["notfa_by_depth_tercile"]=sd.groupby("dq")["u"].apply(f).unstack()
    lr2=stats.linregress(sd.depth,-sd.u)
    out["notfa_slope_short_u_on_depth"]=f"slope {lr2.slope:.4f} t {lr2.slope/lr2.stderr:.2f}"
    # all-profile, nearness grade
    a=cases(d,5).dropna(subset=["near"])
    lr3=stats.linregress(a.near,-a.u)
    out["all_slope_short_u_on_near"]=f"slope {lr3.slope:.4f} t {lr3.slope/lr3.stderr:.2f} n {len(a)}"
    s10=cases(d[~d.fa],10)
    out["notfa10_by_window"]=s10.groupby("w")["u"].apply(f).unstack()
    return out
