def explore(data):
    import numpy as np, pandas as pd
    bars=data["bars"]; days=data["days"]; trades=data["trades"]
    out={}
    def summ(s):
        s=pd.Series(s).dropna(); n=len(s)
        return pd.Series(dict(n=n,mean=s.mean() if n else np.nan,t=s.mean()/(s.std()/np.sqrt(n)) if n>2 else np.nan))
    res={}
    for H in (7,14,28):
        drift={}
        for c in bars:
            rr=[]
            for w,df in bars[c].items():
                cl=df["close"].values
                rr+= [cl[i+H]/cl[i]-1 for i in range(0,len(df)-H,H)]
            drift[c]=np.mean(rr) if rr else np.nan
        rows=[]
        for c in bars:
            for w,df in bars[c].items():
                df=df.reset_index(drop=True); cl=pd.Series(df["close"].values)
                r7=cl.pct_change(7); sc=r7/(r7.abs().rolling(30).mean())
                r60=cl.pct_change(60); r30=cl.pct_change(30)
                dr=cl.pct_change(); v30=dr.rolling(30).std(); v7=dr.rolling(7).std()
                f=df["forecast"].fillna(0).values; reg=df["regime"].values
                for i in range(0,len(df)-H,H):
                    fr=cl[i+H]/cl[i]-1
                    rows.append(dict(coin=c,w=w,f=f[i],inprof=reg[i]=="unknown",sc=sc[i],r60=r60[i],r30=r30[i],
                        vr=v7[i]/v30[i] if v30[i]>0 else np.nan,fr=fr,un=fr-drift[c]))
        res[H]=pd.DataFrame(rows)
    g=res[14]; ip=g[g.inprof]
    hz=[]
    for H,G in res.items():
        I=G[G.inprof]
        for lab,m in [("sc>1",I.sc>1),("sc0-1",(I.sc>0)&(I.sc<=1)),("sc<=0",I.sc<=0)]:
            s=summ(I[m].un); s["H"]=H; s["case"]=lab; hz.append(s)
    out["horizon_by_strength"]=pd.DataFrame(hz)
    # r30 condition: alone vs with signal
    tab=[]
    for lab,m in [("r30>0 & sc>1",(ip.r30>0)&(ip.sc>1)),("r30>0 & sc<=0",(ip.r30>0)&(ip.sc<=0)),
                  ("r30<=0 & sc>1",(ip.r30<=0)&(ip.sc>1)),("r30<=0 & sc<=0",(ip.r30<=0)&(ip.sc<=0)),
                  ("r60>0 & sc>1",(ip.r60>0)&(ip.sc>1)),("r60<=0 & sc>1",(ip.r60<=0)&(ip.sc>1)),
                  ("r60>0 & sc<=0",(ip.r60>0)&(ip.sc<=0)),
                  ("vr>1 & sc>1",(ip.vr>1)&(ip.sc>1)),("vr<=1 & sc>1",(ip.vr<=1)&(ip.sc>1))]:
        s=summ(ip[m].un); s["case"]=lab; tab.append(s)
    out["conditions_14d_inprofile"]=pd.DataFrame(tab)
    # trades: weak vs strong entry, in falls windows
    tr=[]
    for c in trades:
        for w,t in trades[c].items():
            t=t.copy(); t["w"]=w; tr.append(t)
    T=pd.concat(tr)
    T["strong"]=T.entry_forecast>=7
    T["fallw"]=T.w.isin(["w7","w9","w12","w13","w14","w15"])
    out["trades_strong_by_fallwindows"]=T.groupby(["fallw","strong"]).agg(n=("net_profit_loss_percent","size"),net=("net_profit_loss_percent","mean"),med=("net_profit_loss_percent","median"),sumnet=("net_profit_loss_percent","sum"))
    # book contribution by entry strength: share of losses
    out["trades_net_sum_by_strength"]=T.groupby("strong")["net_profit_loss_percent"].agg(["size","sum","mean"])
    return out
