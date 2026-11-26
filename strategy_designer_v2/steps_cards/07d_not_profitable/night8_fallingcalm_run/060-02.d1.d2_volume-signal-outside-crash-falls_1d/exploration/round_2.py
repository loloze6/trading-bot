def explore(data):
    import numpy as np, pandas as pd
    bars=data["bars"]; days=data["days"]
    coins=list(bars.keys())
    wins=sorted({w for c in coins for w in bars[c].keys()}, key=lambda s:int(s[1:]))
    rows=[]
    for c in coins:
        for w in bars[c]:
            b=bars[c][w].reset_index(drop=True)
            cl=b.close; v=b.volume
            a=b.postRebalance_current_allocation.fillna(0)
            lr=np.log(cl).diff()
            s30=lr.rolling(30).std()
            vlog=np.log(v.rolling(30).mean()/v.shift(30).rolling(30).mean())
            df=pd.DataFrame({"c":c,"w":w,"a":a,"g":a*(cl.shift(-1)/cl-1),
                "r20":cl/cl.shift(20)-1,"r60":cl/cl.shift(60)-1,"vlog":vlog,"fc":b.forecast,
                "s30":s30,"s30med":s30.rolling(120,min_periods=60).median(),
                "f5":cl.shift(-5)/cl-1,"f10":cl.shift(-10)/cl-1,"f20":cl.shift(-20)/cl-1,"pos":np.arange(len(b))})
            rows.append(df)
    X=pd.concat(rows,ignore_index=True)
    mu5=X[X.pos%5==0].groupby("c").f5.mean()
    X["e5"]=X.f5-X.c.map(mu5)
    f=lambda x: pd.Series({"mean":x.mean(),"n":len(x),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    res={}
    # falling profile grid, all bars (signal or not), by r20 bucket and volume sign
    G=X[(X.pos%5==0)&(X.r60<-0.10)].dropna(subset=["f5","vlog","r20"]).copy()
    G["r20b"]=pd.cut(G.r20,[-5,-0.2,-0.1,-0.05,0,5])
    G["vs"]=np.sign(G.vlog)
    res["falling: coin excess 5d by r20 x vol sign"]=G.groupby(["r20b","vs"]).e5.apply(f).unstack()
    # the condition alone: r20 bucket, regardless of volume
    res["falling: coin excess 5d by r20 alone"]=G.groupby("r20b").e5.apply(f).unstack()
    # volume tercile within moderate falls
    M=G[(G.r20>=-0.2)&(G.r20<0)].copy()
    M["vq"]=pd.qcut(M.vlog,3,labels=["shrink","mid","grow"])
    M["deep"]=np.where(M.r20<-0.05,"r20<-5%","r20>=-5%")
    res["moderate: excess 5d by depth x vol tercile"]=M.groupby(["deep","vq"]).e5.apply(f).unstack()
    # longer horizon: signal direction returns at 5,10,20 on signal grid
    S=X[(X.pos%5==0)&(X.fc!=0)].dropna(subset=["f20"]).copy()
    s=np.sign(S.fc)
    res["signal dir ret by horizon"]=pd.DataFrame({h:f(s*S[h]) for h in ["f5","f10","f20"]})
    # held bars: gain by window x agitation (s30 vs median)
    H=X[X.a!=0].copy()
    H["agit"]=np.where(H.s30>H.s30med,"agitated","calm")
    H["side"]=np.sign(H.a)
    res["held gain by agitation x side"]=H.groupby(["agit","side"]).g.agg(["mean","sum","count"])
    H["fall"]=H.w.isin(["w10","w11","w12"])
    res["held in fall windows vs rest: r20,r60,vlog"]=H.groupby(["fall","side"])[["r20","r60","vlog","g"]].mean()
    res["held gain fall windows by coin"]=H[H.fall].groupby(["c","side"]).g.sum().unstack()
    # held gain by r20 at bar, deep vs shallow, by window
    H["deep"]=H.r20<-0.05
    res["held gain by window x deep"]=H.groupby(["w","deep"]).g.sum().unstack().reindex(wins)
    # book daily with only deep (r20<-5%) held days, simple approximation
    for lab,mask in [("all",H.index==H.index),("deep only",H.deep)]:
        g=X.g.where(X.index.isin(H[mask].index),0.0)
        X["g_"+lab]=g
    out={}
    for lab in ["all","deep only"]:
        rr=[]
        for w in wins:
            sub=X[X.w==w]
            d=sub.groupby("pos")["g_"+lab].mean()
            rr.append(d)
        r=pd.concat(rr,ignore_index=True).fillna(0)
        val=(1+r).cumprod(); dd=(val/val.cummax()-1).min()
        yr=val.iloc[-1]**(365/len(r))-1
        out[lab]={"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"sharpe":r.mean()/r.std()*np.sqrt(365)}
    res["approx book before costs"]=pd.DataFrame(out)
    return res
