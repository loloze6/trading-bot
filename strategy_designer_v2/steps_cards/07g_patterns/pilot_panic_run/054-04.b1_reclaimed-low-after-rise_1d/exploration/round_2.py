def explore(data):
    import numpy as np, pandas as pd
    H = 10
    rows = []; base = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; l = b["low"].values; h = b["high"].values
            n = len(b)
            for i in range(0, n - H, H):
                base.append((coin, c[i + H] / c[i] - 1))
            ts = pd.to_datetime(b["timestamp"])
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            v30 = pd.Series(r1).rolling(30).std()
            vpct = v30.expanding(60).apply(lambda x: (x <= x[-1]).mean(), raw=True).values
            for i in range(30, n):
                p30 = l[i - 30:i].min()
                rec = l[i] < p30 and c[i] >= p30
                brk = c[i] < p30
                if not (rec or brk): continue
                fwd = c[i + H] / c[i] - 1 if i + H < n else np.nan
                rows.append(dict(coin=coin, w=w, cell=i // H, day=ts.iloc[i].normalize(), fwd=fwd,
                                 kind="rec" if rec else "brk",
                                 ret60=c[i] / c[i - 60] - 1 if i >= 60 else np.nan,
                                 depth=(p30 - l[i]) / c[i], below=(p30 - c[i]) / c[i],
                                 cl=(c[i] - l[i]) / (h[i] - l[i]) if h[i] > l[i] else np.nan,
                                 agit=(vpct[i] > 0.5) if not np.isnan(vpct[i]) else np.nan,
                                 yr=ts.iloc[i].year, wd=ts.iloc[i].dayofweek))
    E = pd.DataFrame(rows)
    bs = pd.DataFrame(base, columns=["coin", "r"])
    drift = bs.groupby("coin")["r"].mean(); usual = bs.groupby("coin")["r"].std()
    E["ab"] = E["fwd"] - E["coin"].map(drift)
    E["str"] = E["ab"] / E["coin"].map(usual)
    def summ(df):
        d = df.dropna(subset=["ab"]).drop_duplicates(["coin", "w", "cell"])
        if len(d) < 3: return pd.Series(dict(n=len(d), days=np.nan, mean=np.nan, t_day=np.nan, strength=np.nan))
        m = d["ab"].mean(); g = (d["ab"] - m).groupby(d["day"]).sum(); D = len(g)
        se = np.sqrt((g ** 2).sum() * D / (D - 1)) / len(d)
        return pd.Series(dict(n=len(d), days=D, mean=m, t_day=m / se, strength=d["str"].mean()))
    out = {}
    for k in ["rec", "brk"]:
        X = E[E.kind == k].copy()
        out[k + " all"] = summ(X)
        X["tr"] = pd.cut(X["ret60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
        out[k + " by trend x agit"] = X.groupby(["tr", "agit"]).apply(summ)
        out[k + " by year"] = X.groupby("yr").apply(summ)
        out[k + " by coin"] = X.groupby("coin").apply(summ)
        X["r60q"] = pd.qcut(X["ret60"], 4, labels=False)
        out[k + " by ret60 quartile"] = X.groupby("r60q").apply(summ)
    X = E[E.kind == "rec"].copy()
    X["dq"] = pd.qcut(X["depth"], 3, labels=False)
    X["fallish"] = X["ret60"] < -0.1
    out["rec depth x falling"] = X.groupby(["fallish", "dq"]).apply(summ)
    X["clq"] = pd.qcut(X["cl"], 3, labels=False)
    out["rec closeloc x falling"] = X.groupby(["fallish", "clq"]).apply(summ)
    Y = E[E.kind == "brk"].copy()
    Y["bq"] = pd.qcut(Y["below"], 3, labels=False)
    out["brk by distance below"] = Y.groupby("bq").apply(summ)
    Y["fallish"] = Y["ret60"] < -0.1
    out["brk dist x falling"] = Y.groupby(["fallish", "bq"]).apply(summ)
    out["any event (rec or brk) by trend"] = E.assign(tr=pd.cut(E["ret60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])).groupby("tr").apply(summ)
    return out
