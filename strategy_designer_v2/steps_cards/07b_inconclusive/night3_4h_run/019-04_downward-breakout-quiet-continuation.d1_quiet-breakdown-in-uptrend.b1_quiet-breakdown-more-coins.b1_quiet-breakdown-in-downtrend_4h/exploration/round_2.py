def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=18
    rows=[]
    for coin, wins in data["bars"].items():
        allr={h:[] for h in (18,36)}
        for w,b in wins.items():
            c=b["close"].values
            for h in allr:
                idx=np.arange(0,len(c)-h,h)
                allr[h]+=list(c[idx+h]/c[idx]-1)
        drift={h:np.nanmean(allr[h]) for h in allr}; sd={h:np.nanstd(allr[h]) for h in allr}
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values
            hi=b["high"]; lo=b["low"]
            plow=lo.shift(1).rolling(12).min()
            rng12=(hi.shift(1).rolling(12).max()-plow)/b["close"].shift(1)
            mbr=((hi-lo)/b["close"]).rolling(180).mean()
            narrow=(mbr/rng12).values
            ret30=(b["close"]/b["close"].shift(180)-1).values
            prev=np.r_[0,f[:-1]]
            sig=(f<=-2)&(f<=prev-2)
            cell=np.arange(len(b))//H
            seen=set()
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            for i in np.where(sig)[0]:
                if cell[i] in seen: continue
                seen.add(cell[i])
                r={"coin":coin,"year":yr[i],"narrow":narrow[i],"ret30z":ret30[i]/(sd[18]*np.sqrt(10)),"ret30":ret30[i]}
                for h in (18,36):
                    if i+h<len(c):
                        r[f"u{h}"]=-(c[i+h]/c[i]-1-drift[h]); r[f"s{h}"]=r[f"u{h}"]/sd[h]
                        r[f"tot{h}"]=-(c[i+h]/c[i]-1)
                rows.append(r)
    d=pd.DataFrame(rows).dropna(subset=["narrow","u18"])
    def summ(g):
        x=g["u18"]
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))),"str":g["s18"].mean(),"tot":g["tot18"].mean()})
    out={}
    d["nq"]=pd.qcut(d["narrow"],4,labels=False)
    out["narrow_cuts"]=d.groupby("nq")["narrow"].agg(["min","median","max"])
    d["rq"]=pd.qcut(d["ret30"],2,labels=["deep","mild"])
    out["nq_x_ret"]=d.groupby(["nq","rq"]).apply(summ)
    top=d[d.nq==3]
    out["top_by_year"]=top.groupby("year").apply(summ)
    out["top_coins_pos_share"]=float((top.groupby("coin")["u18"].mean()>0).mean())
    out["top_ncoins"]=int(top["coin"].nunique())
    out["nq_u36"]=d.dropna(subset=["u36"]).groupby("nq").apply(lambda g: pd.Series({"n":len(g),"mean":g["u36"].mean(),"t":g["u36"].mean()/(g["u36"].std()/np.sqrt(len(g))),"tot":g["tot36"].mean()}))
    d["n10"]=pd.qcut(d["narrow"],10,labels=False)
    out["n10"]=d.groupby("n10").apply(summ)
    out["spearman_narrow_mild"]=float(stats.spearmanr(d.loc[d.rq=="mild","narrow"],d.loc[d.rq=="mild","u18"])[0])
    return out
