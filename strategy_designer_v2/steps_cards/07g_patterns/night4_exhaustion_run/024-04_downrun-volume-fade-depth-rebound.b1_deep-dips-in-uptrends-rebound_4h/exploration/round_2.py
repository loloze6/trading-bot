def explore(data):
    import numpy as np, pandas as pd
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            v = b["volume"].astype(float).values
            n = len(c)
            if n < 2*H: continue
            r = np.r_[np.nan, c[1:]/c[:-1]-1]
            absr = pd.Series(np.abs(r)).rolling(180, min_periods=60).mean().values
            ret180 = pd.Series(c).pct_change(180).values
            ret6 = pd.Series(c).pct_change(6).values
            ret18 = pd.Series(c).pct_change(18).values
            vol30 = pd.Series(r).rolling(180, min_periods=60).std().values
            vol180 = pd.Series(r).rolling(1080, min_periods=300).std().values
            sdown = np.zeros(n); sup = np.zeros(n)
            for i in range(1, n):
                if r[i] < 0: sdown[i] = sdown[i-1] + r[i]
                elif r[i] > 0: sup[i] = sup[i-1] + r[i]
            vma = pd.Series(v).rolling(30, min_periods=10).mean().values
            v2 = pd.Series(v).rolling(2).mean().values
            fwd = np.full(n, np.nan); fwd[:n-H] = c[H:]/c[:n-H]-1
            ts = pd.to_datetime(b["timestamp"])
            fc = b["forecast"].astype(float).values
            al = b["postRebalance_current_allocation"].astype(float).values
            for i in range(0, n, H):
                if np.isnan(fwd[i]): continue
                rows.append(dict(coin=coin, w=w, fwd=fwd[i],
                    dz=-sdown[i]/absr[i] if absr[i]>0 else np.nan,
                    uz=sup[i]/absr[i] if absr[i]>0 else np.nan,
                    ret180=ret180[i], ret1d=ret6[i]/(vol30[i]*np.sqrt(6)) if vol30[i]>0 else np.nan,
                    ret3d=ret18[i]/(vol30[i]*np.sqrt(18)) if vol30[i]>0 else np.nan,
                    vr=v2[i]/vma[i] if vma[i]>0 else np.nan,
                    volratio=vol30[i]/vol180[i] if vol180[i]>0 else np.nan,
                    fc=fc[i], alloc=al[i], wd=ts.iloc[i].weekday(), hr=ts.iloc[i].hour,
                    yr=ts.iloc[i].year))
    df = pd.DataFrame(rows)
    df["un"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    def summ(g):
        x = g["un"].dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(),
                          "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    def q(s, k):
        return pd.qcut(s.rank(method="first"), k, labels=False)
    out = {}
    up = df["ret180"]>0; dn = df["ret180"]<=0
    df["dzb"] = pd.cut(df["dz"], [-0.01,0.01,1,2,3,5,100])
    df["uzb"] = pd.cut(df["uz"], [-0.01,0.01,1,2,3,5,100])
    out["down depth, ret30d>0"] = df[up].groupby("dzb").apply(summ)
    out["down depth, ret30d<=0"] = df[dn].groupby("dzb").apply(summ)
    out["up depth, ret30d>0"] = df[up].groupby("uzb").apply(summ)
    out["up depth, ret30d<=0"] = df[dn].groupby("uzb").apply(summ)
    deep = df[df.dz>=2].copy(); deep["vq"] = q(deep["vr"], 3)
    out["deep down by vol-ratio tercile (0=fade)"] = deep.groupby("vq").apply(summ)
    deepu = df[df.uz>=2].copy(); deepu["vq"] = q(deepu["vr"], 3)
    out["deep up by vol-ratio tercile (0=fade)"] = deepu.groupby("vq").apply(summ)
    d = df.dropna(subset=["ret1d"]).copy(); d["k"] = q(d["ret1d"], 10)
    out["1d return z decile"] = d.groupby("k").apply(summ)
    d = df.dropna(subset=["ret3d"]).copy(); d["k"] = q(d["ret3d"], 10)
    out["3d return z decile"] = d.groupby("k").apply(summ)
    d = df.dropna(subset=["ret180"]).copy(); d["k"] = q(d["ret180"], 5)
    out["30d return quintile"] = d.groupby("k").apply(summ)
    d = df.dropna(subset=["volratio"]).copy(); d["k"] = q(d["volratio"], 5)
    out["vol30/vol180 quintile"] = d.groupby("k").apply(summ)
    out["weekday"] = df.groupby("wd").apply(summ)
    out["hour"] = df.groupby("hr").apply(summ)
    out["by coin"] = df.groupby("coin").apply(summ)
    out["by year"] = df.groupby("yr").apply(summ)
    out["in position vs flat"] = df.groupby(df["alloc"].abs()>0.01).apply(summ)
    # book
    dl = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["book_return","coin_return"]].copy(); x["coin"]=coin; x["w"]=w
            x["wd"] = pd.to_datetime(dd["day"]).dt.weekday
            x["yr"] = pd.to_datetime(dd["day"]).dt.year
            dl.append(x)
    D = pd.concat(dl).dropna()
    bk = D.groupby("coin")["book_return"].agg(["mean","std","count"])
    bk["sharpe"] = bk["mean"]/bk["std"]*np.sqrt(365)
    out["book by coin"] = bk
    out["book by year"] = D.groupby("yr")["book_return"].agg(["mean","count"])
    out["book by window"] = D.groupby("w")["book_return"].agg(["mean","count"]).T
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tt=t.copy(); tt["coin"]=coin; tr.append(tt)
    T = pd.concat(tr)
    T["fq"] = q(T["entry_forecast"].astype(float), 4)
    out["trades by entry forecast quartile"] = T.groupby("fq")["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trades by duration quartile"] = T.assign(k=q(T["duration_minutes"].astype(float),4)).groupby("k")[["net_profit_loss_percent","duration_minutes"]].mean()
    return out
