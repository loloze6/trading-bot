def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            r20=c/c.shift(20)-1
            hi20=c.rolling(20,min_periods=20).max()
            sd20=r1.rolling(20,min_periods=20).std()
            depth=(hi20-c)/c/sd20
            lo20=c.rolling(20,min_periods=20).min()
            hgt=(c-lo20)/c/sd20
            f10=c.shift(-10)/c-1
            f1=c.shift(-1)/c-1
            f3=c.shift(-3)/c-1
            choppy=(b["regime"]!="chop")
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"r1":r1,"r20":r20,"depth":depth,"hgt":hgt,
                             "f10":f10,"f1":f1,"f3":f3,"choppy":choppy,"wd":ts.dt.weekday,"yr":ts.dt.year,
                             "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],"sd20":sd20,
                             "day":ts.dt.floor("D")})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    out={}
    # drift
    g10=d[d.pos%10==0]
    drift10=g10.groupby("coin")["f10"].mean()
    g1=d
    drift1=d.groupby("coin")["f1"].mean()
    g3=d[d.pos%3==0]; drift3=g3.groupby("coin")["f3"].mean()
    d["u10"]=d["f10"]-d.coin.map(drift10)
    d["u1"]=d["f1"]-d.coin.map(drift1)
    d["u3"]=d["f3"]-d.coin.map(drift3)
    def tclust(s,days):
        x=pd.DataFrame({"v":s,"d":days}).dropna()
        if len(x)<5: return np.nan,len(x),0
        dd=x.groupby("d")["v"].sum()
        n=len(x); m=x.v.mean()
        se=np.sqrt(((dd - dd.index.map(x.groupby("d").size())*m)**2).sum())/n
        return m/se if se>0 else np.nan, n, x.d.nunique()
    def tab(sub,col,ucol,q=5):
        sub=sub.dropna(subset=[col,ucol]).copy()
        sub["b"]=pd.qcut(sub[col],q,labels=False,duplicates="drop")
        res=[]
        for k,gg in sub.groupby("b"):
            t,n,nd=tclust(gg[ucol],gg["day"])
            res.append({"bin":k,"lo":gg[col].min(),"hi":gg[col].max(),"mean_u":gg[ucol].mean(),"t":t,"n":n,"days":nd})
        return pd.DataFrame(res)
    G=d[d.pos%10==0]
    ch=G[G.choppy]
    out["10d choppy by depth"]=tab(ch,"depth","u10")
    out["10d choppy up-day r20<0 by depth"]=tab(ch[(ch.r1>0)&(ch.r20<0)],"depth","u10",3)
    out["10d choppy down-day by depth"]=tab(ch[ch.r1<0],"depth","u10")
    out["10d trend(nonchoppy) by depth"]=tab(G[~G.choppy],"depth","u10")
    out["10d choppy by r20"]=tab(ch,"r20","u10")
    out["10d nonchoppy by r20"]=tab(G[~G.choppy],"r20","u10")
    G3=d[d.pos%3==0]
    out["3d choppy by depth"]=tab(G3[G3.choppy],"depth","u3")
    out["1d choppy by r1/sd"]=tab(d[d.choppy].assign(z=d.r1/d.sd20),"z","u1")
    out["1d all by weekday"]=d.groupby("wd")["u1"].agg(["mean","count"]).assign(t=lambda x: x["mean"]/(d.groupby("wd")["u1"].std()/np.sqrt(x["count"])))
    # book
    days=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            days.append(x.assign(coin=coin,w=w))
    D=pd.concat(days)
    bd=D.groupby(["w","day"])["book_return"].mean()
    out["book mean by window"]=D.groupby("w")["book_return"].agg(["mean","std","count"])
    pos=d[d.alloc.abs()>1e-9]
    out["held share by choppy"]=pd.Series({"held_bars":len(pos),"mean_u1_held":pos.u1.mean(),"gain_held":(-pos.f1).mean()})
    return out
