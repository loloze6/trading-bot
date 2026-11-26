def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]; trades=[]
    allret={}
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            b["wd"]=ts.dt.weekday.values
            b["yr"]=ts.dt.year.values
            b["nxt"]=b["close"].shift(-1)/b["close"]-1
            b["nxt_wd"]=b["wd"].shift(-1)
            b["r20"]=b["close"]/b["close"].shift(20)-1
            b["r60"]=b["close"]/b["close"].shift(60)-1
            b["coin"]=coin; b["win"]=w
            b["pos"]=b["postRebalance_current_allocation"]
            rows.append(b[["coin","win","wd","yr","nxt","nxt_wd","r20","r60","pos","forecast","close"]])
        for w,t in data["trades"].get(coin,{}).items():
            if len(t): trades.append(t.assign(coin=coin,win=w))
    d=pd.concat(rows,ignore_index=True)
    mu=d.groupby("coin")["nxt"].mean()
    d["ex"]=d["nxt"]-d["coin"].map(mu)
    d["pnl"]=d["pos"]*d["nxt"]
    d["mkt"]=d["pos"]*d["coin"].map(mu)
    out={}
    def summ(g):
        x=g["ex"].dropna(); 
        return pd.Series({"n":len(x),"mean_ex":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,"mean_raw":g["nxt"].mean()})
    out["next-day excess by next weekday"]=d.dropna(subset=["nxt"]).groupby("nxt_wd").apply(summ)
    fr=d[(d["nxt_wd"]==5)].dropna(subset=["nxt","r20"]).copy()
    fr["r20_q"]=fr.groupby("coin")["r20"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["Saturday excess by r20 quintile (per coin)"]=fr.groupby("r20_q").apply(summ)
    fr["sign20"]=np.sign(fr["r20"])
    out["Saturday by r20 sign"]=fr.groupby("sign20").apply(summ)
    oth=d[(d["nxt_wd"]!=5)].dropna(subset=["nxt","r20"]).copy()
    oth["sign20"]=np.sign(oth["r20"])
    out["non-Saturday by r20 sign"]=oth.groupby(["nxt_wd","sign20"]).apply(summ)
    p=d.dropna(subset=["pnl"])
    out["pnl by coin"]=p.groupby("coin")[["pnl","mkt"]].sum()
    out["pnl by year"]=p.groupby("yr")[["pnl","mkt"]].sum()
    out["pnl by window"]=p.groupby("win")[["pnl"]].sum().T
    out["pnl by next weekday"]=p.groupby("nxt_wd")[["pnl","mkt"]].sum()
    out["total pnl, mkt share"]=pd.Series({"pnl":p["pnl"].sum(),"mkt":p["mkt"].sum()})
    if trades:
        T=pd.concat(trades,ignore_index=True)
        s=T["net_profit_loss_percent"].sort_values(ascending=False)
        out["trades"]=pd.Series({"n":len(s),"sum":s.sum(),"top10":s.head(10).sum(),"top30":s.head(30).sum(),"winrate":(s>0).mean(),"median":s.median(),"mean_dur_h":T["duration_minutes"].mean()/60})
    return out
