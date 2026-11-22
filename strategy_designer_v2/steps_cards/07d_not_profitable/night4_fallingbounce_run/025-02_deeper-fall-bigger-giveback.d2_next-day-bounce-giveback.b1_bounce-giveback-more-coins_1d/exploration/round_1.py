def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=pd.concat([w["close"].pct_change() for w in ws.values()])
        mu=allr.mean()
        for wn,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            d=pd.DataFrame({"coin":coin,"win":wn,"year":pd.to_datetime(b["timestamp"]).dt.year,
                "f":b["forecast"],"z":r/r.rolling(20).std(),"r90":c/c.shift(90)-1,
                "r30":c/c.shift(30)-1,
                "clv":(c-b["low"])/(b["high"]-b["low"]),
                "vrel":b["volume"]/b["volume"].rolling(20).mean(),
                "alloc":b["postRebalance_current_allocation"],"mu":mu})
            for h in [1,2,3,5]:
                d[f"u{h}"]=-(c.shift(-h)/c-1-h*mu)
            d["tot1"]=-(c.shift(-1)/c-1)
            d["gain"]=d["alloc"]*(c.shift(-1)/c-1)
            d["fee"]=(b["postRebalance_total_value"]-b["total_portfolio_value"])/b["total_portfolio_value"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    K=D[D.f<=-2].dropna(subset=["u1"])
    def g(x):
        return pd.Series({"n":len(x),"u1":x.u1.mean(),"t1":x.u1.mean()/x.u1.std()*np.sqrt(len(x)),
            "tot1":x.tot1.mean(),"u3":x.u3.mean(),"u5":x.u5.mean()})
    out={}
    out["by_f"]=K.groupby(pd.cut(K.f,[-20.1,-15,-10,-6,-4,-2]),observed=True).apply(g)
    out["by_z"]=K.groupby(pd.qcut(K.z,5,duplicates="drop"),observed=True).apply(g)
    out["by_r90"]=K.groupby(pd.qcut(K.r90,5),observed=True).apply(g)
    out["by_r30"]=K.groupby(pd.qcut(K.r30,5),observed=True).apply(g)
    out["by_clv"]=K.groupby(pd.qcut(K.clv,4),observed=True).apply(g)
    out["by_vrel"]=K.groupby(pd.qcut(K.vrel,4),observed=True).apply(g)
    out["by_year"]=K.groupby("year").apply(g)
    out["by_coin"]=K.groupby("coin").apply(g)
    act=D[D.alloc.abs()>0]
    out["book_bars"]=pd.Series({"active_bars":len(act),"mean_gain":act.gain.mean(),
        "mean_fee_all_bars":D.fee.mean()*1.0,"sum_gain":D.gain.sum(),"sum_fee":D.fee.sum(),
        "mean_absalloc_active":act.alloc.abs().mean()})
    t=pd.concat([x for ws in data["trades"].values() for x in ws.values()])
    out["trades"]=pd.Series({"n":len(t),"gross":t.profit_loss_percent.mean(),"net":t.net_profit_loss_percent.mean(),
        "dur_days":t.duration_minutes.mean()/1440,"win_net":(t.net_profit_loss_percent>0).mean()})
    return out
