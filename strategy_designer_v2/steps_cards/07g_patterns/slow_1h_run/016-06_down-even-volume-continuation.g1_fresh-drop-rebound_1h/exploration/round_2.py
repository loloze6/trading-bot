import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    g=[]
    for c in bars:
        for wi,(w,df) in enumerate(bars[c].items()):
            cl=df["close"].values; v=df["volume"].values; n=len(cl)
            hr=np.r_[np.nan, cl[1:]/cl[:-1]-1]
            for i in range(0,n,72):
                if i<72 or i+72>=n: continue
                h=hr[i-71:i+1]; ab=np.abs(h)
                r72=cl[i]/cl[i-72]-1; r24=cl[i]/cl[i-24]-1
                eff=abs(r72)/np.nansum(ab)
                h24=hr[i-23:i+1]; eff24=abs(r24)/np.nansum(np.abs(h24))
                vv=v[i-71:i+1]; vconc=np.nanmax(vv)/np.nansum(vv) if np.nansum(vv)>0 else np.nan
                g.append((c,w,int(w[1:]),r72,r24,eff,eff24,vconc,cl[i+72]/cl[i]-1,cl[i+24]/cl[i]-1))
    G=pd.DataFrame(g,columns=["coin","w","wn","r72","r24","eff","eff24","vconc","fwd","fwd24"])
    G["ex"]=G["fwd"]-G.groupby("coin")["fwd"].transform("mean")
    G["ex24"]=G["fwd24"]-G.groupby("coin")["fwd24"].transform("mean")
    G["sgn"]=np.sign(G["r72"]); G["cont"]=G["ex"]*G["sgn"]; G["cont24"]=G["ex24"]*G["sgn"]
    G["effq"]=G.groupby("coin")["eff"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    # eff continuation by direction
    def tt(s): return pd.Series({"mean":s.mean(),"n":s.count(),"t":s.mean()/(s.std()/np.sqrt(s.count()))})
    out["cont by effq, up moves"]=G[G.r72>0].groupby("effq")["cont"].apply(tt).unstack()
    out["cont by effq, down moves"]=G[G.r72<0].groupby("effq")["cont"].apply(tt).unstack()
    out["cont24 by effq"]=G.groupby("effq")["cont24"].apply(tt).unstack()
    out["top eff cont by coin"]=G[G.effq==4].groupby("coin")["cont"].apply(tt).unstack()
    G["half"]=np.where(G.wn<=12,"w1-12","w13-24")
    out["top eff cont by half"]=G[G.effq==4].groupby("half")["cont"].apply(tt).unstack()
    # multivariate: cont on eff, |r72|, vconc (within-coin ranks)
    for col in ["eff","vconc","r72","r24"]:
        G[col+"_rk"]=G.groupby("coin")[col].rank(pct=True)
    G["absr_rk"]=G.groupby("coin")["r72"].transform(lambda x: x.abs().rank(pct=True))
    X=np.c_[np.ones(len(G)),G["eff_rk"],G["absr_rk"],G["vconc_rk"]]
    m=G[["eff_rk","absr_rk","vconc_rk","cont"]].notna().all(1).values
    X=X[m]; y=G["cont"].values[m]
    b,res,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@b
    cov=np.linalg.inv(X.T@X)*(e@e/(len(y)-X.shape[1]))
    out["cont ~ eff,|r72|,vconc ranks t"]=pd.Series(b/np.sqrt(np.diag(cov)),index=["c","eff","absr72","vconc"])
    # signed graded: ex on sgn*eff_rk
    G["seff"]=G["sgn"]*G["eff_rk"]
    sl=stats.linregress(G["seff"],G["ex"]); out["ex ~ sign*eff_rank slope t"]=float(sl.slope/sl.stderr)
    # down regime: deepest r24 quintile; graded within? and by coin/half
    D=G[G.r72<0].copy()
    D["q"]=D.groupby("coin")["r24"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    out["down q0 rebound by coin"]=D[D.q==0].groupby("coin")["ex"].apply(tt).unstack()
    out["down q0 rebound by half"]=D[D.q==0].groupby(G.loc[D.index,"half"][D.q==0])["ex"].apply(tt).unstack()
    D["d"]=pd.qcut(D.groupby("coin")["r24"].rank(pct=True),10,labels=False)
    out["down r24 decile ex"]=D.groupby("d")["ex"].apply(tt).unstack()
    out["down q0 ex24"]=tt(D[D.q==0]["ex24"])
    return out
