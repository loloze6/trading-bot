def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=168
    rows=[]; hr=[]; days=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].astype(float).values; v=b["volume"].astype(float).values
            n=len(c)
            if n<H*2: continue
            s=pd.Series(c); lr=np.log(s).diff()
            ret720=s/s.shift(720)-1
            ret168=s/s.shift(168)-1
            ret24=s/s.shift(24)-1
            vol=lr.rolling(168,min_periods=120).std()
            hi=s.rolling(1440,min_periods=720).max(); dist=1-s/hi
            vr=pd.Series(v).rolling(24).mean()/pd.Series(v).rolling(720,min_periods=240).mean()
            fc=b["forecast"].astype(float).values
            for i in range(0,n-H,H):
                rows.append(dict(coin=coin,w=w,fwd=c[i+H]/c[i]-1,fc=fc[i],r720=ret720.iloc[i],r168=ret168.iloc[i],
                    r24=ret24.iloc[i],vol=vol.iloc[i],dist=dist.iloc[i],vr=vr.iloc[i]))
            ts=pd.to_datetime(b["timestamp"])
            hr.append(pd.DataFrame({"h":ts.dt.hour.values,"r":lr.values,"pos":b["postRebalance_current_allocation"].astype(float).shift(1).values}))
        for w,d in data["days"][coin].items():
            dd=d.copy(); dd["coin"]=coin; dd["w"]=w; days.append(dd)
    g=pd.DataFrame(rows)
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    out={}
    def tab(df,col,q=5):
        d=df.dropna(subset=[col,"ex"]).copy()
        d["b"]=pd.qcut(d[col].rank(method="first"),q,labels=False)
        r=d.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("ex","size"),mean=("ex","mean"),sd=("ex","std"))
        r["t"]=r["mean"]/(r["sd"]/np.sqrt(r["n"]));return r.drop(columns="sd")
    up=g[g.r720>0]; dn=g[g.r720<=0]
    for col in ["r168","r24","vol","dist","vr"]:
        out[f"up_{col}"]=tab(up,col); out[f"dn_{col}"]=tab(dn,col)
    out["fc_pos"]=tab(g[g.fc>0],"fc")
    out["flat_vs_on"]=g.assign(on=g.fc>0).groupby("on")["ex"].agg(["size","mean","std"])
    h=pd.concat(hr).dropna()
    hh=h.groupby("h")["r"].agg(["size","mean","std"]); hh["t"]=hh["mean"]/(hh["std"]/np.sqrt(hh["size"]))
    out["hour_logret"]=hh[["size","mean","t"]]
    D=pd.concat(days); D["day"]=pd.to_datetime(D["day"])
    D["wd"]=D["day"].dt.weekday; D["yr"]=D["day"].dt.year
    dd=D.dropna(subset=["book_return","coin_return"])
    wd=dd.groupby("wd").agg(n=("coin_return","size"),coin=("coin_return","mean"),csd=("coin_return","std"),book=("book_return","mean"))
    wd["t_coin"]=wd["coin"]/(wd["csd"]/np.sqrt(wd["n"])); out["weekday"]=wd.drop(columns="csd")
    bk=dd.groupby("day")[["book_return","coin_return"]].mean().reset_index()
    bk["yr"]=bk["day"].dt.year
    out["book_by_year"]=bk.groupby("yr").agg(n=("book_return","size"),book=("book_return","mean"),coin=("coin_return","mean"),bsd=("book_return","std"))
    return out
