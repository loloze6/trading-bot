def explore(data):
    import numpy as np, pandas as pd
    rows=[]; tr=[]
    H=[2,4,6,8]
    for c in data["bars"]:
        mus={}
        for h in H:
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
            d={"coin":c,"hr":hr,"z":z,"r72":r72,"yr":ts.dt.year}
            for h in H:
                d[f"ex{h}"]=cl.shift(-h)/cl-1-mus[h]
            rows.append(pd.DataFrame(d))
        for w,t in data["trades"][c].items():
            tr.append(t.assign(coin=c))
    D=pd.concat(rows)
    T=pd.concat(tr)
    out={}
    tt=lambda x:x.mean()/(x.std()/np.sqrt(len(x)))
    for hh in [0,8,16]:
        S=D[(D.hr==hh)&(D.z<0)].dropna(subset=["z","ex8"]).copy()
        S["zq"]=pd.qcut(S.z,3,labels=["deep","mid","mild"])
        res={}
        for h in H:
            g=S.groupby("zq")[f"ex{h}"]
            res[h]={"deep":g.mean()["deep"],"mid":g.mean()["mid"],"mild":g.mean()["mild"],"t_deep":tt(S[S.zq=="deep"][f"ex{h}"]),"all":S[f"ex{h}"].mean()}
        out[f"settle_{hh}_thirds_by_h"]=pd.DataFrame(res).T
    S=D[(D.hr==0)&(D.z<0)].dropna(subset=["ex6"])
    out["h0_ex6_by_year"]=S.groupby("yr").ex6.agg(["size","mean",tt])
    out["h0_ex6_by_coin"]=S.groupby("coin").ex6.agg(["size","mean",tt])
    T["fee_pct"]=T.profit_loss_percent-T.net_profit_loss_percent
    T["eh"]=pd.to_datetime(T.entry_time).dt.hour
    out["trades_by_entry_hour"]=T.groupby("eh").agg(n=("fee_pct","size"),gross=("profit_loss_percent","mean"),fee=("fee_pct","mean"),dur=("duration_minutes","mean"))
    return out
