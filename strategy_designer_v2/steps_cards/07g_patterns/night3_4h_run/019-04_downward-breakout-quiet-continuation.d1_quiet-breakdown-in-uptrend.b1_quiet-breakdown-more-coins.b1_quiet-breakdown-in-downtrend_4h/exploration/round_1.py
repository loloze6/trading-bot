def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=18
    ev=[]; grid=[]; hourly=[]; fcs=[]; big=[]
    for coin, wins in data["bars"].items():
        # coin usual move / drift over H on grid
        g=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            g+=list(c[idx+H]/c[idx]-1)
        g=np.array(g); 
        if len(g)<10: continue
        drift=np.nanmean(g); sd=np.nanstd(g)
        r1all=[]
        for w,b in wins.items():
            r=b["close"].pct_change(); r1all.append(r)
        r1all=pd.concat(r1all); d1=r1all.mean(); s1=r1all.std()
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; hi=b["high"]; lo=b["low"]
            rng=(hi-lo)/c
            m180=rng.rolling(180).mean()
            phi=hi.shift(1).rolling(12).max(); plo=lo.shift(1).rolling(12).min()
            srng=(phi-plo)/c.shift(1)
            narrow=m180/srng
            r180=c/c.shift(180)-1
            fwd=c.shift(-H)/c-1
            fwd6=c.shift(-6)/c-1
            n=len(b); pos=np.arange(n); cell=pos//H
            dn=(c<plo); up=(c>phi)
            df=pd.DataFrame({"cell":cell,"narrow":narrow,"r180":r180,"fwd":fwd,"dn":dn,"up":up,
                             "depth_dn":(plo-c)/c,"depth_up":(c-phi)/c,"fc":b["forecast"]})
            df=df[df.fwd.notna()]
            for side in ["dn","up"]:
                e=df[df[side]].groupby("cell").head(1).copy()
                e["side"]=side; e["coin"]=coin
                e["u"]=(e.fwd-drift)/sd*(1 if side=="up" else -1)  # in breakout direction, normalized
                e["upct"]=(e.fwd-drift)*(1 if side=="up" else -1)
                ev.append(e[["side","coin","narrow","r180","u","upct","depth_dn","depth_up"]])
            # grid: abs move vs narrowness
            gi=np.arange(0,n,H)
            gg=pd.DataFrame({"narrow":narrow.iloc[gi].values,"fwd":fwd.iloc[gi].values,"r180":r180.iloc[gi].values})
            gg["az"]=(gg.fwd-drift).abs()/sd; gg["z"]=(gg.fwd-drift)/sd; gg["coin"]=coin
            grid.append(gg)
            ts=pd.to_datetime(b["timestamp"])
            r=c.pct_change().shift(-1)  # next bar return from this bar close
            hourly.append(pd.DataFrame({"hour":ts.dt.hour,"wd":ts.dt.weekday,"z":(r-d1)/s1}))
            act=b["forecast"][b["forecast"]!=0]
            fcs.append(act)
            z0=(c.pct_change()-d1)/s1
            big.append(pd.DataFrame({"z0":z0,"f6":(fwd6-6*d1)/(s1*np.sqrt(6))}))
    E=pd.concat(ev).dropna(subset=["u","narrow"]); G=pd.concat(grid).dropna(); Hh=pd.concat(hourly).dropna(); F=pd.concat(fcs); B=pd.concat(big).dropna()
    out={}
    f=F.describe(percentiles=[.05,.25,.5,.75,.95]); f["share_at_-20"]=(F<=-19.99).mean(); out["forecast_active"]=f
    G["nq"]=pd.qcut(G.narrow,5,labels=False)
    out["absmove_by_narrow_quint"]=G.groupby("nq").agg(n=("az","size"),abs_z=("az","mean"),mean_z=("z","mean"))
    E["reg"]=np.where(E.r180<0,"r30neg","r30pos")
    E["nt"]=E.groupby("side").narrow.transform(lambda x: pd.qcut(x,3,labels=False))
    def agg(x):
        return pd.Series({"n":len(x),"u_mean":x.u.mean(),"upct":x.upct.mean()*100,"t":x.u.mean()/x.u.std()*np.sqrt(len(x))})
    out["break_side_regime"]=E.groupby(["side","reg"]).apply(agg)
    out["break_side_regime_narrowtercile"]=E.groupby(["side","reg","nt"]).apply(agg)
    E["dq"]=np.nan
    for s,col in [("dn","depth_dn"),("up","depth_up")]:
        m=E.side==s; E.loc[m,"dq"]=pd.qcut(E.loc[m,col],3,labels=False)
    out["break_side_depthtercile"]=E.groupby(["side","dq"]).apply(agg)
    out["break_side_coin"]=E.groupby(["side","coin"]).apply(agg)
    hz=Hh.groupby("hour").z.agg(["size","mean","std"]); hz["t"]=hz["mean"]/hz["std"]*np.sqrt(hz["size"]); out["next4h_by_hour"]=hz
    wz=Hh.groupby("wd").z.agg(["size","mean","std"]); wz["t"]=wz["mean"]/wz["std"]*np.sqrt(wz["size"]); out["next4h_by_weekday"]=wz
    B["zb"]=pd.cut(B.z0,[-99,-3,-2,-1,1,2,3,99])
    bb=B.groupby("zb").f6.agg(["size","mean","std"]); bb["t"]=bb["mean"]/bb["std"]*np.sqrt(bb["size"]/6); out["next24h_after_4hmove"]=bb
    return out
