def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy().reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            b["nxt"]=cl.shift(-1)/cl-1
            b["ret20"]=cl/cl.shift(20)-1
            b["ret60"]=cl/cl.shift(60)-1
            b["vol20"]=r.rolling(20).std()
            b["volrel"]=b["vol20"]/r.rolling(60,min_periods=40).std()
            b["pos"]=b["postRebalance_current_allocation"]
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["gross"]=b["pos"]*b["nxt"]
            b["coin"]=c; b["wn"]=int(w[1:]); b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    d=pd.concat(rows,ignore_index=True)
    mu=d.groupby("coin")["nxt"].mean(); d["ex"]=d["nxt"]-d["coin"].map(mu)
    out={}
    dy=[]
    for c in data["days"]:
        for w,x in data["days"][c].items():
            x=x.copy(); x["coin"]=c; x["wn"]=int(w[1:]); dy.append(x)
    dy=pd.concat(dy,ignore_index=True)
    bk=dy.groupby(["wn","day"])[["book_return","coin_return"]].mean().reset_index().sort_values(["wn","day"])
    out["book_days"]=pd.Series({"mean":bk["book_return"].mean(),"sd":bk["book_return"].std(),"hold_mean":bk["coin_return"].mean(),"n":bk["book_return"].notna().sum()})
    out["fee_vs_gross"]=pd.Series({"fee_per_bar_mean_per_coin":d["fee"].mean(),"gross_per_bar":d["gross"].mean(),"turnover_per_bar":d["allocation_change"].abs().mean() if "allocation_change" in d else np.nan})
    eq=(1+bk["book_return"].fillna(0)).cumprod(); dd=eq/eq.cummax()-1
    bk["dd"]=dd.values
    # deepest fall: from peak to trough
    tr=dd.idxmin(); pk=eq.loc[:tr].idxmax()
    out["deepest_fall"]=pd.Series({"dd":dd.min(),"days":tr-pk,"win_start":bk.loc[pk,"wn"],"win_end":bk.loc[tr,"wn"]})
    # in-drawdown (dd<-10%) days vs others: market state
    d2=d.merge(bk[["wn","day","dd"]],on=["wn","day"],how="left")
    d2["indd"]=d2["dd"]<-0.10
    act=d2[d2["forecast"]>0].dropna(subset=["nxt"])
    out["active_by_dd"]=act.groupby("indd").agg(n=("ex","size"),ret20=("ret20","mean"),ret60=("ret60","mean"),volrel=("volrel","mean"),gross=("gross","mean"),ex=("ex","mean"),pos=("pos","mean")).round(5)
    # active bars by ret60 sign and volrel tercile
    act=act.copy()
    act["tr60"]=np.where(act["ret60"]>0,"up60","down60")
    act["vb"]=pd.qcut(act["volrel"],3,labels=["lowv","midv","highv"])
    out["by_trend60_vol"]=act.groupby(["tr60","vb"]).agg(n=("ex","size"),ex=("ex","mean"),gross=("gross","mean"),t=("ex",lambda x:x.mean()/x.std()*np.sqrt(len(x)))).round(5)
    act["fb"]=pd.qcut(act["forecast"],4,labels=False,duplicates="drop")
    out["by_trend60_fbin"]=act.groupby(["tr60","fb"]).agg(n=("ex","size"),ex=("ex","mean"),gross=("gross","mean"),fee=("fee","mean")).round(5)
    # the 10 worst book days: state
    worst=bk.nsmallest(30,"book_return")[["wn","day"]]
    wd=d.merge(worst,on=["wn","day"])
    out["worst30_days_state"]=pd.Series({"book_mean":bk.nsmallest(30,"book_return")["book_return"].mean(),"coin_ret_mean":wd["nxt"].mean(),"prev_pos_mean":wd["previous_allocation"].mean(),"ret20_mean":wd["ret20"].mean(),"ret60_share_down":(wd["ret60"]<0).mean()})
    return out
