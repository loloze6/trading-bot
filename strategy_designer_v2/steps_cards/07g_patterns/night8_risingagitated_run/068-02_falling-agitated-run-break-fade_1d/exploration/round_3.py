def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change(); nxt=c.shift(-1)/c-1
            sgn=np.sign(r).shift(1).fillna(0).values; rv=r.shift(1).fillna(0).values
            dn=[];cum=[];cd=0;cf=0.0
            for s,x in zip(sgn,rv):
                if s<0: cd+=1; cf=(1+cf)*(1+x)-1
                else: cd=0; cf=0.0
                dn.append(cd);cum.append(cf)
            df=pd.DataFrame({"coin":coin,"w":w,"ts":b["timestamp"],"r":r,"nxt":nxt,"dn":dn,"cumfall":cum,
                "tr60":c/c.shift(60)-1,"inprof":(b["regime"]!="chop"),"vol":r.rolling(20).std()})
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["r","nxt"])
    d["ex"]=d["nxt"]-d.groupby("coin")["nxt"].transform("mean")
    def slope(x,col):
        x=x.dropna(subset=[col,"ex"])
        X=x[col].values.astype(float); y=x["ex"].values
        Xc=X-X.mean(); b=(Xc*(y-y.mean())).sum()/(Xc**2).sum()
        e=y-y.mean()-b*Xc
        sc=pd.Series(Xc*e).groupby(x["ts"].values).sum()
        se=np.sqrt((sc**2).sum())/(Xc**2).sum()
        return pd.Series({"n":len(x),"days":x.ts.nunique(),"slope%":100*b,"t":b/se})
    def summ(g):
        def f(x):
            s=x.groupby("ts")["ex"].sum(); n=len(x); m=x["ex"].mean()
            se=s.std(ddof=1)*np.sqrt(len(s))/n if len(s)>1 else np.nan
            return pd.Series({"n":n,"days":len(s),"mean_ex%":100*m,"t":m/se if se else np.nan})
        return g.apply(f)
    out={}
    U=d[(d.r>0)].copy(); U["dnc"]=U.dn.clip(upper=5)
    FC=U[(~U.inprof)&(U.tr60<-0.1)]
    CH=U[(~U.inprof)&(U.tr60.between(-0.1,0.1))]
    P=U[U.inprof]
    out["slope_dn_falling_calm_up"]=slope(FC,"dnc")
    out["slope_dn_choppy_out_up"]=slope(CH,"dnc")
    out["slope_dn_prof_up"]=slope(P,"dnc")
    out["falling_calm_up_by_window_dn2plus"]=summ(FC[FC.dn>=2].groupby("w"))
    out["falling_calm_up_by_coin_dn2plus"]=summ(FC[FC.dn>=2].groupby("coin"))
    PU=P[P.dn>=1].copy(); PU["retr"]=PU.r/(-PU.cumfall)
    out["slope_retr_prof"]=slope(PU.assign(retr=PU.retr.clip(upper=3)),"retr")
    D=d[(d.inprof)].copy(); D["z"]=(-d.r/d.vol)[d.inprof]
    out["slope_minus_today_z_prof_all"]=slope(D,"z")
    return out
