def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    rows=[]
    for H in [1,5,10]:
        for coin,ws in data["bars"].items():
            allr=[]
            for w,b in ws.items():
                b=b.sort_values("timestamp").reset_index(drop=True)
                c=b["close"].values
                idx=np.arange(0,len(b)-H,H)
                allr+=list(c[idx+H]/c[idx]-1)
            dr=np.mean(allr) if allr else 0
            for w,b in ws.items():
                b=b.sort_values("timestamp").reset_index(drop=True)
                d=pd.DataFrame()
                d["inprof"]=b["regime"].isin(["mean_reversion","unknown"])
                rng=(b["high"]-b["low"]).replace(0,np.nan)
                d["clv"]=(b["high"]-b["close"])/rng
                r1=b["close"].pct_change()
                up=(r1>0).astype(int)
                d["streak"]=up.groupby((up!=up.shift()).cumsum()).cumsum()*up
                d["r10"]=b["close"].pct_change(10)
                d["dd20"]=b["close"]/b["close"].rolling(20).max()-1
                f=b["close"].shift(-H)/b["close"]-1
                d["grid"]=(np.arange(len(b))%H==0)&f.notna()
                d["un"]=-(f-dr)
                d["H"]=H; d["coin"]=coin; d["w"]=w
                rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    G=D[D.grid&D.inprof]
    def tt(x):
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["all_by_H"]=G.groupby("H")["un"].apply(tt).unstack()
    for col in ["clv","streak","r10","dd20"]:
        res={}
        for H in [1,5,10]:
            x=G[G.H==H].dropna(subset=[col,"un"])
            r,p=stats.spearmanr(x[col],x["un"]); res[H]=(round(r,3),round(p,4),len(x))
        out["sp_"+col]=pd.DataFrame(res,index=["rho","p","n"]).T
    x=G[G.H==5].dropna(subset=["r10","un"])
    x=x.assign(b=pd.qcut(x["r10"],4,duplicates="drop"))
    out["H5_r10_q"]=x.groupby("b",observed=True)["un"].apply(tt).unstack()
    x=G[G.H==5].dropna(subset=["dd20","un"])
    x=x.assign(b=pd.qcut(x["dd20"],4,duplicates="drop"))
    out["H5_dd20_q"]=x.groupby("b",observed=True)["un"].apply(tt).unstack()
    # book daily returns
    br=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            br.append(d.assign(coin=coin,w=w))
    B=pd.concat(br)
    out["book_ret"]=B["book_return"].describe()
    out["book_by_coin"]=B.groupby("coin")["book_return"].agg(["mean","std","count"])
    return out
