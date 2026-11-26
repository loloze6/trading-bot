def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out={}
    # per-coin vol30 median over all its windows (proxy for past-year median)
    vols={}
    B={}
    for c,ws in data["bars"].items():
        allv=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            r=b["close"].pct_change()
            b["vol30"]=r.rolling(30).std()
            b["r30"]=b["close"].pct_change(30)*100
            b["ts"]=pd.to_datetime(b["timestamp"])
            B[(c,w)]=b
            allv.append(b["vol30"])
        vols[c]=pd.concat(allv).median()
    T=[]
    for c,ws in data["trades"].items():
        for w,t in ws.items():
            if not len(t): continue
            b=B[(c,w)]
            t=t.copy()
            et=pd.to_datetime(t["entry_time"])
            idx=b["ts"].searchsorted(et.values,side="right")-1
            idx=np.clip(idx,0,len(b)-1)
            t["vol30"]=b["vol30"].values[idx]; t["r30"]=b["r30"].values[idx]
            t["agit"]=t["vol30"]>vols[c]
            t["c"]=c; t["w"]=w
            T.append(t)
    T=pd.concat(T)
    def s(x):
        return pd.Series({"n":len(x),"gross":x.profit_loss_percent.mean(),"net":x.net_profit_loss_percent.mean(),
                          "t_net":stats.ttest_1samp(x.net_profit_loss_percent,0).statistic if len(x)>2 else np.nan,
                          "dur_d":x.duration_minutes.mean()/1440,"win":(x.net_profit_loss_percent>0).mean()})
    out["trades_by_agit"]=T.groupby("agit").apply(s).round(3)
    T["dbin"]=pd.cut(T["r30"],[-200,-25,-15,-8,0,200])
    out["trades_by_r30"]=T.groupby("dbin").apply(s).round(3)
    out["trades_by_agit_r30"]=T.groupby(["agit","dbin"]).apply(s).round(3)
    T["yr"]=pd.to_datetime(T["entry_time"]).dt.year
    out["trades_agit_by_year"]=T.groupby(["yr","agit"]).apply(s)[["n","net"]].round(3)
    # grid non-overlap 10d: chop & falling r30, agit vs calm, with/without signal, per window count
    recs=[]
    for (c,w),b in B.items():
        cl=b["close"].values;n=len(cl)
        for i in range(0,n,10):
            if i+10>=n: continue
            recs.append({"c":c,"w":w,"chop":b["regime"].iloc[i]=="chop","sig":b["forecast"].iloc[i]<=-2,
                         "agit":b["vol30"].iloc[i]>vols[c],"r30":b["r30"].iloc[i],"f10":cl[i+10]/cl[i]-1})
    G=pd.DataFrame(recs).dropna()
    G["s10"]=-G.f10*100
    def g(x): return pd.Series({"n":len(x),"short10":x.s10.mean(),"t":stats.ttest_1samp(x.s10,0).statistic if len(x)>2 else np.nan})
    out["grid_agit_sig"]=G.groupby(["chop","agit","sig"]).apply(g).round(3)
    out["grid_agit_sig_windows"]=G[G.chop&G.sig].groupby(["agit","w"]).apply(g)[["n","short10"]].round(2)
    # nonchop falling agitated
    out["grid_nonchop_fall_agit"]=G[(~G.chop)&(G.r30<-8)].groupby("agit").apply(g).round(3)
    return out
