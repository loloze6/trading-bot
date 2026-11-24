def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H=20
    rows=[]; daily=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values
            n=len(c)
            r1=pd.Series(c).pct_change()
            vol20=r1.rolling(20).std()
            for i in range(0,n-H,H):
                rows.append(dict(coin=coin,w=w,fwd=c[i+H]/c[i]-1,fc=b["forecast"].iloc[i],
                    reg=b["regime"].iloc[i],
                    dl=b.get("debug_info.components.dist_low.last_history_value",pd.Series([np.nan]*n)).iloc[i],
                    dstd=b.get("debug_info.components.dist_low.post_pipeline_value",pd.Series([np.nan]*n)).iloc[i],
                    p20=(c[i]/c[i-20]-1) if i>=20 else np.nan,
                    p60=(c[i]/c[i-60]-1) if i>=60 else np.nan,
                    vol=vol20.iloc[i],
                    alloc=b["postRebalance_current_allocation"].iloc[i]))
            ts=pd.to_datetime(b["timestamp"])
            for i in range(1,n-1):
                daily.append(dict(coin=coin,r=r1.iloc[i],nxt=c[i+1]/c[i]-1,wd=ts.iloc[i].dayofweek,
                                  z=r1.iloc[i]/vol20.iloc[i-1] if i>20 else np.nan,
                                  vol=vol20.iloc[i],reg=b["regime"].iloc[i]))
    g=pd.DataFrame(rows)
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    d=pd.DataFrame(daily)
    d["nx"]=d["nxt"]-d.groupby("coin")["nxt"].transform("mean")
    def summ(df,col,q=5):
        df=df.dropna(subset=[col,"ex"]).copy()
        df["b"]=pd.qcut(df[col],q,labels=False,duplicates="drop")
        a=df.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("ex","size"),mean_ex=("ex","mean"),sd=("ex","std"))
        a["t"]=a.mean_ex/(a.sd/np.sqrt(a.n));return a.drop(columns="sd").round(4)
    out={}
    out["n_grid"]=len(g)
    out["by_regime"]=g.groupby("reg")["ex"].agg(["size","mean","std"]).round(4)
    tr=g[g.reg=="trending"]
    out["trend_dstd_q"]=summ(tr,"dstd")
    out["trend_dl_q"]=summ(tr,"dl")
    out["all_p20_q"]=summ(g,"p20")
    out["all_p60_q"]=summ(g,"p60")
    out["all_vol_q"]=summ(g,"vol")
    out["trend_p20_q"]=summ(tr,"p20")
    out["nontrend_p20_q"]=summ(g[g.reg!="trending"],"p20")
    # daily: next-day after z-moves
    dd=d.dropna(subset=["z"]).copy()
    dd["zb"]=pd.cut(dd.z,[-99,-2,-1,0,1,2,99])
    a=dd.groupby("zb")["nx"].agg(["size","mean","std"]);a["t"]=a["mean"]/(a["std"]/np.sqrt(a["size"]))
    out["next1d_by_z"]=a.round(5)
    a=d.groupby("wd")["nx"].agg(["size","mean","std"]);a["t"]=a["mean"]/(a["std"]/np.sqrt(a["size"]))
    out["next1d_by_weekday"]=a.round(5)
    # book by position sign
    bk=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].values;al=b["postRebalance_current_allocation"].values
            for i in range(len(c)-1):
                bk.append(dict(s=np.sign(al[i]),g=al[i]*(c[i+1]/c[i]-1)))
    bk=pd.DataFrame(bk)
    out["gain_by_side"]=bk.groupby("s")["g"].agg(["size","mean","sum"]).round(5)
    t=pd.concat([x for ws in data["trades"].values() for x in ws.values()])
    out["trades_by_side"]=t.groupby("side")["net_profit_loss_percent"].agg(["size","mean","median",lambda s:(s>0).mean()]).round(3)
    return out
