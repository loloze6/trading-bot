def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r1=c.pct_change()
            mabs=r1.abs().rolling(20,min_periods=10).mean()
            rng=(h-l).replace(0,np.nan)
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),"ts":ts.dt.floor("D"),
                "cl":(c-l)/rng,"g":r1/mabs,"rngs":((h-l)/c)/mabs,
                "tr60":c/c.shift(60)-1,"inprof":(b["regime"]!="chop").astype(int),
                "yr":ts.dt.year,
                "vol":b["volume"].astype(float)/b["volume"].astype(float).rolling(20,min_periods=10).mean()})
            for H in (2,5):
                df[f"f{H}"]=c.shift(-H)/c-1
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    for H in (2,5):
        drift=A.groupby("coin")[f"f{H}"].transform(lambda s: s.iloc[::H].mean())
        A[f"u{H}"]=A[f"f{H}"]-drift
    def ct(s,H):
        d=s.groupby("ts")[f"u{H}"].sum(); n=len(s); D=len(d)
        m=s[f"u{H}"].mean()
        se=np.sqrt(((d-s.groupby("ts").size()*m)**2).sum()*D/(D-1))/n if D>1 else np.nan
        return pd.Series({"n":n,"days":D,"mean":m,"t_day":m/se if se else np.nan})
    out={}
    for H in (2,5):
        G=A[A.pos%H==0].dropna(subset=[f"u{H}","rngs","g"]).copy()
        G["rq"]=pd.qcut(G.rngs.rank(method="first"),5,labels=False)
        G["dir"]=np.where(G.g>0,"up","down")
        out[f"u{H}_rngs_x_dir"]=G.groupby(["rq","dir"]).apply(lambda s: ct(s,H)).round(4)
        G["clb"]=pd.cut(G.cl,[-.01,.33,.67,1.01],labels=["low","mid","high"])
        W=G[G.rq==4]
        out[f"u{H}_wide_x_cl"]=W.groupby("clb").apply(lambda s: ct(s,H)).round(4)
        out[f"u{H}_wide_by_year"]=W.groupby("yr").apply(lambda s: ct(s,H)).round(4)
        out[f"u{H}_wide_by_coin"]=W.groupby("coin").apply(lambda s: ct(s,H)).round(4)
        G["tc"]=pd.cut(G.tr60,[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
        out[f"u{H}_wide_x_trend"]=G[G.rq==4].groupby(["tc","dir"]).apply(lambda s: ct(s,H)).round(4)
        G["vq"]=pd.qcut(G.vol.rank(method="first"),3,labels=False)
        out[f"u{H}_rq_x_volq"]=G[G.rq>=3].groupby(["rq","vq"]).apply(lambda s: ct(s,H)).round(4)
    return out
