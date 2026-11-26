def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=14
    bars=data["bars"]; days=data["days"]
    rows=[]
    for c in bars:
        # normal drift
        allr=[]
        for w,df in bars[c].items():
            cl=df["close"].values
            for i in range(0,len(cl)-H,H):
                allr.append(cl[i+H]/cl[i]-1)
        drift=np.mean(allr) if allr else np.nan
        sd=np.std(allr,ddof=1) if len(allr)>1 else np.nan
        for w,df in bars[c].items():
            df=df.reset_index(drop=True)
            cl=df["close"]; vol=df["volume"]
            r14=cl/cl.shift(14)-1; r60=cl/cl.shift(60)-1
            ratio=vol.rolling(14).mean()/vol.rolling(30).mean()-1
            r7=cl/cl.shift(7)-1
            for i in range(0,len(df)-H,H):
                fr=cl.iloc[i+H]/cl.iloc[i]-1
                rows.append(dict(coin=c,w=w,i=i,ts=df["timestamp"].iloc[i],f=df["forecast"].iloc[i],
                    alloc=df["postRebalance_current_allocation"].iloc[i],fr=fr,un=fr-drift,usd=sd,
                    r14=r14.iloc[i],r60=r60.iloc[i],r7=r7.iloc[i],ratio=ratio.iloc[i],year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    g=pd.DataFrame(rows)
    g["day"]=pd.to_datetime(g["ts"]).dt.floor("D")
    g["side"]=np.sign(g["f"])
    g["dir_un"]=g["un"]*g["side"]; g["dir_tot"]=g["fr"]*g["side"]
    def summ(x):
        n=len(x); 
        if n<3: return pd.Series(dict(n=n))
        return pd.Series(dict(n=n,mean_un=x["un"].mean(),t_un=x["un"].mean()/(x["un"].std()/np.sqrt(n)),
             dir_un=x["dir_un"].mean(),dir_tot=x["dir_tot"].mean(),mean_f=x["f"].mean()))
    out={}
    g["fq"]=pd.qcut(g["f"],5,labels=False,duplicates="drop")
    out["by_forecast_quintile"]=g.groupby("fq").apply(summ)
    out["by_side"]=g.groupby("side").apply(summ)
    g["r14s"]=np.sign(g["r14"])
    out["side_x_r14sign"]=g.dropna(subset=["r14"]).groupby(["side","r14s"]).apply(summ)
    g2=g.dropna(subset=["r60"]).copy()
    g2["r60q"]=pd.qcut(g2["r60"],3,labels=False)
    out["side_x_r60tercile"]=g2.groupby(["side","r60q"]).apply(summ)
    # condition alone: r60 tercile regardless of side
    out["r60tercile_alone"]=g2.groupby("r60q").apply(summ)
    out["by_year"]=g.groupby("year").apply(summ)
    g["absq"]=pd.qcut(g["f"].abs(),4,labels=False,duplicates="drop")
    out["side_x_absforecast"]=g.groupby(["side","absq"]).apply(summ)
    # book daily
    dl=[]
    for c in days:
        for w,d in days[c].items():
            b=bars[c][w].copy()
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            al=b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            dd=d.copy(); dd["day"]=pd.to_datetime(dd["day"]).dt.floor("D")
            dd=dd.merge(al.rename("alloc_prev").reset_index(),on="day",how="left")
            dd["coin"]=c; dd["w"]=w; dl.append(dd)
    D=pd.concat(dl)
    D=D.dropna(subset=["book_return"])
    mu=D.groupby("coin")["coin_return"].mean()
    D["mkt"]=D["alloc_prev"]*D["coin"].map(mu)
    D["long"]=D["alloc_prev"]>0
    out["coinday_by_side"]=D.groupby("long").agg(n=("book_return","size"),mean_book=("book_return","mean"),
        mean_mkt=("mkt","mean"),mean_alloc=("alloc_prev","mean"),mean_coin=("coin_return","mean"))
    bk=D.groupby(["w","day"]).agg(b=("book_return","mean"),h=("coin_return","mean")).reset_index()
    wo={f"w{i}":i for i in range(1,30)}
    bk["wn"]=bk["w"].map(wo); bk=bk.sort_values(["wn","day"])
    out["book_by_window"]=bk.groupby("wn").agg(n=("b","size"),book=("b","sum"),hold=("h","sum"))
    v=(1+bk["b"]).cumprod().values; pk=np.maximum.accumulate(v); ddn=v/pk-1
    bk["dd"]=ddn
    trough=int(np.argmin(ddn)); peak=int(np.argmax(v[:trough+1]))
    out["deepest_fall"]=f"depth {ddn[trough]:.3f}, from window {bk['wn'].iloc[peak]} to window {bk['wn'].iloc[trough]}, days {trough-peak}, hold sum in it {bk['h'].iloc[peak+1:trough+1].sum():.3f}"
    # long vs short contribution during fall
    fd=set(zip(bk["w"].iloc[peak+1:trough+1],bk["day"].iloc[peak+1:trough+1]))
    D["infall"]=[ (a,b) in fd for a,b in zip(D["w"],D["day"])]
    out["fall_by_side"]=D[D["infall"]].groupby("long").agg(n=("book_return","size"),sum_book=("book_return","sum"),mean_coin=("coin_return","mean"))
    return out
