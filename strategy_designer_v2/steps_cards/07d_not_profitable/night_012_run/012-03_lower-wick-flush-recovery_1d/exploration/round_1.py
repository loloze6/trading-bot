def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c in data["bars"]:
        allr=[]
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values
            n=len(b)
            for h in (1,3,5,10):
                pass
            r1=b["close"].pct_change()
            sd=r1.rolling(20).std()
            z=r1/sd
            vr=b["volume"]/b["volume"].shift(1).rolling(20).mean()
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            clr=(b["close"]-b["low"])/rng
            r20=b["close"]/b["close"].shift(20)-1
            for i in range(n):
                if b["regime"].iloc[i]!="mean_reversion": continue
                d={"coin":c,"win":w,"z":z.iloc[i],"vr":vr.iloc[i],"clr":clr.iloc[i],"r20":r20.iloc[i],
                   "alloc":b["postRebalance_current_allocation"].iloc[i],"fc":b["forecast"].iloc[i],
                   "ret1d":r1.iloc[i]}
                for h in (1,3,5,10):
                    d[f"f{h}"]=cl[i+h]/cl[i]-1 if i+h<n else np.nan
                d["held_next"]=b["postRebalance_current_allocation"].iloc[i+1] if i+1<n else np.nan
                rows.append(d)
    f=pd.DataFrame(rows)
    out={}
    out["n_flush"]=len(f)
    out["mean_fwd"]=f[["f1","f3","f5","f10"]].agg(["mean","count"]).T
    f["t1"]=[stats.ttest_1samp(f["f1"].dropna(),0).statistic]*len(f)
    out["t_fwd"]=pd.Series({h:stats.ttest_1samp(f[h].dropna(),0).statistic for h in ["f1","f3","f5","f10"]})
    f["clrq"]=pd.qcut(f["clr"],4,labels=False)
    out["by_clr"]=f.groupby("clrq")[["clr","f1","f3","f5","f10","alloc"]].mean().assign(n=f.groupby("clrq").size())
    f["zq"]=pd.qcut(f["z"],3,labels=False)
    out["by_z"]=f.groupby("zq")[["z","f1","f3","f10"]].mean().assign(n=f.groupby("zq").size())
    f["vq"]=pd.qcut(f["vr"],3,labels=False)
    out["by_vr"]=f.groupby("vq")[["vr","f1","f3","f10"]].mean()
    f["tr"]=pd.qcut(f["r20"],3,labels=False)
    out["by_r20"]=f.groupby("tr")[["r20","f1","f3","f10"]].mean().assign(n=f.groupby("tr").size())
    out["alloc_stats"]=f[["alloc","held_next","fc"]].describe()
    out["by_coin"]=f.groupby("coin")[["f1","f3","f10"]].mean().assign(n=f.groupby("coin").size())
    # trades
    t=pd.concat([d for c in data["trades"] for d in data["trades"][c].values()])
    out["trades"]=pd.Series({"n":len(t),"mean_pl":t["profit_loss_percent"].mean(),"mean_net":t["net_profit_loss_percent"].mean(),
        "dur_days_mean":t["duration_minutes"].mean()/1440,"win":(t["net_profit_loss_percent"]>0).mean()})
    # book days
    dd=pd.concat([d.assign(coin=c) for c in data["days"] for d in data["days"][c].values()])
    out["book_days"]=pd.Series({"mean_book":dd["book_return"].mean(),"mean_coin":dd["coin_return"].mean(),
        "share_nonzero":(dd["book_return"].abs()>1e-9).mean()})
    return out
