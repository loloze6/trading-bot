def explore(data):
    import numpy as np, pandas as pd
    rows=[]; drift={}
    for coin,ws in data["bars"].items():
        for H in (3,5,10):
            allr=[]
            for w,b in ws.items():
                c=b["close"].values
                for i in range(0,len(c)-H,H): allr.append(c[i+H]/c[i]-1)
            drift[(coin,H)]=np.mean(allr)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            o,h,l,c=b["open"],b["high"],b["low"],b["close"]
            rng=h-l; r6=c/c.shift(6)-1
            width=rng/rng.rolling(20).mean()
            flat=1-(c-o).abs()/rng.replace(0,np.nan)
            year=pd.to_datetime(b["timestamp"]).dt.year
            for i in range(len(b)):
                if pd.isna(width[i]) or pd.isna(r6[i]): continue
                rec=dict(coin=coin,w=w,i=i,year=year[i],r6=r6[i],width=width[i],flat=flat[i],day=str(pd.to_datetime(b["timestamp"][i]).date()))
                for H in (3,5,10):
                    rec[f"f{H}"]=c[i+H]/c[i]-1-drift[(coin,H)] if i+H<len(b) else np.nan
                rows.append(rec)
    d=pd.DataFrame(rows)
    def summ(sub,col="f10",H=10):
        x=sub.dropna(subset=[col]).copy(); x["v"]=x[col]; x["cell"]=x["i"]//H
        x=x.sort_values("i").groupby(["coin","w","cell"]).head(1)
        pdd=x.groupby("day")["v"].sum(); n=len(pdd)
        t=pdd.mean()/(pdd.std()/np.sqrt(n)) if n>2 else np.nan
        return pd.Series(dict(n=len(x),days=n,mean=x["v"].mean(),hit=(x["v"]>0).mean(),t=t))
    out={}
    up=d.r6>0
    L=d[(d.width>=1.0)&(d.flat>=0.8)&up].copy()
    out["loose_by_year"]=pd.DataFrame({k:summ(g) for k,g in L.groupby("year")}).T
    out["loose_by_coin"]=pd.DataFrame({k:summ(g) for k,g in L.groupby("coin")}).T
    L["r6q"]=pd.qcut(L.r6,3,labels=["low","mid","high"])
    L["wq"]=pd.qcut(L.width,3,labels=["w_low","w_mid","w_high"])
    out["loose_by_rise"]=pd.DataFrame({k:summ(g) for k,g in L.groupby("r6q")}).T
    out["loose_by_width"]=pd.DataFrame({k:summ(g) for k,g in L.groupby("wq")}).T
    out["loose_horizons"]=pd.DataFrame({H:summ(L,f"f{H}",H) for H in (3,5,10)}).T
    # same width, not flat (control)
    out["wide_notflat_up"]=summ(d[(d.width>=1.0)&(d.flat<0.5)&up]).to_frame().T
    out["wide_flat_dn"]=summ(d[(d.width>=1.0)&(d.flat>=0.8)&(d.r6<0)]).to_frame().T
    return out
