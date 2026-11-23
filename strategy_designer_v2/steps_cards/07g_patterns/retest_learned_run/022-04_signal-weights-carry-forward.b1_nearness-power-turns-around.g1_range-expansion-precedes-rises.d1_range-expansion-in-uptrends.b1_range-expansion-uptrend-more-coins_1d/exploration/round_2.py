def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            if len(b)<40: continue
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            rng=(h-l)/c
            rr=rng/rng.rolling(30,min_periods=20).mean()
            ret20=c/c.shift(20)-1
            r1=c/c.shift(1)-1
            vol20=r1.rolling(20).std()
            f5=c.shift(-5)/c-1
            f2=c.shift(-2)/c-1
            f10=c.shift(-10)/c-1
            idx=np.arange(0,len(b),5)
            d=pd.DataFrame({"coin":coin,"win":w,"rr":rr,"ret20":ret20,"r1":r1,"vol20":vol20,"f5":f5,"f2":f2,"f10":f10,
                            "year":pd.to_datetime(b["timestamp"]).dt.year}).iloc[idx]
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["f5","rr","ret20","r1"])
    for k in ["f5","f2","f10"]:
        D["ex"+k]=D[k]-D.groupby("coin")[k].transform("mean")
    D["sgn"]=np.sign(D["r1"])
    D["srr"]=D["rr"]*D["sgn"]
    out={}
    def wt(a,b):
        a=a.dropna(); b=b.dropna()
        t=stats.ttest_ind(a,b,equal_var=False).statistic
        return pd.Series({"nA":len(a),"meanA":a.mean(),"nB":len(b),"meanB":b.mean(),"diff":a.mean()-b.mean(),"t":t})
    up=D[D.ret20>0]; dn=D[D.ret20<=0]
    res={}
    res["up: upday vs downday (rr>median)"]=wt(up[(up.r1>0)&(up.rr>up.rr.median())]["exf5"],up[(up.r1<=0)&(up.rr>up.rr.median())]["exf5"])
    res["dn: downday vs upday (rr>median)"]=wt(dn[(dn.r1<=0)&(dn.rr>dn.rr.median())]["exf5"],dn[(dn.r1>0)&(dn.rr>dn.rr.median())]["exf5"])
    res["all: upday vs downday (rr>median)"]=wt(D[(D.r1>0)&(D.rr>D.rr.median())]["exf5"],D[(D.r1<=0)&(D.rr>D.rr.median())]["exf5"])
    out["splits"]=pd.DataFrame(res).T
    # graded rr within up days, all regimes and uptrend
    def qtab(df,col,ex="exf5",q=5):
        x=df.dropna(subset=[col,ex]).copy()
        x["q"]=pd.qcut(x[col].rank(method="first"),q,labels=False)
        g=x.groupby("q")[ex]
        return pd.DataFrame({"n":g.count(),"mean_ex":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.count())),"rr_mean":x.groupby("q")[col].mean()})
    out["up_trend_upday_rr_q"]=qtab(up[up.r1>0],"rr")
    out["up_trend_downday_rr_q"]=qtab(up[up.r1<=0],"rr")
    out["dn_trend_downday_rr_q"]=qtab(dn[dn.r1<=0],"rr")
    out["dn_trend_upday_rr_q"]=qtab(dn[dn.r1>0],"rr")
    out["all_srr_q"]=qtab(D,"srr")
    out["up_trend_srr_q_f2"]=qtab(up,"srr","exf2")
    out["up_trend_srr_q_f10"]=qtab(up,"srr","exf10")
    # robustness by year and coin: corr of srr with ex in uptrend
    x=up.copy()
    out["up_srr_corr_by_year"]=x.groupby("year").apply(lambda g: pd.Series({"n":len(g),"spearman":stats.spearmanr(g.srr,g.exf5).correlation}))
    cc=x.groupby("coin").apply(lambda g: stats.spearmanr(g.srr,g.exf5).correlation)
    out["up_srr_coins_pos_share"]=float((cc>0).mean())
    out["up_srr_coins_n"]=int(cc.notna().sum())
    out["up_srr_spearman_all"]=float(stats.spearmanr(up.srr,up.exf5).correlation)
    out["up_rr_spearman_all"]=float(stats.spearmanr(up.rr,up.exf5).correlation)
    return out
