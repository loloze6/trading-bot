def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol30=r1.rolling(30,min_periods=20).std()
            r7=c/c.shift(7)-1
            sc=r7/r7.abs().rolling(30,min_periods=20).mean()
            tr60=c/c.shift(60)-1
            agit=vol30/vol30.expanding(min_periods=30).median()
            ts=pd.to_datetime(b["timestamp"])
            for h in (1,3,7):
                fwd=c.shift(-h)/c-1
                idx=np.arange(0,len(b),h)
                rows.append(pd.DataFrame({"coin":coin,"w":w,"h":h,"day":ts.dt.floor("D").iloc[idx].values,
                    "yr":ts.dt.year.iloc[idx].values,"fwd":fwd.iloc[idx].values,
                    "r1s":(r1/vol30).iloc[idx].values,"sc":sc.iloc[idx].values,
                    "tr":tr60.iloc[idx].values,"ag":agit.iloc[idx].values}))
    D=pd.concat(rows).dropna(subset=["fwd","r1s","sc","tr"])
    D["ex"]=D["fwd"]-D.groupby(["coin","h"])["fwd"].transform("mean")
    def summ(g):
        x=g["ex"]; n=len(x)
        if n<3: return pd.Series({"n":n,"mean_ex":x.mean(),"t_day":np.nan,"days":g["day"].nunique()})
        dev=(x-x.mean()); s=dev.groupby(g["day"]).sum()
        se=np.sqrt((s**2).sum())/n
        return pd.Series({"n":n,"mean_ex":x.mean(),"t_day":x.mean()/se,"days":g["day"].nunique()})
    D["trb"]=pd.cut(D["tr"],[-np.inf,-0.1,0.1,np.inf],labels=["falling","choppy","rising"])
    D["agb"]=np.where(D["ag"]>1,"agitated","calm")
    out={}
    s=D[D.h==3]
    s=s.assign(scb=pd.cut(s["sc"],[-np.inf,-1,0,1,2,np.inf]))
    out["sc_h3_daycl"]=s.groupby("scb",observed=True).apply(summ)
    big=s[s.sc>2]
    out["sc_gt2_h3_by_trend_agit"]=big.groupby(["trb","agb"],observed=True).apply(summ)
    out["sc_gt2_h3_by_year"]=big.groupby("yr").apply(summ)
    s7=D[D.h==7]; big7=s7[s7.sc>2]
    out["sc_gt2_h7_by_trend"]=big7.groupby("trb",observed=True).apply(summ)
    r=D[(D.h==1)&(D.trb=="rising")]
    r=r.assign(rb=pd.cut(r["r1s"],[-np.inf,-2,-1,-0.3,0.3,np.inf]))
    out["rising_r1s_h1"]=r.groupby(["agb","rb"],observed=True).apply(summ)
    rc=r[(r.agb=="calm")&(r.r1s<=-1)]
    out["rising_calm_fall_h1_by_year"]=rc.groupby("yr").apply(summ)
    out["rising_calm_fall_h1_by_coin"]=rc.groupby("coin").apply(summ)
    rr=r[r.r1s<0]
    out["rising_slope"]=pd.Series({"corr":np.corrcoef(-rr["r1s"],rr["ex"])[0,1],"n":len(rr)})
    return out
