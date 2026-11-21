def explore(data):
    import numpy as np, pandas as pd
    out={}
    # book daily measures
    dd=[]
    for c in data["days"]:
        for w,d in data["days"][c].items():
            dd.append(d.assign(coin=c,w=w))
    DD=pd.concat(dd)
    g=DD.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book daily"]=pd.Series({"book mean":g.book_return.mean(),"book sharpe":g.book_return.mean()/g.book_return.std()*np.sqrt(365),
        "hold mean":g.coin_return.mean(),"days":len(g)})
    # fade payoff by lookback L and horizon H, top decile of |z| and all
    res=[]; vres=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"]
            lr=np.log(cl).diff(); vol=lr.rolling(168).std()
            for L in [2,6,24]:
                m=cl/cl.shift(L)-1
                z=m/m.abs().rolling(500,min_periods=120).mean().shift(1)
                for H in [2,6,24]:
                    f=cl.shift(-H)/cl-1
                    idx=np.arange(0,len(b),H)
                    res.append(pd.DataFrame({"coin":c,"L":L,"H":H,"z":z.values[idx],"f":f.values[idx],"vol":vol.values[idx]}))
    R=pd.concat(res).dropna()
    R["fx"]=R.f-R.groupby(["coin","H"])["f"].transform("mean")
    R["pay"]=-np.sign(R.z)*R.fx
    R["dec"]=R.groupby(["coin","L","H"])["z"].transform(lambda s: pd.qcut(s.abs().rank(method="first"),10,labels=False))
    def agg(x):
        return pd.Series({"pay_bps":x.pay.mean()*1e4,"t":x.pay.mean()/x.pay.std()*np.sqrt(len(x)),"n":len(x)})
    out["fade payoff all bars, bps"]=R.groupby(["L","H"]).apply(agg).round(2)
    out["fade payoff top |z| decile, bps"]=R[R.dec==9].groupby(["L","H"]).apply(agg).round(2)
    T=R[(R.dec==9)].copy()
    T["vq"]=T.groupby(["coin","L","H"])["vol"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["top decile payoff by vol tercile (L,H=2,2 / 24,24)"]=T[((T.L==2)&(T.H==2))|((T.L==24)&(T.H==24))].groupby(["L","H","vq"]).apply(agg).round(2)
    return out
