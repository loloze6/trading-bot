def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=72
    rows=[]; hrs=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r=c.pct_change()
            sc=(c/c.shift(240)-1)/(r.rolling(480).std()*np.sqrt(240))
            vs=r.rolling(24).std()/r.rolling(480).std()
            rng=(b["high"].rolling(120).max()/b["low"].rolling(120).min()-1)/(r.rolling(480).std()*np.sqrt(120))
            vr=v.rolling(24).mean()/v.rolling(480).mean()
            r24=c/c.shift(24)-1; z24=r24/(r.rolling(480).std()*np.sqrt(24))
            fwd=c.shift(-H)/c-1
            idx=np.arange(0,len(b)-H,H)
            d=pd.DataFrame({"coin":coin,"w":w,"sc":sc.values[idx],"vs":vs.values[idx],"rng":rng.values[idx],
                            "vr":vr.values[idx],"z24":z24.values[idx],"fwd":fwd.values[idx],
                            "fc":b["forecast"].values[idx]})
            rows.append(d)
            ts=pd.to_datetime(b["timestamp"])
            hrs.append(pd.DataFrame({"coin":coin,"h":ts.dt.hour,"wd":ts.dt.weekday,"r":r}))
    g=pd.concat(rows); g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    g["absfwd"]=g["fwd"].abs()
    out={}
    def tab(col,q=5):
        x=g.dropna(subset=[col,"ex"]).copy()
        x["q"]=x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),q,labels=False))
        t=x.groupby("q").agg(n=("ex","size"),mean_ex=("ex","mean"),sd=("ex","std"),absfwd=("absfwd","mean"),mid=(col,"median"))
        t["t"]=t.mean_ex/(t.sd/np.sqrt(t.n)); return t.drop(columns="sd")
    for col in ["sc","vs","rng","vr","z24"]: out["q_"+col]=tab(col)
    # sc by coin: top quintile minus bottom
    x=g.dropna(subset=["sc","ex"]).copy()
    x["q"]=x.groupby("coin")["sc"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    pc=[]
    for coin,xx in x.groupby("coin"):
        a=xx[xx.q==4].ex;bb=xx[xx.q==0].ex;m=xx[(xx.q>0)&(xx.q<4)].ex
        pc.append([coin,a.mean(),bb.mean(),m.mean(),stats.ttest_ind(a,bb,equal_var=False).statistic])
    out["sc_by_coin_top_bot_mid"]=pd.DataFrame(pc,columns=["coin","top","bot","mid","t_top_bot"])
    # compression x direction: sc sign in low-range quintile
    hh=pd.concat(hrs).dropna()
    ht=hh.groupby("h").r.agg(["mean","std","size"]); ht["t"]=ht["mean"]/(ht["std"]/np.sqrt(ht["size"]))
    out["hour"]=ht[["mean","t"]]
    wt=hh.groupby("wd").r.agg(["mean","std","size"]); wt["t"]=wt["mean"]/(wt["std"]/np.sqrt(wt["size"]))
    out["weekday"]=wt[["mean","t"]]
    # book
    ds=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            bb=data["bars"][coin][w]
            ts=pd.to_datetime(bb["timestamp"]); al=bb.groupby(ts.dt.floor("D"))["postRebalance_current_allocation"].mean()
            dd=d.copy(); dd["coin"]=coin; dd["w"]=w; dd["al"]=al.reindex(pd.to_datetime(dd["day"])).values
            ds.append(dd)
    D=pd.concat(ds)
    book=D.groupby(["w","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna()
    out["book_by_window_sharpe"]=book.groupby("w").apply(lambda z: pd.Series({"book":z.br.mean()/z.br.std()*np.sqrt(365),"hold":z.cr.mean()/z.cr.std()*np.sqrt(365)})).T
    D["mkt"]=D["al"]*D.groupby("coin")["coin_return"].transform("mean")
    out["book_mean_vs_market_part"]=pd.Series({"book_mean":book.br.mean(),"market_part":D.groupby(["w","day"]).mkt.mean().mean(),"mean_alloc":D.al.mean()})
    return out
