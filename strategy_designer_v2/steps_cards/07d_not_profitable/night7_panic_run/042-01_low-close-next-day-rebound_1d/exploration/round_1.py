def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; book=[]
    for coin, ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            allr.append(b["close"].pct_change().dropna())
        drift=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            rng=(b.high-b.low)
            cl=(b.high-b.close)/rng.replace(0,np.nan)
            rr=rng/b.close
            rrel=rr/rr.rolling(20,min_periods=10).mean().shift(1)
            r1=b.close.shift(-1)/b.close-1
            dret=b.close.pct_change()
            tr60=b.close/b.close.shift(60)-1
            d=pd.DataFrame({"coin":coin,"w":w,"cl":cl,"rrel":rrel,"dret":dret,"tr60":tr60,
                            "ex":r1-drift,"r1":r1,"fc":b.forecast,"alloc":b.postRebalance_current_allocation,
                            "day":pd.to_datetime(b.timestamp).dt.floor("D")})
            rows.append(d)
            g=b.postRebalance_current_allocation*r1
            fee=(b.total_portfolio_value-b.postRebalance_total_value)/b.total_portfolio_value
            book.append(pd.DataFrame({"g":g,"fee":fee,"alloc":b.postRebalance_current_allocation,"ex":r1-drift}))
    D=pd.concat(rows).dropna(subset=["cl","ex"])
    B=pd.concat(book).dropna()
    out={}
    D["clq"]=pd.qcut(D.cl,10,labels=False)
    out["by_cl_decile"]=D.groupby("clq").ex.agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    D["rq"]=pd.qcut(D.rrel,3,labels=["smallR","midR","bigR"])
    D["c3"]=pd.cut(D.cl,[-.01,.2,.8,1.01],labels=["nearHigh","mid","nearLow"])
    out["cl_x_range_mean_ex_bp"]=D.pivot_table(index="c3",columns="rq",values="ex",aggfunc="mean")*1e4
    out["cl_x_range_n"]=D.pivot_table(index="c3",columns="rq",values="ex",aggfunc="count")
    D["dq"]=pd.qcut(D.dret,3,labels=["down","flat","up"])
    out["cl_x_dayret_bp"]=D.pivot_table(index="c3",columns="dq",values="ex",aggfunc="mean")*1e4
    D["tp"]=pd.cut(D.tr60,[-9,-.1,.1,99],labels=["falling","choppy","rising"])
    out["cl_x_trend_bp"]=D.pivot_table(index="c3",columns="tp",values="ex",aggfunc="mean")*1e4
    out["cl_x_trend_n"]=D.pivot_table(index="c3",columns="tp",values="ex",aggfunc="count")
    X=D.dropna(subset=["dret"])
    import numpy.linalg as la
    A=np.column_stack([np.ones(len(X)),X.cl,X.dret])
    coef=la.lstsq(A,X.ex.values,rcond=None)[0]
    out["ols_ex_on_cl_and_dret"]=pd.Series(coef,index=["const","cl","dret"])
    out["book_gross_mean_bp"]=B.g.mean()*1e4
    out["book_fee_mean_bp"]=B.fee.mean()*1e4
    out["gross_long_bp"]=B.g[B.alloc>0].mean()*1e4
    out["gross_short_bp"]=B.g[B.alloc<0].mean()*1e4
    out["share_long"]=(B.alloc>0).mean()
    out["mean_abs_alloc"]=B.alloc.abs().mean()
    out["mean_abs_alloc_change"]=B.alloc.diff().abs().mean()
    return out
