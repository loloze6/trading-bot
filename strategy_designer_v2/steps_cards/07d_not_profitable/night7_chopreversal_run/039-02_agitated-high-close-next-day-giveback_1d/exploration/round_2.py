def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.copy().reset_index(drop=True)
            rng=(b["high"]-b["low"])
            cl=(b["close"]-b["low"])/rng.replace(0,np.nan)
            r1=b["close"].pct_change()
            nxt=b["close"].shift(-1)/b["close"]-1
            nxt2=b["close"].shift(-2)/b["close"]-1
            vol=r1.rolling(30,min_periods=20).std()
            relrng=(rng/b["close"])/vol
            ret60=b["close"]/b["close"].shift(60)-1
            r3=b["close"]/b["close"].shift(3)-1
            pos=b["postRebalance_current_allocation"]
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"cl":cl,"r1":r1,"nxt":nxt,"nxt2":nxt2,"relrng":relrng,
                            "agit":(b["regime"]=="unknown").values,"pos":pos,"ret60":ret60,"r3z":r3/vol,
                            "yr":ts.dt.year,"day":ts.dt.normalize(),"fc":b["forecast"],
                            "svol":b["sizing_realised_vol"],"i":np.arange(len(b))})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["cl","nxt","relrng"])
    cm=D.groupby("coin")["nxt"].mean(); D["ex"]=D["nxt"]-D["coin"].map(cm)
    cm2=D.dropna(subset=["nxt2"]).groupby("coin")["nxt2"].mean(); D["ex2"]=D["nxt2"]-D["coin"].map(cm2)
    A=D[D.agit].copy()
    rrq=A["relrng"].quantile([1/3,2/3]).values
    A["wide"]=A.relrng>rrq[1]
    A["low"]=A.cl<=0.2; A["high"]=A.cl>=0.8
    A["tr"]=np.where(A.ret60>0.1,"rising",np.where(A.ret60<-0.1,"falling","choppy"))
    def st(x,c="ex"):
        x=x[c].dropna(); return pd.Series({"n":len(x),"mean%":x.mean()*100,"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["conditions_alone_vs_with_signal"]=pd.DataFrame({
        "wide_all":st(A[A.wide]),"wide_not_low":st(A[A.wide&~A.low]),"low_wide":st(A[A.wide&A.low]),
        "low_notwide":st(A[~A.wide&A.low]),
        "falling_all":st(A[A.tr=="falling"]),"falling_notlow":st(A[(A.tr=="falling")&~A.low]),"falling_low":st(A[(A.tr=="falling")&A.low]),
        "rising_all":st(A[A.tr=="rising"]),"rising_high":st(A[(A.tr=="rising")&A.high]),
        "notrising_high":st(A[(A.tr!="rising")&A.high]),"low_all":st(A[A.low]),
        "low_all_2d":st(A[A.low],"ex2"),"lowwide_2d":st(A[A.wide&A.low],"ex2")}).T
    # graded: cl decile slope within wide vs not wide
    A["lowness"]=1-A.cl
    g=[]
    for k,X in A.groupby("wide"):
        s=np.polyfit(X.lowness,X.ex,1)[0]; g.append((k,len(X),s*100))
    out["slope_ex_on_lowness_by_wide"]=pd.DataFrame(g,columns=["wide","n","slope%"])
    # graded within low by range tercile of the low bars
    L=A[A.cl<=0.3].copy(); L["rq"]=pd.qcut(L.relrng,4,labels=False)
    out["lowclose_by_range_quartile"]=L.groupby("rq").apply(lambda x:st(x))
    # stability of low-wide by year and coin
    LW=A[A.low&A.wide]
    out["lowwide_by_year"]=LW.groupby("yr").apply(lambda x:st(x))
    out["lowwide_by_coin"]=LW.groupby("coin").apply(lambda x:st(x))
    out["highclose_by_year"]=A[A.high].groupby("yr").apply(lambda x:st(x))
    out["low_by_year"]=A[A.low].groupby("yr").apply(lambda x:st(x))
    # sizing: abs position relation
    P=D[D.pos.abs()>1e-9]
    out["pos_stats"]=pd.Series({"mean_abs_pos":P.pos.abs().mean(),"mean_abs_fc":P.fc.abs().mean(),"mean_svol":P.svol.mean(),
                                "share_fc_abs_gt2":(P.fc.abs()>2).mean()})
    # book drawdowns: daily book chained
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items(): dd.append(x.assign(coin=coin,w=w))
    DD=pd.concat(dd)
    bk=DD.groupby(["w","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).reset_index()
    bk["wn"]=bk.w.str[1:].astype(int); bk=bk.sort_values(["wn","day"]).dropna()
    v=(1+bk.br).cumprod(); dpk=v/v.cummax()-1
    bk["dd"]=dpk.values
    i=bk.dd.idxmin(); 
    out["deepest_dd%"]=float(bk.dd.min()*100)
    out["dd_by_window_min%"]=bk.groupby("w").dd.min()*100
    # book daily return by trend of coin mean
    return out
