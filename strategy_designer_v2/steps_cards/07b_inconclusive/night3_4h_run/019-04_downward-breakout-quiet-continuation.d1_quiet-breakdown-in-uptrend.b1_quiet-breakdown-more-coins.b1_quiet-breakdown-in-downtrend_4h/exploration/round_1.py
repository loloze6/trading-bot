def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=18
    rows=[]
    for coin, wins in data["bars"].items():
        # coin drift/std on grid
        allr={h:[] for h in (6,12,18,36)}
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
            depth=((plow-b["close"])/b["close"]).values
            ret30=(b["close"]/b["close"].shift(180)-1).values
            raw=b.get("debug_info.components.nr_break_down.last_history_value")
            raw=raw.values if raw is not None else np.full(len(b),np.nan)
            prev=np.r_[0,f[:-1]]
            sig=(f<=-2)&(f<=prev-2)
            cell=np.arange(len(b))//H
            seen=set()
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            for i in np.where(sig)[0]:
                if cell[i] in seen: continue
                seen.add(cell[i])
                r={"coin":coin,"w":w,"year":yr[i],"absf":abs(f[i]),"raw":raw[i],
                   "narrow":narrow[i],"depth":depth[i],"ret30":ret30[i]}
                for h in (6,12,18,36):
                    if i+h<len(c):
                        r[f"u{h}"]=-(c[i+h]/c[i]-1-drift[h]); r[f"s{h}"]=r[f"u{h}"]/sd[h]
                rows.append(r)
    d=pd.DataFrame(rows)
    def summ(g):
        x=g["u18"].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,"str":g["s18"].mean()})
    out={}
    out["absf_dist"]=d["absf"].describe()
    out["absf_eq20_share"]=float((d["absf"]>=19.99).mean())
    hz={}
    for h in (6,12,18,36):
        x=d[f"u{h}"].dropna(); hz[h]=[len(x),x.mean(),x.mean()/(x.std()/np.sqrt(len(x))),d[f"s{h}"].mean()]
    out["horizons"]=pd.DataFrame(hz,index=["n","mean","t","strength"]).T
    for col in ("raw","narrow","depth","ret30"):
        q=pd.qcut(d[col],4,labels=False,duplicates="drop")
        out["by_"+col]=d.groupby(q).apply(summ)
    out["by_year"]=d.groupby("year").apply(summ)
    out["by_coin"]=d.groupby("coin").apply(summ)
    out["spearman_raw_u18"]=float(stats.spearmanr(d["raw"],d["u18"],nan_policy="omit")[0])
    out["spearman_narrow_u18"]=float(stats.spearmanr(d["narrow"],d["u18"],nan_policy="omit")[0])
    return out
