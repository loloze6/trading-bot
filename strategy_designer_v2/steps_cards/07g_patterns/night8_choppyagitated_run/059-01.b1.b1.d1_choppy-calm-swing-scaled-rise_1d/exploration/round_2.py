def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol30=r1.rolling(30,min_periods=20).std()
            tr60=c/c.shift(60)-1
            agit=vol30/vol30.expanding(min_periods=30).median()
            volr=vol30/vol30.rolling(60,min_periods=30).median()
            ts=pd.to_datetime(b["timestamp"])
            for h in (1,2,7):
                fwd=c.shift(-h)/c-1
                idx=np.arange(0,len(b),h)
                rows.append(pd.DataFrame({"coin":coin,"w":w,"h":h,"day":ts.dt.floor("D").iloc[idx].values,
                    "yr":ts.dt.year.iloc[idx].values,"fwd":fwd.iloc[idx].values,
                    "r1s":(r1/vol30).iloc[idx].values,"tr":tr60.iloc[idx].values,
                    "ag":agit.iloc[idx].values,"volr":volr.iloc[idx].values}))
    D=pd.concat(rows).dropna(subset=["fwd","r1s"])
    D["ex"]=D["fwd"]-D.groupby(["coin","h"])["fwd"].transform("mean")
    def summ(g):
        x=g["ex"]; n=len(x)
        if n<3: return pd.Series({"n":n,"mean_ex":x.mean(),"t_day":np.nan,"days":g["day"].nunique()})
        dev=(x-x.mean()); s=dev.groupby(g["day"]).sum()
        se=np.sqrt((s**2).sum())/n
        return pd.Series({"n":n,"mean_ex":x.mean(),"t_day":x.mean()/se,"days":g["day"].nunique()})
    out={}
    D["r1b"]=pd.cut(D["r1s"],[-np.inf,-2,-1,-0.3,0.3,1,2,np.inf])
    D["trb"]=pd.cut(D["tr"],[-np.inf,-0.1,0.1,np.inf],labels=["falling","choppy","rising"])
    D["agb"]=np.where(D["ag"]>1,"agitated","calm")
    for h in (1,2):
        s=D[D.h==h]
        out[f"r1s_h{h}_daycl"]=s.groupby("r1b",observed=True).apply(summ)
        f=s[s.r1s<=-1]
        out[f"fall_le_-1_h{h}_by_trend_agit"]=f.groupby(["trb","agb"],observed=True).apply(summ)
        out[f"fall_le_-1_h{h}_by_year"]=f.groupby("yr").apply(summ)
        out[f"fall_le_-1_h{h}_by_coin"]=f.groupby("coin").apply(summ)
    s=D[(D.h==1)&(D.r1s<0)]
    out["slope_h1_on_fall"]=pd.Series({"corr":np.corrcoef(-s["r1s"],s["ex"])[0,1],"n":len(s)})
    s=D[D.h==7].dropna(subset=["volr"])
    s=s.assign(vq=pd.qcut(s["volr"],4,labels=False))
    out["volr_h7_by_year_lowq"]=s[s.vq==0].groupby("yr").apply(summ)
    out["volr_h7_daycl"]=s.groupby("vq").apply(summ)
    return out
