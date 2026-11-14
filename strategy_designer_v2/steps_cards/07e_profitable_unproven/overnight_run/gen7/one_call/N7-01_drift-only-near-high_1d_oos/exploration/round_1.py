def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for c in data["days"]:
        for w,d in data["days"][c].items():
            b=data["bars"][c][w].copy()
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            al=b.groupby("day").agg(alloc=("postRebalance_current_allocation","last"),
                                    fc=("forecast","last"),reg=("regime","last"))
            dd=d.copy(); dd["day"]=pd.to_datetime(dd["day"]).dt.floor("D")
            dd=dd.merge(al,left_on="day",right_index=True,how="left")
            # position held during day t is allocation at end of day t-1
            dd["pos"]=dd["alloc"].shift(1)
            dd["fcprev"]=dd["fc"].shift(1)
            dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D=pd.concat(rows,ignore_index=True).dropna(subset=["book_return"])
    D["year"]=D["day"].dt.year
    book=D.groupby("day").agg(br=("book_return","mean"),mr=("coin_return","mean"),w=("w","first"),year=("year","first"))
    out={}
    def sh(x): return x.mean()/x.std()*np.sqrt(365) if x.std()>0 else np.nan
    out["book overall"]=pd.Series({"n":len(book),"mean":book.br.mean(),"t":book.br.mean()/book.br.std()*np.sqrt(len(book)),"sharpe":sh(book.br),"mkt_mean":book.mr.mean(),"mkt_sharpe":sh(book.mr)})
    X=np.column_stack([np.ones(len(book)),book.mr.values]); beta=np.linalg.lstsq(X,book.br.values,rcond=None)[0]
    res=book.br.values-X@beta
    out["beta regress"]=pd.Series({"alpha":beta[0],"beta":beta[1],"alpha_t":beta[0]/(res.std()/np.sqrt(len(res)))})
    out["by window"]=book.groupby("w").agg(n=("br","size"),book=("br","mean"),mkt=("mr","mean"))
    out["by year"]=book.groupby("year").agg(n=("br","size"),book=("br","mean"),mkt=("mr","mean"))
    nC=D.groupby("day")["coin"].transform("size")
    D["contrib"]=D["book_return"]/nC
    cc=D.groupby("coin").agg(contrib=("contrib","sum"),book_mean=("book_return","mean"),coin_mean=("coin_return","mean"),expo=("pos","mean"))
    out["by coin"]=cc
    # leave-one-coin-out
    lo={}
    for c in D.coin.unique():
        b2=D[D.coin!=c].groupby("day").book_return.mean(); lo[c]=b2.mean()
    out["leave coin out mean"]=pd.Series(lo)
    # in vs out of market
    D["inm"]=D["pos"].fillna(0).abs()>1e-6
    out["in vs out"]=D.groupby("inm").agg(n=("book_return","size"),book=("book_return","mean"),coin=("coin_return","mean"))
    out["coin mean all"]=D.coin_return.mean()
    # timing: coin return on in-days minus coin's overall mean, per coin
    cm=D.groupby("coin").coin_return.transform("mean")
    D["ex"]=D.coin_return-cm
    e=D[D.inm].ex; out["in-day excess coin ret"]=pd.Series({"n":len(e),"mean":e.mean(),"t":e.mean()/e.std()*np.sqrt(len(e))})
    # forecast bucket of held position
    ii=D[D.inm].copy(); ii["fb"]=pd.qcut(ii["fcprev"].rank(method="first"),4,labels=False)
    out["by fc quartile (in days)"]=ii.groupby("fb").agg(n=("ex","size"),fc=("fcprev","mean"),ex=("ex","mean"),book=("book_return","mean"))
    # trades
    T=pd.concat([data["trades"][c][w].assign(coin=c) for c in data["trades"] for w in data["trades"][c]],ignore_index=True)
    p=T.net_profit_loss_percent.sort_values(ascending=False)
    out["trades"]=pd.Series({"n":len(T),"mean":p.mean(),"median":p.median(),"win":(p>0).mean(),"top10sum":p.head(10).sum(),"allsum":p.sum(),"durdays_mean":T.duration_minutes.mean()/1440})
    return out
