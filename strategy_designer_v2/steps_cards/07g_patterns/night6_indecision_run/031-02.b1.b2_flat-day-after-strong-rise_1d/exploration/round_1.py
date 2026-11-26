def explore(data):
    import numpy as np, pandas as pd
    H=10
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            o,h,l,c=b.open,b.high,b.low,b.close
            rng=(h-l)
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b))})
            d["day"]=pd.to_datetime(b.timestamp).dt.floor("D")
            d["r5"]=c/c.shift(5)-1
            d["r20"]=c/c.shift(20)-1
            d["r1"]=c/c.shift(1)-1
            d["body"]=(c-o).abs()/rng.replace(0,np.nan)
            d["sbody"]=(c-o)/rng.replace(0,np.nan)
            d["rm"]=rng/rng.rolling(20).mean()
            d["clpos"]=(c-l)/rng.replace(0,np.nan)
            d["vol20"]=c.pct_change().rolling(20).std()
            d["fwd"]=c.shift(-H)/c-1
            d["wd"]=d.day.dt.weekday
            d["year"]=d.day.dt.year
            d["fc"]=b.forecast.values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    # coin drift & usual move on grid
    G=D[(D.pos%H==0)&D.fwd.notna()]
    drift=G.groupby("coin").fwd.mean(); usual=G.groupby("coin").fwd.std()
    D["un"]=D.fwd-D.coin.map(drift)
    D["str"]=D.un/D.coin.map(usual)
    D["cell"]=D.pos//H
    def cases(mask,sign=1):
        x=D[mask & D.fwd.notna()]
        x=x.groupby(["coin","win","cell"]).head(1)
        if len(x)<5: return pd.Series({"n":len(x)})
        u=x.un*sign
        dev=(u-u.mean()).groupby(x.day).sum()
        nd=len(dev); se=np.sqrt((dev**2).sum()*nd/(nd-1))/len(u)
        return pd.Series({"n":len(x),"days":nd,"unusual":u.mean(),"t":u.mean()/se,"total":(x.fwd*sign).mean(),"strength":(x.str*sign).mean()})
    doji=D.body<=0.1; wide=D.rm>=1
    up=D.r5>0; dn=D.r5<0
    out={}
    out["situations_long"]=pd.DataFrame({
      "doji_wide_up5":cases(doji&wide&up),
      "doji_narrow_up5":cases(doji&~wide&up),
      "doji_wide_dn5":cases(doji&wide&dn),
      "doji_narrow_dn5":cases(doji&~wide&dn),
      "anybody_wide_up5":cases(wide&up),
      "notdoji_wide_up5":cases(~doji&wide&up),
      "all_up5":cases(up),"all_dn5":cases(dn),
      "doji_any":cases(doji),
      "wide_rm>1.5_up5":cases((D.rm>=1.5)&up),
      "rm<0.7_any":cases(D.rm<0.7),
      "rm>1.5_any":cases(D.rm>=1.5),
    }).T
    g=D[(D.pos%H==0)&D.un.notna()].copy()
    for col in ["r5","r20","rm","sbody","clpos","vol20","r1"]:
        g[col+"_q"]=g.groupby("coin")[col].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
        out["grid_by_"+col]=g.groupby(col+"_q").agg(n=("un","size"),unusual=("un","mean"),sd=("un","std")).assign(t=lambda z:z.unusual/(z.sd/np.sqrt(z.n)))
    out["grid_by_weekday"]=g.groupby("wd").un.agg(["size","mean","std"])
    out["grid_by_year"]=g.groupby("year").un.agg(["size","mean"])
    sig=D[doji&wide&up&D.fwd.notna()].groupby(["coin","win","cell"]).head(1)
    out["tested_by_coin"]=sig.groupby("coin").un.agg(["size","mean"])
    out["tested_by_year"]=sig.groupby("year").un.agg(["size","mean"])
    sig=sig.copy(); sig["r5q"]=pd.qcut(sig.r5.rank(method="first"),4,labels=False)
    out["tested_by_r5_quartile"]=sig.groupby("r5q").agg(n=("un","size"),un=("un","mean"),r5=("r5","mean"))
    sig["rmq"]=pd.qcut(sig.rm.rank(method="first"),3,labels=False)
    out["tested_by_rm_tercile"]=sig.groupby("rmq").agg(n=("un","size"),un=("un","mean"),rm=("rm","mean"))
    sig["r20up"]=sig.r20>0
    out["tested_by_r20sign"]=sig.groupby("r20up").un.agg(["size","mean"])
    return out
