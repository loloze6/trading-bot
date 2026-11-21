def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=26
    drift={}
    for c,ws in data["bars"].items():
        rr=[]
        for w,b in ws.items():
            cl=b["close"].values
            for i in range(0,len(cl)-H,H): rr.append(cl[i+H]/cl[i]-1)
        drift[c]=np.mean(rr)
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True); cl=b["close"].values; hi=b["high"].values; lo=b["low"].values
            raw=b["debug_info.components.slow_fall.last_history_value"]
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            for i in range(0,len(cl)-H,H):
                if b["forecast"].iloc[i]<0:
                    r=cl[i+H]/cl[i]-1
                    s=max(0,i-25)
                    rng=(cl[i]-lo[s:i+1].min())/(hi[s:i+1].max()-lo[s:i+1].min()+1e-12)
                    vol=np.std(np.diff(np.log(cl[max(0,i-20):i+1]))) if i>=5 else np.nan
                    dd=cl[i]/hi[s:i+1].max()-1
                    rows.append(dict(coin=c,win=w,year=yr[i],raw=raw.iloc[i],short_tot=-r,short_unus=-(r-drift[c]),
                        rng=rng,vol=vol,dd=dd,winq=int(w[1:])))
    d=pd.DataFrame(rows)
    def agg(g):
        return pd.Series(dict(n=len(g),tot=g.short_tot.mean(),unus=g.short_unus.mean(),
            t=stats.ttest_1samp(g.short_tot,0).statistic if len(g)>2 else np.nan))
    out={}
    for k in ["rng","dd","vol"]:
        dd=d.dropna(subset=[k]).copy(); dd["q"]=pd.qcut(dd[k].rank(method="first"),4,labels=False)
        out["by_"+k]=dd.groupby("q").apply(agg); out[k+"_qmean"]=dd.groupby("q")[k].mean()
    d["rawh"]=(d.raw>d.raw.median()).astype(int)
    d["ddh"]=(d.dd>d.dd.median()).astype(int)
    out["raw_x_dd"]=d.groupby(["rawh","ddh"]).apply(agg)
    d["bull"]=d.year.isin([2020,2021,2023,2024]).astype(int)
    out["raw_x_bullyears"]=d.groupby(["rawh","bull"]).apply(agg)
    # book: windows' mean return, worst
    br=[]
    for c,ws in data["days"].items():
        for w,x in ws.items():
            br.append(pd.DataFrame(dict(win=w,b=x["book_return"],c=x["coin_return"])).dropna())
    br=pd.concat(br)
    g=br.groupby("win").agg(book=("b","mean"),coin=("c","mean"))
    out["win_book"]=g.sort_values("book")
    out["corr_win_book_coin"]=float(g.corr().iloc[0,1])
    return out
