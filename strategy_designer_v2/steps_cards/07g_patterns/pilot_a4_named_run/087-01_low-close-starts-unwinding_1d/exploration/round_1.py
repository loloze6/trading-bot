def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=3
    rows=[]; drift={}
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].values
            idx=np.arange(0,len(b)-H,H)
            allr+=list(c[idx+H]/c[idx]-1)
        drift[coin]=np.mean(allr) if allr else 0
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            d=pd.DataFrame()
            d["inprof"]=b["regime"].isin(["mean_reversion","unknown"])
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            d["clv"]=(b["high"]-b["close"])/rng
            d["r1"]=b["close"].pct_change()
            d["r5"]=b["close"].pct_change(5)
            d["r20"]=b["close"].pct_change(20)
            d["rngp"]=rng/b["close"]
            d["rngrel"]=d["rngp"]/d["rngp"].rolling(20).mean()
            d["volrel"]=b["volume"]/b["volume"].rolling(20).mean()
            d["gap_up"]=(b["close"]/b["close"].rolling(20).max())
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            f=b["close"].shift(-H)/b["close"]-1
            d["grid"]=(np.arange(len(b))%H==0)&f.notna()
            d["un_short"]=-(f-drift[coin])
            d["coin"]=coin; d["w"]=w
            d["pos"]=b["postRebalance_current_allocation"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    G=D[D.grid&D.inprof].copy()
    out={"n_inprof_grid":len(G),"share_inprof_all":float(D.inprof.mean()),
         "drift":pd.Series(drift)}
    def tab(col,q=5):
        x=G.dropna(subset=[col,"un_short"])
        x=x.assign(b=pd.qcut(x[col],q,duplicates="drop"))
        g=x.groupby("b",observed=True)["un_short"]
        return pd.DataFrame({"n":g.size(),"mean":g.mean(),
            "t":g.mean()/(g.std()/np.sqrt(g.size()))})
    for col in ["clv","r1","r5","r20","rngrel","volrel","gap_up","rngp"]:
        out["q_"+col]=tab(col)
    g=G.groupby("wd")["un_short"]
    out["wd"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    g=G.groupby("coin")["un_short"]
    out["coin"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    g=G.groupby("w")["un_short"]
    out["win"]=pd.DataFrame({"n":g.size(),"mean":g.mean()})
    # spearman correlations
    sp={}
    for col in ["clv","r1","r5","r20","rngrel","volrel","gap_up","rngp"]:
        x=G.dropna(subset=[col,"un_short"])
        r,p=stats.spearmanr(x[col],x["un_short"]); sp[col]=(round(r,3),round(p,4),len(x))
    out["spearman"]=pd.DataFrame(sp,index=["rho","p","n"]).T
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items(): tr.append(t)
    T=pd.concat(tr)
    out["trades"]=T.groupby("side")["net_profit_loss_percent"].describe()
    return out
