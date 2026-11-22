def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # daily book returns by window, mean over coins
    rows=[]
    for c,ws in data["days"].items():
        for w,d in ws.items():
            d=d.dropna(subset=["book_return"])
            rows.append(pd.DataFrame({"c":c,"w":w,"day":d["day"].values,"b":d["book_return"].values,"h":d["coin_return"].values}))
    D=pd.concat(rows)
    P=D.groupby(["w","day"])[["b","h"]].mean().reset_index()
    def sh(x): return x.mean()/x.std()*np.sqrt(365)
    pw=P.groupby("w").agg(book_mean=("b","mean"),hold_mean=("h","mean"),book_sum=("b","sum"),n=("b","size"))
    pw["book_sh"]=P.groupby("w")["b"].apply(sh)
    pw["hold_sh"]=P.groupby("w")["h"].apply(sh)
    out["per_window"]=pw.round(5)
    out["per_coin_book_mean"]=D.groupby("c")[["b","h"]].mean()
    # cases
    cs=[]
    for c,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            cl=b["close"].values
            r=cl[48::48]/cl[:-48:48]-1 if len(cl)>96 else np.array([])
            allr.append(r)
        drift=np.nanmean(np.concatenate(allr))
        for w,b in ws.items():
            ts=pd.to_datetime(b["timestamp"])
            cl=b["close"].values
            n=len(b)
            idx=np.where((ts.dt.dayofweek==6)&(ts.dt.hour==23))[0]
            for i in idx:
                if i+48>=n or i<720: continue
                f=b["forecast"].iloc[i]
                fwd=cl[i+48]/cl[i]-1
                wk=cl[i]/cl[i-48]-1
                r30=cl[i-48]/cl[i-720]-1
                r7=cl[i-48]/cl[i-216]-1
                lr=np.diff(np.log(cl[i-216:i+1]))
                vr=lr[-48:].std()/lr[:168].std()
                cs.append(dict(c=c,w=w,f=f,fwd=fwd,ex=-(fwd-drift),tot=-fwd,wk=wk,r30=r30,r7=r7,vr=vr,
                               alloc=b["postRebalance_current_allocation"].iloc[i],yr=ts.iloc[i].year))
    C=pd.DataFrame(cs)
    out["all_sundays_n"]=len(C)
    S=C[C.f<0].copy()
    out["short_cases"]=len(S)
    def g(df,key):
        x=df.groupby(key).agg(n=("tot","size"),tot_short=("tot","mean"),ex_short=("ex","mean"),
                              t=("tot",lambda v: v.mean()/v.std()*np.sqrt(len(v))),alloc=("alloc","mean"))
        return x.round(4)
    S["fq"]=pd.qcut(S.f.abs(),5,labels=False)
    out["by_forecast_q"]=g(S,"fq")
    S["r30q"]=pd.qcut(S.r30,5,labels=False)
    out["by_prior30d_ret_q"]=g(S,"r30q")
    S["wkq"]=pd.qcut(S.wk,5,labels=False)
    out["by_weekend_ret_q"]=g(S,"wkq")
    S["vrq"]=pd.qcut(S.vr,5,labels=False)
    out["by_volratio_q"]=g(S,"vrq")
    out["by_year"]=g(S,"yr")
    out["by_window"]=g(S,"w")
    # all weekends incl rises: sign of weekend vs next 48h
    C["wkq"]=pd.qcut(C.wk,10,labels=False)
    out["all_weekends_by_wk_decile_fwd_mean"]=C.groupby("wkq").agg(n=("fwd","size"),wk=("wk","mean"),fwd=("fwd","mean")).round(4)
    return out
