def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]
    H=[5,7,10,14,20]
    drift={}
    for c,ws in bars.items():
        for h in H:
            rs=[]
            for w,df in ws.items():
                cl=df["close"].values
                for i in range(0,len(cl)-h,h):
                    rs.append(cl[i+h]/cl[i]-1)
            drift[(c,h)]=np.mean(rs) if rs else np.nan
    out={}
    def clus_t(v,days):
        s=pd.Series(v).groupby(np.asarray(days)).sum()
        D=len(s); n=len(v); m=np.mean(v)
        dev=(pd.Series(v)-m).groupby(np.asarray(days)).sum()
        se=np.sqrt((dev**2).sum()*D/(D-1))/n if D>1 else np.nan
        return m, m/se if se else np.nan, D
    summ={}; grade={}; byq={}; bywin={}
    for h in H:
        rows=[]
        for c,ws in bars.items():
            for w,df in ws.items():
                cl=df["close"].values; n=len(cl); reg=df["regime"].values; fc=df["forecast"].values
                ts=pd.to_datetime(df["timestamp"]).dt.floor("D").values
                raw=pd.to_numeric(df["debug_info.components.fall30.last_history_value"],errors="coerce").values if "debug_info.components.fall30.last_history_value" in df else np.full(n,np.nan)
                for i in range(0,n-h,h):
                    if reg[i]!="unknown": continue
                    r30=raw[i]
                    if np.isnan(r30) and i>=30: r30=(cl[i]/cl[i-30]-1)*100
                    if np.isnan(r30) or r30>=0: continue
                    rows.append({"day":ts[i],"coin":c,"wn":int(w[1:]),"r30":r30,"fc":fc[i],
                                 "c":-(cl[i+h]/cl[i]-1-drift[(c,h)]),"tot":-(cl[i+h]/cl[i]-1)})
        X=pd.DataFrame(rows)
        m,t,D=clus_t(X.c.values,X.day.values)
        summ[f"h{h}"]={"n":len(X),"days":D,"mean_unusual":m,"t":t,"mean_total":X.tot.mean(),
                       "spearman_r30_vs_cont":stats.spearmanr(-X.r30,X.c)[0],
                       "spearman_fc_vs_cont":stats.spearmanr(-X.fc,X.c)[0]}
        X["deep"]=np.where(X.r30<-10,"deep<-10","shallow")
        for k,g in X.groupby("deep"):
            m,t,D=clus_t(g.c.values,g.day.values)
            byq[(f"h{h}",k)]={"n":len(g),"days":D,"mean":m,"t":t}
        X["third"]=pd.qcut(X.r30.rank(method="first"),3,labels=["deepest","mid","shallowest"])
        for k,g in X.groupby("third"):
            m,t,D=clus_t(g.c.values,g.day.values)
            grade[(f"h{h}",k)]={"n":len(g),"mean":m,"t":t,"r30_mean":g.r30.mean()}
        if h in (5,10):
            X["yrgrp"]=pd.cut(X.wn,[6,10,14,18],labels=["w7-10","w11-14","w15-18"])
            for k,g in X.groupby("yrgrp"):
                m,t,D=clus_t(g.c.values,g.day.values) if len(g)>2 else (np.nan,np.nan,0)
                bywin[(f"h{h}",k)]={"n":len(g),"mean":m,"t":t}
    out["fall side, non-overlap, clustered t"]=pd.DataFrame(summ).T
    out["deep vs shallow fall"]=pd.DataFrame(byq).T
    out["thirds by raw r30"]=pd.DataFrame(grade).T
    out["by window group"]=pd.DataFrame(bywin).T
    return out
