def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        grid=[]
        for w, b in wins.items():
            c=b.sort_values("timestamp")["close"].values
            if len(c)>2: grid.extend(list(c[2::2]/c[:-2:2]-1))
        drift=np.nanmean(grid); usual=np.nanstd(grid)
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]); c=b["close"]
            lr=np.log(c).diff()
            vol=lr.rolling(720,min_periods=300).std()
            fwd2=c.shift(-2)/c-1
            okts=(ts.shift(-2)-ts)==pd.Timedelta(hours=2)
            ok3=(ts-ts.shift(3))==pd.Timedelta(hours=3)
            p3=(c/c.shift(3)-1).where(ok3)
            df=pd.DataFrame({"coin":coin,"hour":ts.dt.hour,"year":ts.dt.year,
                "ex":(fwd2-drift).where(okts),"p3z":p3/(vol*np.sqrt(3)),"p3":p3,"vol":vol,
                "pos":b["postRebalance_current_allocation"]})
            rows.append(df.iloc[::2] if False else df)
    d=pd.concat(rows).dropna(subset=["ex","p3z"])
    def g(x):
        n=len(x); m=x["ex"].mean()
        return pd.Series({"n":n,"mean_ex_pct":100*m,"t":m/(x["ex"].std()/np.sqrt(n)),"mean_p3_pct":100*x["p3"].mean()})
    out={}
    e=d[d.hour==20].copy()
    out["corr_pos_vol_at20"]=float(e[["pos","vol"]].corr().iloc[0,1])
    e["dec"]=pd.qcut(e["p3z"].rank(method="first"),10,labels=False)
    out["at20_by_prior3h_volscaled_decile"]=e.groupby("dec").apply(g)
    e["vq"]=e.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    e["pq"]=pd.qcut(e["p3z"].rank(method="first"),3,labels=False)
    out["at20_vol_tercile_x_p3_tercile"]=e.groupby(["vq","pq"]).apply(g)
    out["at20_p3_bottom_tercile_by_year"]=e[e.pq==0].groupby("year").apply(g)
    # same reversal at other hours (bottom decile of prior 3h)
    d["dec"]=d.groupby("hour")["p3z"].transform(lambda s: pd.qcut(s.rank(method="first"),10,labels=False))
    sub=d[d.dec==0].groupby("hour").apply(g)
    out["bottom_decile_prior3h_by_hour"]=sub
    out["slope_ex_on_p3z_at20"]=float(np.polyfit(e["p3z"].clip(-4,4),e["ex"],1)[0])
    return out
