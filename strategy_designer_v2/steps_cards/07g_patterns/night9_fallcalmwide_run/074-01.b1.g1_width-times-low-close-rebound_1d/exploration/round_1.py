import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            d=pd.DataFrame({"w":w,"coin":coin,"ts":pd.to_datetime(b["timestamp"])})
            d["r"]=r; d["nxt"]=c.shift(-1)/c-1
            d["nxt3"]=c.shift(-3)/c-1
            sd=r.rolling(30,min_periods=20).std()
            d["sd"]=sd
            d["width"]=(b["high"]-b["low"])/c/sd
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            d["low_near"]=(b["high"]-c)/rng
            d["tr60"]=c/c.shift(60)-1
            d["fc"]=b["forecast"]; d["alloc"]=b["postRebalance_current_allocation"]
            d["z"]=r/sd.shift(1)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mean_r=D.groupby("coin")["r"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(mean_r)
    D["ex3"]=D["nxt3"]-3*D["coin"].map(mean_r)
    med_sd=D.groupby("coin")["sd"].median()
    D["agit"]=np.where(D["sd"]>D["coin"].map(med_sd),"agit","calm")
    D["trend"]=pd.cut(D["tr60"],[-np.inf,-0.1,0.1,np.inf],labels=["fall","chop","rise"])
    D["prof"]=D["trend"].astype(str)+"_"+D["agit"]
    D["day"]=D["ts"].dt.floor("D")
    def tday(g,col="ex"):
        g=g.dropna(subset=[col])
        if len(g)<5: return pd.Series({"n":len(g),"mean":np.nan,"t":np.nan})
        s=g.groupby("day")[col].sum()
        return pd.Series({"n":len(g),"days":len(s),"mean":g[col].mean(),"t":s.mean()/(s.std()/np.sqrt(len(s)))*1.0})
    D["sit"]="other"
    D.loc[(D.width>=2)&(D.low_near>=0.8),"sit"]="wide_low"
    D.loc[(D.width>=2)&(D.low_near<=0.2),"sit"]="wide_high"
    D.loc[(D.width>=2)&(D.low_near>0.2)&(D.low_near<0.8),"sit"]="wide_mid"
    out={}
    out["prof_sit"]=D[D.tr60.notna()].groupby(["prof","sit"]).apply(tday).round(4)
    W=D[(D.sit=="wide_low")].copy()
    W["score"]=W.width*W.low_near
    W["q"]=pd.qcut(W.score,4,labels=False)
    out["wide_low_score_q_all"]=W.groupby("q").apply(tday).round(4)
    W["wq"]=pd.qcut(W.width,3,labels=False)
    out["wide_low_widthq_ex3"]=W.groupby("wq").apply(lambda g:tday(g,"ex3")).round(4)
    D["zq"]=pd.qcut(D.z,10,labels=False)
    out["zdecile_next"]=D.groupby("zq").apply(tday).round(4)
    D["wd"]=D.ts.dt.dayofweek
    out["weekday_next"]=D.groupby("wd").apply(tday).round(4)
    D["volq"]=D.groupby("coin")["sd"].transform(lambda s:pd.qcut(s,4,labels=False,duplicates="drop"))
    out["volq_by_zsign"]=D.groupby(["volq",np.sign(D.z)]).apply(tday).round(4)
    # book days
    bd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            bd.append(x.assign(coin=coin,w=w))
    B=pd.concat(bd)
    br=B.groupby("day")["book_return"].mean().dropna()
    out["book_ret_desc"]=br.describe()
    top=br.abs().sort_values(ascending=False)
    out["book_share_top10days_of_sum"]=float(br.loc[top.index[:10]].sum()/br.sum())
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()]) if any(len(ws) for ws in data["trades"].values()) else pd.DataFrame()
    if len(T):
        T["yr"]=pd.to_datetime(T.entry_time).dt.year
        out["trades_by_year"]=T.groupby("yr")["net_profit_loss_percent"].agg(["count","mean"])
        out["trades_by_coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean"])
    return out
