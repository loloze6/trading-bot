import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"].astype(float)
            r=cl.pct_change()
            sd=r.rolling(20,min_periods=20).std()
            z=r/sd
            vp=sd.rolling(100,min_periods=20).apply(lambda x:(x<=x[-1]).mean(),raw=True).rolling(5).mean()
            nxt=cl.shift(-1)/cl-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":c,"win":w,"wn":int(w[1:]),"z":z,"vp":vp,"nxt":nxt,
                "wd":ts.dt.dayofweek,"yr":ts.dt.year,"alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    cm=D.groupby("coin")["nxt"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(cm)
    D["vlev"]=pd.cut(D["vp"],[-0.01,0.3,0.6,0.8,1.01],labels=["lo","mid","mhi","hi"])
    E=D.dropna(subset=["ex","z","vp"])
    out={}
    res={}
    for (lv,sg),s in E.assign(sg=np.where(E["z"]<0,"down","up")).groupby(["vlev","sg"]):
        sl=stats.linregress(s["z"].abs(),s["ex"]); res[f"{lv}_{sg}"]=(sl.slope,sl.slope/sl.stderr,len(s))
    out["slope ex on |z| by vol and side"]=pd.DataFrame(res,index=["slope","t","n"]).T
    # interaction: ex ~ z*vp continuous, pooled
    X=np.column_stack([np.ones(len(E)),E["z"],E["vp"],E["z"]*E["vp"]])
    y=E["ex"].values
    beta,_,_,_=np.linalg.lstsq(X,y,rcond=None)
    resid=y-X@beta; s2=resid@resid/(len(y)-4)
    se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["ex ~ z + vp + z*vp"]=pd.DataFrame({"beta":beta,"t":beta/se},index=["c","z","vp","z*vp"])
    # robustness: z*vp interaction by window halves and by coin
    rr={}
    for name,s in [("w1-12",E[E.wn<=12]),("w13-24",E[E.wn>12])]+[(c,E[E.coin==c]) for c in E.coin.unique()]:
        X=np.column_stack([np.ones(len(s)),s["z"],s["vp"],s["z"]*s["vp"]]);y=s["ex"].values
        b_,_,_,_=np.linalg.lstsq(X,y,rcond=None);rs=y-X@b_
        se_=np.sqrt(np.diag(rs@rs/(len(y)-4)*np.linalg.inv(X.T@X)))
        rr[name]=(b_[3],b_[3]/se_[3],len(s))
    out["z*vp interaction robustness"]=pd.DataFrame(rr,index=["beta","t","n"]).T
    # weekday robustness
    W=D.dropna(subset=["ex"])
    W["thfr"]=W["wd"].isin([3,4])
    out["thu+fri minus other, by year"]=W.groupby("yr").apply(lambda s:pd.Series({"diff":s[s.thfr].ex.mean()-s[~s.thfr].ex.mean(),"t":stats.ttest_ind(s[s.thfr].ex,s[~s.thfr].ex,equal_var=False).statistic}))
    out["thu+fri minus other, by coin"]=W.groupby("coin").apply(lambda s:pd.Series({"diff":s[s.thfr].ex.mean()-s[~s.thfr].ex.mean(),"t":stats.ttest_ind(s[s.thfr].ex,s[~s.thfr].ex,equal_var=False).statistic}))
    # book concentration
    br=[]
    for c,ws in data["days"].items():
        for w,d in ws.items(): br.append(d.assign(coin=c,win=w))
    B=pd.concat(br)
    bk=B.groupby(["win","day"])["book_return"].mean().dropna().sort_values(ascending=False)
    out["book: share of total gain from top 1%/5% days"]=pd.Series({"top1pct":bk.iloc[:len(bk)//100].sum()/bk.sum(),"top5pct":bk.iloc[:len(bk)//20].sum()/bk.sum(),"days_active_share":(B.groupby(["win","day"])["book_return"].apply(lambda x:(x.abs()>0).mean())).mean()})
    return out
