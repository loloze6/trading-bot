def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=26
    rows=[]; drift={}; usual={}
    for c,ws in data["bars"].items():
        rr=[]
        for w,b in ws.items():
            cl=b["close"].values
            for i in range(0,len(cl)-H,H): rr.append(cl[i+H]/cl[i]-1)
        drift[c]=np.mean(rr); usual[c]=np.std(rr)
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True); cl=b["close"].values
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            raw=b.get("debug_info.components.slow_fall.last_history_value")
            for i in range(0,len(cl)-H,H):
                if b["forecast"].iloc[i]<0:
                    r=cl[i+H]/cl[i]-1
                    p26=cl[i]/cl[i-26]-1 if i>=26 else np.nan
                    p13=cl[i]/cl[i-13]-1 if i>=13 else np.nan
                    p52=cl[i]/cl[i-52]-1 if i>=52 else np.nan
                    rows.append(dict(coin=c,win=w,year=yr[i],raw=raw.iloc[i] if raw is not None else np.nan,
                        fc=b["forecast"].iloc[i],short_tot=-r,short_unus=-(r-drift[c]),p13=p13,p26=p26,p52=p52))
    d=pd.DataFrame(rows)
    def agg(g):
        return pd.Series(dict(n=len(g),tot=g.short_tot.mean(),unus=g.short_unus.mean(),
            t=stats.ttest_1samp(g.short_tot,0).statistic if len(g)>2 else np.nan,hit=(g.short_tot>0).mean()))
    out={"drift":pd.Series(drift),"usual":pd.Series(usual)}
    out["by_coin"]=d.groupby("coin").apply(agg)
    out["by_year"]=d.groupby("year").apply(agg)
    d["rawq"]=pd.qcut(d.raw.rank(method="first"),4,labels=False)
    out["by_raw_q"]=d.groupby("rawq").apply(agg)
    out["raw_q_mean"]=d.groupby("rawq").raw.mean()
    for k in ["p13","p26","p52"]:
        dd=d.dropna(subset=[k]).copy(); dd["q"]=pd.qcut(dd[k].rank(method="first"),4,labels=False)
        out["by_"+k]=dd.groupby("q").apply(agg)
        out[k+"_qmean"]=dd.groupby("q")[k].mean()
    out["corr_raw_p26"]=d[["raw","p26","p13"]].corr()
    # book daily
    br=[]
    for c,ws in data["days"].items():
        for w,dd in ws.items():
            x=dd[["book_return","coin_return"]].dropna().copy(); x["coin"]=c;x["win"]=w
            x["year"]=pd.to_datetime(dd.loc[x.index,"day"]).dt.year
            br.append(x)
    br=pd.concat(br)
    out["book_by_year"]=br.groupby("year").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","size"))
    out["book_by_coin"]=br.groupby("coin").agg(book=("book_return","mean"),sd=("book_return","std"))
    # timing vs drift on bars
    pos=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            x=b["postRebalance_current_allocation"].values[:-1]; r=b["close"].pct_change().shift(-1).values[:-1]
            pos.append(pd.DataFrame(dict(coin=c,x=x,r=r)))
    pos=pd.concat(pos).dropna()
    md=pos.groupby("coin").r.transform("mean")
    out["gain_split"]=pd.Series(dict(total=(pos.x*pos.r).mean(),drift_part=(pos.x*md).mean(),mean_pos=pos.x.mean(),share_short=(pos.x<0).mean()))
    return out
