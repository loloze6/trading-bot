def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; hourly=[]
    H=72
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            c=df["close"].values.astype(float); v=df["volume"].values.astype(float)
            lr=np.diff(np.log(c),prepend=np.nan)
            ts=pd.to_datetime(df["timestamp"])
            r1=pd.Series(c).pct_change().shift(-1).values
            hourly.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour.values,"wd":ts.dt.weekday.values,"r":r1,"absr":np.abs(lr),"pos":df["postRebalance_current_allocation"].values}))
            n=len(c)
            for t in range(H,n-H,H):
                seg=lr[t-H+1:t+1]; vs=v[t-H+1:t+1]
                if np.any(~np.isfinite(seg)): continue
                past=c[t]/c[t-H]-1; fwd=c[t+H]/c[t]-1
                sabs=np.abs(seg).sum()
                eff=abs(seg.sum())/sabs if sabs>0 else np.nan  # path efficiency (grind)
                conc=(seg**2).sum()/sabs**2 if sabs>0 else np.nan # jump concentration
                even=np.median(vs)/vs.mean() if vs.mean()>0 else np.nan
                vol=np.sqrt((seg**2).sum())
                rows.append(dict(coin=coin,w=w,past=past,fwd=fwd,eff=eff,conc=conc,even=even,vol=vol,year=ts.iloc[t].year))
    g=pd.DataFrame(rows)
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    out={}
    def tb(sub,col):
        sub=sub.dropna(subset=[col,"ex"])
        q=sub[col].rank(pct=True)
        a=sub.loc[q>2/3,"ex"]; b=sub.loc[q<=1/3,"ex"]
        t=stats.ttest_ind(a,b,equal_var=False).statistic
        rho=stats.spearmanr(sub[col],sub["ex"]).correlation
        return [len(sub),a.mean(),b.mean(),t,rho]
    res={}
    for side,sub in [("up",g[g.past>0]),("down",g[g.past<=0]),("all",g)]:
        for col in ["past","eff","conc","even","vol"]:
            res[f"{side}_{col}"]=tb(sub,col)
    out["top_minus_bottom"]=pd.DataFrame(res,index=["n","top_ex","bot_ex","welch_t","spearman"]).T.round(4)
    # signed: past*eff, past*conc regression on ex
    import numpy.linalg as la
    gg=g.dropna().copy()
    gg["pz"]=(gg.past-gg.past.mean())/gg.past.std()
    X=np.column_stack([np.ones(len(gg)),gg.pz,gg.pz*(gg.eff-gg.eff.mean())/gg.eff.std(),gg.pz*(gg.conc-gg.conc.mean())/gg.conc.std(),(gg.vol-gg.vol.mean())/gg.vol.std()])
    b,_,_,_=la.lstsq(X,gg.ex.values,rcond=None)
    resid=gg.ex.values-X@b; s2=resid@resid/(len(gg)-X.shape[1]); se=np.sqrt(np.diag(s2*la.inv(X.T@X)))
    out["regress_ex"]=pd.DataFrame({"b":b,"t":b/se},index=["c","past","past*eff","past*conc","vol"]).round(5)
    # per coin past sign
    pc={}
    for coin,sub in g.groupby("coin"):
        pc[coin]=tb(sub,"past")+tb(sub,"vol")[3:4]
    out["per_coin_past_t_volt"]=pd.DataFrame(pc,index=["n","top","bot","t_past","rho","t_vol"]).T.round(4)
    h=pd.concat(hourly).dropna(subset=["r"])
    hr=h.groupby("hour")["r"].agg(["mean","std","count"]); hr["t"]=hr["mean"]/(hr["std"]/np.sqrt(hr["count"]))
    out["by_hour"]=hr[["mean","t"]].round(6)
    wd=h.groupby("wd")["r"].agg(["mean","std","count"]); wd["t"]=wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    out["by_weekday"]=wd[["mean","t"]].round(6)
    d=[]
    for coin,ws in data["days"].items():
        for w,df in ws.items():
            x=df[["day","book_return","coin_return"]].copy(); x["coin"]=coin; x["w"]=w; d.append(x)
    d=pd.concat(d); d["year"]=pd.to_datetime(d["day"]).dt.year
    out["book_by_year"]=d.groupby("year")[["book_return","coin_return"]].mean().round(5)
    out["book_by_coin"]=d.groupby("coin")[["book_return","coin_return"]].mean().round(5)
    return out
