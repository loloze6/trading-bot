def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    rows=[]; book=[]
    for c in bars:
        for w,df in bars[c].items():
            d=df.copy()
            ts=pd.to_datetime(d["timestamp"],utc=True)
            d["ch"]=((ts.dt.hour+1)%24).values
            d["wd"]=ts.dt.weekday.values
            cl=d["close"].values
            r1=np.r_[np.nan,cl[1:]/cl[:-1]-1]
            nxt=np.r_[cl[1:]/cl[:-1]-1,np.nan]
            d["r1"]=r1
            d["gross"]=d["postRebalance_current_allocation"].values*nxt
            d["fee"]=(d["postRebalance_total_value"]-d["total_portfolio_value"])/d["total_portfolio_value"]
            ret72=pd.Series(cl).pct_change(72)
            z=(ret72-ret72.rolling(72,min_periods=20).mean())/ret72.rolling(72,min_periods=20).std()
            d["z"]=z.values
            vol=pd.Series(r1).rolling(24).std()
            d["vol24"]=vol.values
            d["r24"]=pd.Series(cl).pct_change(24).values
            f2=np.r_[cl[2:]/cl[:-2]-1,np.nan,np.nan]
            d["f2"]=f2
            d["coin"]=c; d["win"]=w
            book.append(d[["coin","win","gross","fee","postRebalance_current_allocation","regime","ch"]])
            g=d.iloc[::2]
            rows.append(g[["coin","win","ch","wd","z","vol24","r1","r24","f2","forecast"]])
    G=pd.concat(rows); B=pd.concat(book)
    G["f2x"]=G["f2"]-G.groupby("coin")["f2"].transform("mean")
    G=G.dropna(subset=["f2x"])
    out={}
    out["book_gross_vs_fee_per_bar"]=B.groupby("coin")[["gross","fee"]].mean()*1e4
    out["book_by_closehour_gross_bp"]=B.groupby("ch")["gross"].agg(["mean","count"]).assign(mean=lambda x:x["mean"]*1e4).T
    def tt(s): return pd.Series({"mean_bp":s.mean()*1e4,"t":s.mean()/s.std()*np.sqrt(len(s)),"n":len(s)})
    out["fwd2_by_closehour"]=G.groupby("ch")["f2x"].apply(tt).unstack()
    G["zf"]=(-G["z"]).clip(lower=0)
    G["fall"]=pd.cut(-G["z"],[-np.inf,-1.5,-0.5,0.5,1.5,np.inf])
    G["off"]=G["ch"].isin([2,3,4,5,10,11,12,13,18,19,20,21])
    out["fwd2_by_z_bucket_x_off"]=G.groupby(["fall","off"])["f2x"].apply(tt).unstack()
    G["r1q"]=pd.qcut(G["r1"]/G["vol24"],5,labels=False)
    out["fwd2_by_last1h_scaled_q"]=G.groupby("r1q")["f2x"].apply(tt).unstack()
    G["r24q"]=pd.qcut(G["r24"],5,labels=False)
    out["fwd2_by_24h_ret_q"]=G.groupby("r24q")["f2x"].apply(tt).unstack()
    G["vq"]=G.groupby("coin")["vol24"].transform(lambda s:pd.qcut(s,3,labels=False))
    out["fwd2_by_vol_x_r1q"]=G.groupby(["vq","r1q"])["f2x"].mean().unstack()*1e4
    out["fwd2_by_weekday"]=G.groupby("wd")["f2x"].apply(tt).unstack()
    return out
