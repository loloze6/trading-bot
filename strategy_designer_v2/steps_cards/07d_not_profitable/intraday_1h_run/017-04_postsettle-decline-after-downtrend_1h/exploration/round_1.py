def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; book=[]
    for c in data["bars"]:
        allr=[]
        for w,b in data["bars"][c].items():
            cl=b["close"].values
            r2=pd.Series(cl).shift(-2)/pd.Series(cl)-1
            allr.append(r2.iloc[::2])
        mu=pd.concat(allr).mean()
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True)
            cl=b["close"]
            r72=cl/cl.shift(72)-1
            z=(r72-r72.rolling(73,min_periods=20).mean())/r72.rolling(73,min_periods=20).std()
            r2=cl.shift(-2)/cl-1
            ts=pd.to_datetime(b["timestamp"])
            hr=((ts+pd.Timedelta(hours=1)).dt.hour)
            d=pd.DataFrame({"coin":c,"hr":hr,"z":z,"ex":r2-mu,"r24":cl/cl.shift(24)-1})
            rows.append(d)
            # book gross vs fee
            a=b["postRebalance_current_allocation"].fillna(0)
            ret1=cl.shift(-1)/cl-1
            gross=(a*ret1)/1.0
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            book.append(pd.DataFrame({"coin":c,"gross":gross,"fee":fee,"hr":hr,"a":a}))
    D=pd.concat(rows).dropna()
    B=pd.concat(book)
    out={}
    D["neg"]=D.z<0
    N=D[D.neg].copy()
    N["zq"]=pd.qcut(N.z,3,labels=["deep","mid","mild"])
    g=N.groupby(["hr"]).agg(n=("ex","size"),mean_ex=("ex","mean"))
    g["t"]=N.groupby("hr")["ex"].apply(lambda x: x.mean()/(x.std()/np.sqrt(len(x))))
    g["deep_minus_mild"]=N.groupby("hr").apply(lambda x: x[x.zq=="deep"].ex.mean()-x[x.zq=="mild"].ex.mean())
    out["neg_z_by_close_hour"]=g
    S=N[N.hr.isin([0,8,16])]
    out["settle_by_third"]=S.groupby("zq").ex.agg(["size","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    P=D[(~D.neg)&D.hr.isin([0,8,16])]
    out["settle_posz"]=pd.Series({"n":len(P),"mean":P.ex.mean(),"t":P.ex.mean()/(P.ex.std()/np.sqrt(len(P)))})
    out["settle_by_coin"]=S.groupby("coin").ex.agg(["size","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    out["book_gross_fee"]=pd.Series({"gross_sum_per_bar_mean":B.gross.mean(),"fee_mean":B.fee.mean(),"gross_total":B.gross.sum(),"fee_total":B.fee.sum(),"active_share":(B.a!=0).mean()})
    out["gross_by_hr_active"]=B[B.a!=0].groupby("hr").gross.agg(["size","mean"])
    dd=[]
    for c in data["days"]:
        for w,d in data["days"][c].items():
            dd.append(d.assign(coin=c))
    DD=pd.concat(dd)
    out["daily"]=DD.groupby("coin").book_return.agg(["mean","std"])
    return out
