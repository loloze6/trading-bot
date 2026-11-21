def explore(data):
    import numpy as np, pandas as pd
    rows=[]; tr=[]
    for c in data["bars"]:
        mus={}
        for h in [2,4,8,24]:
            allr=[]
            for w,b in data["bars"][c].items():
                cl=pd.Series(b["close"].values)
                allr.append((cl.shift(-h)/cl-1).iloc[::h])
            mus[h]=pd.concat(allr).mean()
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True)
            cl=b["close"]
            r72=cl/cl.shift(72)-1
            z=(r72-r72.rolling(73,min_periods=20).mean())/r72.rolling(73,min_periods=20).std()
            ts=pd.to_datetime(b["timestamp"])
            hr=(ts+pd.Timedelta(hours=1)).dt.hour
            d={"coin":c,"hr":hr,"z":z,"r72":r72}
            for h in [2,4,8,24]:
                d[f"ex{h}"]=cl.shift(-h)/cl-1-mus[h]
            rows.append(pd.DataFrame(d))
        t=data["trades"][c][w] if False else None
        for w,t in data["trades"][c].items():
            tr.append(t.assign(coin=c))
    D=pd.concat(rows)
    T=pd.concat(tr)
    out={}
    S=D[D.hr.isin([0,8,16])&(D.z<0)].dropna(subset=["z"]).copy()
    S["zq"]=pd.qcut(S.z,3,labels=["deep","mid","mild"])
    res={}
    for h in [2,4,8,24]:
        x=S[f"ex{h}"].dropna()
        res[h]={"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))),
                "deep":S[S.zq=="deep"][f"ex{h}"].mean(),"mild":S[S.zq=="mild"][f"ex{h}"].mean()}
    out["settle_negz_by_horizon"]=pd.DataFrame(res).T
    res={}
    for hh in [0,8,16]:
        s=S[S.hr==hh]
        for h in [2,4,8]:
            x=s[f"ex{h}"].dropna()
            res[(hh,h)]={"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))}
    out["by_settle_hour_horizon"]=pd.DataFrame(res).T
    # 24h graded, non-overlapping grid of 24 at any hour
    G=D[D.z<0].dropna(subset=["ex24"])
    G=G.iloc[::24].copy()
    G["zq"]=pd.qcut(G.z,3,labels=["deep","mid","mild"])
    out["any_negz_24h_by_third"]=G.groupby("zq").ex24.agg(["size","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    out["trades"]=pd.Series({"n":len(T),"mean_gross_pct":T.profit_loss_percent.mean(),"mean_net_pct":T.net_profit_loss_percent.mean(),
        "mean_dur_min":T.duration_minutes.mean(),"win_gross":(T.profit_loss_percent>0).mean()})
    out["trades_by_side"]=T.groupby("side").agg(n=("profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"))
    return out
