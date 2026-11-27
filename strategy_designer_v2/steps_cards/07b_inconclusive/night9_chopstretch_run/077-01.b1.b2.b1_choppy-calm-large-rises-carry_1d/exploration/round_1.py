import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30).std()
            vsr=(c/c.shift(14)-1)/(sd*np.sqrt(14))
            yr=pd.to_datetime(b["timestamp"]).dt.year
            inprof=(b["regime"]!="chop")
            n=len(b)
            for h in (3,7,14):
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,i=i,year=yr[i],ret=c[i+h]/c[i]-1,
                        vsr=vsr[i],prof=inprof[i],reg=b["regime"][i],day=str(b["timestamp"][i])[:10]))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby(["coin","h"])["ret"].transform("mean")
    d["u"]=d["ret"]-d["drift"]
    d=d.dropna(subset=["vsr"])
    def summ(g):
        dd=g.groupby("day")["u"].sum()
        t=dd.mean()/(dd.std(ddof=1)/np.sqrt(len(dd))) if len(dd)>1 else np.nan
        return pd.Series(dict(n=len(g),days=len(dd),mean_u=g["u"].mean(),t=t,
              corr=g["u"].corr(g["vsr"]) if len(g)>2 else np.nan))
    out={}
    bins=[-99,-2,-1,0,1,2,99]
    d["vb"]=pd.cut(d["vsr"],bins)
    for h in (3,7,14):
        x=d[d.h==h]
        out[f"h{h}_prof_by_vsr"]=x.groupby(["prof","vb"],observed=True).apply(summ)
    x=d[(d.h==7)&d.prof]
    out["h7_inprof_corr_all"]=summ(x)
    big=x[x.vsr>=2]
    out["h7_big_by_year"]=big.groupby("year").apply(summ)
    out["h7_big_by_coin"]=big.groupby("coin").apply(summ)
    neg=x[x.vsr<=-2]
    out["h7_bigfall_by_year"]=neg.groupby("year").apply(summ)
    y=d[(d.h==7)&~d.prof]
    out["h7_outprof_big_rise"]=summ(y[y.vsr>=2])
    out["h7_inprof_signed_abs>=1"]=summ(x[x.vsr.abs()>=1].assign(u=lambda z: z.u*np.sign(z.vsr)))
    return out
