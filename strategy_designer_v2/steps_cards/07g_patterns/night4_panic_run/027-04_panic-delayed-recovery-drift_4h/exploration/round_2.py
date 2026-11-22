def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = {"1d":6, "3d":18, "7d":42, "14d":84}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float); hi = df["high"].astype(float); lo = df["low"].astype(float)
            r1 = c.pct_change()
            f = pd.DataFrame(index=df.index)
            f["coin"] = coin; f["win"] = w
            f["r24"] = c/c.shift(6)-1
            sd6 = f["r24"].rolling(180, min_periods=60).std()
            f["z24"] = f["r24"]/sd6
            rng = hi.rolling(6).max()/lo.rolling(6).min()-1
            f["rngx"] = rng/rng.rolling(180, min_periods=60).mean()
            f["r7d"] = c/c.shift(42)-1
            f["vol30"] = r1.rolling(180, min_periods=60).std()
            col = "debug_info.components.panic.last_history_value"
            f["panic"] = pd.to_numeric(df[col], errors="coerce") if col in df.columns else np.nan
            f["fc"] = pd.to_numeric(df["forecast"], errors="coerce")
            ts = pd.to_datetime(df["timestamp"])
            f["hour"] = ts.dt.hour.values; f["wd"] = ts.dt.weekday.values
            f["ret1"] = c.shift(-1)/c-1
            pos = np.arange(len(df))
            for k,h in H.items():
                fr = c.shift(-h)/c-1
                f["fwd_"+k] = np.where(pos % h == 0, fr, np.nan)
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    for k in H:
        g = A.groupby("coin")["fwd_"+k]
        A["u_"+k] = A["fwd_"+k]-g.transform("mean")
        A["s_"+k] = A["u_"+k]/g.transform("std")
    out = {}
    def tab(feat, q=5, cond=None):
        B = A if cond is None else A[cond]
        B = B.dropna(subset=[feat]).copy()
        B["b"] = B.groupby("coin")[feat].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        res = {}
        for k in H:
            s = B.groupby("b")["s_"+k]
            res["str_"+k] = s.mean().round(4)
            res["t_"+k] = (s.mean()/(s.std()/np.sqrt(s.count()))).round(2)
        res["u_14d"] = B.groupby("b")["u_14d"].mean().round(4)
        res["n_1d"] = B.groupby("b")["s_1d"].count()
        res["n_14d"] = B.groupby("b")["s_14d"].count()
        res["feat_med"] = B.groupby("b")[feat].median().round(4)
        return pd.DataFrame(res)
    def safe(name, fn):
        try: out[name] = fn()
        except Exception as e: out[name] = "err: "+str(e)[:100]
    safe("z24_quintile", lambda: tab("z24"))
    safe("rngx_quintile", lambda: tab("rngx"))
    safe("r7d_quintile", lambda: tab("r7d"))
    safe("vol30_quintile", lambda: tab("vol30"))
    safe("panic_raw_quintile_nonzero", lambda: tab("panic", cond=A["panic"]>0))
    safe("z24_quintile_high_range", lambda: tab("z24", cond=A["rngx"]>A.groupby("coin")["rngx"].transform("median")))
    A["u1"] = A["ret1"]-A.groupby("coin")["ret1"].transform("mean")
    def hw(key):
        g=A.groupby(key)["u1"]
        return pd.DataFrame({"mean":g.mean().round(5),"t":(g.mean()/(g.std()/np.sqrt(g.count()))).round(2),"n":g.count()})
    safe("by_hour", lambda: hw("hour")); safe("by_weekday", lambda: hw("wd"))
    def act():
        B=A.assign(on=A["fc"]>0)
        r={}
        for k in H:
            g=B.groupby("on")["s_"+k]
            r["str_"+k]=g.mean().round(4); r["t_"+k]=(g.mean()/(g.std()/np.sqrt(g.count()))).round(2); r["n_"+k]=g.count()
        return pd.DataFrame(r)
    safe("fc_active_vs_not", act)
    def book():
        D=[]
        for coin,wins in data["days"].items():
            for w,d in wins.items():
                d=d.copy(); d["coin"]=coin; d["win"]=w
                cr=d["coin_return"]
                d["cr_prev3"]=(1+cr).rolling(3).apply(np.prod,raw=True).shift(1)-1
                d["cr_next3"]=(1+cr).rolling(3).apply(np.prod,raw=True).shift(-3)-1
                D.append(d)
        D=pd.concat(D).dropna(subset=["book_return"])
        D["bq"]=pd.qcut(D["book_return"].rank(method="first"),10,labels=False)
        return D
    try:
        D=book()
        out["book_decile"]=D.groupby("bq")[["book_return","coin_return","cr_prev3","cr_next3"]].mean().round(4)
        D["year"]=pd.to_datetime(D["day"]).dt.year
        out["book_by_year"]=D.groupby("year")[["book_return","coin_return"]].mean().round(5)
        out["book_by_coin"]=D.groupby("coin")[["book_return","coin_return"]].mean().round(5)
        out["book_by_window"]=D.groupby("win")["book_return"].agg(["mean","count"]).round(5)
    except Exception as e:
        out["book"]="err: "+str(e)[:100]
    return out
