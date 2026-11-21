import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    def reg(s,xs,y):
        s=s[xs+[y]].dropna()
        if len(s)<30: return pd.Series(dict(n=len(s)))
        X=np.c_[np.ones(len(s)),s[xs].values]; yv=s[y].values
        bta=np.linalg.lstsq(X,yv,rcond=None)[0]; e=yv-X@bta
        cov=np.linalg.inv(X.T@X)*(e@e)/(len(s)-X.shape[1]); tt=bta/np.sqrt(np.diag(cov))
        return pd.Series(dict(n=len(s),**{f"b_{x}":bta[i+1] for i,x in enumerate(xs)},**{f"t_{x}":tt[i+1] for i,x in enumerate(xs)}))
    out={}
    for h in [24,72]:
        rows=[]
        for coin,wins in data["bars"].items():
            for w,b in wins.items():
                c=b["close"].values.astype(float)
                hr=np.r_[np.nan,c[1:]/c[:-1]-1]; n=len(c)
                for t in range(0,n-h,h):
                    if t<168: continue
                    hh=hr[t-167:t+1]
                    if np.isnan(hh).any(): continue
                    rows.append(dict(coin=coin,w=int(w[1:]),r24=c[t]/c[t-24]-1,r72=c[t]/c[t-72]-1,
                        f6=c[t+6]/c[t]-1,f624=(c[t+24]/c[t+6]-1),fh=c[t+h]/c[t]-1,
                        vol7=np.std(hh),vol1=np.std(hh[-24:])))
        d=pd.DataFrame(rows)
        for k in ["fh","f6","f624"]:
            d[k+"x"]=d[k]-d.groupby("coin")[k].transform("mean")
        d["z24"]=d.groupby("coin")["r24"].transform(lambda s:(s-s.mean())/s.std())
        d["z72"]=d.groupby("coin")["r72"].transform(lambda s:(s-s.mean())/s.std())
        d["vq7"]=d.groupby("coin")["vol7"].transform(lambda s:pd.qcut(s,3,labels=False))
        d["vq1"]=d.groupby("coin")["vol1"].transform(lambda s:pd.qcut(s,3,labels=False))
        d["half"]=np.where(d.w<=12,"a","b")
        tab={}
        for q in range(3):
            g=d[d.vq7==q]
            tab[f"vq7_{q}_z24"]=reg(g,["z24"],"fhx")
            tab[f"vq7_{q}_z72"]=reg(g,["z72"],"fhx")
            for hf in ["a","b"]:
                tab[f"vq7_{q}_z24_half{hf}"]=reg(g[g.half==hf],["z24"],"fhx")
        tab["vq1_2_z24"]=reg(d[d.vq1==2],["z24"],"fhx")
        tab["vq1_0_z24"]=reg(d[d.vq1==0],["z24"],"fhx")
        out[f"vol_split_h{h}"]=pd.DataFrame(tab).T
        if h==24:
            dn=d[d.r72<0]
            out["down72_timing"]=pd.DataFrame({"0-6h":reg(dn,["z24"],"f6x"),"6-24h":reg(dn,["z24"],"f624x")}).T
            hv=d[d.vq1==2]
            out["hivol_coin_h24"]=pd.DataFrame({c:reg(g,["z24"],"fhx") for c,g in hv.groupby("coin")}).T
        if h==72:
            lv=d[d.vq7==0]
            out["lowvol_coin_h72"]=pd.DataFrame({c:reg(g,["z24"],"fhx") for c,g in lv.groupby("coin")}).T
    return out
