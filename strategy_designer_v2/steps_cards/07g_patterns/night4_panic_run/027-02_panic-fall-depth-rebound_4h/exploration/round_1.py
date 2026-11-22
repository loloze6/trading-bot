def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=84
    rows=[]; allgrid=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(b)
            rng=(b["high"]-b["low"])/b["close"]
            ratio=(rng.rolling(6).mean()/rng.rolling(180).mean()).values
            r6=(b["close"]/b["close"].shift(6)-1).values
            r42=(b["close"]/b["close"].shift(42)-1).values
            r180=(b["close"]/b["close"].shift(180)-1).values
            ts=pd.to_datetime(b["timestamp"])
            for g0 in range(0,n-H,H):
                fwd=c[g0+H]/c[g0]-1
                allgrid.append(dict(coin=coin,w=w,fwd=fwd,ratio=ratio[g0],r6=r6[g0],r180=r180[g0]))
                cell=range(g0,min(g0+H,n-H))
                for kind in ["panic_fall","panic_rise","calm_fall"]:
                    for t in cell:
                        if np.isnan(ratio[t]) or np.isnan(r6[t]): continue
                        if kind=="panic_fall" and ratio[t]>=3 and r6[t]<0: pass
                        elif kind=="panic_rise" and ratio[t]>=3 and r6[t]>0: pass
                        elif kind=="calm_fall" and ratio[t]<1.5 and r6[t]<-0.05: pass
                        else: continue
                        f={}
                        for h in [6,18,42,84]:
                            f["f%d"%h]=c[t+h]/c[t]-1 if t+h<n else np.nan
                        rows.append(dict(coin=coin,w=w,kind=kind,t=t,ratio=ratio[t],r6=r6[t],r42=r42[t],r180=r180[t],hour=ts[t].hour,wd=ts[t].weekday(),**f))
                        break
    G=pd.DataFrame(allgrid); R=pd.DataFrame(rows)
    drift=G.groupby("coin")["fwd"].agg(["mean","std"])
    R=R.join(drift,on="coin")
    for h in [6,18,42,84]:
        R["x%d"%h]=R["f%d"%h]-R["mean"]*h/84
    out={}
    def summ(df,col="x84"):
        s=df[col].dropna()
        return pd.Series(dict(n=len(s),mean=s.mean(),t=s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan))
    out["by_kind_84"]=R.groupby("kind").apply(summ)
    for h in [6,18,42]:
        out["by_kind_%d"%h]=R.groupby("kind").apply(lambda d: summ(d,"x%d"%h))
    P=R[R.kind=="panic_fall"].copy()
    P["ratio_q"]=pd.qcut(P["ratio"],3,labels=False)
    out["pf_by_ratio_tercile"]=P.groupby("ratio_q").apply(summ)
    P["r180_sign"]=np.sign(P["r180"])
    out["pf_by_prior30d_sign"]=P.groupby("r180_sign").apply(summ)
    P["r42_q"]=pd.qcut(P["r42"],3,labels=False)
    out["pf_by_prior7d_tercile"]=P.groupby("r42_q").apply(summ)
    out["pf_by_coin"]=P.groupby("coin").apply(summ)
    Q=R[R.kind=="panic_rise"].copy()
    Q["ratio_q"]=pd.qcut(Q["ratio"],3,labels=False)
    out["pr_by_ratio_tercile"]=Q.groupby("ratio_q").apply(summ)
    A=R[R.kind!="calm_fall"].copy(); A["ratio_q"]=pd.qcut(A["ratio"],4,labels=False)
    out["panic_any_ratio_quartile"]=A.groupby("ratio_q").apply(summ)
    sl=stats.linregress(A["ratio"].values[~A.x84.isna()],(A["x84"]/A["std"]).dropna().values)
    out["panic_any_slope_x84std_on_ratio"]=pd.Series(dict(slope=sl.slope,t=sl.slope/sl.stderr,n=A.x84.notna().sum()))
    # all grid: forward by vol ratio level
    G=G.join(drift,on="coin"); G["x"]=(G["fwd"]-G["mean"])/G["std"]
    G["rq"]=pd.qcut(G["ratio"],5,labels=False)
    out["grid_by_ratio_quintile"]=G.groupby("rq")["x"].agg(["count","mean","std"])
    G["r180q"]=pd.qcut(G["r180"],5,labels=False)
    out["grid_by_prior30d_quintile"]=G.groupby("r180q")["x"].agg(["count","mean","std"])
    # book days
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd=d.copy(); dd["coin"]=coin; dd["w"]=w; D.append(dd)
    D=pd.concat(D)
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    out["book_by_coin"]=D.groupby("coin")[["book_return","coin_return"]].mean()
    out["book_by_window"]=D.groupby("w")["book_return"].agg(["mean","sum"])
    T=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            tt=t.copy(); tt["coin"]=coin; T.append(tt)
    T=pd.concat(T)
    out["trades_summary"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"])
    T["eq"]=pd.qcut(T["entry_forecast"].rank(method="first"),3,labels=False)
    out["trades_by_entry_forecast_tercile"]=T.groupby("eq")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
