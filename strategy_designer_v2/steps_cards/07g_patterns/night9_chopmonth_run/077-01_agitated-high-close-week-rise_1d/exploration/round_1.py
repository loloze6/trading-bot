def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].values; h=b["high"].values; l=b["low"].values; o=b["open"].values
            rng=h-l
            clv=np.where(rng>0,(c-l)/np.where(rng>0,rng,1),np.nan)
            r1=pd.Series(c).pct_change().values
            n=len(b)
            vol20=pd.Series(r1).rolling(20).std().values
            for i in range(n):
                d=dict(coin=coin,w=w,pos=i,clv=clv[i],ret1=r1[i],agit=(b["regime"].iloc[i]!="chop"),
                       wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday(),
                       rngrel=rng[i]/c[i]/vol20[i] if vol20[i]==vol20[i] and vol20[i]>0 else np.nan,
                       ret5=c[i]/c[i-5]-1 if i>=5 else np.nan,
                       ret20=c[i]/c[i-20]-1 if i>=20 else np.nan)
                for hh in (1,3,7):
                    d[f"f{hh}"]=c[i+hh]/c[i]-1 if i+hh<n else np.nan
                    d[f"g{hh}"]=(i%hh==0)
                rows.append(d)
    df=pd.DataFrame(rows)
    for hh in (1,3,7):
        g=df[df[f"g{hh}"]]
        df[f"x{hh}"]=df[f"f{hh}"]-df.coin.map(g.groupby("coin")[f"f{hh}"].mean())
    out={}
    def tab(sub,key,hh,q=5):
        s=sub[sub[f"g{hh}"]].dropna(subset=[key,f"x{hh}"]).copy()
        s["b"]=pd.qcut(s[key],q,labels=False,duplicates="drop")
        a=s.groupby("b")[f"x{hh}"].agg(["mean","count","std"])
        a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
        return a.drop(columns="std").round(4)
    for ag in (True,False):
        for hh in (1,3,7):
            out[f"clv_q x{hh} agit={ag}"]=tab(df[df.agit==ag],"clv",hh)
    for hh in (1,3,7):
        out[f"ret1_q x{hh} all"]=tab(df,"ret1",hh)
        out[f"ret5_q x{hh} all"]=tab(df,"ret5",hh)
        out[f"ret20_q x{hh} all"]=tab(df,"ret20",hh)
        out[f"rngrel_q x{hh} all"]=tab(df,"rngrel",hh)
    s=df[df.g1].dropna(subset=["x1"])
    a=s.groupby("wd")["x1"].agg(["mean","count","std"]);a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["weekday x1"]=a.round(4)
    s=df[df.g7].dropna(subset=["x7"])
    out["agit vs calm x7"]=s.groupby("agit")["x7"].agg(["mean","count"]).round(4)
    out["by window x7 clv>0.5 agit minus clv<0.5"]=s[s.agit].groupby("w").apply(lambda z: z[z.clv>0.5].x7.mean()-z[z.clv<=0.5].x7.mean()).round(4)
    return out
