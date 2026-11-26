def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; daily=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            f5=c.shift(-5)/c-1
            r20=c/c.shift(20)-1
            sd20=r1.rolling(20).std()
            sc=r20/sd20
            r60=c/c.shift(60)-1
            sd30=r1.rolling(30).std()
            r1z=r1/sd20.shift(1)
            r5p=c/c.shift(5)-1
            d=pd.DataFrame({"coin":coin,"w":w,"fc":b["forecast"].astype(float),"f5":f5,"r20":r20,"sc":sc,"r60":r60,
                            "sd30":sd30,"r1z":r1z,"r5p":r5p,"r1":r1,"nx1":r1.shift(-1),
                            "wd":pd.to_datetime(b["timestamp"]).dt.dayofweek,"yr":pd.to_datetime(b["timestamp"]).dt.year,
                            "pos":np.arange(len(b))})
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    # drift per coin over all grid
    G=A[(A.pos%5==0)&A.f5.notna()].copy()
    G["drift"]=G.groupby("coin").f5.transform("mean")
    G["ex"]=G.f5-G.drift
    G["volr"]=G.sd30/G.groupby("coin").sd30.transform("median")
    out={}
    def summ(g):
        g=g.dropna(subset=["ex"])
        n=len(g); m=g.ex.mean(); s=g.ex.std()
        return pd.Series({"n":n,"mean_ex%":100*m,"t":m/(s/np.sqrt(n)) if n>2 else np.nan})
    def slope(g,x="fc"):
        g=g.dropna(subset=[x,"ex"])
        if len(g)<30: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        r=stats.linregress(g[x],g.ex)
        return pd.Series({"n":len(g),"slope":r.slope,"t":r.slope/r.stderr})
    G["fq"]=pd.qcut(G.fc.rank(method="first"),5,labels=False)
    out["fc quintile -> ex5"]=G.groupby("fq").apply(summ)
    G["side"]=np.sign(G.fc)
    out["slope by fc sign"]=G.groupby("side").apply(slope)
    G["trend"]=pd.cut(G.r60,[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    G["agit"]=np.where(G.volr>1,"agit","calm")
    G.loc[G.volr.isna(),"agit"]=np.nan
    out["slope by trend x agit"]=G.groupby(["trend","agit"]).apply(slope)
    out["slope by coin"]=G.groupby("coin").apply(slope)
    out["slope by year"]=G.groupby("yr").apply(slope)
    G["vq"]=G.groupby("coin").sd30.transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["slope by vol tercile"]=G.groupby("vq").apply(slope)
    G["rawq"]=pd.qcut(G.r20.rank(method="first"),5,labels=False)
    out["raw r20 quintile -> ex5"]=G.groupby("rawq").apply(summ)
    G["zq"]=pd.qcut(G.r1z.rank(method="first"),5,labels=False)
    out["1d move z quintile -> ex5"]=G.groupby("zq").apply(summ)
    G["r5q"]=pd.qcut(G.r5p.rank(method="first"),5,labels=False)
    out["past5d quintile -> ex5"]=G.groupby("r5q").apply(summ)
    # weekday next-day return all bars
    A2=A.dropna(subset=["nx1"])
    out["weekday next1d"]=A2.groupby("wd").nx1.agg(lambda s: pd.Series([100*s.mean()])[0]).to_frame("mean%").join(
        A2.groupby("wd").nx1.agg(lambda s: s.mean()/(s.std()/np.sqrt(len(s)))).to_frame("t"))
    # book daily
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; D.append(d)
    D=pd.concat(D); D["day"]=pd.to_datetime(D["day"])
    bk=D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    bk["yr"]=bk.index.get_level_values("day").year
    out["book by year"]=bk.groupby("yr").agg(n=("book_return","size"),book_mean_pct=("book_return",lambda s:100*s.mean()),
        hold_mean_pct=("coin_return",lambda s:100*s.mean()),book_sh=("book_return",lambda s:s.mean()/s.std()*np.sqrt(365)),
        hold_sh=("coin_return",lambda s:s.mean()/s.std()*np.sqrt(365)))
    br=bk.book_return.sort_values()
    k=int(len(br)*0.05)
    out["book tails"]=pd.Series({"total_sum%":100*br.sum(),"top5%_sum":100*br.iloc[-k:].sum(),"bot5%_sum":100*br.iloc[:k].sum(),
        "corr_book_hold":bk.book_return.corr(bk.coin_return)})
    return out
