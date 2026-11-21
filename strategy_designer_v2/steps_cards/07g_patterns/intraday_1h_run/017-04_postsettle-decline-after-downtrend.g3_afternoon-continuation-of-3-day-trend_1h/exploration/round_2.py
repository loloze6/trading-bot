def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            ts = pd.to_datetime(b["timestamp"])
            c = pd.Series(b["close"].astype(float).values)
            r1 = c.pct_change().values
            fwd1 = np.r_[c.values[1:]/c.values[:-1]-1, np.nan]
            fwd2 = np.r_[c.values[2:]/c.values[:-2]-1, np.nan, np.nan]
            r72 = c.pct_change(72)
            z = (r72/r72.rolling(73,min_periods=20).std()).values
            fwd24 = (c.shift(-24)/c-1).values
            r24 = c.pct_change(24).values
            sd24 = pd.Series(r1).rolling(24).std().values
            rows.append(pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(c)),"hour":ts.dt.hour.values,
                "year":ts.dt.year.values,"r1":r1,"fwd1":fwd1,"fwd2":fwd2,"z":z,"r24":r24,"fwd24":fwd24,"sd24":sd24}))
    D=pd.concat(rows,ignore_index=True)
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean_bp":x.mean()*1e4,"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    # late-evening drift: return of bars stamped 21,22 (21:00->23:00)
    ev=D[D.hour.isin([21,22])].copy()
    out["evening_drift_by_year"]=ev.groupby("year")["r1"].apply(tt).unstack()
    out["evening_drift_by_coin"]=ev.groupby("coin")["r1"].apply(tt).unstack()
    # graded with prior 24h vol? evening drift by 24h return tercile
    ev["q"]=ev.groupby("coin")["r24"].transform(lambda x: pd.qcut(x,3,labels=False))
    out["evening_drift_by_r24_tercile"]=ev.groupby("q")["r1"].apply(tt).unstack()
    # 24h reversal on grid, by year and coin, and z-graded
    G=D[D.pos%24==0].copy()
    G["zz"]=G["r24"]/(G["sd24"]*np.sqrt(24))
    G["s"]=-np.clip(G["zz"],-3,3)*(G["fwd24"]-G.groupby("coin")["fwd24"].transform("mean"))
    out["rev24_signed_by_year"]=G.groupby("year")["s"].apply(tt).unstack()
    out["rev24_signed_by_coin"]=G.groupby("coin")["s"].apply(tt).unstack()
    G["b"]=pd.cut(G["zz"],[-np.inf,-2,-1,-0.5,0,0.5,1,2,np.inf])
    out["next24_by_z24_bin"]=G.groupby("b",observed=True)["fwd24"].apply(tt).unstack()
    # midday trend reversal: hour 11-13 signed (stamped -> 2h fwd), by year
    D["s2"]=np.clip(D["z"],-2,2)*(D["fwd2"]-D.groupby("coin")["fwd2"].transform("mean"))
    md=D[D.hour==12]; 
    out["midday12_trend_signed_by_year"]=md.groupby("year")["s2"].apply(tt).unstack()
    lt=D[D.hour==22]
    out["late22_trend_signed_by_year"]=lt.groupby("year")["s2"].apply(tt).unstack()
    # 1h reversal by year: signed -zr * fwd1
    D["s1"]=-np.clip(D["r1"]/D["sd24"],-3,3)*D["fwd1"]
    out["rev1h_by_year"]=D.groupby("year")["s1"].apply(tt).unstack()
    return out
