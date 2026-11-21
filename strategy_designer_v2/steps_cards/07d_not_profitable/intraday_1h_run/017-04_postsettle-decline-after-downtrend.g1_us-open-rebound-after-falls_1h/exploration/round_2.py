def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True).copy()
            ts=pd.to_datetime(b["timestamp"]); cl=b["close"].values
            idx=np.where((ts.dt.hour==11).values & (b["forecast"].fillna(0).values>0))[0]
            for i in idx:
                r={}
                for h in [1,2,3,5,9,13,25]:
                    r[f"r{h}"]=cl[i+h]/cl[i]-1 if i+h<len(cl) else np.nan
                r["r_1to2"]=cl[i+2]/cl[i+1]-1 if i+2<len(cl) else np.nan
                r["fc"]=b["forecast"].iloc[i]; r["a"]=b["postRebalance_current_allocation"].iloc[i]
                r["fall72"]=cl[i]/cl[i-72]-1 if i>=72 else np.nan
                r["ret24"]=cl[i]/cl[i-24]-1 if i>=24 else np.nan
                r["c"]=c; r["wd"]=ts.iloc[i].weekday()
                rows.append(r)
    D=pd.DataFrame(rows)
    D["fq"]=pd.qcut(D["fc"],5,labels=False,duplicates="drop")
    cols=["r1","r_1to2","r2","r3","r5","r9","r13","r25"]
    byfq=D.groupby("fq")[cols+["fc","a"]].mean()*1
    byfq["n"]=D.groupby("fq").size()
    D["dq"]=pd.qcut(D["fall72"],5,labels=False,duplicates="drop")
    bydepth=D.groupby("dq")[["fall72","r2","r_1to2","r13","r25"]].mean(); bydepth["n"]=D.groupby("dq").size()
    D["q24"]=pd.qcut(D["ret24"],5,labels=False,duplicates="drop")
    by24=D.groupby("q24")[["ret24","r2","r_1to2","r25"]].mean(); by24["n"]=D.groupby("q24").size()
    tt={h:stats.ttest_1samp(D[h].dropna(),0).statistic for h in cols}
    bywd=D.groupby("wd")[["r2"]].mean(); bywd["n"]=D.groupby("wd").size()
    return {"byfq":byfq,"bydepth":bydepth,"by24":by24,"t_raw":pd.Series(tt),"bywd":bywd,"n":len(D)}
