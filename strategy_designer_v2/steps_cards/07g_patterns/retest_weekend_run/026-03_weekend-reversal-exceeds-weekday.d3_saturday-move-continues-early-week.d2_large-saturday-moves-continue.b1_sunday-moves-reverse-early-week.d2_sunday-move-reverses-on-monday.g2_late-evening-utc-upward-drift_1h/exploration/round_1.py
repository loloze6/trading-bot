def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b[["timestamp","close"]].copy()
            b["timestamp"] = pd.to_datetime(b["timestamp"], utc=True)
            b["r1"] = b["close"].shift(-1)/b["close"]-1
            b["hour"] = b["timestamp"].dt.hour
            b["wd"] = b["timestamp"].dt.weekday
            b["coin"] = c; b["win"] = w
            b["pos"] = np.arange(len(b))
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B["r1d"] = B["r1"] - B.groupby("coin")["r1"].transform("mean")
    # hour-of-day excess, pooled
    g = B.groupby("hour")["r1d"]
    hh = pd.DataFrame({"mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()})
    out["hour_excess_pooled"] = hh.round(2)
    # weekday daily-level: 24h returns from 00:00 bar
    dd = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["day"] = pd.to_datetime(d["day"])
            d["coin"] = c; d["wd"] = d["day"].dt.weekday
            d["next"] = d["coin_return"].shift(-1)
            d["prev"] = d["coin_return"]
            d["prev3"] = (d["close"]/d["close"].shift(3)-1)
            d["next2"] = d["close"].shift(-2)/d["close"]-1
            d["book"] = d["book_return"]
            d["vol30"] = d["coin_return"].rolling(30).std()
            dd.append(d)
    D = pd.concat(dd, ignore_index=True)
    D["cr"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    g = D.groupby("wd")["cr"]
    out["weekday_excess_daily"] = pd.DataFrame({"mean_pct": g.mean()*100, "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()}).round(3)
    # daily return vs next day: by quintile of standardized prev return
    D["z"] = D["prev"]/D["vol30"]
    D["nz"] = D["next"]/D["vol30"]
    D["q"] = pd.qcut(D["z"], 5, labels=False)
    g = D.groupby("q")["nz"]
    out["next_day_by_prev_z_quintile"] = pd.DataFrame({"mean_z": g.mean(), "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count(), "next_pct": D.groupby("q")["next"].mean()*100}).round(3)
    # 3-day return vs next 2 days, non-overlapping grid every 3 days? use pos%5
    D["dpos"] = D.groupby(["coin"]).cumcount()
    E = D[D["dpos"]%5==0].dropna(subset=["prev3","next2","vol30"]).copy()
    E["z3"] = E["prev3"]/E["vol30"]; E["q3"]=pd.qcut(E["z3"],5,labels=False)
    g = E.groupby("q3")["next2"]
    out["next2d_by_prev3d_quintile"] = pd.DataFrame({"mean_pct": g.mean()*100, "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()}).round(3)
    # vol regime: daily excess by vol tercile
    D["vt"] = D.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    g = D.groupby("vt")["cr"]
    out["daily_excess_by_vol_tercile"] = pd.DataFrame({"mean_pct": g.mean()*100, "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()}).round(3)
    # 6h block returns by start hour, non-overlapping grid
    B6 = B[B["hour"]%6==0].copy()
    # compute 6h fwd within window
    res=[]
    for (c,w), b in B.groupby(["coin","win"]):
        b = b.set_index("pos")
        f = b["close"].shift(-6)/b["close"]-1
        sel = b[b["hour"]%6==0].index
        res.append(pd.DataFrame({"coin":c,"hour":b.loc[sel,"hour"],"wd":b.loc[sel,"wd"],"r6":f.loc[sel]}))
    R6 = pd.concat(res).dropna()
    R6["x"] = R6["r6"]-R6.groupby("coin")["r6"].transform("mean")
    g = R6.groupby("hour")["x"]
    out["6h_block_excess"] = pd.DataFrame({"mean_pct": g.mean()*100, "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()}).round(3)
    # 21-23 excess per coin and by year
    s = B[B["hour"].isin([21,22])]
    g = s.groupby("coin")["r1d"]
    out["h21_22_per_coin_bp"] = pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count()))}).round(2)
    s = s.assign(yr=s["timestamp"].dt.year)
    g = s.groupby("yr")["r1d"]
    out["h21_22_per_year_bp"] = pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count()))}).round(2)
    return out
