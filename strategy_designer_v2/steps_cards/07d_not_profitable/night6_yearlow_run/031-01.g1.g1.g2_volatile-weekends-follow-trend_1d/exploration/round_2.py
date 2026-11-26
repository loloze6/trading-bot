def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # Rebuild a per-bar book from allocation x next return, with variants that drop cases
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
            # attribute each held bar to the Friday case that opened it
            case_vr=np.full(len(b),np.nan); case_side=np.zeros(len(b))
            last_vr=np.nan; last_side=0
            for i in range(len(b)):
                if f[i]!=0:
                    last_vr=vr.iloc[i]; last_side=np.sign(f[i])
                if a[i]!=0:
                    case_vr[i]=last_vr; case_side[i]=last_side
            fee=0.0019/2
            ch=np.abs(np.diff(np.r_[0,a]))
            for i in range(len(b)-1):
                rows.append(dict(coin=c,wn=int(w[1:]),day=ts[i].normalize(),year=ts[i].year,
                                 g=a[i]*nxt[i]-ch[i]*fee, cvr=case_vr[i], cside=case_side[i],
                                 held=a[i]!=0))
            for i in range(len(b)-2):
                if ts[i].dayofweek==4:
                    frid.append(dict(coin=c,vr=vr.iloc[i],ret2=cl[i+2]/cl[i]-1,f=f[i],
                                     r14=cl[i]/cl[i-14]-1 if i>=14 else np.nan))
    B=pd.DataFrame(rows)
    def book(mask):
        x=B.copy(); x.loc[~mask,"g"]=0.0
        d=x.groupby(["wn","day"])["g"].mean().reset_index().sort_values(["wn","day"])
        v=(1+d["g"]).cumprod(); dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(d))-1
        return pd.Series(dict(yearly=yr,maxdd=dd,calmar=yr/abs(dd),sharpe=d["g"].mean()/d["g"].std()*np.sqrt(365)))
    allm=pd.Series(True,index=B.index)
    out["variants"]=pd.DataFrame({
        "all":book(allm),
        "long_only":book(B["cside"]>=0),
        "vr_gt_1.28":book((B["cvr"]>1.28)|(~B["held"])),
        "long_vr_gt_1.28":book(((B["cvr"]>1.28)&(B["cside"]>0))|(~B["held"])),
        "short_only":book(B["cside"]<=0),
    }).T
    # where the deepest fall comes from: side contributions inside window 11-15
    x=B[B["held"]]
    out["pnl_by_window_side"]=x.pivot_table(index="wn",columns="cside",values="g",aggfunc="sum").loc[[2,11,12,13,14,15,24]]
    # condition alone check: all Fridays long (weekend drift) by vr bucket, and vr high w/o signal
    F=pd.DataFrame(frid).dropna(subset=["vr"])
    mu=F.groupby("coin")["ret2"].mean(); F["ex"]=F["ret2"]-F["coin"].map(mu)
    F["vrb"]=pd.cut(F["vr"],[0,1,1.28,1.52,10])
    def s(g): return pd.Series(dict(n=len(g),ret2=g["ret2"].mean(),ex=g["ex"].mean(),t=g["ex"].mean()/g["ex"].std()*np.sqrt(len(g))))
    out["fridays_plain_by_vr"]=F.groupby("vrb").apply(s)
    F["up"]=F["r14"]>0
    F["sg"]=np.sign(F["r14"])*F["ex"]
    out["r14sign_by_vr_and_dir"]=F.dropna(subset=["r14"]).groupby(["vrb","up"]).apply(lambda g: pd.Series(dict(n=len(g),g=g["sg"].mean(),t=g["sg"].mean()/g["sg"].std()*np.sqrt(len(g)))))
    return out
