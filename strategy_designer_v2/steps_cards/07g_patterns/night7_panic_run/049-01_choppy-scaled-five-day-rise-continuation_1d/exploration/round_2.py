def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); n=len(b)
            r1=c.pct_change(); sd30=r1.rolling(30).std()
            ret5=c/c.shift(5)-1; ret60=c/c.shift(60)-1
            sdlong=r1.rolling(180,min_periods=120).std()
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(n),
                "s5":ret5/sd30,"s10":(c/c.shift(10)-1)/sd30,"ret60":ret60,
                "agit":(sd30>sdlong).astype(float).where(sdlong.notna()),
                "choppy":(b["regime"]=="unknown").astype(int),
                "f3":c.shift(-3)/c-1,"f5":c.shift(-5)/c-1,
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in (3,5):
        m=D[D.pos%h==0].groupby("coin")["f%d"%h].mean()
        D["x%d"%h]=D["f%d"%h]-D.coin.map(m)
    D["s5q"]=D.groupby("coin")["s5"].transform(lambda v: pd.qcut(v,5,labels=False,duplicates="drop"))
    D["s5d"]=D.groupby("coin")["s5"].transform(lambda v: pd.qcut(v,10,labels=False,duplicates="drop"))
    D["s10q"]=D.groupby("coin")["s10"].transform(lambda v: pd.qcut(v,5,labels=False,duplicates="drop"))
    D["nonchop"]=1-D.choppy
    def tab(h,key,mask=None):
        sub=D[(D.pos%h==0)].dropna(subset=["x%d"%h])
        if mask is not None: sub=sub[mask(sub)]
        out=[]
        for k,s in sub.groupby(key):
            x=s["x%d"%h]
            dd=s.assign(dev=x-x.mean()).groupby("day")["dev"].sum()
            se=np.sqrt((dd**2).sum())/len(s)
            out.append(pd.Series({"n":len(s),"days":len(dd),"mean%":100*x.mean(),"t_day":x.mean()/se if se>0 else np.nan},name=k))
        return pd.DataFrame(out)
    def slope(h,mask):
        sub=D[(D.pos%h==0)].dropna(subset=["x%d"%h,"s5"]); sub=sub[mask(sub)]
        x=sub.s5.clip(-6,6); y=sub["x%d"%h]
        bta=np.cov(x,y)[0,1]/x.var(); e=y-y.mean()-bta*(x-x.mean())
        dd=(sub.assign(u=e*(x-x.mean())).groupby("day")["u"].sum())
        se=np.sqrt((dd**2).sum())/((x-x.mean())**2).sum()
        return pd.Series({"n":len(sub),"beta%":100*bta,"t_day":bta/se})
    res={}
    res["f3 by s5 decile, non-choppy"]=tab(3,"s5d",lambda s:s.nonchop==1)
    res["f5 by s5 quintile x choppy"]=tab(5,["choppy","s5q"])
    res["f3 top s5 quintile by year, non-choppy"]=tab(3,"yr",lambda s:(s.nonchop==1)&(s.s5q==4))
    res["f3 top s5 quintile by window, non-choppy"]=tab(3,"w",lambda s:(s.nonchop==1)&(s.s5q==4))
    res["f3 top s5 quintile by coin, non-choppy"]=tab(3,"coin",lambda s:(s.nonchop==1)&(s.s5q==4))
    res["f3 top s5 quintile by agitation, non-choppy"]=tab(3,"agit",lambda s:(s.nonchop==1)&(s.s5q==4))
    res["f3 by s10 quintile"]=tab(3,"s10q")
    res["slope f3 on s5, positive s5, non-choppy"]=slope(3,lambda s:(s.nonchop==1)&(s.s5>0)).to_frame().T
    res["slope f3 on s5, positive s5, all"]=slope(3,lambda s:(s.s5>0)).to_frame().T
    res["slope f3 on s5, negative s5, all"]=slope(3,lambda s:(s.s5<0)).to_frame().T
    res["slope f5 on s5, all"]=slope(5,lambda s:s.s5.notna()).to_frame().T
    return res
