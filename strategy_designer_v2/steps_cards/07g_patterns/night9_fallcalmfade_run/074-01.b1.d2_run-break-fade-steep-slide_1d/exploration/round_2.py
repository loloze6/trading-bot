def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            d=df.sort_values("timestamp").reset_index(drop=True)
            c=d["close"].astype(float); o=d["open"].astype(float)
            r=c.pct_change(); nxt=c.shift(-1)/c-1; nxt2=c.shift(-2)/c-1
            n=len(d)
            tr60=c/c.shift(60)-1; ret20=c/c.shift(20)-1; ret5=c/c.shift(5)-1
            sd30=r.shift(1).rolling(30).std()
            sdy=r.rolling(30).std()
            pct=sdy.rolling(365,min_periods=120).apply(lambda a:(a<=a[-1]).mean(),raw=True)
            dn=(r<0).astype(int).values; up=(r>0).astype(int).values
            drun=np.zeros(n); urun=np.zeros(n)
            for i in range(1,n):
                drun[i]=drun[i-1]+1 if dn[i] else 0
                urun[i]=urun[i-1]+1 if up[i] else 0
            rng=(d["high"]-d["low"])/c
            clv=(c-d["low"])/(d["high"]-d["low"]).replace(0,np.nan)
            ts=pd.to_datetime(d["timestamp"])
            x=pd.DataFrame({"coin":coin,"w":w,"day":ts.dt.floor("D"),"wd":ts.dt.weekday,"year":ts.dt.year,
                "r":r,"nxt":nxt,"nxt2":nxt2,"tr60":tr60,"ret20":ret20,"ret5":ret5,"sd30":sd30,"pct":pct,
                "prev_drun":pd.Series(drun).shift(1).values,"prev_urun":pd.Series(urun).shift(1).values,
                "rng":rng,"clv":clv,"fc":d["forecast"].values,
                "alloc":d["postRebalance_current_allocation"].values})
            rows.append(x)
    X=pd.concat(rows,ignore_index=True).dropna(subset=["nxt","r","tr60","sd30"])
    X["cmean"]=X.groupby("coin")["nxt"].transform("mean")
    X["ex"]=X["nxt"]-X["cmean"]
    X["trend"]=np.where(X.tr60>0.10,"rising",np.where(X.tr60<-0.10,"falling","choppy"))
    X["agit"]=np.where(X.pct>0.5,"agit",np.where(X.pct.notna(),"calm","na"))
    X["rz"]=X.r/X.sd30
    def ct(s,days):
        g=(s-0).groupby(days).sum(); G=len(g)
        if G<3: return np.nan
        se=np.sqrt((g**2).sum()*G/(G-1))/len(s)
        return s.mean()/se if se>0 else np.nan
    def summ(gb,col="ex"):
        out={}
        for k,sub in gb:
            sub=sub.dropna(subset=[col])
            out[k]={"n":len(sub),"mean%":100*sub[col].mean(),"t_day":ct(sub[col],sub["day"]),"days":sub["day"].nunique()}
        return pd.DataFrame(out).T
    res={}
    # 1. up days in falling market graded by rz, any run
    F=X[X.trend=="falling"].copy()
    U=F[F.r>0].copy()
    U["rzb"]=pd.qcut(U.rz,5,duplicates="drop")
    res["fall_up_by_rz_quint"]=summ(U.groupby("rzb",observed=True))
    U["exz"]=U.ex/U.sd30
    sl=stats.linregress(U.rz.clip(upper=5),U.exz)
    res["fall_up_slope_exz_on_rz"]=pd.Series({"slope":sl.slope,"t":sl.slope/sl.stderr,"n":len(U)})
    # same in rising, choppy
    for tr in ["rising","choppy"]:
        V=X[(X.trend==tr)&(X.r>0)].copy(); V["exz"]=V.ex/V.sd30
        s2=stats.linregress(V.rz.clip(upper=5),V.exz)
        res[f"{tr}_up_slope"]=pd.Series({"slope":s2.slope,"t":s2.slope/s2.stderr,"n":len(V)})
    # 2. up days in falling: by close location, by agitation
    U["clvb"]=pd.cut(U.clv,[0,0.33,0.67,1.01],include_lowest=True)
    res["fall_up_by_clv"]=summ(U.groupby("clvb",observed=True))
    res["fall_upbig_rz1plus_by_agit"]=summ(U[U.rz>1].groupby("agit"))
    # 3. mirror: first down day after up run >=3 in falling
    D=X[(X.r<0)&(X.prev_urun>=3)]
    res["downbreak_run3plus_by_trend"]=summ(D.groupby("trend"))
    # 4. choppy agitated: up/down days
    CA=X[(X.trend=="choppy")&(X.agit=="agit")].copy()
    CA["sgn"]=np.where(CA.r>0,"up","down")
    res["choppy_agit_by_sign"]=summ(CA.groupby("sgn"))
    # 5. book's own cases: by coin, year, weekday
    B=X[X.fc<0]
    res["book_cases_by_year"]=summ(B.groupby("year"))
    res["book_cases_by_coin"]=summ(B.groupby("coin"))
    res["book_cases_by_rz"]=summ(B.groupby(pd.cut(B.rz,[0,0.5,1,2,99]),observed=True))
    res["book_cases_by_agit"]=summ(B.groupby("agit"))
    # 6. weekday in falling market, all days
    res["fall_by_weekday"]=summ(F.groupby("wd"))
    return res
