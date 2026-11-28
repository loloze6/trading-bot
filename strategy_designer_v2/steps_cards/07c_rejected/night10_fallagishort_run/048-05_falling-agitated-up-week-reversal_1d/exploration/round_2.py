import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30).std()
            sw=(c/c.shift(7)-1)/(sd*np.sqrt(7))
            sw3=(c/c.shift(3)-1)/(sd*np.sqrt(3))
            sw1=r/sd
            reg=b["regime"].astype(str)
            fc=b["forecast"].astype(float)
            n=len(b)
            for h in (1,2,3):
                fwd=c.shift(-h)/c-1
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,sw=sw[i],sw3=sw3[i],sw1=sw1[i],fwd=fwd[i],
                                     inprof=reg[i] in ("mean_reversion","unknown"),fc=fc[i]))
    d=pd.DataFrame(rows).dropna(subset=["sw","fwd","sw3","sw1"])
    drift=d.groupby(["coin","h"])["fwd"].mean().rename("drift")
    d=d.join(drift,on=["coin","h"]); d["y"]=d["fwd"]-d["drift"]
    fa=d[d.inprof].copy()
    out={}
    def reg_t(s,x):
        if len(s)<10: return pd.Series(dict(n=len(s)))
        lr=stats.linregress(s[x],s["y"])
        return pd.Series(dict(n=len(s),slope=lr.slope,t=lr.slope/lr.stderr,meany=s["y"].mean(),
                              t_meany=s["y"].mean()/(s["y"].std()/np.sqrt(len(s)))))
    res=[]
    for x in ("sw","sw3","sw1"):
        for h in (1,2,3):
            s=fa[fa.h==h]
            for side,ss in (("all",s),("up",s[s[x]>0]),("down",s[s[x]<=0])):
                r_=reg_t(ss,x); r_["x"]=x; r_["h"]=h; r_["side"]=side; res.append(r_)
    out["fa_measures"]=pd.DataFrame(res).set_index(["x","h","side"])
    up3=fa[(fa.h==3)&(fa.sw>0)].copy()
    up3["q"]=pd.qcut(up3["sw"],3,labels=False)
    out["up3_tercile"]=up3.groupby("q").agg(n=("y","size"),sw=("sw","mean"),y=("y","mean"),ystd=("y","std"),fwd=("fwd","mean"))
    dn3=fa[(fa.h==3)&(fa.sw<=0)].copy()
    dn3["q"]=pd.qcut(dn3["sw"],3,labels=False)
    out["down3_tercile"]=dn3.groupby("q").agg(n=("y","size"),sw=("sw","mean"),y=("y","mean"),ystd=("y","std"))
    up3["fneg"]=up3["fc"]<0
    out["up3_fc_vs_sw_corr"]=float(up3.loc[up3.fneg,["fc","sw"]].corr().iloc[0,1]) if up3.fneg.sum()>3 else np.nan
    out["up3_by_coin"]=up3.groupby("coin").apply(lambda s: reg_t(s,"sw"))
    return out
