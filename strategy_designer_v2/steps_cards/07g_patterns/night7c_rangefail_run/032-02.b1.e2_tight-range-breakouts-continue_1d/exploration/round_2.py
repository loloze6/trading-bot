import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out={}
    rows=[]; daily=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); hi=b["high"].astype(float); lo=b["low"].astype(float)
            n=len(c); ts=pd.to_datetime(b["timestamp"])
            r1=c.pct_change()
            ch=(c-c.shift(60)).abs(); vol=c.diff().abs().rolling(60,min_periods=60).sum()
            er=(ch/vol).rolling(5,min_periods=1).mean()
            v20=r1.rolling(20,min_periods=15).std()
            feats=dict(r10=c/c.shift(10)-1,r20=c/c.shift(20)-1,r40=c/c.shift(40)-1,r60=c/c.shift(60)-1)
            for H in (5,10,20):
                fwd=c.shift(-H)/c-1
                for i in range(0,n,H):
                    if i+H>=n: break
                    d=dict(coin=coin,w=w,H=H,yr=ts[i].year,day=ts[i].normalize(),fwd=fwd[i],er=er[i],v20=v20[i])
                    for k,v in feats.items(): d[k]=v[i]
                    d["r20v"]=feats["r20"][i]/(v20[i]*np.sqrt(20)) if v20[i]>0 else np.nan
                    rows.append(d)
            dd=data["days"][coin][w]
            daily.append(pd.DataFrame(dict(coin=coin,w=w,yr=pd.to_datetime(dd["day"]).dt.year,
                 wd=pd.to_datetime(dd["day"]).dt.dayofweek,cr=dd["coin_return"].values,br=dd["book_return"].values)))
    s=pd.DataFrame(rows)
    s["u"]=s["fwd"]-s.groupby(["coin","H"])["fwd"].transform("mean")
    def ct(g,col="u"):
        x=g.dropna(subset=[col]); dsum=x.groupby("day")[col].sum(); D=len(dsum)
        m=x[col].mean(); se=np.sqrt((dsum-dsum.mean()*0).pow(2).sum()*0+((x.groupby("day")[col].sum()-x.groupby("day")[col].count()*m)**2).sum()*D/(D-1))/len(x)
        return m/se if se>0 else np.nan
    res=[]
    for H in (5,10,20):
        for f in ["r10","r20","r40","r60","r20v"]:
            q=s[(s.H==H)].dropna(subset=[f,"u"])
            rho=stats.spearmanr(q[f],q.u)[0]; n=len(q)
            q=q.assign(sg=np.sign(q[f]))
            q=q.assign(su=q.sg*q.u)
            res.append(dict(H=H,f=f,n=n,rho=rho,t_rho=rho*np.sqrt((n-2)/(1-rho**2)),
                            signed_u=q.su.mean()*100,t_signed=ct(q,"su")))
    out["momentum_grid"]=pd.DataFrame(res)
    q=s[s.H==10].dropna(subset=["r20","u"])
    out["r20_rho_by_coin"]=q.groupby("coin").apply(lambda g: pd.Series(dict(n=len(g),rho=stats.spearmanr(g.r20,g.u)[0])))
    out["r20_rho_by_year"]=q.groupby("yr").apply(lambda g: pd.Series(dict(n=len(g),rho=stats.spearmanr(g.r20,g.u)[0])))
    q=q.assign(erb=pd.cut(q.er,[0,0.15,0.3,1.01]))
    out["r20_rho_by_er"]=q.dropna(subset=["erb"]).groupby("erb",observed=True).apply(lambda g: pd.Series(dict(n=len(g),rho=stats.spearmanr(g.r20,g.u)[0])))
    D=pd.concat(daily).dropna(subset=["cr"])
    D["fs"]=D.wd.isin([4,5])
    D["dm"]=D.cr-D.groupby("coin").cr.transform("mean")
    out["frisat_by_coin"]=D.groupby(["coin","fs"]).cr.mean().unstack()*100
    out["frisat_by_year"]=D.groupby(["yr","fs"]).cr.mean().unstack()*100
    out["frisat_by_year_n"]=D.groupby(["yr"]).cr.count()
    a=D[D.fs].cr; b2=D[~D.fs].cr
    out["frisat_welch"]=pd.Series(dict(t=stats.ttest_ind(a,b2,equal_var=False)[0],n_fs=len(a),n_other=len(b2)))
    # book big days
    B=D.groupby(["w","yr"]).br.apply(list)
    bd=pd.concat(daily).groupby(["w",pd.concat(daily).index]).agg(br=("br","mean"),cr=("cr","mean"),wd=("wd","first")).dropna()
    out["book_by_wd"]=bd.groupby("wd").br.agg(["mean","count"])
    out["book_top20_wd"]=bd.nlargest(20,"br").wd.value_counts().sort_index()
    return out
