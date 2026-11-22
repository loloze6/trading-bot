def explore(data):
    import numpy as np, pandas as pd
    rows=[]; days=[]; hold=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(720,min_periods=240).std()
            vr=b["volume"]/b["volume"].rolling(720,min_periods=240).mean()
            z=r/sd
            r24=c/c.shift(24)-1
            r24z=r24/(sd*np.sqrt(24))
            fw={h:c.shift(-h)/c-1 for h in [1,2,6,24]}
            idx=np.arange(0,len(b),6)
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"vr":vr,"r24z":r24z,"fc":b["forecast"],
                            "alloc":b["postRebalance_current_allocation"],**{f"f{h}":fw[h] for h in fw}}).iloc[idx]
            rows.append(d)
            a=b["postRebalance_current_allocation"]; fc=b["forecast"]
            hold.append(pd.DataFrame({"coin":coin,"alloc_when_fc0":a[fc<=0].mean(),"alloc_when_fcpos":a[fc>0].mean(),
                                      "share_long_fc0":(a[fc<=0]>0).mean(),"n_fc0":(fc<=0).sum()},index=[0]))
        for w,dd in data["days"][coin].items():
            days.append(dd.assign(coin=coin,w=w))
    d=pd.concat(rows).dropna(subset=["z","vr","f24"])
    for h in [1,2,6,24]:
        d[f"u{h}"]=d[f"f{h}"]-d.groupby("coin")[f"f{h}"].transform("mean")
    def agg(g):
        o={"n":len(g)}
        for h in [1,2,6,24]:
            m=g[f"u{h}"].mean(); o[f"u{h}_bp"]=m*1e4; o[f"t{h}"]=m/(g[f"u{h}"].std()/np.sqrt(len(g)))
        return pd.Series(o)
    out={}
    d["sz"]=d.z*d.vr
    d["szbin"]=pd.cut(d.sz,[-1e9,-10,-3,-1,1,3,10,1e9])
    out["by_sz_horizons"]=d.groupby("szbin").apply(agg)
    big=d[d.z>2].copy()
    big["trend"]=pd.cut(big.r24z,[-99,0,2,99])
    out["up_surge_by_prior24h_trend"]=big.groupby("trend").apply(agg)
    bd=d[d.z<-2].copy(); bd["trend"]=pd.cut(bd.r24z,[-99,-2,0,99])
    out["down_surge_by_prior24h_trend"]=bd.groupby("trend").apply(agg)
    out["holding_when_flat_forecast"]=pd.concat(hold).groupby("coin").agg({"alloc_when_fc0":"mean","alloc_when_fcpos":"mean","share_long_fc0":"mean"})
    D=pd.concat(days).dropna(subset=["book_return","coin_return"])
    pooled=D.groupby(["w","day"]).agg(b=("book_return","mean"),c=("coin_return","mean")).reset_index()
    pooled["bin"]=pd.qcut(pooled.c,5)
    out["book_vs_coin_day_quintile"]=pooled.groupby("bin").agg(n=("b","size"),book_bp=("b",lambda x:x.mean()*1e4),coin_bp=("c",lambda x:x.mean()*1e4))
    out["book_coin_corr_beta"]=pd.Series({"corr":pooled.b.corr(pooled.c),"beta":np.polyfit(pooled.c,pooled.b,1)[0],"book_mean_bp":pooled.b.mean()*1e4,"coin_mean_bp":pooled.c.mean()*1e4})
    return out
