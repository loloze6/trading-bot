def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(720,min_periods=120).std()
            vr=b["volume"]/b["volume"].rolling(720,min_periods=120).mean()
            z=r/sd; p=z*vr
            yr=pd.to_datetime(b["timestamp"]).dt.year
            for h in (1,2,3,4,6,12):
                fr=c.shift(-h)/c-1
                idx=np.arange(0,len(b)-h,h)
                d=pd.DataFrame(dict(z=z.iloc[idx].values,vr=vr.iloc[idx].values,p=p.iloc[idx].values,
                                    fr=fr.iloc[idx].values,yr=yr.iloc[idx].values))
                d["h"]=h; d["coin"]=coin; d["w"]=w; rows.append(d)
    D=pd.concat(rows).dropna(subset=["z","vr","fr"])
    D["u"]=D.fr-D.groupby(["coin","h"])["fr"].transform("mean")
    D["sd_h"]=D.groupby(["coin","h"])["fr"].transform("std")
    D["rev"]=-np.sign(D.z)*D.u   # positive = reversal
    D["revtot"]=-np.sign(D.z)*D.fr
    D["pb"]=pd.cut(D.p.abs(),[0,1,3,6,12,25,1e9])
    out={}
    def agg(g):
        m=g["rev"].mean(); s=g["rev"].std(); n=len(g)
        return pd.Series(dict(rev_mean=m,tot_mean=g["revtot"].mean(),strength=(g["rev"]/g["sd_h"]).mean(),n=n,t=m/(s/np.sqrt(n)) if n>1 else np.nan))
    out["reversal_by_absproduct_h"]=D.groupby(["h","pb"],observed=True).apply(agg).round(5)
    big=D[D.p.abs()>12]
    out["big_by_side_h"]=big.groupby(["h",np.sign(big.z)]).apply(agg).round(5)
    b2=D[(D.h==2)&(D.p.abs()>6)]
    out["h2_p>6_by_year"]=b2.groupby("yr").apply(agg).round(5)
    out["h2_p>6_by_coin"]=b2.groupby("coin").apply(agg).round(5)
    b2["vb"]=pd.cut(b2.vr,[0,2,4,8,1e9]); b2["zb"]=pd.cut(b2.z.abs(),[0,2,3,5,1e9])
    out["h2_p>6_by_vr"]=b2.groupby("vb",observed=True).apply(agg).round(5)
    out["h2_p>6_by_absz"]=b2.groupby("zb",observed=True).apply(agg).round(5)
    sp=D[(D.h==2)&(D.p.abs()>1)]
    from scipy.stats import spearmanr
    out["h2_spearman_absp_rev"]=float(spearmanr(sp.p.abs(),sp.rev).correlation)
    # book daily
    dd=pd.concat([x.assign(coin=c) for c in data["days"] for x in data["days"][c].values()])
    out["book_daily"]=dd.groupby("coin")[["book_return","coin_return"]].mean()
    return out
