def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    cost_side = 0.0019/2
    rows = []; C = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            a = b["postRebalance_current_allocation"].fillna(0)
            pa = b["previous_allocation"].fillna(0)
            r = b["close"].shift(-1)/b["close"]-1
            al = a.clip(lower=0); pl = pa.clip(lower=0)
            ash = a.clip(upper=0); psh = pa.clip(upper=0)
            gl = al*r - (al-pl).abs()*cost_side
            gs = ash*r - (ash-psh).abs()*cost_side
            df = pd.DataFrame({"coin":c,"wn":int(w[1:]),"day":ts.dt.floor("D"),"gl":gl,"gs":gs})
            rows.append(df.dropna())
            r1=b["close"].pct_change(); v24=r1.rolling(24).std()
            fwd=b["close"].shift(-24)/b["close"]-1
            r168=b["close"]/b["close"].shift(168)-1
            e=pd.DataFrame({"coin":c,"hr":ts.dt.hour,"wd":ts.dt.weekday,"z":r1/v24,"fwd":fwd,"r168":r168})
            C.append(e[(e["hr"]==0)&e["wd"].isin([5,6])])
    G=pd.concat(rows)
    Dc=G.groupby(["coin","wn","day"])[["gl","gs"]].sum().reset_index()
    Dd=Dc.groupby(["wn","day"])[["gl","gs"]].mean().reset_index().sort_values(["wn","day"])
    Dd["tot"]=Dd["gl"]+Dd["gs"]
    def calm(x):
        v=(1+x).cumprod(); dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(x))-1
        return pd.Series({"mean":x.mean(),"sharpe":x.mean()/x.std()*np.sqrt(365),"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd)})
    out["net_side_books"]=pd.DataFrame({k:calm(Dd[k]) for k in ["gl","gs","tot"]})
    W=pd.concat(C).dropna(subset=["fwd","z","r168"])
    def s(x):
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    W["dn7"]=W["r168"]<0
    out["short_capture_all_weekend00_by_7d"]=(-W["fwd"]).groupby(W["dn7"]).apply(s).unstack()
    U=W[W["z"]>0]
    out["short_capture_uphour_by_7d"]=(-U["fwd"]).groupby(U["dn7"]).apply(s).unstack()
    out["short_capture_uphour_z_gt1_by_7d"]=(-U[U["z"]>1]["fwd"]).groupby(U[U["z"]>1]["dn7"]).apply(s).unstack()
    out["short_capture_uphour_by_zbin"]=(-U["fwd"]).groupby(pd.cut(U["z"],[0,0.5,1,1.5,2,99])).apply(s).unstack()
    return out
