def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]
    coins=list(bars.keys())
    wins=sorted({w for c in coins for w in bars[c].keys()}, key=lambda s:int(s[1:]))
    rows=[]
    for c in coins:
        for w in bars[c]:
            b=bars[c][w].reset_index(drop=True)
            cl=b.close; v=b.volume
            a=b.postRebalance_current_allocation.fillna(0)
            vlog=np.log(v.rolling(30).mean()/v.shift(30).rolling(30).mean())
            df=pd.DataFrame({"c":c,"w":w,"a":a,"g":a*(cl.shift(-1)/cl-1),
                "r20":cl/cl.shift(20)-1,"r60":cl/cl.shift(60)-1,"vlog":vlog,"fc":b.forecast,
                "f5":cl.shift(-5)/cl-1,"f10":cl.shift(-10)/cl-1,"f20":cl.shift(-20)/cl-1,"pos":np.arange(len(b))})
            rows.append(df)
    X=pd.concat(rows,ignore_index=True)
    f=lambda x: pd.Series({"mean":x.mean(),"n":len(x),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    res={}
    # signal grid: direction return by depth, horizons
    S=X[(X.pos%5==0)&(X.fc!=0)].dropna(subset=["f5"]).copy()
    S["s"]=np.sign(S.fc)
    S["depth"]=pd.cut(S.r20,[-5,-0.2,-0.1,-0.05,0,5])
    out={}
    for h in ["f5","f10","f20"]:
        d=S.dropna(subset=[h])
        out[h]=d.groupby("depth").apply(lambda x: (x.s*x[h]).mean())
    out["n"]=S.groupby("depth").size()
    res["signal dir ret by depth x horizon"]=pd.DataFrame(out)
    # spread shrink vs grow (Welch) in falling grid by depth
    G=X[(X.pos%5==0)&(X.r60<-0.10)].dropna(subset=["f5","vlog","r20"]).copy()
    G["deep"]=np.where(G.r20<-0.2,"crash",np.where(G.r20<-0.05,"deep","shallow"))
    sp={}
    for k,g in G.groupby("deep"):
        gr=g[g.vlog>0].f5; sh=g[g.vlog<=0].f5
        t=stats.ttest_ind(gr,sh,equal_var=False).statistic
        sp[k]={"grow":gr.mean(),"shrink":sh.mean(),"grow-shrink":gr.mean()-sh.mean(),"t":t,"n":len(g),
               "corr vlog f5":np.corrcoef(g.vlog,g.f5)[0,1]}
    res["grow minus shrink by depth (falling)"]=pd.DataFrame(sp).T
    # approx books before costs: held positions kept only in a band of r20
    def book(mask):
        g=X.g.where(mask,0.0).fillna(0)
        rr=[]
        for w in wins:
            sub=X[X.w==w].assign(gg=g[X.w==w])
            rr.append(sub.groupby("pos").gg.mean())
        r=pd.concat(rr,ignore_index=True).fillna(0)
        val=(1+r).cumprod(); dd=(val/val.cummax()-1)
        yr=val.iloc[-1]**(365/len(r))-1
        return {"yearly":yr,"maxdd":dd.min(),"calmar":yr/abs(dd.min()),"sharpe":r.mean()/r.std()*np.sqrt(365),
                "held share":(mask&(X.a!=0)).mean()}
    held=X.a!=0
    res["approx books"]=pd.DataFrame({
        "all":book(held),
        "r20<-5%":book(held&(X.r20<-0.05)),
        "-20%<=r20<-5%":book(held&(X.r20<-0.05)&(X.r20>=-0.2)),
        "r20<-5% short only":book(held&(X.r20<-0.05)&(X.a<0)),
        "r20<-5% long only":book(held&(X.r20<-0.05)&(X.a>0))})
    # by window gain, deep held
    H=X[held&(X.r20<-0.05)]
    res["deep held gain by window"]=H.groupby("w").g.agg(["sum","count"]).reindex(wins)
    return res
