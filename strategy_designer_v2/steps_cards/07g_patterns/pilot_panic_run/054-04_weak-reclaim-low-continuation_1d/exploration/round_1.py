import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H=5
    rows=[]; allret=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; lo=b["low"].values; hi=b["high"].values; op=b["open"].values
            n=len(b)
            low30=pd.Series(lo).shift(1).rolling(30).min().values
            ret60=pd.Series(c).pct_change(60).values
            r1=pd.Series(c).pct_change().values
            vol30=pd.Series(r1).rolling(30).std().values
            vol120=pd.Series(r1).rolling(120,min_periods=60).median().values if False else pd.Series(pd.Series(r1).rolling(30).std()).rolling(90,min_periods=30).median().values
            fa=(b["regime"].values!="chop")
            ts=pd.to_datetime(b["timestamp"])
            for g in range(0,n-H,H):
                for t in range(g,min(g+H,n-H)):
                    pass
            # per bar features
            fwd={h:np.full(n,np.nan) for h in (1,3,5,10)}
            for h in fwd:
                fwd[h][:n-h]=c[h:]/c[:n-h]-1
            rng=hi-lo
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(n),"pierce":(lo<low30)&(c>low30),
                "breakdown":(c<low30),"near":np.where(rng>0,1-(c-low30)/rng,np.nan),
                "clv":np.where(rng>0,(c-lo)/rng,np.nan),"r1":r1,"ret60":ret60,"volr":vol30/vol120,
                "fa":fa,"wd":ts.dt.weekday.values,"year":ts.dt.year.values,
                "f1":fwd[1],"f3":fwd[3],"f5":fwd[5],"f10":fwd[10],
                "alloc":b["postRebalance_current_allocation"].values})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    out={}
    # normal drift per coin over grid
    def grid(sub,h,col):
        # first event per grid cell per coin-window
        s=sub[sub[col]] if col else sub
        s=s.assign(cell=s.pos//h)
        return s.groupby(["coin","w","cell"]).head(1)
    drift={}
    for h in (1,3,5,10):
        g=d[d.pos%h==0]
        drift[h]=g.groupby("coin")["f%d"%h].mean()
    def summ(s,h):
        x=s["f%d"%h]-s.coin.map(drift[h]); x=x.dropna()
        if len(x)<3: return [len(x),np.nan,np.nan]
        return [len(x),x.mean(),x.mean()/x.std()*np.sqrt(len(x))]
    res=[]
    for ev in ["pierce","breakdown"]:
        for prof in ["all","fa","notfa"]:
            sub=d if prof=="all" else d[d.fa] if prof=="fa" else d[~d.fa]
            for h in (1,3,5,10):
                s=grid(sub,h,ev)
                res.append([ev,prof,h]+summ(s,h))
    out["events"]=pd.DataFrame(res,columns=["ev","prof","h","n","unusual","t"])
    # pierce, by nearness tercile (all profiles), h=5
    s=grid(d,5,"pierce").copy(); s["u"]=s.f5-s.coin.map(drift[5])
    s["nq"]=pd.qcut(s.near,3,labels=False,duplicates="drop")
    out["pierce_near_h5"]=s.groupby("nq")["u"].agg(["count","mean",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["pierce_ret60_h5"]=s.groupby(pd.cut(s.ret60,[-9,-0.3,-0.1,0.1,9]))["u"].agg(["count","mean",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    # all grid bars: next 1d by prior 1d return quintile and by clv
    g=d[d.pos%1==0].copy(); g["u"]=g.f1-g.coin.map(drift[1])
    g["q"]=g.groupby("coin")["r1"].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
    out["next1_by_r1q"]=g.groupby("q")["u"].agg(["count","mean",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    g5=d[d.pos%5==0].copy(); g5["u"]=g5.f5-g5.coin.map(drift[5])
    g5["q"]=g5.groupby("coin")["r1"].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
    out["next5_by_r1q"]=g5.groupby("q")["u"].agg(["count","mean",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    g5["vq"]=g5.groupby("coin")["volr"].transform(lambda x: pd.qcut(x,3,labels=False,duplicates="drop"))
    out["next5_by_volratio"]=g5.groupby("vq")["u"].agg(["count","mean",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    g5["tq"]=pd.cut(g5.ret60,[-9,-0.3,-0.1,0.1,0.3,9])
    out["next5_by_ret60"]=g5.groupby("tq")["u"].agg(["count","mean",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["next1_by_weekday"]=g.groupby("wd")["u"].agg(["count","mean",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["fa_share"]=d.fa.mean()
    return out
