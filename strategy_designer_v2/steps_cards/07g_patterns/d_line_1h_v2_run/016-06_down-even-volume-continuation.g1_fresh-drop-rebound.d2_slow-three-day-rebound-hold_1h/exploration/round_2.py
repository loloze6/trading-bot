import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    def build(h):
        rows=[]
        for coin,wins in data["bars"].items():
            for w,b in wins.items():
                c=b["close"].values.astype(float); v=b["volume"].values.astype(float)
                ts=pd.to_datetime(b["timestamp"])
                hr=np.r_[np.nan,c[1:]/c[:-1]-1]; n=len(c)
                for t in range(0,n-h,h):
                    if t<72: continue
                    hh=hr[t-23:t+1]; vv=v[t-23:t+1]
                    if np.isnan(hh).any() or vv.sum()<=0: continue
                    rows.append(dict(coin=coin,w=w,r24=c[t]/c[t-24]-1,r72=c[t]/c[t-72]-1,
                        fh=c[t+h]/c[t]-1, f2472=(c[t+72]/c[t+24]-1) if h==72 else np.nan,
                        jump=np.abs(hh).max()/(np.abs(hh).sum()+1e-12),
                        vconc=vv.max()/vv.sum(), vol=np.std(hh), hour=ts.iloc[t].hour))
        d=pd.DataFrame(rows)
        for k in ["fh","f2472"]:
            d[k+"x"]=d[k]-d.groupby("coin")[k].transform("mean")
        d["z24"]=d.groupby("coin")["r24"].transform(lambda s:(s-s.mean())/s.std())
        d["volq"]=d.groupby("coin")["vol"].transform(lambda s:pd.qcut(s,3,labels=False))
        d["sgn"]=np.sign(d.r24)
        return d
    out={}
    def reg(s,xs,y):
        s=s[xs+[y]].dropna(); X=np.c_[np.ones(len(s)),s[xs].values]; yv=s[y].values
        bta,res,_,_=np.linalg.lstsq(X,yv,rcond=None); e=yv-X@bta
        cov=np.linalg.inv(X.T@X)*(e@e)/(len(s)-X.shape[1]); tt=bta/np.sqrt(np.diag(cov))
        return pd.Series(dict(n=len(s),**{f"b_{x}":bta[i+1] for i,x in enumerate(xs)},**{f"t_{x}":tt[i+1] for i,x in enumerate(xs)}))
    for h in [24,72]:
        d=build(h)
        tab={}
        tab["all"]=reg(d,["z24"],"fhx")
        tab["down72"]=reg(d[d.r72<0],["z24"],"fhx")
        tab["up72"]=reg(d[d.r72>=0],["z24"],"fhx")
        for q in range(3):
            tab[f"volq{q}"]=reg(d[d.volq==q],["z24"],"fhx")
        d["zj"]=d.z24*d.jump; d["zv"]=d.z24*d.vconc
        tab["z+jump_int"]=reg(d,["z24","jump","zj"],"fhx")
        tab["z+vconc_int"]=reg(d,["z24","vconc","zv"],"fhx")
        out[f"reg_h{h}"]=pd.DataFrame(tab).T
        if h==72:
            out["f2472_reg"]=pd.DataFrame({"all":reg(d,["z24"],"f2472x"),"up72":reg(d[d.r72>=0],["z24"],"f2472x"),
                "rise_jump":reg(d[d.r24>0],["z24","jump"],"f2472x"),"fall_jump":reg(d[d.r24<0],["z24","jump"],"f2472x")}).T
            out["coin_down72_h72"]=pd.DataFrame({c:reg(g[g.r72<0],["z24"],"fhx") for c,g in d.groupby("coin")}).T
            d["half"]=np.where(d.w.str[1:].astype(int)<=12,"w1-12","w13-24")
            out["half_down72_h72"]=pd.DataFrame({c:reg(g[g.r72<0],["z24"],"fhx") for c,g in d.groupby("half")}).T
        if h==24:
            d["sf"]=d.fhx*d.sgn
            out["h24_signed_by_volq"]=d.groupby("volq")["sf"].agg(["mean","count",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
            out["h24_by_hour_fall_slope"]=pd.DataFrame({hh:reg(g,["z24"],"fhx") for hh,g in d.groupby("hour")}).T
    return out
