import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    allmean={}
    for coin,ws in data["bars"].items():
        rets=[]
        for w,b in ws.items():
            c=b["close"].values
            rets.append(pd.Series(c[1:]/c[:-1]-1))
        allmean[coin]=pd.concat(rets).mean()
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; lo=b["low"]; hi=b["high"]
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b))})
            d["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            d["r0"]=c/c.shift(1)-1
            for h in (1,3,5):
                d[f"f{h}"]=c.shift(-h)/c-1-allmean[coin]*h
            d["lowdist"]=c/lo.shift(1).rolling(20).min()-1
            d["highdist"]=c/hi.shift(1).rolling(20).max()-1
            d["tr60"]=c/c.shift(60)-1
            d["tr30"]=c/c.shift(30)-1
            d["vol20"]=d["r0"].rolling(20).std()
            d["z0"]=d["r0"]/d["vol20"].shift(1)
            d["fc"]=b["forecast"]
            d["alloc"]=b["postRebalance_current_allocation"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def tc(s,col):
        s=s.dropna(subset=[col])
        if len(s)<3: return pd.Series({"n":len(s),"days":0,"mean":np.nan,"t":np.nan})
        m=s[col].mean(); dev=(s[col]-m).groupby(s["day"]).sum(); k=len(dev)
        se=np.sqrt((dev**2).sum()*k/(k-1))/len(s)
        return pd.Series({"n":len(s),"days":k,"mean":m,"t":m/se})
    def trd(x):
        return np.where(x>0.10,"rising",np.where(x<-0.10,"falling","choppy"))
    D["trend"]=pd.Series(trd(D["tr60"].fillna(0)),index=D.index).where(D["tr60"].notna(),"na")
    out={}
    # downside breaks and upside breaks by trend, horizons
    res=[]
    for side,mask,sg in (("dn",D.lowdist<0,1),("up",D.highdist>0,-1)):
        for tr in ("choppy","rising","falling","na"):
            for h in (1,3,5):
                s=D[mask&(D.trend==tr)&(D.pos%h==0)].copy()
                s["y"]=s[f"f{h}"]*sg
                r=tc(s,"y"); r.name=f"{side}_{tr}_h{h}"; res.append(r)
    out["breaks_fade_sign_by_trend"]=pd.DataFrame(res)
    # depth bins of downside breaks, all trends, h1
    dn=D[D.lowdist<0].copy()
    dn["bin"]=pd.qcut(dn.lowdist,4,labels=["deep","q2","q3","shallow"])
    out["dn_depth_h1"]=dn.groupby("bin").apply(lambda s:tc(s,"f1"))
    up=D[D.highdist>0].copy()
    up["bin"]=pd.qcut(up.highdist,4,labels=["small","q2","q3","large"])
    out["up_size_h1_raw"]=up.groupby("bin").apply(lambda s:tc(s,"f1"))
    # large daily moves by z
    D["zbin"]=pd.cut(D.z0,[-99,-2.5,-1.5,-0.5,0.5,1.5,2.5,99])
    out["next1_by_z0"]=D.groupby("zbin").apply(lambda s:tc(s,"f1"))
    out["next3_by_z0_grid"]=D[D.pos%3==0].groupby("zbin").apply(lambda s:tc(s,"f3"))
    out["next1_by_z0_choppy"]=D[D.trend=="choppy"].groupby("zbin").apply(lambda s:tc(s,"f1"))
    out["next1_by_weekday"]=D.groupby("wd").apply(lambda s:tc(s,"f1"))
    D["vq"]=D.groupby("coin")["vol20"].transform(lambda x:pd.qcut(x,3,labels=["lowv","midv","highv"]))
    out["next1_by_vol"]=D.groupby("vq").apply(lambda s:tc(s,"f1"))
    out["next1_by_trend"]=D.groupby("trend").apply(lambda s:tc(s,"f1"))
    out["active_share"]=float((D.fc>0).mean())
    return out
