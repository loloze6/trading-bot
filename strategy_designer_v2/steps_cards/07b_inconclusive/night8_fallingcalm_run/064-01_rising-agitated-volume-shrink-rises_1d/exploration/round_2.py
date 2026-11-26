def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    def getcomp(x,key):
        try:
            if isinstance(x,str):
                import json; x=json.loads(x)
            return x["vol_dryup"][key]
        except Exception:
            return np.nan
    rows=[]
    for coin,ws in data["bars"].items():
        mus={}
        for h in (5,10,20):
            allr=[]
            for w,b in ws.items():
                c=b["close"].values
                for i in range(0,len(c)-h,h): allr.append(c[i+h]/c[i]-1)
            mus[h]=np.mean(allr)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; v=b["volume"]
            vr=np.log(v.rolling(30).mean()/v.shift(30).rolling(30).mean()).values
            raw=b["debug_info.components"].apply(lambda x:getcomp(x,"last_history_value")).values if "debug_info.components" in b else np.full(len(b),np.nan)
            for h in (5,10,20):
                for i in range(0,len(b)-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,day=str(b["timestamp"].iloc[i])[:10],
                        year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                        inprof=b["regime"].iloc[i]=="unknown",fc=b["forecast"].iloc[i],
                        vr=vr[i],raw=raw[i],ex=c[i+h]/c[i]-1-mus[h]))
    d=pd.DataFrame(rows)
    out["raw_component_nonnull_share_inprof"]=float(d[d.inprof].raw.notna().mean())
    def sl(df,x):
        df=df[[x,"ex"]].dropna()
        if len(df)<10 or df[x].std()==0: return pd.Series([len(df),np.nan,np.nan],index=["n","slope","t"])
        s=stats.linregress(df[x],df["ex"]); return pd.Series([len(df),s.slope,s.slope/s.stderr],index=["n","slope","t"])
    res={}
    for h in (5,10,20):
        p=d[(d.h==h)&d.inprof].copy(); p["nraw"]=-p.raw; p["nvr"]=-p.vr
        res[f"h{h}_fc"]=sl(p,"fc"); res[f"h{h}_negraw"]=sl(p,"nraw"); res[f"h{h}_negvr"]=sl(p,"nvr")
        pos=p[p.fc>0].dropna(subset=["ex"])
        g=pos.groupby("day").ex.sum(); nd=len(g)
        res[f"h{h}_fcpos_mean"]=pd.Series([len(pos),pos.ex.mean(), pos.ex.sum()/len(pos)/(g.std(ddof=1)*np.sqrt(nd)/len(pos)) if nd>1 else np.nan],index=["n","slope","t"])
    out["by_horizon"]=pd.DataFrame(res).T
    for h in (10,20):
        p=d[(d.h==h)&d.inprof].copy(); p["nraw"]=-p.raw
        out[f"h{h}_fc_by_coin"]=pd.DataFrame({c:sl(g,"fc") for c,g in p.groupby("coin")}).T
        out[f"h{h}_fc_by_year"]=pd.DataFrame({c:sl(g,"fc") for c,g in p.groupby("year")}).T
        p["q"]=pd.qcut(p.raw.rank(method="first"),4,labels=False) if p.raw.notna().sum()>20 else np.nan
        out[f"h{h}_by_raw_quartile"]=p.groupby("q").agg(n=("ex","size"),raw=("raw","mean"),ex=("ex","mean"),med=("ex","median"))
        # trimmed: drop top/bottom 2% ex
        lo,hi=p.ex.quantile([.02,.98]); out[f"h{h}_fc_trimmed"]=sl(p[(p.ex>lo)&(p.ex<hi)],"fc")
    return out
