def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            sig = r1.rolling(720, min_periods=360).std()
            vr = v / v.rolling(720, min_periods=360).mean()
            z = r1 / sig
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for h in (2, 6, 24):
                idx = np.arange(0, n - h, h)
                fr = (c.shift(-h) / c - 1).values[idx]
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "z": z.values[idx], "vr": vr.values[idx],
                    "sig": sig.values[idx], "fr": fr, "hour": ts.dt.hour.values[idx], "wd": ts.dt.weekday.values[idx],
                    "year": ts.dt.year.values[idx],
                    "r24": (c / c.shift(24) - 1).values[idx], "sig24": (sig*np.sqrt(24)).values[idx]}))
    df = pd.concat(rows).dropna()
    # drift per coin per h
    drift = df.groupby(["coin","h"])["fr"].transform("mean")
    df["ur"] = df["fr"] - drift
    df["uz"] = df["ur"] / (df["sig"]*np.sqrt(df["h"]))
    def summ(g):
        return pd.Series({"n": len(g), "mean_ur_%": g.ur.mean()*100, "t": g.ur.mean()/(g.ur.std()/np.sqrt(len(g))), "strength": g.uz.mean()})
    df["zbin"] = pd.cut(df.z, [-99,-4,-2.5,-1.5,1.5,2.5,4,99])
    df["vbin"] = pd.cut(df.vr, [0,1,2,4,999])
    for h in (2,6,24):
        d = df[df.h==h]
        out[f"z_x_vol h{h}"] = d.groupby(["zbin","vbin"], observed=True).apply(summ).reset_index()
    d = df[df.h==24]
    d["mbin"] = pd.qcut(d.r24/d.sig24, 10, duplicates="drop")
    out["past24h_move_decile h24"] = d.groupby("mbin", observed=True).apply(summ).reset_index()
    d["sbin"] = d.groupby("coin")["sig"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["vol_quintile h24"] = d.groupby("sbin").apply(summ).reset_index()
    d1 = df[df.h==2]
    out["hour h2"] = d1.groupby("hour").apply(summ).reset_index()
    out["weekday h24"] = d.groupby("wd").apply(summ).reset_index()
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    dd = pd.concat(dd).dropna(subset=["book_return","coin_return"])
    dd["year"] = pd.to_datetime(dd["day"]).dt.year
    out["book by coin"] = dd.groupby("coin").agg(book=("book_return","mean"), hold=("coin_return","mean"), n=("book_return","size"))
    out["book by year"] = dd.groupby("year").agg(book=("book_return","mean"), hold=("coin_return","mean"), n=("book_return","size"))
    return out
