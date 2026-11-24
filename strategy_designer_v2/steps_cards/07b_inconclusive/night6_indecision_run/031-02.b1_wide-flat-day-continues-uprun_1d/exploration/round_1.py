def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; drift={}; usual={}
    for coin,ws in data["bars"].items():
        for H in (3,5,10,20):
            allr=[]
            for w,b in ws.items():
                c=b["close"].values
                for i in range(0,len(c)-H,H): allr.append(c[i+H]/c[i]-1)
            drift[(coin,H)]=np.mean(allr); usual[(coin,H)]=np.std(allr)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            o,h,l,c=b["open"],b["high"],b["low"],b["close"]
            rng=h-l; r6=c/c.shift(6)-1
            width=rng/rng.rolling(20).mean()
            flat=1-(c-o).abs()/rng.replace(0,np.nan)
            year=pd.to_datetime(b["timestamp"]).dt.year
            for i in range(len(b)):
                if pd.isna(width[i]) or pd.isna(r6[i]): continue
                rec=dict(coin=coin,w=w,i=i,year=year[i],r6=r6[i],width=width[i],flat=flat[i],day=str(pd.to_datetime(b["timestamp"][i]).date()),fc=b["forecast"][i])
                for H in (3,5,10,20):
                    rec[f"f{H}"]=c[i+H]/c[i]-1-drift[(coin,H)] if i+H<len(b) else np.nan
                rec["cell"]=i//10
                rows.append(rec)
    d=pd.DataFrame(rows)
    def summ(sub,col="f10",sign=1):
        x=sub.dropna(subset=[col]).copy(); x["v"]=sign*x[col]
        x=x.sort_values("i").groupby(["coin","w","cell"]).head(1)
        pd_=x.groupby("day")["v"].sum(); n=len(pd_)
        t=pd_.mean()/ (pd_.std()/np.sqrt(n)) if n>2 else np.nan
        return pd.Series(dict(n=len(x),days=n,mean=x["v"].mean(),hit=(x["v"]>0).mean(),t=t))
    wide=(d.width>=1.5)&(d.flat>=0.9)
    up=d.r6>0; dn=d.r6<0
    out={}
    out["setups"]=pd.DataFrame({k:summ(s) for k,s in {"wideflat_up":d[wide&up],"wideflat_dn":d[wide&dn],"narrowflat_up":d[(d.width<0.8)&(d.flat>=0.9)&up],"all_up":d[up],"wideflat_all":d[wide]}.items()}).T
    out["horizons_wideflat_up"]=pd.DataFrame({H:summ(d[wide&up],f"f{H}") for H in (3,5,10,20)}).T
    out["horizons_wideflat_dn"]=pd.DataFrame({H:summ(d[wide&dn],f"f{H}") for H in (3,5,10,20)}).T
    s=d[wide&up]
    out["by_coin"]=pd.DataFrame({k:summ(g) for k,g in s.groupby("coin")}).T
    out["by_year"]=pd.DataFrame({k:summ(g) for k,g in s.groupby("year")}).T
    s=s.copy(); s["r6q"]=pd.qcut(s.r6,3,labels=["low","mid","high"]); s["wq"]=pd.qcut(s.width,3,labels=["w_low","w_mid","w_high"])
    out["by_rise_tercile"]=pd.DataFrame({k:summ(g) for k,g in s.groupby("r6q")}).T
    out["by_width_tercile"]=pd.DataFrame({k:summ(g) for k,g in s.groupby("wq")}).T
    # looser width threshold
    out["loose_width_up"]=pd.DataFrame({th:summ(d[(d.width>=th)&(d.flat>=0.8)&up]) for th in (1.0,1.2,1.5,2.0)}).T
    return out
