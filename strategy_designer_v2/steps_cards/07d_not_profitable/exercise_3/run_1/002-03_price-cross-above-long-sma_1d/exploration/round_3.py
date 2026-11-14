def explore(data):
    import pandas as pd, numpy as np
    out={}
    rows=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl=b["close"]; a=b["postRebalance_current_allocation"]
            fc=b["forecast"]
            t=pd.DataFrame({"ts":pd.to_datetime(b["timestamp"]),"g":a*(cl.shift(-1)/cl-1),"a":a,"coin":c,"wn":int(w[1:]),
              "fcchg20":fc-fc.shift(20),"fcchg5":fc-fc.shift(5),"past60":cl/cl.shift(60)-1,"fc":fc})
            rows.append(t)
    B=pd.concat(rows).dropna(subset=["g"])
    B["day"]=B["ts"].dt.floor("D")
    def calm(mask,name):
        x=B.copy(); x.loc[~mask,"g"]=0.0
        P=x.groupby(["wn","day"])["g"].mean().reset_index().sort_values(["wn","day"])
        r=P["g"]; eq=(1+r).cumprod(); dd=(eq/eq.cummax()-1).min()
        yr=eq.iloc[-1]**(365/len(r))-1
        return {"mean":r.mean(),"sharpe":r.mean()/r.std()*np.sqrt(365),"maxdd":dd,"calmar":yr/abs(dd),"share_active":float((mask&(B.a>0)).sum()/(B.a>0).sum())}
    res={}
    res["all"]=calm(B.a==B.a,"all")
    res["fcchg20>0"]=calm((B.fcchg20>0).fillna(False),"")
    res["fcchg5>0"]=calm((B.fcchg5>0).fillna(False),"")
    res["fcchg20>=0"]=calm((B.fcchg20>=0).fillna(False),"")
    res["past60<0.5"]=calm((B.past60<0.5).fillna(False),"")
    out["what-if before fees"]=pd.DataFrame(res).T.round(4)
    L=B[(B.a>0)].dropna(subset=["fcchg20"])
    F=L[L.wn.isin([16,17,18])]
    out["fall windows long gain by fcchg20 sign"]=F.groupby(np.sign(F.fcchg20)).agg(n=("g","size"),gain=("g","mean"),sum=("g","sum"),a=("a","mean")).round(4)
    out["all long gain by fc at cap & fcchg sign"]=L.groupby([L.fc>=19.99,np.sign(L.fcchg20)]).agg(n=("g","size"),gain=("g","mean"),sd=("g","std")).round(5)
    return out
