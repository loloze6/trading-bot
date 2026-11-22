def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    hourrows = []
    for coin, wins in data["bars"].items():
        per = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            v = b["volume"].astype(float).values
            n = len(c)
            if n < 200: continue
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            mabs = pd.Series(np.abs(r1)).rolling(180, min_periods=90).mean().values
            # streaks
            sl = np.zeros(n); sstart = np.zeros(n, dtype=int)
            for i in range(1, n):
                s = np.sign(r1[i])
                if i > 1 and np.sign(r1[i-1]) == s and s != 0:
                    sl[i] = sl[i-1] + s
                    sstart[i] = sstart[i-1]
                else:
                    sl[i] = s; sstart[i] = i - 1
            sgain = c / c[sstart] - 1
            vfade = np.log(np.maximum(v[np.minimum(sstart + 1, n - 1)], 1e-12) / np.maximum(v, 1e-12))
            r6 = np.r_[[np.nan]*6, c[6:]/c[:-6]-1]
            r18p = np.r_[[np.nan]*18, c[18:]/c[:-18]-1]
            vol30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            vol180 = pd.Series(r1).rolling(180, min_periods=90).std().values
            vrel = pd.Series(v).rolling(6).sum().values / pd.Series(v).rolling(180, min_periods=90).mean().values / 6
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fwd=c[i+H]/c[i]-1, fwd6=c[min(i+6,n-1)]/c[i]-1,
                    sl=sl[i], sg=sgain[i]/mabs[i] if mabs[i] > 0 else np.nan, vf=vfade[i],
                    m6=r6[i]/mabs[i] if mabs[i] > 0 else np.nan,
                    m18=r18p[i]/mabs[i] if mabs[i] > 0 else np.nan,
                    vr=vol30[i]/vol180[i] if vol180[i] > 0 else np.nan, vrel=vrel[i],
                    wd=ts.iloc[i].dayofweek, yr=ts.iloc[i].year))
            for i in range(1, n - 1):
                hourrows.append((coin, ts.iloc[i].hour, ts.iloc[i].dayofweek, c[i+1]/c[i]-1))
    df = pd.DataFrame(rows)
    df["adj"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    df["adj6"] = df["fwd6"] - df.groupby("coin")["fwd6"].transform("mean")
    def tab(col, q=5, sub=None, y="adj"):
        d = df if sub is None else df[sub]
        d = d.dropna(subset=[col, y])
        g = pd.qcut(d[col].rank(method="first"), q, labels=False)
        out = d.groupby(g)[y].agg(["count", "mean", "std"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        out["xmean"] = d.groupby(g)[col].mean()
        return out.round(5)
    res = {}
    res["up streak gain (usual moves), up bars"] = tab("sg", sub=df["sl"] > 0)
    res["down streak loss, down bars"] = tab("sg", sub=df["sl"] < 0)
    res["streak length all"] = df.groupby(df["sl"].clip(-5, 5))["adj"].agg(["count", "mean"]).assign(t=lambda x: x["mean"]/ (df.groupby(df["sl"].clip(-5,5))["adj"].std()/np.sqrt(x["count"]))).round(5)
    res["vol fade, up streaks >=3"] = tab("vf", q=4, sub=df["sl"] >= 3)
    res["past 1d move"] = tab("m6", q=5)
    res["past 3d move"] = tab("m18", q=5)
    res["vol ratio 30/180"] = tab("vr", q=5)
    res["volume 1d rel"] = tab("vrel", q=5)
    res["past 3d move, 1d fwd"] = tab("m18", q=5, y="adj6")
    h = pd.DataFrame(hourrows, columns=["coin", "hour", "wd", "r"])
    h["a"] = h["r"] - h.groupby("coin")["r"].transform("mean")
    g = h.groupby("hour")["a"].agg(["count", "mean", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    res["hour next bar"] = g.round(6)
    g = h.groupby("wd")["a"].agg(["count", "mean", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    res["weekday next bar"] = g.round(6)
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    D = pd.concat(dd)
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    bd = D.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    bd["yr"] = pd.to_datetime(bd.index).year
    res["book by year"] = bd.groupby("yr").agg(n=("book_return", "count"), book=("book_return", "mean"), coin=("coin_return", "mean")).round(5)
    res["corr book vs coin daily"] = float(bd["book_return"].corr(bd["coin_return"]))
    return res
