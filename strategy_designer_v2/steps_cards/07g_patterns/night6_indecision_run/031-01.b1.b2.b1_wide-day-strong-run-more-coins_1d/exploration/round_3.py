def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True).copy()
            if len(b)<30: continue
            c=b["close"]; h=b["high"]; l=b["low"]; o=b["open"]
            hl=h-l
            rm=hl/hl.rolling(20,min_periods=10).mean().shift(1)
            ret1=c/c.shift(1)-1
            vol20=ret1.rolling(20,min_periods=10).std()
            up5=(c/c.shift(5)-1>0).astype(int)
            runlen=up5.groupby((up5!=up5.shift()).cumsum()).cumsum()*up5
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"pos":np.arange(len(b)),"day":ts.dt.floor("D"),"year":ts.dt.year,
                "rm":rm,"lrm":np.log(rm),"ret5":c/c.shift(5)-1,"ret20":c/c.shift(20)-1,"vol20":vol20,
                "runlen":runlen,"fwd3":c.shift(-3)/c-1,"fwd7":c.shift(-7)/c-1,
                "dd60":c/c.rolling(60,min_periods=20).max()-1})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def cs(g,x,y="z"):
        g=g[[x,y,"day"]].dropna()
        if len(g)<50: return pd.Series({"n":len(g)})
        X=np.column_stack([np.ones(len(g)),g[x].values]); Y=g[y].values
        beta=np.linalg.lstsq(X,Y,rcond=None)[0]; e=Y-X@beta
        XtXi=np.linalg.inv(X.T@X)
        S=pd.DataFrame(X*e[:,None]).groupby(g.day.values).sum().values
        V=XtXi@(S.T@S)@XtXi; G_=len(S); n=len(g); V*=G_/(G_-1)*(n-1)/(n-2)
        return pd.Series({"n":n,"days":G_,"slope":beta[1],"t":beta[1]/np.sqrt(V[1,1])})
    def summ(g):
        n=len(g); m=g.ex.mean(); dsum=(g.ex-m).groupby(g.day).sum(); se=np.sqrt((dsum**2).sum())/n
        return pd.Series({"n":n,"days":g.day.nunique(),"mean_ex%":100*m,"t":m/se,"strength":g.z.mean()})
    out={}
    for H,col in [(3,"fwd3"),(7,"fwd7")]:
        G=D[(D.pos%H==0)&D[col].notna()].copy()
        dr=G.groupby("coin")[col].mean(); sd=G.groupby("coin")[col].std()
        G["ex"]=G[col]-G.coin.map(dr); G["z"]=G.ex/G.coin.map(sd)
        G["zr20"]=G.ret20/(G.vol20*np.sqrt(20))
        neg=G[G.zr20<0].copy(); neg["dep"]=-neg.zr20
        out[f"h{H} neg20: slope z on depth, by year"]=neg.groupby("year").apply(lambda g: cs(g,"dep"))
        out[f"h{H} neg20 excl 2022"]=cs(neg[neg.year!=2022],"dep").to_frame().T
        out[f"h{H} lrm slope by year"]=G.groupby("year").apply(lambda g: cs(g,"lrm"))
        out[f"h{H} lrm excl 2020-21"]=cs(G[~G.year.isin([2020,2021])],"lrm").to_frame().T
        G["runq"]=pd.cut(G.runlen,[-1,0,2,5,10,1000])
        out[f"h{H} by 5d-rise run length (days)"]=G.groupby("runq").apply(summ)
        G["ddq"]=pd.qcut(G.dd60,5,labels=False)
        out[f"h{H} by drawdown from 60d high quintile"]=G.groupby("ddq").apply(summ)
    return out
