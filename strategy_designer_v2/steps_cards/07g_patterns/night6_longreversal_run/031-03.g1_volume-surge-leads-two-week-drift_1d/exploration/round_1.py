def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=14
    rows=[]; daily=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            fwd=c.shift(-H)/c-1
            f1=c.shift(-1)/c-1
            past30=c/c.shift(30)-1
            past60=c/c.shift(60)-1
            vol20=r1.rolling(20).std()
            vr=np.log(v.rolling(14).mean()/v.rolling(30).mean())
            vr1=np.log(v/v.rolling(30).mean())
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"fwd":fwd,"f1":f1,"r1":r1,
                "p30":past30,"p60":past60,"vol20":vol20,"vr":vr,"vr1":vr1,"fc":b["forecast"],
                "alloc":b["postRebalance_current_allocation"],"day":ts.dt.floor("D"),"wd":ts.dt.dayofweek,"yr":ts.dt.year})
            rows.append(df)
    A=pd.concat(rows)
    # coin drift and usual move over H on grid
    G=A[(A.pos%H==0)&A.fwd.notna()].copy()
    drift=G.groupby("coin").fwd.mean(); usual=G.groupby("coin").fwd.std()
    G["ex"]=(G.fwd-G.coin.map(drift))/G.coin.map(usual)
    def clus_t(sub,x):
        s=sub.dropna(subset=[x,"ex"]).copy()
        s["xz"]=s.groupby("coin")[x].transform(lambda z:(z-z.mean())/z.std())
        s["p"]=s.xz*s.ex
        d=s.groupby("day").p.sum()
        return pd.Series({"n":len(s),"days":len(d),"corr_like":s.p.mean(),"t_dayclust":d.mean()/d.std()*np.sqrt(len(d))})
    out={}
    out["slope_tests_14d"]=pd.DataFrame({x:clus_t(G,x) for x in ["p30","p60","vol20","vr","vr1","r1"]}).T
    # quintiles of past30 standardized by usual
    G["p30z"]=G.p30/G.coin.map(usual)
    s=G.dropna(subset=["p30z"]).copy(); s["q"]=pd.qcut(s.p30z,5,labels=False)
    out["p30_quintile_ex"]=s.groupby("q").ex.agg(["mean","count",lambda z:z.mean()/z.std()*np.sqrt(len(z))])
    s=G.dropna(subset=["vol20"]).copy(); s["q"]=s.groupby("coin").vol20.transform(lambda z:pd.qcut(z,5,labels=False))
    out["vol20_quintile_ex"]=s.groupby("q").ex.agg(["mean","count",lambda z:z.mean()/z.std()*np.sqrt(len(z))])
    s=G.dropna(subset=["vr"]).copy(); s["q"]=s.groupby("coin").vr.transform(lambda z:pd.qcut(z,5,labels=False))
    out["vr_quintile_ex"]=s.groupby("q").ex.agg(["mean","count",lambda z:z.mean()/z.std()*np.sqrt(len(z))])
    # 1-day: after large moves, non-overlapping by nature (h=1)
    D=A.dropna(subset=["r1","f1"]).copy()
    D["z"]=D.r1/D.groupby("coin").r1.transform("std")
    D["f1x"]=(D.f1-D.groupby("coin").f1.transform("mean"))/D.groupby("coin").f1.transform("std")
    D["zb"]=pd.cut(D.z,[-99,-2.5,-1.5,-0.5,0.5,1.5,2.5,99])
    out["next_day_after_move"]=D.groupby("zb").f1x.agg(["mean","count",lambda z:z.mean()/z.std()*np.sqrt(len(z))])
    out["weekday_next_ret"]=D.groupby((D.wd+1)%7).f1x.agg(["mean","count",lambda z:z.mean()/z.std()*np.sqrt(len(z))])
    # year breakdown of book gain
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; t["w"]=w; dd.append(t)
    DD=pd.concat(dd)
    bk=DD.groupby("day").agg(b=("book_return","mean"),c=("coin_return","mean")).dropna()
    bk["yr"]=pd.to_datetime(bk.index).year
    out["book_by_year"]=bk.groupby("yr").agg(book=("b","mean"),hold=("c","mean"),n=("b","size"))
    # book extreme days: coin return that day
    q=bk.b.quantile([0.02,0.98])
    out["book_extremes"]=pd.DataFrame({"low":[bk[bk.b<=q.iloc[0]].b.mean(),bk[bk.b<=q.iloc[0]].c.mean()],
        "high":[bk[bk.b>=q.iloc[1]].b.mean(),bk[bk.b>=q.iloc[1]].c.mean()]},index=["book","coins"])
    out["corr_book_coins"]=float(bk.b.corr(bk.c))
    out["share_long"]=float((A.alloc>0).mean())
    return out
