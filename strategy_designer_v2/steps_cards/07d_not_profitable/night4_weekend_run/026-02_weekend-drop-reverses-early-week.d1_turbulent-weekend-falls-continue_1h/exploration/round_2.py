def explore(data):
    import pandas as pd, numpy as np
    out = {}
    cs=[]
    for c,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            cl=b["close"].values
            if len(cl)>96: allr.append(cl[48::48]/cl[:-48:48]-1)
        drift=np.nanmean(np.concatenate(allr))
        for w,b in ws.items():
            ts=pd.to_datetime(b["timestamp"]); cl=b["close"].values; n=len(b)
            idx=np.where((ts.dt.dayofweek==6)&(ts.dt.hour==23))[0]
            for i in idx:
                if i+48>=n or i<216: continue
                fwd=cl[i+48]/cl[i]-1; wk=cl[i]/cl[i-48]-1
                lr=np.diff(np.log(cl[i-216:i+1]))
                vr=lr[-48:].std()/lr[:168].std()
                # same-size weekday move: Wed00-Fri00 then Fri00-Sun00? use Wed 00 -> Fri 00 move then next 48
                cs.append(dict(c=c,w=w,f=b["forecast"].iloc[i],fwd=fwd,ex=fwd-drift,wk=wk,vr=vr,
                               alloc=b["postRebalance_current_allocation"].iloc[i],
                               gain=-(fwd)*abs(b["postRebalance_current_allocation"].iloc[i])))
    C=pd.DataFrame(cs)
    def tt(v): return v.mean()/v.std()*np.sqrt(len(v))
    F=C[C.wk<0].copy()
    F["wk3"]=pd.qcut(F.wk,3,labels=["bigfall","mid","small"])
    F["vr3"]=pd.qcut(F.vr,3,labels=["calm","mid","turb"])
    g=F.groupby(["wk3","vr3"]).agg(n=("ex","size"),ex_fwd=("ex","mean"),t=("ex",tt),alloc=("alloc","mean"),book_gain=("gain","mean"))
    out["falls_wk_x_vr_fwd_excess"]=g.round(4)
    R=C[C.wk>0].copy()
    R["vr3"]=pd.qcut(R.vr,3,labels=["calm","mid","turb"])
    R["wk3"]=pd.qcut(R.wk,3,labels=["small","mid","bigrise"])
    out["rises_wk_x_vr_fwd_excess"]=R.groupby(["wk3","vr3"]).agg(n=("ex","size"),ex_fwd=("ex","mean"),t=("ex",tt)).round(4)
    # all weekends: vol ratio alone with sign of weekend
    C["vr5"]=pd.qcut(C.vr,5,labels=False)
    C["sgn_ex"]=np.sign(C.wk)*C.ex
    out["all_by_vr_continuation"]=C.groupby("vr5").agg(n=("ex","size"),vr=("vr","mean"),cont=("sgn_ex","mean"),t=("sgn_ex",tt)).round(4)
    # correlation of weekend z-scaled fall with fwd among falls
    F["wkz"]=F.wk/F.groupby("c").wk.transform("std")
    out["falls_corr"]=pd.Series({"corr_wk_ex":F[["wk","ex"]].corr().iloc[0,1],"corr_vr_ex":F[["vr","ex"]].corr().iloc[0,1],
                                 "corr_absf_alloc":F[["f","alloc"]].corr().iloc[0,1],"book_gain_total_mean":F.gain.mean()}).round(4)
    return out
