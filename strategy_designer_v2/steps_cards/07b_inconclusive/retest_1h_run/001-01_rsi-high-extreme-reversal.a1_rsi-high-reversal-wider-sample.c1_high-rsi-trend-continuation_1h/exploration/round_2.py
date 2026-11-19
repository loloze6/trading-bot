import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H=240
    out={}
    rows=[]
    G=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values; r=b["regime"].values
            n=len(b)
            for i in range(0,n,H):
                rows.append({"coin":coin,"w":w,"f":f[i],"reg":r[i],"r240":c[i+H]/c[i]-1 if i+H<n else np.nan})
            a=b["postRebalance_current_allocation"].fillna(0).values
            nr=np.append(c[1:]/c[:-1]-1,np.nan)
            gross=a*nr
            day=pd.to_datetime(b["timestamp"]).dt.floor("D").values
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"]).values/b["total_portfolio_value"].values
            turn=np.abs(b["postRebalance_current_allocation"].fillna(0)-b["previous_allocation"].fillna(0)).values
            G.append(pd.DataFrame({"coin":coin,"w":w,"day":day,"gross":gross,"fee":fee,"turn":turn,"a":a,"nr":nr}))
    g=pd.DataFrame(rows).dropna(subset=["r240"])
    g["x"]=g["r240"]-g.groupby("coin")["r240"].transform("mean")
    L=[]
    for k,d in g[g.f>0].groupby("reg"):
        s=stats.linregress(d["f"],d["x"]); L.append({"reg":k,"slope_pos":s.slope,"t":s.slope/s.stderr,"n":len(d),"mean_x":d.x.mean()})
    for k,d in g.groupby(["reg","coin"]):
        if d.f.std()>0:
            s=stats.linregress(d["f"],d["x"]); L.append({"reg":str(k),"slope_pos":s.slope,"t":s.slope/s.stderr,"n":len(d),"mean_x":d.x.mean()})
    out["regime_slopes"]=pd.DataFrame(L)
    Gd=pd.concat(G)
    dd=Gd.groupby(["coin","w","day"]).agg(gross=("gross","sum"),fee=("fee","sum"),turn=("turn","sum"),a=("a","mean")).reset_index()
    bd=dd.groupby(["w","day"])[["gross","fee","turn","a"]].mean()
    out["book_decomp"]=pd.DataFrame({"mean":bd.mean(),"t":bd.mean()/(bd.std()/np.sqrt(len(bd)))})
    # market part vs timing
    cm=Gd.groupby("coin")["nr"].mean()
    Gd["mkt"]=Gd["a"]*Gd["coin"].map(cm)
    md=Gd.groupby(["coin","w","day"])["mkt"].sum().groupby(["w","day"]).mean()
    out["gross_market_part_daily"]=float(md.mean())
    return out
