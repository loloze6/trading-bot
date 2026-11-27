import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            vsr=(c/c.shift(14)-1)/(r.rolling(30).std()*np.sqrt(14))
            r60=c/c.shift(60)-1
            f7=c.shift(-7)/c-1
            f1=c.shift(-1)/c-1
            f3=c.shift(-3)/c-1
            vol30=r.rolling(30).std()
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"vsr":vsr,"r60":r60,"f7":f7,"f3":f3,"f1":f1,
                            "r1":r,"vol30":vol30,"reg":b["regime"].values,
                            "wd":pd.to_datetime(b["timestamp"]).dt.weekday.values,
                            "yr":pd.to_datetime(b["timestamp"]).dt.year.values})
            d["cc"]=(d["reg"]!="chop")
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    out["regime share"]=D["reg"].value_counts(normalize=True)
    g7=D[(D.pos%7==0)].dropna(subset=["f7","vsr"]).copy()
    drift=g7.groupby("coin")["f7"].mean()
    g7["u7"]=g7["f7"]-g7["coin"].map(drift)
    g7["vb"]=pd.cut(g7["vsr"],[-99,-2,-1,0,1,2,99])
    def summ(x):
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["u7 by vsr bucket, choppy calm"]=g7[g7.cc].groupby("vb")["u7"].apply(summ).unstack()
    out["u7 by vsr bucket, other profiles"]=g7[~g7.cc].groupby("vb")["u7"].apply(summ).unstack()
    g7["tb"]=pd.cut(g7["r60"],[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    out["u7 by trend x vsr sign>|1|"]=g7[g7.vsr.abs()>1].assign(s=np.sign(g7.vsr)).groupby(["tb","s"])["u7"].apply(summ).unstack()
    # correlation of vsr with u7 per profile group
    out["corr vsr-u7 cc / other"]=pd.Series({"cc":stats.spearmanr(g7[g7.cc].vsr,g7[g7.cc].u7)[0],"other":stats.spearmanr(g7[~g7.cc].vsr,g7[~g7.cc].u7)[0],
        "n_cc":g7.cc.sum(),"n_other":(~g7.cc).sum()})
    # daily: next-day after large moves, by vol-scaled one-day return
    g1=D.dropna(subset=["f1","r1","vol30"]).copy()
    g1["z"]=g1.r1/g1.vol30
    g1["zb"]=pd.cut(g1.z,[-99,-2.5,-1.5,-0.5,0.5,1.5,2.5,99])
    out["f1 by 1-day z"]=g1.groupby("zb")["f1"].apply(summ).unstack()
    g3=D[D.pos%3==0].dropna(subset=["f3","r1","vol30"]).copy()
    g3["z"]=g3.r1/g3.vol30
    g3["zb"]=pd.cut(g3.z,[-99,-2,-1,1,2,99])
    out["f3 by 1-day z, cc vs other"]=g3.groupby(["cc","zb"])["f3"].apply(summ).unstack()
    out["f1 by weekday"]=g1.groupby("wd")["f1"].apply(summ).unstack()
    out["u7 by year (vsr>=1, cc)"]=g7[g7.cc&(g7.vsr>=1)].groupby("yr")["u7"].apply(summ).unstack()
    return out
