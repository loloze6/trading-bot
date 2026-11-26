def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            n = len(b)
            fwd1 = c.shift(-1)/c - 1
            fwd2 = c.shift(-2)/c - 1
            sd20 = r1.rolling(20).std()
            hh20 = b["high"].rolling(20).max()
            ll20 = b["low"].rolling(20).min()
            pos20 = (c - ll20)/(hh20 - ll20)
            depth = (c - hh20)/c/sd20
            tr = c/c.shift(min(60,n-1)) - 1 if n > 60 else pd.Series(np.nan, index=b.index)
            tr60 = c/c.shift(60) - 1
            vol_rel = r1.rolling(20).std()/r1.rolling(60).std()
            rng = (b["high"]-b["low"])/c
            clv = (c - b["low"])/(b["high"]-b["low"])
            r5 = c/c.shift(5)-1
            df = pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(n),"r1":r1,"fwd1":fwd1,"fwd2":fwd2,
                "sd20":sd20,"pos20":pos20,"depth":depth,"tr60":tr60,"vol_rel":vol_rel,"rng":rng,"clv":clv,
                "r5":r5,"fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],
                "wd":pd.to_datetime(b["timestamp"]).dt.dayofweek,"yr":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    # drift per coin (non-overlapping 2-bar and 1-bar)
    g2 = d[d.pos % 2 == 0]
    drift2 = g2.groupby("coin")["fwd2"].mean(); sd2 = g2.groupby("coin")["fwd2"].std()
    drift1 = d.groupby("coin")["fwd1"].mean()
    d["ex2"] = d["fwd2"] - d["coin"].map(drift2)
    d["ex1"] = d["fwd1"] - d["coin"].map(drift1)
    d["z2"] = d["ex2"]/d["coin"].map(sd2)
    def summ(x, col):
        x = x.dropna(subset=[col])
        m = x[col].mean(); s = x[col].std(); k = len(x)
        return pd.Series({"n":k,"mean%":100*m,"t":m/(s/np.sqrt(k)) if k>2 else np.nan})
    gg = d[d.pos % 2 == 0].copy()
    up = gg[gg.r1 > 0].copy()
    # 1. forecast buckets on up days
    up["fcb"] = pd.cut(up["fc"], [-20.1,-15,-10,-5,-0.01,0.01])
    out["up days: ex2 by forecast bucket"] = up.groupby("fcb", observed=True).apply(lambda x: summ(x,"ex2"))
    # 2. range position (20d) on up and down days, ex2 and ex1
    gg["p20b"] = pd.qcut(gg["pos20"], 5, labels=False)
    gg["updn"] = np.where(gg.r1>0,"up","down")
    out["ex2 by updown x pos20 quintile"] = gg.groupby(["updn","p20b"]).apply(lambda x: summ(x,"ex2"))
    out["ex1 by updown x pos20 quintile (all bars)"] = d.assign(p20b=pd.qcut(d.pos20,5,labels=False),updn=np.where(d.r1>0,"up","down")).groupby(["updn","p20b"]).apply(lambda x: summ(x,"ex1"))
    # 3. by trend regime
    gg["trend"] = pd.cut(gg["tr60"], [-10,-0.1,0.1,10], labels=["falling","choppy","rising"])
    gg["agit"] = np.where(gg.vol_rel>1,"agit","calm")
    upg = gg[gg.r1>0].copy()
    upg["deep"] = pd.qcut(upg["depth"], 3, labels=["deep","mid","shallow"])
    out["up days ex2 short-sign by trend x depth tercile"] = upg.groupby(["trend","deep"], observed=True).apply(lambda x: summ(x,"ex2"))
    out["ex2 all bars by trend x agit"] = gg.groupby(["trend","agit"], observed=True).apply(lambda x: summ(x,"ex2"))
    # 4. large moves: r1 quintile scaled
    d["r1z"] = d.r1/d.sd20
    d["r1zb"] = pd.qcut(d["r1z"], 7, labels=False)
    out["ex1 by r1/sd20 septile"] = d.groupby("r1zb").apply(lambda x: summ(x,"ex1"))
    # 5. weekday
    out["ex1 by weekday"] = d.groupby("wd").apply(lambda x: summ(x,"ex1"))
    # 6. close location in day's range
    d["clvb"] = pd.qcut(d["clv"], 5, labels=False)
    out["ex1 by clv quintile"] = d.groupby("clvb").apply(lambda x: summ(x,"ex1"))
    # 7. range width relative
    d["rngz"] = d.rng/d.sd20
    d["rngb"] = pd.qcut(d["rngz"],5,labels=False)
    out["ex1 by range/sd20 quintile"] = d.groupby("rngb").apply(lambda x: summ(x,"ex1"))
    # 8. year of the deep-fade cases
    upg["yrs"] = upg["yr"]
    out["up days deep tercile ex2 by year"] = upg[upg.deep=="deep"].groupby("yrs").apply(lambda x: summ(x,"ex2"))
    # 9. book days
    bd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            bd.append(x.assign(coin=coin, win=w))
    bd = pd.concat(bd)
    out["book daily by window mean% and coin mean%"] = bd.groupby("win")[["book_return","coin_return"]].mean()*100
    out["book daily corr with coin"] = float(bd[["book_return","coin_return"]].corr().iloc[0,1])
    return out
