def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.reset_index(drop=True).copy()
            c=d["close"].astype(float)
            r=np.log(c).diff()
            d["r1"]=r
            d["f1"]=r.shift(-1)
            d["f10"]=np.log(c.shift(-10)/c)
            d["vol20"]=r.rolling(20).std()
            d["z"]=r/d["vol20"].shift(1)
            d["ret10p"]=np.log(c/c.shift(10))
            col="debug_info.components.below_sma200.last_history_value"
            d["dist"]=d[col] if col in d else np.nan
            d["coin"]=coin; d["w"]=w; d["i"]=np.arange(len(d))
            d["wd"]=pd.to_datetime(d["timestamp"]).dt.weekday
            d["yr"]=pd.to_datetime(d["timestamp"]).dt.year
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    A["m10"]=A.groupby("coin")["f10"].transform("mean")
    A["x10"]=A["f10"]-A["m10"]
    G=A[(A["i"]%10==0)&A["f10"].notna()].copy()
    def summ(g,col):
        x=g[col].dropna(); n=len(x)
        return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan,"hit":(x>0).mean()})
    out={}
    G["fb"]=pd.cut(G["forecast"],[-1,0,0.5,2,5,10,21],include_lowest=True)
    out["fc_bucket_x10"]=G.groupby("fb").apply(lambda g:summ(g,"x10"))
    G["db"]=pd.qcut(G["dist"],8,duplicates="drop")
    out["dist_oct_x10"]=G.groupby("db").apply(lambda g:summ(g,"x10"))
    G["vb"]=G.groupby("coin")["vol20"].transform(lambda s:pd.qcut(s,3,labels=False,duplicates="drop"))
    out["vol_tercile_x10"]=G.groupby("vb").apply(lambda g:summ(g,"x10"))
    G["mb"]=G.groupby("coin")["ret10p"].transform(lambda s:pd.qcut(s,5,labels=False,duplicates="drop"))
    out["past10_quint_x10"]=G.groupby("mb").apply(lambda g:summ(g,"x10"))
    A["zb"]=pd.cut(A["z"],[-99,-3,-2,-1,1,2,3,99])
    A["xf1"]=A["f1"]-A.groupby("coin")["f1"].transform("mean")
    out["bigmove_next1"]=A.groupby("zb").apply(lambda g:summ(g,"xf1"))
    out["weekday_r1"]=A.groupby("wd").apply(lambda g:summ(g,"xf1"))
    out["coin_fc_x10"]=G[G["forecast"]>=5].groupby("coin").apply(lambda g:summ(g,"x10"))
    out["year_fc_x10"]=G[G["forecast"]>=2].groupby("yr").apply(lambda g:summ(g,"x10"))
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()],ignore_index=True)
    T["eb"]=pd.cut(T["entry_forecast"],[0,1,3,8,21])
    out["trades_by_entryfc"]=T.groupby("eb").agg(n=("net_profit_loss_percent","size"),mean=("net_profit_loss_percent","mean"),med=("net_profit_loss_percent","median"),hit=("net_profit_loss_percent",lambda x:(x>0).mean()),dur_d=("duration_minutes",lambda x:x.mean()/1440))
    return out
