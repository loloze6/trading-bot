def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; book=[]; fee=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy(); b["ts"]=pd.to_datetime(b["timestamp"]); b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            vol20=r.rolling(20).std(); vol60=r.rolling(60).std()
            ret20=c/c.shift(20)-1; ret5=c/c.shift(5)-1
            for k in range(1,6): b[f"f{k}"]=c.shift(-k)/c-1
            b["r"]=r; b["z"]=r/vol20; b["vr"]=vol20/vol60; b["ret20z"]=ret20/(vol20*np.sqrt(20)); b["ret5"]=ret5
            b["coin"]=coin; b["w"]=w; b["year"]=b["ts"].dt.year
            s=b[(b["ts"].dt.weekday==6)&(b["forecast"]!=0)]
            rows.append(s)
            fee.append(((b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]).sum())
            d=data["days"][coin][w]; book.append(d.assign(coin=coin,w=w))
    S=pd.concat(rows); D=pd.concat(book)
    S["side"]=-np.sign(S["r"])
    out={}
    for k in range(1,6):
        x=(S["side"]*S[f"f{k}"]).dropna()
        out[f"signed_f{k}"]=f"mean {x.mean():.5f} t {stats.ttest_1samp(x,0)[0]:.2f} n {len(x)}"
    # incremental days
    for k in range(2,6):
        x=(S["side"]*((1+S[f"f{k}"])/(1+S[f"f{k-1}"])-1)).dropna()
        out[f"signed_day{k}_only"]=f"mean {x.mean():.5f} t {stats.ttest_1samp(x,0)[0]:.2f}"
    S["zq"]=pd.qcut(S["z"].abs(),4,labels=False)
    g=S.groupby("zq").apply(lambda q: pd.Series({"n":len(q),"s1":(q.side*q.f1).mean(),"s2":(q.side*q.f2).mean(),"s3":(q.side*q.f3).mean()}))
    out["by_absz_quartile"]=g
    S["trendagree"]=np.sign(S["r"])==np.sign(S["ret20z"])
    S["tq"]=pd.qcut(S["ret20z"]*np.sign(S["r"]),4,labels=False)
    out["by_trend_alignment_quartile(r20z*sign sun)"]=S.groupby("tq").apply(lambda q: pd.Series({"n":len(q),"s1":(q.side*q.f1).mean(),"t1":stats.ttest_1samp((q.side*q.f1).dropna(),0)[0],"s2":(q.side*q.f2).mean()}))
    S["side_up"]=S["r"]>0
    out["by_sunday_sign"]=S.groupby("side_up").apply(lambda q: pd.Series({"n":len(q),"s1":(q.side*q.f1).mean(),"s2":(q.side*q.f2).mean(),"t2":stats.ttest_1samp((q.side*q.f2).dropna(),0)[0]}))
    out["by_year"]=S.groupby("year").apply(lambda q: pd.Series({"n":len(q),"s1":(q.side*q.f1).mean(),"s2":(q.side*q.f2).mean()}))
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    out["book_by_weekday"]=D.groupby("wd")["book_return"].agg(["mean","std","count"])
    out["coin_by_weekday"]=D.groupby("wd")["coin_return"].agg(["mean","std"])
    out["fees_total_sum_share"]=float(np.sum(fee))
    out["mean_alloc_abs_sunday"]=float(S["postRebalance_current_allocation"].abs().mean())
    return out
