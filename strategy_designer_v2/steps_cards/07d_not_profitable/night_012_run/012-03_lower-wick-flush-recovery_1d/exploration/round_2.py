def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values; n=len(b)
            r1=b["close"].pct_change()
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            clr=(b["close"]-b["low"])/rng
            r20=b["close"]/b["close"].shift(20)-1
            r5=b["close"]/b["close"].shift(5)-1
            a=b["postRebalance_current_allocation"].values
            tv=b["postRebalance_total_value"].values
            for i in range(n):
                if b["regime"].iloc[i]!="mean_reversion": continue
                d={"coin":c,"win":w,"clr":clr.iloc[i],"r20":r20.iloc[i],"r5":r5.iloc[i],"ret":r1.iloc[i],"alloc":a[i]}
                for h in (1,3,5):
                    d[f"f{h}"]=cl[i+h]/cl[i]-1 if i+h<n else np.nan
                d["pnl1"]=a[i]*d["f1"] if i+1<n else np.nan
                d["bookret1"]=b["total_portfolio_value"].iloc[i+1]/tv[i]-1 if i+1<n else np.nan
                d["fee"]=1-tv[i]/b["total_portfolio_value"].iloc[i]
                d["fee_exit"]=(1-tv[i+1]/b["total_portfolio_value"].iloc[i+1]) if i+1<n else np.nan
                rows.append(d)
    f=pd.DataFrame(rows)
    out={}
    def tt(x): x=x.dropna(); return pd.Series({"mean":x.mean(),"t":stats.ttest_1samp(x,0).statistic,"n":len(x)})
    f["clrq"]=pd.qcut(f["clr"],4,labels=False)
    out["f1_by_clr"]=f.groupby("clrq")["f1"].apply(tt).unstack()
    out["corr_clr_f1"]=pd.Series({"spearman_f1":stats.spearmanr(f["clr"],f["f1"],nan_policy="omit")[0],
                                  "spearman_f3":stats.spearmanr(f["clr"],f["f3"],nan_policy="omit")[0],
                                  "spearman_r20_f1":stats.spearmanr(f["r20"],f["f1"],nan_policy="omit")[0],
                                  "spearman_r20_f3":stats.spearmanr(f["r20"],f["f3"],nan_policy="omit")[0],
                                  "spearman_r5_f3":stats.spearmanr(f["r5"],f["f3"],nan_policy="omit")[0],
                                  "spearman_ret_f3":stats.spearmanr(f["ret"],f["f3"],nan_policy="omit")[0]})
    out["pnl_by_clr"]=f.groupby("clrq")[["pnl1","bookret1","fee","fee_exit","alloc"]].mean()
    out["pnl_tot"]=pd.Series({"pnl1_sum":f["pnl1"].sum(),"bookret1_sum":f["bookret1"].sum(),"fee_sum":f["fee"].sum()+f["fee_exit"].sum(),
       "alloc1_f1_sum":f["f1"].sum()})
    f["r20q"]=pd.qcut(f["r20"],4,labels=False)
    out["f3_by_r20"]=f.groupby("r20q")["f3"].apply(tt).unstack()
    out["f1_by_r20"]=f.groupby("r20q")["f1"].apply(tt).unstack()
    # book days: where are losses
    dd=pd.concat([d.assign(coin=c,win=w) for c in data["days"] for w,d in data["days"][c].items()])
    nz=dd[dd["book_return"].abs()>1e-9]
    out["book_nz"]=pd.Series({"n":len(nz),"mean":nz["book_return"].mean(),"sum":nz["book_return"].sum(),
        "min":nz["book_return"].min(),"share_neg":(nz["book_return"]<0).mean()})
    out["book_by_win"]=dd.groupby("win")["book_return"].sum().sort_values().head(8)
    return out
