def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            o,h,l,c=b.open,b.high,b.low,b.close
            rng=(h-l)
            rr=rng/rng.rolling(20,min_periods=20).mean()
            loc=(c-l)/rng.replace(0,np.nan)
            r1=c.pct_change()
            vol=r1.rolling(20).std()
            vr=vol/vol.rolling(60,min_periods=30).mean()
            z=r1/vol.shift(1)
            n=len(b); pos=np.arange(n)
            d=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b.timestamp).dt.floor("D"),
                "rr":rr,"loc":loc,"r1":r1,"z":z,"vr":vr,"vol":vol,
                "f1":c.shift(-1)/c-1,"f3":c.shift(-3)/c-1,"g3":(pos%3==0),
                "ret20":c/c.shift(20)-1})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu1=D.groupby("coin").f1.mean(); mu3=D.groupby("coin").f3.mean()
    D["x1"]=D.f1-D.coin.map(mu1); D["x3"]=D.f3-D.coin.map(mu3)
    D["s1"]=D.x1/D.vol
    def st(g,col="x1"):
        g=g.dropna(subset=[col]); n=len(g)
        if n<5: return pd.Series({"n":n,"mean":np.nan,"t":np.nan})
        m=g[col].mean(); ds=(g[col]-m).groupby(g.day).sum()
        se=np.sqrt((ds**2).sum())/n
        return pd.Series({"n":n,"mean":m,"t":m/se if se>0 else np.nan})
    out={}
    D["zb"]=pd.cut(D.z,[-20,-3,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,3,20])
    out["all_by_z_x1"]=D.groupby("zb").apply(st)
    out["all_by_z_x1_volunits"]=D.groupby("zb").apply(lambda g:st(g,"s1"))
    out["all_by_z_x3_grid"]=D[D.g3].groupby("zb").apply(lambda g:st(g,"x3"))
    D["vrb"]=pd.qcut(D.vr,3,labels=["vr_lo","vr_mid","vr_hi"])
    dn=D[D.z<=-1.5]
    out["bigdown_by_vr"]=dn.groupby("vrb").apply(st)
    out["bigdown_by_vr_volunits"]=dn.groupby("vrb").apply(lambda g:st(g,"s1"))
    lc=D[(D["loc"]<=0.25)]
    out["lowclose_by_vr"]=lc.groupby("vrb").apply(st)
    lc2=lc.copy(); lc2["rrb"]=pd.cut(lc2.rr,[0,1,1.5,2.5,10])
    out["lowclose_rr_x_vr"]=lc2.groupby(["vrb","rrb"]).apply(st)
    out["all_by_vr"]=D.groupby("vrb").apply(st)
    D["t20"]=pd.qcut(D.ret20,3,labels=["down20","flat20","up20"])
    out["bigdown_by_trend20"]=dn.assign(t20=D.loc[dn.index,"t20"]).groupby("t20").apply(st)
    # book
    bk=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            bk.append(dd.assign(coin=coin,w=w))
    B=pd.concat(bk)
    Bd=B.groupby(["w","day"]).agg(br=("book_return","mean")).dropna()
    q=Bd.br.quantile([0.01,0.99])
    out["book_tails"]=pd.Series({"q01":q.iloc[0],"q99":q.iloc[1],"top10_sum":Bd.br.nlargest(10).sum(),"bot10_sum":Bd.br.nsmallest(10).sum(),"total_sum":Bd.br.sum()})
    return out
