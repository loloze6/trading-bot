import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20).std()
            z=r/sd
            r30=c/c.shift(30)-1; r90=c/c.shift(90)-1
            f1=c.shift(-1)/c-1; f3=c.shift(-3)/c-1
            rows.append(pd.DataFrame({"coin":coin,"w":w,"z":z,"r30":r30,"r90":r90,"f1":f1,"f3":f3,
                "pos":b["postRebalance_current_allocation"].astype(float),"pos_i":np.arange(len(b)),
                "regime":b["regime"]}))
    d=pd.concat(rows)
    drift=d.groupby("coin")["f1"].mean()
    d["a1"]=d["f1"]-d["coin"].map(drift); d["a3"]=d["f3"]-3*d["coin"].map(drift)
    out={}
    def reg(x,y):
        m=x.notna()&y.notna(); x=x[m]; y=y[m]
        rr,p=stats.pearsonr(x,y); sl=np.polyfit(x,y,1)[0]
        return {"n":len(x),"corr":rr,"p":p,"slope%_per_z":100*sl}
    res={}
    for name,mask in {"r30neg_up":(d.r30<0)&(d.z>0),"r30neg_up_r90neg":(d.r30<0)&(d.r90<0)&(d.z>0),
                      "r30neg_up_r90pos":(d.r30<0)&(d.r90>=0)&(d.z>0),"r30pos_up":(d.r30>=0)&(d.z>0)}.items():
        s=d[mask]
        res[name+"_1d"]=reg(s.z,s.a1)
        g=s[s.pos_i%3==0]; res[name+"_3d_grid"]=reg(g.z,g.a3)
    out["graded z vs next move"]=pd.DataFrame(res).T.round(4)
    # depth of r30 among up days in r30<0
    s=d[(d.r30<0)&(d.z>0)].copy()
    s["r30b"]=pd.qcut(s.r30,4)
    out["r30neg up days by r30 quartile"]=s.groupby("r30b",observed=True)["a1"].agg(["count","mean"]).assign(mean=lambda x:100*x["mean"]).round(3)
    # share of up days in r30<0
    out["counts"]=pd.Series({"r30neg_up_bars":int(((d.r30<0)&(d.z>0)).sum()),"r30neg_up_z_ge1":int(((d.r30<0)&(d.z>=1)).sum()),
        "active_regime_bars":int((d.regime=="mean_reversion").sum()),"bars":len(d)})
    return out
