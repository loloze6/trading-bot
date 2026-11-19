def explore(data):
    import numpy as np, pandas as pd
    out={}
    rows=[]
    for coin, wins in data["bars"].items():
        for w,b in wins.items():
            ts=pd.to_datetime(b["timestamp"])
            c=pd.Series(b["close"].astype(float).values)
            r72=c.pct_change(72); z=(r72/r72.rolling(73,min_periods=20).std()).values
            r24=c.pct_change(24); sd=c.pct_change().rolling(168).std()
            z24=(r24/(sd*np.sqrt(24))).values
            fwd2=(c.shift(-2)/c-1).values
            rows.append(pd.DataFrame({"coin":coin,"w":w,"hour":ts.dt.hour.values,"year":ts.dt.year.values,
                "z":z,"z24":z24,"fwd2":fwd2}))
    D=pd.concat(rows,ignore_index=True)
    D["ex"]=D["fwd2"]-D.groupby("coin")["fwd2"].transform("mean")
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean_bp":x.mean()*1e4,"t":x.mean()/x.std()*np.sqrt(len(x))})
    # evening: bar stamped 20 closes 21:00 -> fwd2 = 21:00->23:00
    ev=D[D.hour==20].dropna(subset=["z24","ex"]).copy()
    out["eve_unconditional_excess"]=tt(ev["ex"]).to_frame().T
    ev["q"]=ev.groupby("coin")["z24"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["eve_excess_by_prior24h_quintile"]=ev.groupby("q")["ex"].apply(tt).unstack()
    ev["q3"]=ev.groupby("coin")["z"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["eve_excess_by_prior3d_quintile"]=ev.groupby("q3")["ex"].apply(tt).unstack()
    out["eve_excess_by_coin"]=ev.groupby("coin")["ex"].apply(tt).unstack()
    # midday: bar stamped 12 closes 13:00 -> 13:00->15:00, by 3d quintile
    md=D[D.hour==12].dropna(subset=["z","ex"]).copy()
    md["q"]=md.groupby("coin")["z"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["mid13_excess_by_3d_quintile"]=md.groupby("q")["ex"].apply(tt).unstack()
    md["s"]=-np.clip(md["z"],-2,2)*md["ex"]
    out["mid13_against_trend_by_coin"]=md.groupby("coin")["s"].apply(tt).unstack()
    # placebo clock: tested slot (stamped 15) by 3d quintile, for grading
    sl=D[D.hour==15].dropna(subset=["z","ex"]).copy()
    sl["q"]=sl.groupby("coin")["z"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["slot16_excess_by_3d_quintile"]=sl.groupby("q")["ex"].apply(tt).unstack()
    return out
