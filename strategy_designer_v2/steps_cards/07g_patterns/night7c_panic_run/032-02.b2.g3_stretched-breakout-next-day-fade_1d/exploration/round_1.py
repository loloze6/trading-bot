def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c, h, l = b["close"].astype(float), b["high"].astype(float), b["low"].astype(float)
            r1 = c.pct_change()
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            d["ret1"] = r1
            d["fwd1"] = c.shift(-1)/c - 1
            d["fwd3"] = c.shift(-3)/c - 1
            d["fwd5"] = c.shift(-5)/c - 1
            d["r5"] = c/c.shift(5) - 1
            d["r30"] = c/c.shift(30) - 1
            hh = h.shift(1).rolling(30).max(); ll = l.shift(1).rolling(30).min()
            d["dhigh"] = c/hh - 1
            d["dlow"] = c/ll - 1
            rng = (h - l)/c
            d["rng"] = rng
            d["rngz"] = rng/rng.shift(1).rolling(30).mean()
            d["vol20"] = r1.rolling(20).std()
            d["volratio"] = r1.rolling(5).std()/r1.rolling(60).std()
            d["clv"] = (c - l)/(h - l).replace(0, np.nan)
            d["z1"] = r1/r1.shift(1).rolling(60).std()
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.dayofweek
            d["year"] = pd.to_datetime(b["timestamp"]).dt.year
            d["alloc"] = b["postRebalance_current_allocation"].astype(float)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = {k: D.loc[D.pos % k == 0].groupby("coin")[f"fwd{k}"].mean() for k in (1,3,5)}
    for k in (1,3,5):
        D[f"ex{k}"] = D[f"fwd{k}"] - D["coin"].map(drift[k])
    out = {}
    def qtab(var, k=1, q=5, sub=None):
        X = D if sub is None else D[sub]
        X = X[X.pos % k == 0].dropna(subset=[var, f"ex{k}"]).copy()
        X["q"] = X.groupby("coin")[var].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        g = X.groupby("q")[f"ex{k}"]
        t = g.mean()/(g.std()/np.sqrt(g.count()))
        res = pd.DataFrame({"mean%": g.mean()*100, "t": t, "n": g.count()})
        # slope t pooled (per-coin standardised var)
        X["vs"] = X.groupby("coin")[var].transform(lambda s: (s - s.mean())/s.std())
        sl = stats.linregress(X["vs"], X[f"ex{k}"])
        res.loc["slope_t", "t"] = sl.slope/sl.stderr
        return res
    for var in ["z1","r5","r30","dhigh","dlow","rngz","volratio","clv"]:
        out[f"{var}_h1"] = qtab(var, 1)
    for var in ["z1","r5","r30","dlow","clv"]:
        out[f"{var}_h3"] = qtab(var, 3)
    # volatile decline: r30<0 and volratio top
    sub = (D.r30 < 0) & (D.volratio > D.groupby("coin").volratio.transform("median"))
    out["dlow_in_volfall_h3"] = qtab("dlow", 3, 5, sub)
    out["z1_in_volfall_h1"] = qtab("z1", 1, 5, sub)
    g = D.dropna(subset=["ex1"]).groupby("wd")["ex1"]
    out["weekday_h1"] = pd.DataFrame({"mean%": g.mean()*100, "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()})
    g = D.dropna(subset=["ex1"]).groupby("year")["ex1"]
    out["year_h1"] = pd.DataFrame({"mean%": g.mean()*100, "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()})
    br = D[D.dhigh > 0]
    g = br.dropna(subset=["ex1"]).groupby("coin")["ex1"]
    out["breakout_by_coin_h1"] = pd.DataFrame({"mean%": g.mean()*100, "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()})
    out["breakout_fwd5"] = qtab("dhigh", 5, 3, D.dhigh > 0)
    return out
