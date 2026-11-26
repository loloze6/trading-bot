import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H=10
    rows=[]
    daily=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); hi=b["high"].astype(float); lo=b["low"].astype(float)
            n=len(c)
            ph=hi.shift(1).rolling(60,min_periods=60).max()
            pl=lo.shift(1).rolling(60,min_periods=60).min()
            ch=(c-c.shift(60)).abs(); vol=c.diff().abs().rolling(60,min_periods=60).sum()
            er=(ch/vol).rolling(5,min_periods=1).mean()
            r20=c/c.shift(20)-1
            r5=c/c.shift(5)-1
            r1=c.pct_change()
            v20=r1.rolling(20,min_periods=15).std()
            fwd=c.shift(-H)/c-1
            rng=(ph-pl)/c
            up=(c-ph)/c; dn=(pl-c)/c
            for i in range(0,n,H):
                if i+H>=n: break
                rows.append(dict(coin=coin,w=w,er=er[i],r20=r20[i],r5=r5[i],r1=r1[i],v20=v20[i],
                                 fwd=fwd[i],rng=rng[i],up=up[i],dn=dn[i],
                                 wd=b["timestamp"][i].dayofweek if hasattr(b["timestamp"][i],"dayofweek") else pd.Timestamp(b["timestamp"][i]).dayofweek))
            d=data["days"][coin][w]
            daily.append(pd.DataFrame(dict(coin=coin,w=w,wd=pd.to_datetime(d["day"]).dt.dayofweek,
                        cr=d["coin_return"],br=d["book_return"])))
    s=pd.DataFrame(rows)
    s["drift"]=s.groupby("coin")["fwd"].transform("mean")
    s["u"]=s["fwd"]-s["drift"]
    out={}
    def summ(g):
        x=g["u"].dropna()
        return pd.Series(dict(n=len(x),mean_u=x.mean()*100,t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    s["state"]=np.where(s.up>0,"up_break",np.where(s.dn>0,"down_break","inside"))
    s["er_b"]=pd.cut(s.er,[0,0.15,0.3,0.5,1.01])
    out["state_by_er"]=s.dropna(subset=["er"]).groupby(["state","er_b"],observed=True).apply(summ)
    for col in ["r20","r5","r1","v20","rng"]:
        q=s.dropna(subset=[col])
        q=q.assign(qq=q.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False)))
        out["q_"+col]=q.groupby("qq").apply(summ)
    out["weekday_u"]=s.groupby("wd").apply(summ)
    for col in ["r20","r5","v20","rng"]:
        q=s.dropna(subset=[col,"u"])
        out["spearman_"+col]=float(stats.spearmanr(q[col],q["u"])[0])
    D=pd.concat(daily)
    D["cm"]=D.groupby("coin")["cr"].transform("mean")
    out["daily_weekday"]=D.groupby("wd").apply(lambda g: pd.Series(dict(n=g.cr.count(),coin_mean=g.cr.mean()*100,
        t=g.cr.mean()/(g.cr.std()/np.sqrt(g.cr.count())),book_mean=g.br.mean()*100)))
    # book: mean daily over coins
    B=D.groupby(["w",D.index]).agg(br=("br","mean"),cr=("cr","mean")).dropna()
    B=B.reset_index(drop=True)
    out["book_top_share"]=pd.Series(dict(total=B.br.sum(),top10=B.br.nlargest(10).sum(),bot10=B.br.nsmallest(10).sum(),
        corr_coin=B.br.corr(B.cr)))
    # breakouts sized by overshoot among up breaks
    ub=s[s.state=="up_break"].dropna(subset=["u"])
    out["upbreak_spear_up_rng_er"]=pd.Series(dict(n=len(ub),sp_up=stats.spearmanr(ub.up,ub.u)[0],
        sp_rng=stats.spearmanr(ub.rng,ub.u)[0],sp_er=stats.spearmanr(ub.er,ub.u)[0]))
    return out
