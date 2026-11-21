def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=26
    rows=[]
    for coin,ws in data["bars"].items():
        grid=[]
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values
            for i in range(0,len(df)-H,H):
                grid.append((w,i,c[i+H]/c[i]-1,df["forecast"].iloc[i],df["timestamp"].iloc[i],
                             df.get("debug_info.components.slope_size.post_pipeline_value",pd.Series([np.nan]*len(df))).iloc[i],
                             df.get("debug_info.components.vol30.post_pipeline_value",pd.Series([np.nan]*len(df))).iloc[i],
                             c[min(i+5,len(c)-1)]/c[i]-1, c[min(i+10,len(c)-1)]/c[i]-1))
        g=pd.DataFrame(grid,columns=["w","i","r","f","ts","s","v","r5","r10"])
        g["coin"]=coin; g["drift"]=g["r"].mean()
        rows.append(g)
    G=pd.concat(rows)
    G["ex"]=G["r"]-G["drift"]
    G["year"]=pd.to_datetime(G["ts"]).dt.year
    A=G[G["f"]<0].copy()
    A["m"]=-A["f"]/10*A["ex"]
    def summ(x):
        return pd.Series({"n":len(x),"mean_m":x["m"].mean(),"t_m":stats.ttest_1samp(x["m"],0).statistic if len(x)>2 else np.nan,
                          "mean_ex":x["ex"].mean(),"med_ex":x["ex"].median(),"mean_raw":x["r"].mean(),"share_raw_neg":(x["r"]<0).mean(),"mean_f":x["f"].mean()})
    out={}
    out["all"]=summ(A).to_frame().T
    out["by_coin"]=A.groupby("coin").apply(summ)
    out["by_year"]=A.groupby("year").apply(summ)
    A["fq"]=pd.qcut(A["f"],4,labels=["q1_strongest","q2","q3","q4_weakest"])
    out["by_fquart"]=A.groupby("fq").apply(summ)
    A["sq"]=pd.qcut(A["s"].rank(method="first"),3,labels=["slow","mid","steep"])
    A["vq"]=pd.qcut(A["v"].rank(method="first"),3,labels=["calm","mid","wild"])
    out["by_slope"]=A.groupby("sq").apply(summ)
    out["by_vol"]=A.groupby("vq").apply(summ)
    out["drift_coin"]=G.groupby("coin")["drift"].first()
    out["short_horizons"]=pd.Series({"r5_mean":A["r5"].mean(),"r10_mean":A["r10"].mean(),"r26_mean":A["r"].mean(),
        "inactive_r26_mean":G[G["f"]==0]["r"].mean(),"inactive_n":(G["f"]==0).sum()})
    out["active_minus_inactive_t"]=stats.ttest_ind(A["r"],G[G["f"]==0]["r"],equal_var=False).statistic
    return out
