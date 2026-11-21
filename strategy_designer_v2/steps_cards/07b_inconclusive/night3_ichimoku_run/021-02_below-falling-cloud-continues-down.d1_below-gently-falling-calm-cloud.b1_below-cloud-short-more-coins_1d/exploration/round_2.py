def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=26
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values
            s=df.get("debug_info.components.slope_size.post_pipeline_value",pd.Series([np.nan]*len(df)))
            sr=df.get("debug_info.components.slope_size.last_history_value",pd.Series([np.nan]*len(df)))
            v=df.get("debug_info.components.vol30.post_pipeline_value",pd.Series([np.nan]*len(df)))
            vr=df.get("debug_info.components.vol30.last_history_value",pd.Series([np.nan]*len(df)))
            for i in range(0,len(df)-H,H):
                rows.append((coin,w,c[i+H]/c[i]-1,df["forecast"].iloc[i],df["timestamp"].iloc[i],s.iloc[i],sr.iloc[i],v.iloc[i],vr.iloc[i]))
    G=pd.DataFrame(rows,columns=["coin","w","r","f","ts","s","sr","v","vr"])
    G["drift"]=G.groupby("coin")["r"].transform("mean")
    G["ex"]=G["r"]-G["drift"]
    G["year"]=pd.to_datetime(G["ts"]).dt.year
    G["bear"]=G["year"].isin([2018,2019,2022,2025])
    A=G[G["f"]<0].copy()
    out={}
    def sm(x):
        return pd.Series({"n":len(x),"mean_ex":x["ex"].mean(),"t_ex":stats.ttest_1samp(x["ex"],0).statistic if len(x)>2 else np.nan,"mean_raw":x["r"].mean()})
    out["sign_check"]=pd.Series({"mean_short_gain_f/10*ex":(A["f"]/10*A["ex"]).mean(),
        "t":stats.ttest_1samp(A["f"]/10*A["ex"],0).statistic,"mean_ex":A["ex"].mean(),"t_ex":stats.ttest_1samp(A["ex"],0).statistic})
    out["spearman"]=pd.DataFrame({k:list(stats.spearmanr(A[k],A["ex"],nan_policy="omit")) for k in ["s","sr","v","vr","f"]},index=["rho","p"])
    A["sq"]=pd.qcut(A["s"].rank(method="first"),3,labels=["slow","mid","steep"])
    A["vq"]=pd.qcut(A["v"].rank(method="first"),3,labels=["calm","mid","wild"])
    out["slope_x_vol"]=A.groupby(["sq","vq"]).apply(sm)
    out["slope_x_bear"]=A.groupby(["bear","sq"]).apply(sm)
    out["vol_x_bear"]=A.groupby(["bear","vq"]).apply(sm)
    A["s5"]=pd.qcut(A["s"].rank(method="first"),5,labels=False)
    out["slope_quint"]=A.groupby("s5").apply(sm)
    A["half"]=np.where(A["year"]<=2021,"early","late")
    out["slope_x_half"]=A.groupby(["half","sq"]).apply(sm)
    A["coingrp"]=np.where(A["coin"].isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"]),"default6","other13")
    out["slope_x_coingrp"]=A.groupby(["coingrp","sq"]).apply(sm)
    out["inactive"]=sm(G[G["f"]==0])
    return out
