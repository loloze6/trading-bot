import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars=data["bars"]; days=data["days"]; trades=data["trades"]
    out={}
    H=5
    # book daily returns pooled (mean across coins per day within window)
    allb=[]
    for c in days:
        for w,df in days[c].items():
            d=df[["day","book_return","coin_return"]].copy(); d["coin"]=c; d["win"]=w; allb.append(d)
    B=pd.concat(allb)
    B["year"]=pd.to_datetime(B["day"]).dt.year
    P=B.groupby(["win","day"]).agg(book=("book_return","mean"),coin=("coin_return","mean"),year=("year","first")).reset_index()
    out["book_by_year"]=P.groupby("year").agg(n=("book","size"),book_mean=("book","mean"),book_sum=("book","sum"),coin_mean=("coin","mean"))
    out["book_by_window"]=P.groupby("win").agg(book_sum=("book","sum"),coin_sum=("coin","sum"),book_min=("book","min")).sort_values("book_sum").head(10)
    # trades: features at entry
    recs=[]
    for c in bars:
        sds=[]
        for w,df in bars[c].items():
            cl=df["close"].values
            for i in range(0,len(cl)-H,H): sds.append(cl[i+H]/cl[i]-1)
        drift=np.mean(sds)
        for w,df in bars[c].items():
            tr=trades[c].get(w)
            if tr is None or len(tr)==0: continue
            ts=pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            cl=df["close"].reset_index(drop=True); v=df["volume"].reset_index(drop=True)
            r60=cl/cl.shift(60)-1; r20=cl/cl.shift(20)-1; r5=cl/cl.shift(5)-1
            vol20=cl.pct_change().rolling(20).std()
            vol60=cl.pct_change().rolling(60).std()
            ma50=cl/cl.rolling(50).mean()-1
            for _,t in tr.iterrows():
                et=pd.to_datetime(t["entry_time"])
                idx=ts.searchsorted(et,side="right")-1
                if idx<0: continue
                recs.append(dict(coin=c,year=et.year,net=t["net_profit_loss_percent"],gross=t["profit_loss_percent"],
                                 r60=r60.iloc[idx],r20=r20.iloc[idx],r5=r5.iloc[idx],volratio=vol20.iloc[idx]/vol60.iloc[idx] if vol60.iloc[idx]>0 else np.nan,
                                 ma50=ma50.iloc[idx],dur=t["duration_minutes"]/1440))
    T=pd.DataFrame(recs)
    def s(g):
        x=g["gross"]
        return pd.Series(dict(n=len(x),gross=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,net=g["net"].mean(),win=(g["net"]>0).mean()))
    out["trades_all"]=s(T)
    out["trades_by_year"]=T.groupby("year").apply(s)
    out["trades_gross_quantiles"]=T["gross"].describe(percentiles=[.05,.1,.25,.5,.75,.9,.95])
    for col in ["r60","r20","r5","volratio","ma50"]:
        q=pd.qcut(T[col].rank(method="first"),4,labels=False)
        out["trades_by_"+col+"_q"]=T.groupby(q).apply(s).join(T.groupby(q)[col].mean())
    # worst trades features
    w=T.nsmallest(15,"gross")
    out["worst15_mean_feats"]=w[["gross","r60","r20","r5","ma50","volratio"]].mean()
    out["all_mean_feats"]=T[["gross","r60","r20","r5","ma50","volratio"]].mean()
    # correlation gross vs features
    out["spearman_gross"]=pd.Series({col:stats.spearmanr(T[col],T["gross"],nan_policy="omit")[0] for col in ["r60","r20","r5","ma50","volratio"]})
    return out
