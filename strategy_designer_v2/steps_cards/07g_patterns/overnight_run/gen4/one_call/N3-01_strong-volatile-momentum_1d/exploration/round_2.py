def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            c = d["close"].astype(float)
            r = np.log(c).diff()
            d["f1"] = r.shift(-1)
            d["f5"] = np.log(c.shift(-5) / c)
            d["ret20"] = c / c.shift(20) - 1
            d["ret60"] = c / c.shift(60) - 1
            d["vol20"] = r.rolling(20).std()
            d["z"] = r / d["vol20"].shift(1)
            ts = pd.to_datetime(d["timestamp"])
            d["wd"] = ts.dt.weekday; d["yr"] = ts.dt.year
            d["nwd"] = (ts + pd.Timedelta(days=1)).dt.weekday
            d["coin"] = coin; d["win"] = w; d["pos"] = np.arange(len(d))
            rows.append(d[["coin","win","pos","f1","f5","ret20","ret60","vol20","z","wd","nwd","yr","forecast"]])
    A = pd.concat(rows, ignore_index=True)
    A["xf1"] = A["f1"] - A["coin"].map(A.groupby("coin")["f1"].mean())
    def summ(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    A["thufri"] = A["wd"].isin([3,4])
    out["thu/fri bar next-day excess by year"] = A[A["thufri"]].groupby("yr")["xf1"].apply(summ).unstack()
    out["thu/fri bar next-day excess by coin"] = A[A["thufri"]].groupby("coin")["xf1"].apply(summ).unstack()
    out["mon/wed bar next-day excess by year"] = A[A["wd"].isin([0,2])].groupby("yr")["xf1"].apply(summ).unstack()
    # positive shock continuation robustness
    cm5 = A[A["pos"]%5==0].groupby("coin")["f5"].mean()
    ev = []
    for (coin,w), g in A.groupby(["coin","win"]):
        last = -10
        for _,row in g[g["z"].abs()>2].iterrows():
            if row["pos"]-last>=5 and not np.isnan(row["f5"]):
                ev.append((coin, row["yr"], np.sign(row["z"]), row["ret60"]>0, row["f5"]-cm5[coin])); last=row["pos"]
    E = pd.DataFrame(ev, columns=["coin","yr","sgn","up60","x5"])
    P = E[E["sgn"]>0]
    out["up-shock 5d excess by coin"] = P.groupby("coin")["x5"].apply(summ).unstack()
    out["up-shock 5d excess by year"] = P.groupby("yr")["x5"].apply(summ).unstack()
    out["shock 5d excess by sign x ret60>0"] = E.groupby(["sgn","up60"])["x5"].apply(summ).unstack()
    # up/up combo robustness
    G = A[A["pos"]%5==0].copy()
    G["xf5"] = G["f5"] - G["coin"].map(cm5)
    U = G[(G["ret20"]>0)&(G["ret60"]>0)]
    out["up/up 5d excess by coin"] = U.groupby("coin")["xf5"].apply(summ).unstack()
    out["up/up 5d excess by year"] = U.groupby("yr")["xf5"].apply(summ).unstack()
    out["up/up 5d excess active vs not"] = U.groupby(U["forecast"]>0)["xf5"].apply(summ).unstack()
    return out
