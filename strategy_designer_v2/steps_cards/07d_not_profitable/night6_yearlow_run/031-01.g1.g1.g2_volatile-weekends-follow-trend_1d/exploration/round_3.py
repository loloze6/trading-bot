def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows=[]; frid=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"])
            cl=pd.Series(b["close"].values)
            r=cl.pct_change()
            vol=r.rolling(20).std()
            vr=vol/vol.rolling(60).mean()
            a=b["postRebalance_current_allocation"].fillna(0).values
            nxt=(cl.shift(-1)/cl-1).values
            f=b["forecast"].fillna(0).values
            side=np.zeros(len(b)); last=0
            for i in range(len(b)):
                if f[i]!=0: last=np.sign(f[i])
                if a[i]!=0: side[i]=last
            ch=np.abs(np.diff(np.r_[0,a])); fee=0.0019/2
            for i in range(len(b)-1):
                rows.append(dict(coin=c,wn=int(w[1:]),day=ts[i].normalize(),g=a[i]*nxt[i]-ch[i]*fee,side=side[i],held=a[i]!=0,
                                 coinr=nxt[i]))
            for i in range(14,len(b)-2):
                if ts[i].dayofweek==4:
                    frid.append(dict(coin=c,wn=int(w[1:]),year=ts[i].year,vr=vr.iloc[i],ret2=cl[i+2]/cl[i]-1,f=f[i],a=a[i],
                                     r14=cl[i]/cl[i-14]-1))
    B=pd.DataFrame(rows)
    def book(x):
        d=x.groupby(["wn","day"])["g"].mean().reset_index().sort_values(["wn","day"])
        v=(1+d["g"]).cumprod(); dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(d))-1
        return yr,dd,d
    L=B.copy(); L.loc[L["side"]<0,"g"]=0.0
    yr,dd,d=book(L)
    out["long_only"]=pd.Series(dict(yearly=yr,maxdd=dd,calmar=yr/abs(dd)))
    loo=[]
    for w in sorted(L["wn"].unique()):
        y,dd2,_=book(L[L["wn"]!=w]); loo.append(dict(wn=w,calmar=y/abs(dd2)))
    lo=pd.DataFrame(loo); out["long_only_loo_calmar_min_max"]=pd.Series(dict(min=lo["calmar"].min(),max=lo["calmar"].max(),worst_wn=lo.loc[lo["calmar"].idxmin(),"wn"]))
    S=B.copy(); S.loc[S["side"]>0,"g"]=0.0
    _,_,ds=book(S); ds["year"]=pd.to_datetime(ds["day"]).dt.year
    out["short_side_book_by_year_sum"]=ds.groupby("year")["g"].sum()
    F=pd.DataFrame(frid).dropna(subset=["vr"])
    mu=F.groupby("coin")["ret2"].mean(); F["ex"]=F["ret2"]-F["coin"].map(mu)
    hv=F[F["vr"]>1]
    def s(g): return pd.Series(dict(n=len(g),ex=g["ex"].mean(),t=g["ex"].mean()/g["ex"].std()*np.sqrt(len(g))))
    out["hv_long_signal_vs_not"]=hv.groupby(hv["r14"]>0).apply(s)
    out["lv_up_vs_down_ex"]=F[F["vr"]<=1].groupby(F["r14"]>0).apply(s)
    up=hv[hv["r14"]>0].copy(); up["q"]=pd.qcut(up["r14"],3,labels=False)
    out["hv_up_graded_by_r14"]=up.groupby("q").apply(s)
    dn=hv[hv["r14"]<0].copy(); dn["q"]=pd.qcut(dn["r14"],3,labels=False)
    out["hv_down_graded_by_r14_ex"]=dn.groupby("q").apply(s)
    return out
