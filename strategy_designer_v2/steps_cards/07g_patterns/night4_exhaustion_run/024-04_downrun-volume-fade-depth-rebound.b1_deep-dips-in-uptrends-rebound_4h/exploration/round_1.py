def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
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
            ret36 = pd.Series(c).pct_change(6).values  # 1-day
            vol30 = pd.Series(r).rolling(180, min_periods=60).std().values
            vol180 = pd.Series(r).rolling(1080, min_periods=300).std().values if n>1080 else np.full(n,np.nan)
            # streaks
            sdown = np.zeros(n); sup = np.zeros(n); ldown = np.zeros(n); lup=np.zeros(n)
            vstreak = np.full(n, np.nan)
            for i in range(1, n):
                if r[i] < 0:
                    sdown[i] = sdown[i-1] + r[i]; ldown[i] = ldown[i-1]+1
                elif r[i] > 0:
                    sup[i] = sup[i-1] + r[i]; lup[i] = lup[i-1]+1
            vma = pd.Series(v).rolling(30, min_periods=10).mean().values
            # volume fade: last 2 bars volume vs 30-bar mean
            v2 = pd.Series(v).rolling(2).mean().values
            fwd = np.full(n, np.nan)
            fwd[:n-H] = c[H:]/c[:n-H]-1
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, n, H)
            for i in idx:
                if np.isnan(fwd[i]): continue
                rows.append(dict(coin=coin, w=w, fwd=fwd[i],
                    dz=-sdown[i]/absr[i] if absr[i]>0 else np.nan,
                    uz=sup[i]/absr[i] if absr[i]>0 else np.nan,
                    ld=ldown[i], lu=lup[i], ret180=ret180[i], ret1d=ret36[i],
                    vr=v2[i]/vma[i] if vma[i]>0 else np.nan,
                    vol30=vol30[i], volratio=vol30[i]/vol180[i] if vol180[i]>0 else np.nan,
                    fc=b["forecast"].iloc[i], alloc=b["postRebalance_current_allocation"].iloc[i],
                    wd=ts.iloc[i].weekday(), hr=ts.iloc[i].hour))
    df = pd.DataFrame(rows)
    df["un"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    def summ(g):
        x = g["un"].dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    up = df["ret180"]>0
    df["dzb"] = pd.cut(df["dz"], [-0.01,0.01,1,2,3,5,100])
    df["uzb"] = pd.cut(df["uz"], [-0.01,0.01,1,2,3,5,100])
    out["down streak depth, ret30d>0"] = df[up].groupby("dzb").apply(summ)
    out["down streak depth, ret30d<=0"] = df[~up & df.ret180.notna()].groupby("dzb").apply(summ)
    out["up streak depth, ret30d>0"] = df[up].groupby("uzb").apply(summ)
    out["up streak depth, ret30d<=0"] = df[~up & df.ret180.notna()].groupby("uzb").apply(summ)
    # volume fade within deep down streaks
    deep = df[(df.dz>=2)]
    deep = deep.assign(vq=pd.qcut(deep["vr"], 3, labels=["fade","mid","high"]))
    out["deep down (dz>=2) by volume tercile"] = deep.groupby("vq").apply(summ)
    deepu = df[(df.uz>=2)]
    deepu = deepu.assign(vq=pd.qcut(deepu["vr"], 3, labels=["fade","mid","high"]))
    out["deep up (uz>=2) by volume tercile"] = deepu.groupby("vq").apply(summ)
    df["r1q"] = pd.qcut(df["ret1d"], 10, labels=False)
    out["1-day return decile"] = df.groupby("r1q").apply(summ)
    df["r30q"] = pd.qcut(df["ret180"], 5, labels=False)
    out["30-day return quintile"] = df.groupby("r30q").apply(summ)
    df["vq"] = pd.qcut(df["volratio"], 5, labels=False)
    out["vol30/vol180 quintile"] = df.groupby("vq").apply(summ)
    out["weekday"] = df.groupby("wd").apply(summ)
    out["by coin"] = df.groupby("coin").apply(summ)
    return out
