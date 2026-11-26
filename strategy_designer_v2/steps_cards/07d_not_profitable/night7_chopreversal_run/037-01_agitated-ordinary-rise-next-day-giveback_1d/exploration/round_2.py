def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; r=c.pct_change(); sd=r.rolling(30).std()
            vsr=r/sd
            n1=c.shift(-1)/c-1; n2=c.shift(-2)/c-1
            tr60=c/c.shift(60)-1
            pos=b["postRebalance_current_allocation"]
            d=pd.DataFrame({"coin":coin,"w":w,"regime":b["regime"],"vsr":vsr,"n1":n1,"n2":n2,"tr60":tr60,
                            "pos":pos,"gain":pos*n1,"i":np.arange(len(b)),"year":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    dr1=D.groupby("coin")["n1"].mean(); D["ex1"]=D["n1"]-D["coin"].map(dr1)
    # two-day on grid: positions 0,2,4 per window
    dr2=D[D.i%2==0].groupby("coin")["n2"].mean(); D["ex2"]=D["n2"]-D["coin"].map(dr2)
    D["agit"]=np.where(D.regime=="chop","calm","agit")
    D["trend"]=pd.cut(D.tr60,[-50,-0.1,0.1,50],labels=["falling","choppy","rising"])
    D["sig"]=np.where((D.vsr>0)&(D.vsr<=1),"rise_in_swing","other")
    def tab(X,col):
        g=X.dropna(subset=[col,"trend"]).groupby(["agit","trend","sig"],observed=True)[col]
        m=-g.mean(); s=g.std(); n=g.size()
        return pd.DataFrame({"n":n,"short_ex":m,"t":m/(s/np.sqrt(n))})
    out={}
    out["1d short ex: agit x trend x signal"]=tab(D,"ex1")
    out["2d short ex (grid) agit x trend x signal"]=tab(D[D.i%2==0],"ex2")
    # grading inside agitated falling/choppy
    S=D[(D.agit=="agit")&(D.sig=="rise_in_swing")].dropna(subset=["ex1","trend"]).copy()
    S["vb"]=pd.cut(S.vsr,[0,0.33,0.66,1.0])
    g=S.groupby(["trend","vb"],observed=True)["ex1"]
    out["grading: agit signal, trend x vsr third"]=pd.DataFrame({"n":g.size(),"short_ex":-g.mean(),"t":-g.mean()/(g.std()/np.sqrt(g.size()))})
    # by year in agit falling signal
    F=S[S.trend!="rising"]
    g=F.groupby("year")["ex1"]
    out["agit non-rising signal short ex by year"]=pd.DataFrame({"n":g.size(),"short_ex":-g.mean()})
    # book daily return by trend of coin
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    Dd=pd.concat(dd)
    out["book daily return mean/std per coin-day"]=pd.Series({"mean":Dd.book_return.mean(),"std":Dd.book_return.std(),"n":Dd.book_return.notna().sum()})
    # position gain by trend in regime MR vs other
    P=D[D.pos.abs()>1e-9].dropna(subset=["n1","trend"])
    g=P.groupby(["trend","regime"],observed=True)["gain"]
    out["pos gain sum by trend x regime"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"sum":g.sum()})
    return out
