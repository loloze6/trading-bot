def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.sort_values("timestamp").reset_index(drop=True)
            c=df["close"].astype(float)
            fwd=c.shift(-20)/c-1
            sma50=c.rolling(50,min_periods=30).mean()
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(df)),"year":pd.to_datetime(df["timestamp"]).dt.year,
                "fc":df["forecast"].astype(float),"fwd":fwd,
                "above50":(c>sma50).where(sma50.notna())})
            rows.append(d.iloc[::20])
    D=pd.concat(rows).dropna(subset=["fwd","fc"])
    D["ex"]=D["fwd"]-D.groupby("coin")["fwd"].transform("mean")
    # market-relative: subtract the cross-coin mean fwd at the same window & position
    D["mkt"]=D.groupby(["w","pos"])["fwd"].transform("mean")
    D["rel"]=D["fwd"]-D["mkt"]
    def st(g,col):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out={}
    A=D.dropna(subset=["above50"]).copy()
    A["grp"]=np.where((A.fc>0)&(A.above50==True),"long_up",np.where((A.fc<0)&(A.above50==False),"short_down","mixed"))
    out["grp_ex"]=A.groupby("grp").apply(lambda g:st(g,"ex"))
    out["grp_rel"]=A.groupby("grp").apply(lambda g:st(g,"rel"))
    LU=A[A.grp=="long_up"]
    out["longup_ex_by_coin"]=LU.groupby("coin").apply(lambda g:st(g,"ex"))
    out["longup_ex_by_year"]=LU.groupby("year").apply(lambda g:st(g,"ex"))
    LU2=LU.copy(); LU2["strong"]=LU2.fc>=10
    out["longup_by_strength"]=LU2.groupby("strong").apply(lambda g:st(g,"ex"))
    B=D[D.fc<=-12]
    out["deepdrop_ex"]=st(B,"ex"); out["deepdrop_rel"]=st(B,"rel")
    out["deepdrop_by_coin"]=B.groupby("coin").apply(lambda g:st(g,"ex"))
    out["deepdrop_by_year"]=B.groupby("year").apply(lambda g:st(g,"ex"))
    out["above50_all_ex"]=A.groupby("above50").apply(lambda g:st(g,"ex"))
    D["q"]=pd.qcut(D.fc,5,labels=False)
    out["q_rel"]=D.groupby("q").apply(lambda g:st(g,"rel"))
    out["share_var_market"]=float(D["mkt"].var()/D["fwd"].var())
    return out
