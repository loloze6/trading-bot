import numpy as np, pandas as pd

def explore(data):
    allmean={}
    for coin,ws in data["bars"].items():
        rets=[]
        for w,b in ws.items():
            c=b["close"].values
            rets.append(pd.Series(c[1:]/c[:-1]-1))
        allmean[coin]=pd.concat(rets).mean()
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; lo=b["low"]; hi=b["high"]
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b))})
            d["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            d["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            d["r0"]=c/c.shift(1)-1
            for h in (1,2,3):
                d[f"f{h}"]=c.shift(-h)/c-1-allmean[coin]*h
            d["lowdist"]=c/lo.shift(1).rolling(20).min()-1
            d["highdist"]=c/hi.shift(1).rolling(20).max()-1
            d["vol20"]=d["r0"].rolling(20).std()
            d["z0"]=d["r0"]/d["vol20"].shift(1)
            d["ldz"]=d["lowdist"]/d["vol20"]
            d["hdz"]=d["highdist"]/d["vol20"]
            d["prof"]=np.where(b["regime"]=="chop","trend","choppy")
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def tc(s,col):
        s=s.dropna(subset=[col])
        if len(s)<3: return pd.Series({"n":len(s),"days":0,"mean":np.nan,"t":np.nan})
        m=s[col].mean(); dev=(s[col]-m).groupby(s["day"]).sum(); k=len(dev)
        se=np.sqrt((dev**2).sum()*k/(k-1))/len(s)
        return pd.Series({"n":len(s),"days":k,"mean":m,"t":m/se})
    def slope(s,x,y):
        s=s.dropna(subset=[x,y])
        if len(s)<5: return pd.Series({"n":len(s),"slope":np.nan,"t":np.nan})
        X=s[x]-s[x].mean(); b=(X*s[y]).sum()/(X**2).sum()
        e=s[y]-s[y].mean()-b*X
        sc=(X*e).groupby(s["day"]).sum(); k=len(sc)
        se=np.sqrt((sc**2).sum()*k/(k-1))/(X**2).sum()
        return pd.Series({"n":len(s),"days":k,"slope":b,"t":b/se})
    out={}
    out["prof_share"]=D.prof.value_counts(normalize=True)
    res=[]
    for side,col,mask,sg in (("dn","lowdist",D.lowdist<0,1),("up","highdist",D.highdist>0,-1)):
        for pr in ("choppy","trend","all"):
            for h in (1,2,3):
                s=D[mask&((D.prof==pr)|(pr=="all"))&(D.pos%h==0)].copy()
                s["y"]=s[f"f{h}"]*sg
                r=tc(s,"y"); r.name=f"{side}_{pr}_h{h}_fade"; res.append(r)
    out["breaks_fade_by_profile"]=pd.DataFrame(res)
    res=[]
    for pr in ("choppy","trend","all"):
        s=D[(D.lowdist<0)&((D.prof==pr)|(pr=="all"))]
        r=slope(s,"lowdist","f1"); r.name=f"dn_{pr}_f1_on_dist"; res.append(r)
        r=slope(s,"ldz","f1"); r.name=f"dn_{pr}_f1_on_distz"; res.append(r)
        s=D[(D.highdist>0)&((D.prof==pr)|(pr=="all"))]
        r=slope(s,"highdist","f1"); r.name=f"up_{pr}_f1_on_dist"; res.append(r)
    for pr in ("choppy","trend","all"):
        s=D[(D.z0<0)&((D.prof==pr)|(pr=="all"))]
        r=slope(s,"z0","f1"); r.name=f"downday_{pr}_f1_on_z0"; res.append(r)
        s=D[(D.z0>0)&((D.prof==pr)|(pr=="all"))]
        r=slope(s,"z0","f1"); r.name=f"upday_{pr}_f1_on_z0"; res.append(r)
    out["slopes"]=pd.DataFrame(res)
    dn=D[D.lowdist<0].copy()
    dn["bin"]=pd.qcut(dn.lowdist,3,labels=["deep","mid","shallow"])
    out["dn_depth_by_profile_h1"]=dn.groupby(["prof","bin"]).apply(lambda s:tc(s,"f1"))
    out["dn_deep_by_year"]=dn[dn.bin=="deep"].groupby("yr").apply(lambda s:tc(s,"f1"))
    out["dn_by_coin"]=dn.groupby("coin").apply(lambda s:tc(s,"f1"))
    out["dn_by_window"]=dn.groupby("w").apply(lambda s:tc(s,"f1"))
    return out
