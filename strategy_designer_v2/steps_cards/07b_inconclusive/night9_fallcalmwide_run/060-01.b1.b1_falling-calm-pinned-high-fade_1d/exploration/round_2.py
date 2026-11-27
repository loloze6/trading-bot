def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        allr=[(b["close"].shift(-1)/b["close"]-1).dropna() for b in ws.values()]
        drift[coin]=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30).std()
            df=pd.DataFrame(dict(coin=coin,w=w,regime=b["regime"],
                width=((b["high"]-b["low"])/c)/sd,
                loc=(c-b["low"])/(b["high"]-b["low"]),
                day=pd.to_datetime(b["timestamp"]).dt.strftime("%Y-%m-%d"),
                f1=c.shift(-1)/c-1, f2=c.shift(-2)/c-1, f3=c.shift(-3)/c-1))
            rows.append(df)
    df=pd.concat(rows,ignore_index=True)
    df["dr"]=df.coin.map(drift)
    for h in (1,2,3):
        df[f"u{h}"]=-(df[f"f{h}"]-h*df["dr"])
    df["prof"]=np.where(df.regime=="chop","out","fallcalm")
    def ct(g,col="u1"):
        g=g.dropna(subset=[col])
        if len(g)<3: return pd.Series(dict(n=len(g),days=g.day.nunique(),mean=g[col].mean(),t=np.nan))
        dev=g[col]-g[col].mean()
        s=dev.groupby(g.day).sum()
        D=len(s); se=np.sqrt((s**2).sum()*D/(D-1))/len(g)
        return pd.Series(dict(n=len(g),days=D,mean=g[col].mean(),t=g[col].mean()/se))
    out={}
    d=df.dropna(subset=["width","loc"])
    d=d.assign(wb=pd.cut(d.width,[0,1,1.5,2,2.5,3,100]),lb=pd.cut(d["loc"],[-0.01,0.5,0.7,0.8,0.9,1.01]))
    fc=d[d.prof=="fallcalm"]
    out["fc_width_hiLoc"]=fc[fc["loc"]>=0.9].groupby("wb").apply(ct)
    out["fc_loc_wide"]=fc[fc.width>=2].groupby("lb").apply(ct)
    out["fc_loc_mid_wide15"]=fc[fc.width>=1.5].groupby("lb").apply(ct)
    out["out_width_hiLoc"]=d[(d.prof=="out")&(d["loc"]>=0.9)].groupby("wb").apply(ct)
    out["fc_all_loc"]=fc.groupby("lb").apply(ct)
    s=fc[(fc.width>=2)&(fc["loc"]>=0.9)]
    out["fc_sit_horizons"]=pd.DataFrame({h:ct(s,f"u{h}") for h in ("u1","u2","u3")})
    s2=fc[(fc.width>=1.5)&(fc["loc"]>=0.8)]
    out["fc_loose_horizons"]=pd.DataFrame({h:ct(s2,f"u{h}") for h in ("u1","u2","u3")})
    out["fc_loose_by_coin"]=s2.groupby("coin").apply(ct)
    out["fc_loose_by_window"]=s2.groupby("w").apply(ct)
    out["fc_share_bars"]=pd.Series(dict(fc=(d.prof=="fallcalm").mean(),n_fc=(d.prof=="fallcalm").sum()))
    return out
