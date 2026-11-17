def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            b["wd"]=ts.dt.weekday; b["year"]=ts.dt.year
            c=pd.Series(b["close"].values)
            b["r0"]=c.pct_change(); b["r1"]=c.shift(-1)/c-1; b["r2b"]=c.shift(-2)/c.shift(-1)-1
            b["wk2"]=c/c.shift(2)-1
            b["ret20"]=c/c.shift(20)-1
            b["absmean60"]=b["r0"].abs().shift(1).rolling(60,min_periods=20).mean()
            b["alloc"]=b["postRebalance_current_allocation"]
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["coin"]=coin; b["w"]=w
            rows.append(b)
    B=pd.concat(rows,ignore_index=True)
    out={}
    S=B[(B.wd==6)&(B.forecast!=0)&B.r1.notna()&B.r2b.notna()].copy()
    S["g_mon"]=S.alloc*S.r1; S["g_tue"]=S.alloc*S.r2b
    out["fees"]=pd.Series({"mean_fee_sunday":B.loc[B.wd==6,"fee"].mean(),"mean_fee_monday":B.loc[B.wd==0,"fee"].mean(),
        "gross_mon_gain_per_case":S.g_mon.mean(),"gross_tue_gain_if_held":S.g_tue.mean(),
        "t_mon":stats.ttest_1samp(S.g_mon,0).statistic,"t_tue":stats.ttest_1samp(S.g_tue,0).statistic,"n":len(S)})
    # Saturday+Sunday move vs Sunday-only as grade
    S["z1"]=S.r0/S.absmean60; S["z2"]=S.wk2/(S.absmean60*np.sqrt(2))
    S["rev2"]=-(S.r1+S.r2b+S.r1*S.r2b)
    for k in ["z1","z2"]:
        x=S[[k,"rev2","r1"]].dropna()
        out["corr_"+k]=pd.Series({"spearman_with_2day_reversal":stats.spearmanr(x[k],x.rev2).correlation,"spearman_with_mon_reversal":stats.spearmanr(x[k],-x.r1).correlation,"n":len(x)})
    # worst Mondays: book contribution and what preceded
    S["absz"]=S.z1.abs()
    S["dec"]=pd.qcut(S.g_mon.rank(method="first"),10,labels=False)
    out["by_gain_decile"]=S.groupby("dec").agg(n=("g_mon","size"),g=("g_mon","mean"),absz=("absz","mean"),ret20=("ret20","mean"),signed_r0=("r0","mean"),short_share=("forecast",lambda x:(x<0).mean()))
    # reversal on Monday by |z| quintile and trend alignment (move with or against 20d trend)
    S["with_trend"]=np.sign(S.r0)==np.sign(S.ret20-S.r0)
    S["zq"]=pd.qcut(S.absz.rank(method="first"),4,labels=["q1","q2","q3","q4"])
    S["sg2"]=np.sign(S.forecast)*(S.r1+S.r2b)
    out["by_z_trendalign"]=S.groupby(["zq","with_trend"]).agg(n=("r1","size"),signed_mon=("r1",lambda x:np.nan),g_mon=("g_mon","mean"),sg2=("sg2","mean"))
    out["by_z_trendalign"]=out["by_z_trendalign"].drop(columns="signed_mon")
    # window-level book: worst windows
    rows=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            rows.append(d.assign(w=w))
    D=pd.concat(rows); port=D.groupby(["w","day"]).book_return.mean().dropna().reset_index()
    wk=port.groupby("w").book_return.agg(["sum","size"])
    out["windows_book_sum_sorted"]=wk.sort_values("sum").head(8)
    return out
