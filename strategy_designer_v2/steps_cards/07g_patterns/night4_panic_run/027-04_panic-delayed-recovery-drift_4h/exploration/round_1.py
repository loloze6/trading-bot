def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = {"1d":6, "3d":18, "7d":42, "14d":84}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float); hi = df["high"].astype(float); lo = df["low"].astype(float)
            r1 = c.pct_change()
            f = pd.DataFrame({"coin":coin, "win":w})
            f["r24"] = c/c.shift(6)-1
            sd6 = (c/c.shift(6)-1).rolling(180, min_periods=60).std()
            f["z24"] = f["r24"]/sd6
            rng = hi.rolling(6).max()/lo.rolling(6).min()-1
            f["rngx"] = rng/rng.rolling(180, min_periods=60).mean()
            f["r7d"] = c/c.shift(42)-1
            f["vol30"] = r1.rolling(180, min_periods=60).std()
            f["panic"] = df.get("debug_info.components.panic.last_history_value")
            f["fc"] = df["forecast"]
            ts = pd.to_datetime(df["timestamp"])
            f["hour"] = ts.dt.hour; f["wd"] = ts.dt.weekday; f["year"] = ts.dt.year
            f["ret1"] = c.shift(-1)/c-1
            for k,h in H.items():
                fr = c.shift(-h)/c-1
                grid = (np.arange(len(df)) % h)==0
                f["fwd_"+k] = np.where(grid, fr, np.nan)
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    for k in H:
        col="fwd_"+k
        g = A.groupby("coin")[col]
        A["u_"+k] = A[col]-g.transform("mean")
        A["s_"+k] = A["u_"+k]/g.transform("std")
    out = {}
    def tab(feat, q=5, cond=None):
        B = A if cond is None else A[cond]
        B = B.dropna(subset=[feat]).copy()
        B["b"] = B.groupby("coin")[feat].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        res = {}
        for k in H:
            s = B.groupby("b")["s_"+k]
            u = B.groupby("b")["u_"+k]
            res["str_"+k] = s.mean().round(4)
            res["t_"+k] = (s.mean()/(s.std()/np.sqrt(s.count()))).round(2)
            res["u_"+k] = u.mean().round(4)
        res["n_14d"] = B.groupby("b")["s_14d"].count()
        res["feat_med"] = B.groupby("b")[feat].median().round(4)
        return pd.DataFrame(res)
    out["z24_quintile"] = tab("z24")
    out["rngx_quintile"] = tab("rngx")
    out["r7d_quintile"] = tab("r7d")
    out["vol30_quintile"] = tab("vol30")
    out["panic_raw_quintile_nonzero"] = tab("panic", cond=A["panic"]>0)
    out["z24_quintile_high_range"] = tab("z24", cond=A["rngx"]>A.groupby("coin")["rngx"].transform("median"))
    # hour / weekday
    A["u1"] = A["ret1"]-A.groupby("coin")["ret1"].transform("mean")
    def hw(key):
        g=A.groupby(key)["u1"]
        return pd.DataFrame({"mean":g.mean().round(5),"t":(g.mean()/(g.std()/np.sqrt(g.count()))).round(2),"n":g.count()})
    out["by_hour"]=hw("hour"); out["by_weekday"]=hw("wd")
    # forecast active vs not
    out["fc_active_vs_not"] = A.assign(on=A["fc"]>0).groupby("on")[["s_1d","s_3d","s_14d"]].agg(["mean","count"]).round(4)
    # book days
    D=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["win"]=w
            d["cr_prev3"]=(1+d["coin_return"]).rolling(3).apply(np.prod,raw=True).shift(1)-1
            D.append(d)
    D=pd.concat(D)
    D=D.dropna(subset=["book_return"])
    D["bq"]=pd.qcut(D["book_return"].rank(method="first"),10,labels=False)
    out["book_decile"]=D.groupby("bq")[["book_return","coin_return","cr_prev3"]].mean().round(4)
    D["year"]=pd.to_datetime(D["day"]).dt.year
    out["book_by_year"]=D.groupby("year")[["book_return","coin_return"]].agg(["mean","count"]).round(5)
    return out
