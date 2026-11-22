def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(720,min_periods=240).std()
            vr=b["volume"]/b["volume"].rolling(720,min_periods=240).mean()
            rz=r/sd
            d=pd.DataFrame({"coin":coin,"w":w,"rz":rz,"vr":vr,"sc":rz*vr,
                            "fc":b["forecast"],
                            "tr":c/c.shift(720)-1,"r24":c/c.shift(24)-1})
            for h in [1,2,3,6,12,24]:
                d[f"f{h}"]=c.shift(-h)/c-1
            d["cell"]=np.arange(len(b))//6
            d["abssc"]=d["sc"].abs()
            d=d.dropna(subset=["sc","f6"])
            # per cell, bar with largest |score|
            idx=d.groupby("cell")["abssc"].idxmax()
            rows.append(d.loc[idx])
    E=pd.concat(rows)
    # drift per coin per horizon
    for h in [1,2,3,6,12,24]:
        E[f"x{h}"]=E[f"f{h}"]-E.groupby("coin")[f"f{h}"].transform("mean")
    E["usual"]=E.groupby("coin")["f6"].transform("std")
    def tab(g):
        o={}
        o["n"]=len(g)
        for h in [1,3,6,24]:
            x=g[f"x{h}"].dropna(); o[f"x{h}%"]=x.mean()*100; o[f"t{h}"]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        return pd.Series(o)
    E["scbin"]=pd.qcut(E["sc"],[0,.01,.05,.2,.5,.8,.95,.99,1],labels=False)
    out={}
    out["by_signed_score_bin"]=E.groupby("scbin").apply(tab).round(3)
    big=E[E["rz"].abs()>3].copy()
    big["dir"]=np.sign(big["rz"])
    big["vrbin"]=pd.cut(big["vr"],[0,1,2,3,5,100])
    out["bigmove_dir_by_volratio"]=big.groupby(["dir","vrbin"]).apply(tab).round(3)
    up=E[E["sc"]>E["sc"].quantile(.95)].copy()
    up["trend"]=np.where(up["tr"]>0,"up30d","down30d")
    out["top5pct_by_trend"]=up.groupby(["coin","trend"]).apply(tab).round(3)
    up["r24b"]=pd.qcut(up["r24"],4,labels=False)
    out["top5pct_by_prior24h"]=up.groupby("r24b").apply(tab).round(3)
    # book side
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()])
    out["trades"]=pd.Series({"n":len(tr),"gross_mean%":tr["profit_loss_percent"].mean(),
        "net_mean%":tr["net_profit_loss_percent"].mean(),"dur_h":tr["duration_minutes"].mean()/60,
        "win_gross":(tr["profit_loss_percent"]>0).mean()})
    dd=pd.concat([d.assign(coin=c,w=w) for c,ws in data["days"].items() for w,d in ws.items()])
    out["book_by_window"]=dd.groupby("w")[["book_return","coin_return"]].mean().mul(100).round(3).T
    return out
