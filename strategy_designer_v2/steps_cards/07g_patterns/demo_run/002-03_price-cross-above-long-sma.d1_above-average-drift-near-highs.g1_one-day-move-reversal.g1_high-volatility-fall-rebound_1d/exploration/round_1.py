import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"].astype(float)
            r=cl.pct_change()
            sd=r.rolling(20,min_periods=20).std()
            z=r/sd
            vp=sd.rolling(100,min_periods=20).apply(lambda x:(x<=x[-1]).mean(),raw=True).rolling(5).mean()
            nxt=cl.shift(-1)/cl-1
            r5=cl/cl.shift(5)-1
            r20=cl/cl.shift(20)-1
            f5=cl.shift(-5)/cl-1
            pos=np.arange(len(b))
            d=pd.DataFrame({"coin":c,"win":w,"r":r,"z":z,"vp":vp,"nxt":nxt,"r5":r5,"r20":r20,"f5":f5,
                "grid5":pos%5==0,"wd":pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],"reg":b["regime"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    cm=D.groupby("coin")["nxt"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(cm)
    out={}
    D["vlev"]=pd.cut(D["vp"],[-0.01,0.3,0.6,0.8,1.01],labels=["lo","mid","mhi","hi"])
    D["zb"]=pd.cut(D["z"],[-99,-2,-1,-0.3,0.3,1,2,99])
    g=D.dropna(subset=["ex","z","vp"]).groupby(["vlev","zb"])["ex"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["next-day excess by vol level and z"]=g
    # slope by vol level
    res={}
    for lv,s in D.dropna(subset=["ex","z","vp"]).groupby("vlev"):
        sl=stats.linregress(s["z"],s["ex"]); res[str(lv)]=(sl.slope,sl.slope/sl.stderr,len(s))
    out["slope ex on z by vol"]=pd.DataFrame(res,index=["slope","t","n"]).T
    # momentum 20d -> next 5d, grid
    G=D[D["grid5"]].dropna(subset=["r20","f5"]).copy()
    G["f5ex"]=G["f5"]-G["coin"].map(G.groupby("coin")["f5"].mean())
    G["q"]=G.groupby("coin")["r20"].transform(lambda x:pd.qcut(x,5,labels=False))
    out["next5 excess by r20 quintile"]=G.groupby("q")["f5ex"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    G["q5"]=G.groupby("coin")["r5"].transform(lambda x:pd.qcut(x,5,labels=False))
    out["next5 excess by r5 quintile"]=G.groupby("q5")["f5ex"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["next-day excess by weekday"]=D.dropna(subset=["ex"]).groupby("wd")["ex"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    # per coin slope in hi vol
    pc={}
    for c,s in D[D["vp"]>=0.8].dropna(subset=["ex","z"]).groupby("coin"):
        sl=stats.linregress(s["z"],s["ex"]); pc[c]=(sl.slope,sl.slope/sl.stderr,len(s))
    out["hi vol slope per coin"]=pd.DataFrame(pc,index=["slope","t","n"]).T
    # book
    br=[]
    for c,ws in data["days"].items():
        for w,d in ws.items():
            br.append(d.assign(coin=c,win=w))
    B=pd.concat(br)
    bk=B.groupby(["win","day"])["book_return"].mean().dropna()
    out["book daily mean,std,n"]=pd.Series({"mean":bk.mean(),"sd":bk.std(),"n":len(bk),"skew":stats.skew(bk)})
    out["book by year"]=bk.groupby(pd.to_datetime(bk.index.get_level_values("day")).year).agg(["mean","count"])
    return out
