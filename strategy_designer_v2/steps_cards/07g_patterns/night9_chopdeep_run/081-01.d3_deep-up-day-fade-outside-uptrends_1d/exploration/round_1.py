def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            allr.append(r.dropna())
        drift=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            d=pd.DataFrame({"ts":b["timestamp"]})
            d["coin"]=coin; d["w"]=w
            d["r1"]=r
            sd=r.rolling(20,min_periods=15).std()
            d["sd"]=sd
            d["depth"]=(c.rolling(20,min_periods=15).max()/c-1)/sd
            d["tr60"]=c/c.shift(60)-1
            d["r3"]=c/c.shift(3)-1
            d["fwd"]=c.shift(-1)/c-1
            d["fwd2"]=c.shift(-2)/c-1
            d["un"]=d["fwd"]-drift
            d["rz"]=r/sd
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            d["clv"]=(c-b["low"])/rng
            d["volz"]=b["volume"]/b["volume"].rolling(20,min_periods=15).mean()
            d["vrank"]=sd.rolling(60,min_periods=30).rank(pct=True)
            d["pos"]=b["postRebalance_current_allocation"]
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.dayofweek
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["un","depth","r1"])
    D["day"]=pd.to_datetime(D["ts"]).dt.floor("D")
    D["trend"]=np.where(D["tr60"]>0.1,"rising",np.where(D["tr60"]<-0.1,"falling",np.where(D["tr60"].isna(),"na","choppy")))
    def summ(g):
        x=g["un"]; s=g.groupby("day")["un"].sum()
        se=np.sqrt(len(s)/(len(s)-1)*(((s-x.mean()*g.groupby("day").size())**2).sum()))/len(x) if len(s)>2 else np.nan
        return pd.Series({"n":len(x),"days":len(s),"mean_un_%":100*x.mean(),"t_dayp":x.mean()/se if se else np.nan})
    out={}
    D["dq"]=D.groupby(D["r1"]>0)["depth"].transform(lambda v:pd.qcut(v.rank(method="first"),5,labels=False))
    D["up"]=np.where(D["r1"]>0,"up","down")
    out["by_up_depthq"]=D.groupby(["up","dq"]).apply(summ)
    U=D[(D.r1>0)&(D.trend!="na")]
    U["dq3"]=U.groupby("trend")["depth"].transform(lambda v:pd.qcut(v.rank(method="first"),3,labels=False))
    out["up_trend_depth3"]=U.groupby(["trend","dq3"]).apply(summ)
    Dn=D[(D.r1<=0)&(D.trend!="na")]
    Dn["dq3"]=Dn.groupby("trend")["depth"].transform(lambda v:pd.qcut(v.rank(method="first"),3,labels=False))
    out["down_trend_depth3"]=Dn.groupby(["trend","dq3"]).apply(summ)
    D["rzq"]=pd.qcut(D["rz"].rank(method="first"),10,labels=False)
    out["all_by_dayreturn_z_decile"]=D.groupby("rzq").apply(summ)
    deepup=D[(D.r1>0)&(D.dq>=3)]
    deepup["clq"]=pd.qcut(deepup["clv"].rank(method="first"),3,labels=False)
    out["deepup_by_closeloc3"]=deepup.groupby("clq").apply(summ)
    deepup["vq"]=pd.qcut(deepup["volz"].rank(method="first"),3,labels=False)
    out["deepup_by_volume3"]=deepup.groupby("vq").apply(summ)
    out["all_by_weekday"]=D.groupby("wd").apply(summ)
    out["all_by_vrank3"]=D.dropna(subset=["vrank"]).assign(q=lambda x:pd.qcut(x.vrank.rank(method="first"),3,labels=False)).groupby("q").apply(summ)
    # book
    bd=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            x=dd[["day","book_return","coin_return"]].copy(); x["w"]=w; bd.append(x)
    B=pd.concat(bd).dropna()
    bk=B.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    bk["wd"]=pd.to_datetime(bk["day"]).dt.dayofweek
    out["book_by_weekday"]=bk.groupby("wd").agg(n=("book_return","size"),book_mean_bp=("book_return",lambda v:1e4*v.mean()),t=("book_return",lambda v:v.mean()/v.std()*np.sqrt(len(v))))
    out["book_by_window"]=bk.groupby("w").agg(n=("book_return","size"),book_bp=("book_return",lambda v:1e4*v.mean()),coin_bp=("coin_return",lambda v:1e4*v.mean()),corr=("book_return",lambda v:np.corrcoef(v,bk.loc[v.index,"coin_return"])[0,1]))
    q=bk["book_return"]
    out["book_tails"]=pd.Series({"top5pct_sum_share":q[q>=q.quantile(.95)].sum()/q.sum(),"bot5pct_sum_share":q[q<=q.quantile(.05)].sum()/q.sum(),"coin_ret_on_top5_bp":1e4*bk.coin_return[q>=q.quantile(.95)].mean(),"coin_ret_on_bot5_bp":1e4*bk.coin_return[q<=q.quantile(.05)].mean()})
    return out
