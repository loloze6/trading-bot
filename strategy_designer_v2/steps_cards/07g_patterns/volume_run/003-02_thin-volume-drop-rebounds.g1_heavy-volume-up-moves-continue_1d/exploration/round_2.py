def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r=c.pct_change()
            vol20=r.rolling(20).std()
            z=r/vol20.shift(1)
            vr=v/v.rolling(30).mean().shift(1)
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"vr":vr,
                "f1":c.shift(-1)/c-1,"f2_5":c.shift(-5)/c.shift(-1)-1,"f5":c.shift(-5)/c-1,
                "f10":c.shift(-10)/c-1,"f6_10":c.shift(-10)/c.shift(-5)-1,
                "f3":c.shift(-3)/c-1,
                "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],
                "wd":ts.dt.weekday,"yr":ts.dt.year})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for col in ["f1","f2_5","f5","f10","f6_10","f3"]:
        D["x"+col]=D[col]-D.groupby("coin")[col].transform("mean")
    D=D.dropna(subset=["z","vr"])
    D["vrt"]=D.groupby("coin").vr.transform(lambda s:pd.qcut(s,3,labels=["thin","mid","heavy"]))
    def tt(s):
        s=s.dropna(); return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    res={}
    # path after big up moves (all bars; each horizon h needs grid; use grid 10 for robustness)
    for nm,cond in [("up z>1.5",D.z>1.5),("down z<-1.5",D.z<-1.5)]:
        sub=D[cond]
        out={}
        for col in ["xf1","xf2_5","xf5","xf6_10","xf10"]:
            for vt in ["thin","mid","heavy"]:
                out[(col,vt)]=tt(sub[sub.vrt==vt][col])
        res["path "+nm+" (all event bars)"]=pd.DataFrame(out).T
    # down-move 1-day rebound graded by z and volume
    dn=D[D.z<-1].copy()
    res["down z<-1 xf1 by vrt"]=dn.groupby("vrt",observed=True).xf1.apply(tt).unstack()
    res["corr down z vs xf1 (spearman)"]=float(stats.spearmanr(dn.z,dn.xf1,nan_policy="omit")[0])
    res["n down"]=len(dn)
    # 3-day after down moves, grid 3
    g3=D[D.pos%3==0]
    dn3=g3[g3.z<-1]
    res["down z<-1 xf3 grid3 by vrt"]=dn3.groupby("vrt",observed=True).xf3.apply(tt).unstack()
    # weekday stability
    wk=D.copy()
    wk["half"]=np.where(wk.yr<=2021,"2018-21","2022-25")
    res["xf1 weekday by half"]=wk.groupby(["wd","half"]).xf1.mean().unstack()
    res["xf1 weekday by coin"]=wk.groupby(["wd","coin"]).xf1.mean().unstack()
    # forecast high: next day vs days 2-5
    D["fcb"]=pd.cut(D.fc,[-1,0,2,5,21])
    res["fc bucket path"]=D.groupby("fcb",observed=True)[["xf1","xf2_5","xf6_10"]].mean()
    res["fc bucket t xf2_5"]=D.groupby("fcb",observed=True).xf2_5.apply(tt).unstack()
    # book around largest gains/losses
    bk=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            dd=dd.reset_index(drop=True).copy()
            dd["nxt_coin"]=dd.coin_return.shift(-1); dd["nxt_book"]=dd.book_return.shift(-1)
            dd["prv_coin"]=dd.coin_return.shift(1)
            bk.append(dd.assign(cn=coin,w=w))
    B=pd.concat(bk).dropna(subset=["book_return"])
    B=B[B.book_return!=0]
    q=B.book_return.quantile([0.02,0.98])
    res["book extremes"]=pd.DataFrame({
        "worst2%":B[B.book_return<=q.iloc[0]][["book_return","coin_return","prv_coin","nxt_coin","nxt_book"]].mean(),
        "best2%":B[B.book_return>=q.iloc[1]][["book_return","coin_return","prv_coin","nxt_coin","nxt_book"]].mean()})
    return res
