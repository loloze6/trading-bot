def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]; allret=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values.astype(float); v=b["volume"].values.astype(float)
            n=len(c)
            for i in range(0,n-H,H): allret.append((coin,c[i+H]/c[i]-1))
            for t in range(24,n-H):
                if t%H: continue
                j=None
                for k in (1,2,3):
                    jj=t-k
                    if jj-20<0: continue
                    ph=c[jj-20:jj].max()
                    if c[jj]>ph: j=jj; hi=ph; break
                if j is None or c[t]>=hi: continue
                vol=np.std(np.diff(np.log(c[max(1,t-30):t+1])))
                vol_l=np.std(np.diff(np.log(c[max(1,t-120):t+1]))) if t>=60 else np.nan
                rng=c[j-20:j].max()/c[j-20:j].min()-1
                rows.append(dict(coin=coin,w=w,fwd=c[t+H]/c[t]-1,vol=vol,volrel=vol/vol_l if vol_l else np.nan,
                    bo=c[j]/hi-1,bo_v=(c[j]/hi-1)/vol,rng=rng,rng_v=rng/vol,
                    a=b["postRebalance_current_allocation"].iloc[t]))
    ev=pd.DataFrame(rows)
    ar=pd.DataFrame(allret,columns=["coin","r"]); drift=ar.groupby("coin")["r"].mean()
    ev["u"]=-(ev["fwd"]-ev["coin"].map(drift)); ev["tot"]=-ev["fwd"]
    out={}
    def g(d,col,q):
        d=d.dropna(subset=[col]).copy(); d["b"]=pd.qcut(d[col],q,labels=False,duplicates="drop")
        r=d.groupby("b").agg(n=("u","size"),lo=(col,"min"),hi=(col,"max"),u=("u","mean"),tot=("tot","mean"))
        r["t"]=d.groupby("b")["u"].apply(lambda x:x.mean()/(x.std()/np.sqrt(len(x))))
        return r
    def slope(d,col):
        d=d.dropna(subset=[col]); r=stats.linregress(d[col],d["u"])
        sp=stats.spearmanr(d[col],d["u"])
        return pd.Series({"n":len(d),"slope":r.slope,"t":r.slope/r.stderr,"spearman":sp.correlation,"sp_p":sp.pvalue})
    out["slopes"]=pd.DataFrame({c:slope(ev,c) for c in ["vol","volrel","bo","bo_v","rng","rng_v"]}).T
    out["by_vol5"]=g(ev,"vol",5)
    out["by_rng_v"]=g(ev,"rng_v",4)
    out["by_volrel"]=g(ev,"volrel",4)
    lo=ev[ev.vol<=ev.vol.median()]
    out["lowvol_by_coin"]=lo.groupby("coin").agg(n=("u","size"),u=("u","mean"))
    out["lowvol_by_w"]=pd.Series({"windows":lo.w.nunique(),"share_w_pos":(lo.groupby("w")["u"].mean()>0).mean()})
    # book decomposition
    dd=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True); c=b["close"].astype(float)
            r=c.shift(-1)/c-1; a=b["postRebalance_current_allocation"].astype(float)
            vol=np.log(c).diff().rolling(30).std()
            dd.append(pd.DataFrame({"coin":coin,"r":r,"a":a,"g":a*r,"vol":vol}))
    B=pd.concat(dd).dropna()
    md=B.groupby("coin")["r"].transform("mean")
    act=B[B.a!=0].copy()
    out["book_decomp"]=pd.Series({"share_bars_in":(B.a!=0).mean(),"mean_alloc_in":act.a.mean(),
        "gain_per_bar_all":B.g.mean(),"drift_part":(B.a*md).mean(),"timing_part":(B.g-B.a*md).mean()})
    act["vb"]=pd.qcut(act.vol,4,labels=False)
    out["book_in_by_vol"]=act.groupby("vb").agg(n=("g","size"),vol=("vol","mean"),alloc=("a","mean"),g=("g","mean"),r=("r","mean"))
    return out
