def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=96
    out={}
    rows=[]
    for coin,wins in data["bars"].items():
        rs=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            rs+=list(c[idx+H]/c[idx]-1)
        dr=np.mean(rs)
        for w,b in wins.items():
            s=pd.Series(b["close"].values)
            r24=s.pct_change(24)
            ma=r24.abs().rolling(720).mean()
            z=(-r24/ma).values
            r30=s.pct_change(720).values
            raw=b["debug_info.components.plunge_in_uptrend.last_history_value"].values
            c=s.values; n=len(c)
            for t in range(0,n-H,H):
                if np.isnan(z[t]) or np.isnan(r30[t]): continue
                rows.append({"coin":coin,"z":z[t],"r30":r30[t],"raw":raw[t],
                             "u":c[t+H]/c[t]-1-dr,
                             "u192":(c[t+192]/c[t]-1-2*dr) if t+192<n else np.nan})
    d=pd.DataFrame(rows)
    def g(x):
        x=x.dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    d["zb"]=pd.cut(d.z,[-np.inf,0,0.5,1,1.5,2,3,np.inf])
    d["up"]=np.where(d.r30>0,"r30_pos","r30_nonpos")
    out["grid_by_fall_and_trend"]=d.groupby(["up","zb"]).apply(lambda x: pd.concat([g(x.u),g(x.u192).add_suffix("_192")])).unstack(0) if False else d.groupby(["up","zb"]).apply(lambda x: g(x.u))
    out["grid_by_fall_192"]=d.groupby(["up","zb"]).apply(lambda x: g(x.u192))
    p=d[(d.r30>0)&(d.z>0)].copy()
    p["prod"]=p.z*p.r30*100
    out["n_pos_cells"]=len(p)
    for col in ["z","r30","prod"]:
        med=p[col].median()
        a=p[p[col]>med].u; bb=p[p[col]<med].u
        out[f"split_{col}"]=pd.Series({"med":med,"above":a.mean(),"below":bb.mean(),"diff":a.mean()-bb.mean(),"welch_t":stats.ttest_ind(a,bb,equal_var=False).statistic,"n_a":len(a),"n_b":len(bb)})
        out[f"spearman_{col}"]=pd.Series(stats.spearmanr(p[col],p.u)[:2],index=["rho","p"])
    q=d[d.z>0].copy()
    out["spearman_z_r30nonpos"]=pd.Series(stats.spearmanr(q[q.r30<=0].z,q[q.r30<=0].u)[:2],index=["rho","p"])
    p["r30q"]=pd.qcut(p.r30,4,labels=False)
    p["zq"]=pd.qcut(p.z,3,labels=False)
    out["pos_r30q_x_zq_mean"]=p.groupby(["r30q","zq"]).u.mean().unstack()
    out["pos_r30q_x_zq_n"]=p.groupby(["r30q","zq"]).u.size().unstack()
    return out
