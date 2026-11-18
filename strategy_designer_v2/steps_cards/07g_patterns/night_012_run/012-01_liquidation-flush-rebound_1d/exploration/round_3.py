def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; r=c.pct_change()
            vol=r.rolling(20).std().shift(1)
            z=r/vol
            vr=b["volume"]/b["volume"].rolling(30).mean().shift(1)
            yr=pd.to_datetime(b["timestamp"]).dt.year
            for h in (3,):
                fwd=c.shift(-h)/c-1
                grid=(np.arange(len(b))%h==0)
                rows.append(pd.DataFrame({"coin":coin,"wn":int(w[1:]),"z":z,"vr":vr,"fwd":fwd,"grid":grid,"yr":yr,"vol":vol}))
    D=pd.concat(rows,ignore_index=True)
    D=D[D.grid].dropna(subset=["fwd","z","vr"])
    D["ex"]=D["fwd"]-D.groupby("coin")["fwd"].transform("mean")
    F=D[D.z<=-1].copy()
    F["vrb"]=pd.cut(F.vr,[0,1,1.5,2,3,np.inf])
    lo,hi=F.ex.quantile([0.02,0.98]); F["exw"]=F.ex.clip(lo,hi)
    def summ(g):
        n=len(g); return pd.Series({"n":n,"mean":g.ex.mean(),"median":g.ex.median(),"pos_share":(g.ex>0).mean(),
            "wins_mean":g.exw.mean(),"t_wins":g.exw.mean()/(g.exw.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    out["falls_h3_by_vr_robust"]=F.groupby("vrb",observed=True).apply(summ)
    pc={}
    for coin,g in F.groupby("coin"):
        rr=stats.spearmanr(g.vr,g.ex); pc[coin]={"rho":rr[0],"p":rr[1],"n":len(g)}
    out["falls_h3_rho_vr_by_coin"]=pd.DataFrame(pc).T
    py={}
    for y,g in F.groupby("yr"):
        rr=stats.spearmanr(g.vr,g.ex); py[y]={"rho":rr[0],"n":len(g)}
    out["falls_h3_rho_vr_by_year"]=pd.DataFrame(py).T
    X=np.column_stack([np.ones(len(F)),np.log(F.vr),F.z]); y=F.exw.values
    beta=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@beta
    cov=np.linalg.inv(X.T@X)*(e@e/(len(y)-3))
    out["reg_wins_h3"]=pd.DataFrame({"beta":beta,"t":beta/np.sqrt(np.diag(cov))},index=["c","logvr","z"])
    return out
