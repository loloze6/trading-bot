def explore(data):
    import numpy as np, pandas as pd
    rows=[]; book=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(720,min_periods=120).std()
            vr=b["volume"]/b["volume"].rolling(720,min_periods=120).mean()
            z=r/sd
            a=b["postRebalance_current_allocation"].fillna(0)
            gross=(a*(c.shift(-1)/c-1)).sum()
            tpv=b["total_portfolio_value"]; tv=b["postRebalance_total_value"]
            book.append(dict(coin=coin,w=w,gross_sum=gross,
                             fee_sum=((tpv-tv)/tpv).sum(),
                             turnover=a.diff().abs().sum(), n=len(b),
                             share_short=(a<0).mean()))
            for h in (2,6,24):
                fr=c.shift(-h)/c-1
                idx=np.arange(0,len(b)-h,h)
                d=pd.DataFrame(dict(z=z.iloc[idx].values,vr=vr.iloc[idx].values,
                                    fr=fr.iloc[idx].values,f=b["forecast"].iloc[idx].values))
                d["h"]=h; d["coin"]=coin; rows.append(d)
    D=pd.concat(rows).dropna(subset=["z","vr","fr"])
    out={}
    bk=pd.DataFrame(book)
    out["book_gross_vs_fee_sum_by_coin"]=bk.groupby("coin")[["gross_sum","fee_sum","turnover","n"]].sum()
    out["share_bars_short"]=bk.groupby("coin")["share_short"].mean()
    for h in (2,6,24):
        d=D[D.h==h].copy()
        d["u"]=d.fr-d.groupby("coin")["fr"].transform("mean")
        d["zb"]=pd.cut(d.z,[-99,-4,-2.5,-1.5,-0.5,0.5,1.5,2.5,4,99])
        d["vb"]=pd.cut(d.vr,[0,1,2,4,999])
        g=d.groupby(["zb","vb"],observed=True)["u"].agg(["mean","count","std"])
        g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        out[f"h{h}_unusual_by_z_vol"]=g[["mean","count","t"]].round(5)
    d=D[D.h==6].copy(); d["u"]=d.fr-d.groupby("coin")["fr"].transform("mean")
    d["fb"]=pd.cut(d.f,[-21,-10,-4,-1,-0.01,0.01,21])
    g=d.groupby("fb",observed=True)["u"].agg(["mean","count","std"])
    g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["h6_unusual_by_forecast"]=g
    return out
