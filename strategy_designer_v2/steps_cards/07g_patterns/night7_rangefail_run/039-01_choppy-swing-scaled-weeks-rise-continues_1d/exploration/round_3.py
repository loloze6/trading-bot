def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    for H in [1,3,5,10]:
        drift={}
        for coin,wins in data["bars"].items():
            allr=[]
            for w,b in wins.items():
                c=b["close"].values
                for i in range(0,len(c)-H,H): allr.append(c[i+H]/c[i]-1)
            drift[coin]=np.mean(allr)
        rows=[]
        for coin,wins in data["bars"].items():
            for w,b in wins.items():
                b=b.reset_index(drop=True)
                c=b["close"]; r=c.pct_change()
                sd20=r.rolling(20).std()
                r1z=r/sd20.shift(1)
                r3z=np.log(c/c.shift(3))/(sd20.shift(3)*np.sqrt(3))
                z20=np.log(c/c.shift(20))/(sd20*np.sqrt(20))
                ts=pd.to_datetime(b["timestamp"])
                fwd=c.shift(-H)/c-1
                for i in range(0,len(b)-H,H):
                    rows.append(dict(coin=coin,day=ts.iloc[i].normalize(),yr=ts.iloc[i].year,r1z=r1z[i],r3z=r3z[i],
                        z20=z20[i],ex=fwd[i]-drift[coin],reg=b["regime"].iloc[i]))
        df=pd.DataFrame(rows).dropna(subset=["r1z","ex"])
        ch=df[df.reg=="unknown"].copy()
        def ps(d,col):
            d=d.dropna(subset=[col,"ex"]); p=d.groupby("day")[[col,"ex"]].mean()
            if len(p)<15: return "n/a"
            s=stats.linregress(p[col],p["ex"]); return f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} days {len(p)}"
        res={"r1z choppy":ps(ch,"r1z"),"r3z choppy":ps(ch,"r3z"),"r1z nonchoppy":ps(df[df.reg!="unknown"],"r1z")}
        if H==5:
            w=ch.copy(); w["r1z"]=w.r1z.clip(-3,3); w["ex"]=w.ex.clip(w.ex.quantile(0.02),w.ex.quantile(0.98))
            res["r1z choppy winsorized"]=ps(w,"r1z")
            res["r1z choppy 2018-19"]=ps(ch[ch.yr<=2019],"r1z"); res["r1z choppy 2020-21"]=ps(ch[ch.yr>=2020],"r1z")
            res["r1z choppy, z20 in model"]=""
            d=ch.dropna(subset=["z20"]); p=d.groupby("day")[["r1z","z20","ex"]].mean()
            X=np.column_stack([np.ones(len(p)),p.r1z,p.z20]); bta,_,_,_=np.linalg.lstsq(X,p.ex,rcond=None)
            e=p.ex-X@bta; s2=(e**2).sum()/(len(p)-3); cov=s2*np.linalg.inv(X.T@X)
            res["r1z choppy, z20 in model"]=f"r1z t {bta[1]/np.sqrt(cov[1,1]):.2f} z20 t {bta[2]/np.sqrt(cov[2,2]):.2f}"
            ch["b"]=pd.qcut(ch.r1z,5,labels=False); q={}
            for bq,m in ch.groupby("b"):
                x=m.ex; dev=pd.Series((x-x.mean()).values,index=m.day.values).groupby(level=0).sum()
                q[bq]=f"r1z {m.r1z.mean():.2f} ex {x.mean():.4f} t {x.mean()/(np.sqrt((dev**2).sum())/len(x)):.2f} n {len(x)}"
            out["r1z choppy quint H5"]=pd.Series(q)
            cc={}
            for coin,m in ch.groupby("coin"):
                if len(m)>=15:
                    s=stats.linregress(m.r1z,m.ex); cc[coin]=f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(m)}"
            out["r1z choppy by coin H5"]=pd.Series(cc)
        out[f"H{H}"]=pd.Series(res)
    return out
