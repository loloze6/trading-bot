def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book per coin
    rows=[]
    for c in data["days"]:
        br=[];cr=[]
        for w,d in data["days"][c].items():
            br.append(d["book_return"].dropna()); cr.append(d["coin_return"].dropna())
        b=pd.concat(br); h=pd.concat(cr)
        tr=pd.concat([t for t in data["trades"][c].values()]) if len(data["trades"][c]) else pd.DataFrame()
        rows.append(dict(coin=c, book_mean=b.mean(), book_sh=b.mean()/b.std()*np.sqrt(365), hold_sh=h.mean()/h.std()*np.sqrt(365),
                         n_trades=len(tr), gross_pl_mean=tr["profit_loss_percent"].mean() if len(tr) else np.nan,
                         net_pl_mean=tr["net_profit_loss_percent"].mean() if len(tr) else np.nan,
                         dur_h=tr["duration_minutes"].median()/60 if len(tr) else np.nan))
    out["per_coin_book"]=pd.DataFrame(rows)
    # recompute signals from prices: z of 24h run, also 72h and 168h run; forward returns at 24,72,168
    recs=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            cl=b["close"].values.astype(float); n=len(cl)
            r1=np.diff(np.log(cl),prepend=np.nan)
            s=pd.Series(r1)
            vol=s.rolling(168,min_periods=84).std()
            volL=s.rolling(720,min_periods=360).std()
            f=b["forecast"].values
            for L in (24,72,168):
                pass
            idx=np.arange(0,n,24)
            for i in idx:
                if i<168: continue
                rec=dict(coin=c,w=w,fc=f[i],vol=vol.iloc[i],vrat=vol.iloc[i]/volL.iloc[i] if volL.iloc[i]>0 else np.nan,hour=0)
                for L in (24,72,168):
                    rec[f"z{L}"]=(cl[i]/cl[i-L]-1)/(vol.iloc[i]*np.sqrt(L)) if i-L>=0 else np.nan
                for H in (24,72,168):
                    rec[f"f{H}"]=cl[i+H]/cl[i]-1 if i+H<n else np.nan
                recs.append(rec)
    df=pd.DataFrame(recs)
    for H in (24,72,168):
        df[f"f{H}"]=df[f"f{H}"]-df.groupby("coin")[f"f{H}"].transform("mean")
    def tab(key,q):
        g=df.dropna(subset=[key]).copy()
        g["b"]=pd.qcut(g[key],q,labels=False,duplicates="drop")
        res=[]
        for bb,x in g.groupby("b"):
            row=dict(bucket=bb,lo=x[key].min(),hi=x[key].max(),n=len(x))
            for H in (24,72,168):
                v=x[f"f{H}"].dropna(); row[f"m{H}"]=v.mean(); row[f"t{H}"]=v.mean()/v.std()*np.sqrt(len(v))
            res.append(row)
        return pd.DataFrame(res)
    out["by_z24"]=tab("z24",10)
    out["by_z72"]=tab("z72",10)
    out["by_z168"]=tab("z168",10)
    # extreme 24h run reversal by vol regime
    g=df.dropna(subset=["z24","vrat"]).copy()
    g["s"]=-np.sign(g["z24"])*g["f24"]; g["s72"]=-np.sign(g["z24"])*g["f72"]
    g["ext"]=g["z24"].abs()>g["z24"].abs().quantile(0.8)
    g["vb"]=pd.qcut(g["vrat"],4,labels=False)
    r=g[g.ext].groupby("vb").agg(n=("s","size"),m24=("s","mean"),m72=("s72","mean"),vr=("vrat","mean"))
    out["ext_by_volratio"]=r
    out["ext_by_coin"]=g[g.ext].groupby("coin").agg(n=("s","size"),m24=("s","mean"),m72=("s72","mean"))
    # usual move per coin
    out["usual"]=df.groupby("coin")[["f24","f72","f168"]].std()
    return out
