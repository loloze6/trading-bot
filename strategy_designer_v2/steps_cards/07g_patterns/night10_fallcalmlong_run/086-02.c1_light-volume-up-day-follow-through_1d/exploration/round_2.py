def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; v=b["volume"]
            b["ret1"]=c.pct_change()
            b["ret10p"]=c/c.shift(10)-1
            b["vr"]=v/v.shift(1).rolling(20,min_periods=15).mean()
            b["lvr"]=np.log(b["vr"])
            b["sd20"]=b["ret1"].shift(1).rolling(20,min_periods=15).std()
            b["z1"]=b["ret1"]/b["sd20"]
            b["rev"]=-b["z1"]*b["lvr"]   # positive when heavy down day or light up day
            b["fwd5"]=c.shift(-5)/c-1
            b["pos"]=np.arange(len(b))
            b["inprof"]=b["regime"].isin(["mean_reversion","unknown"])
            b["coin"]=coin; b["win"]=w; b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B=pd.concat(rows,ignore_index=True)
    drift={}
    for coin in B.coin.unique():
        g=B[(B.coin==coin)&(B.pos%5==0)]["fwd5"].dropna(); drift[coin]=g.mean()
    B["unus"]=B["fwd5"]-B["coin"].map(drift)
    def tday(df):
        s=df.groupby("day")["unus"].sum(); n=len(df); m=df.unus.mean()
        dev=df.groupby("day").apply(lambda x:(x.unus-m).sum())
        G=len(dev); se=np.sqrt((dev**2).sum()*G/(G-1))/n
        return m/se if se>0 else np.nan
    def summ(df,key):
        out=[]
        for k,g in df.groupby(key):
            out.append({"k":k,"n":len(g),"mean":round(g.unus.mean(),4),"t_day":round(tday(g),2)})
        return pd.DataFrame(out).set_index("k")
    res={}
    P=B[B.inprof & B.fwd5.notna()].dropna(subset=["lvr","z1"]).copy()
    # by offset grid, heavy down days and light down days
    tab=[]
    for off in range(5):
        G=P[P.pos%5==off]
        for lab,m in [("down_heavy",(G.ret1<0)&(G.vr>1)),("down_light",(G.ret1<0)&(G.vr<=1)),("up_heavy",(G.ret1>0)&(G.vr>1)),("up_light",(G.ret1>0)&(G.vr<=1))]:
            g=G[m]; tab.append({"off":off,"grp":lab,"n":len(g),"mean":round(g.unus.mean(),4)})
    res["offsets"]=pd.DataFrame(tab).pivot(index="off",columns="grp",values="mean")
    G=P[P.pos%5==0].copy()
    D=G[G.ret1<0].copy()
    D["q"]=pd.qcut(D["lvr"],4,labels=False)
    res["down_by_vol_q"]=summ(D,"q")
    D["q2"]=pd.qcut(D["z1"],3,labels=False)
    res["down_heavy_by_size"]=summ(D[D.vr>1],"q2")
    res["down_heavy_by_win"]=summ(D[D.vr>1],"win")
    res["down_heavy_by_coin"]=summ(D[D.vr>1],"coin")
    G["q"]=pd.qcut(G["rev"],5,labels=False)
    res["rev_q"]=summ(G,"q")
    res["rev_q_corr"]=round(G[["rev","unus"]].corr().iloc[0,1],4)
    G["q10"]=pd.qcut(G["ret10p"],4,labels=False)
    res["ret10p_by_win_top"]=summ(G[G.q10==3],"win")
    # all-bars (overlapping, rough) graded correlation of rev, for count
    res["allbars_corr_rev"]=round(P[["rev","unus"]].corr().iloc[0,1],4)
    res["allbars_n"]=len(P)
    return res
