def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; bk=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(720,min_periods=240).std()
            vr=b["volume"]/b["volume"].rolling(720,min_periods=240).mean()
            rz=r/sd
            d=pd.DataFrame({"coin":coin,"w":w,"rz":rz,"vr":vr,"sc":rz*vr,
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
                "r24z":(c/c.shift(24)-1)/(sd*np.sqrt(24)),
                "f6":c.shift(-6)/c-1,"f24":c.shift(-24)/c-1})
            d=d.iloc[::6].dropna(subset=["sc","f6","r24z"])
            rows.append(d)
            a=b["postRebalance_current_allocation"]; nr=c.shift(-1)/c-1
            bk.append(pd.DataFrame({"coin":coin,"a":a,"g":a*nr,"nr":nr}).dropna())
    E=pd.concat(rows)
    for h in ["f6","f24"]:
        E["x"+h]=E[h]-E.groupby("coin")[h].transform("mean")
    out={}
    def t1(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean%":x.mean()*100,"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    # reversal: excess 6h return in direction opposite to the hour, by year
    E["rev6"]=-np.sign(E["rz"])*E["xf6"]
    out["reversal6_by_year"]=E.groupby("yr")["rev6"].apply(t1).unstack().round(3)
    out["reversal6_by_rzbin"]=E.groupby(pd.qcut(E["rz"].abs(),5,labels=False))["rev6"].apply(t1).unstack().round(3)
    # regressions on up hours: xf6 on sc and r24z
    U=E[E["sc"]>0]
    X=np.column_stack([np.ones(len(U)),U["sc"],U["r24z"]]); y=U["xf6"].values
    beta,res,_,_=np.linalg.lstsq(X,y,rcond=None)
    e=y-X@beta; s2=e@e/(len(y)-3); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["up_hours_ols_xf6"]=pd.DataFrame({"beta%":beta*100,"t":beta/se},index=["const","sc","r24z"]).round(4)
    # down hours: xf6 on sc (negative) 
    D=E[E["sc"]<0]
    out["down_hours_corr_sc_xf6"]=pd.Series(stats.pearsonr(D["sc"],D["xf6"]),index=["r","p"])
    out["down_hours_bySc"]=D.groupby(pd.qcut(D["sc"],5,labels=False))["xf6"].apply(t1).unstack().round(3)
    B=pd.concat(bk)
    out["book_bars"]=B.groupby("coin").apply(lambda g: pd.Series({"share_long":(g["a"]>0).mean(),"mean_alloc":g["a"].mean(),
        "gain_bps":g["g"].mean()*1e4,"market_part_bps":g["a"].mean()*g["nr"].mean()*1e4})).round(4)
    return out
