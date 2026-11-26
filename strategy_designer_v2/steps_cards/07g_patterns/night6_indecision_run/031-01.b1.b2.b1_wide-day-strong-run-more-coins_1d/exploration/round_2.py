def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True).copy()
            if len(b)<30: continue
            c=b["close"]; o=b["open"]; h=b["high"]; l=b["low"]
            hl=(h-l)
            rm=hl/hl.rolling(20,min_periods=10).mean().shift(1)
            ret1=c/c.shift(1)-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),"day":ts.dt.floor("D"),"year":ts.dt.year,
                "rm":rm,"ret5":c/c.shift(5)-1,"ret20":c/c.shift(20)-1,"ret60":c/c.shift(60)-1,
                "clv":(c-l)/hl.replace(0,np.nan),"vol20":ret1.rolling(20,min_periods=10).std(),
                "fwd3":c.shift(-3)/c-1,"fwd7":c.shift(-7)/c-1,"fc":b["forecast"],
                "alloc":b["postRebalance_current_allocation"],"ret1":ret1})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    def clus_slope(g,x,y):
        g=g[[x,y,"day"]].dropna()
        X=np.column_stack([np.ones(len(g)),g[x].values]); Y=g[y].values
        beta=np.linalg.lstsq(X,Y,rcond=None)[0]; e=Y-X@beta
        XtXi=np.linalg.inv(X.T@X)
        S=pd.DataFrame(X*e[:,None]).groupby(g.day.values).sum().values
        V=XtXi@(S.T@S)@XtXi; G_=len(S); n=len(g)
        V*=G_/(G_-1)*(n-1)/(n-2)
        return pd.Series({"n":n,"days":G_,"slope":beta[1],"t":beta[1]/np.sqrt(V[1,1])})
    for H,col in [(3,"fwd3"),(7,"fwd7")]:
        G=D[(D.pos%H==0)&D[col].notna()].copy()
        dr=G.groupby("coin")[col].mean(); sd=G.groupby("coin")[col].std()
        G["ex"]=G[col]-G.coin.map(dr); G["z"]=G.ex/G.coin.map(sd)
        G["clvc"]=G.clv-0.5
        G["rm_clv"]=(G.rm-1)*G.clvc
        G["zr20"]=G.ret20/(G.vol20*np.sqrt(20))
        G["zr5"]=G.ret5/(G.vol20*np.sqrt(5))
        G["zr60"]=G.ret60/(G.vol20*np.sqrt(60))
        res={}
        for x in ["zr5","zr20","zr60","rm","clvc","rm_clv","vol20"]:
            res[x]=clus_slope(G,x,"z")
        up=G[G.ret5>0]; dn=G[G.ret5<0]
        res["up: rm_clv"]=clus_slope(up,"rm_clv","z")
        res["dn: rm_clv"]=clus_slope(dn,"rm_clv","z")
        res["up: clvc"]=clus_slope(up,"clvc","z")
        res["dn: clvc"]=clus_slope(dn,"clvc","z")
        wide=G[G.rm>G.rm.quantile(0.67)]
        res["wide: clvc"]=clus_slope(wide,"clvc","z")
        res["narrow: clvc"]=clus_slope(G[G.rm<G.rm.quantile(0.33)],"clvc","z")
        res["pos zr20: zr20"]=clus_slope(G[G.zr20>0],"zr20","z")
        res["neg zr20: zr20"]=clus_slope(G[G.zr20<0],"zr20","z")
        out[f"slopes of z on x, h={H}"]=pd.DataFrame(res).T
    # yearly split of key slopes h=3
    G=D[(D.pos%3==0)&D.fwd3.notna()].copy()
    dr=G.groupby("coin").fwd3.mean(); sd=G.groupby("coin").fwd3.std()
    G["z"]=(G.fwd3-G.coin.map(dr))/G.coin.map(sd); G["clvc"]=G.clv-0.5; G["rm_clv"]=(G.rm-1)*G.clvc
    G["zr20"]=G.ret20/(G.vol20*np.sqrt(20))
    out["by year: slope z on rm_clv"]=G.groupby("year").apply(lambda g: clus_slope(g,"rm_clv","z"))
    out["by year: slope z on zr20"]=G.groupby("year").apply(lambda g: clus_slope(g,"zr20","z"))
    # book: daily returns, position contribution
    dd=[]
    for coin,wins in data["days"].items():
        for w,t in wins.items():
            t=t.copy(); t["coin"]=coin; t["win"]=w; dd.append(t)
    DD=pd.concat(dd,ignore_index=True)
    DD["year"]=pd.to_datetime(DD.day).dt.year
    bk=DD.groupby(["day"]).agg(br=("book_return","mean"),cr=("coin_return","mean"),year=("year","first"))
    out["book by year"]=bk.groupby("year").apply(lambda g: pd.Series({"days":len(g),"book_mean%":100*g.br.mean(),"hold_mean%":100*g.cr.mean(),"book_sharpe":g.br.mean()/g.br.std()*np.sqrt(365)}))
    # trades
    tr=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): t=t.copy(); t["coin"]=coin; tr.append(t)
    T=pd.concat(tr,ignore_index=True)
    T["dur_d"]=T.duration_minutes/1440
    T["dq"]=pd.cut(T.dur_d,[0,3.5,7,14,30,1e5])
    out["trades by duration"]=T.groupby("dq").agg(n=("net_profit_loss_percent","size"),mean_net=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda s:(s>0).mean()),total=("net_profit_loss_percent","sum"))
    T["eq"]=pd.cut(T.entry_forecast,[-0.1,5,10,15,20.1])
    out["trades by entry forecast"]=T.groupby("eq").agg(n=("net_profit_loss_percent","size"),mean_net=("net_profit_loss_percent","mean"),med=("net_profit_loss_percent","median"))
    return out
