def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    hourly = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].values.astype(float)
            v = df["volume"].values.astype(float)
            n = len(c)
            if n < 400: continue
            lr = np.r_[np.nan, np.diff(np.log(c))]
            ts = pd.to_datetime(df["timestamp"])
            hr = ts.dt.hour.values; wd = ts.dt.weekday.values
            hourly.append(pd.DataFrame({"coin": coin, "hour": hr, "wd": wd, "r": np.r_[c[1:]/c[:-1]-1, np.nan]}))
            for H in (24, 72):
                for t in range(0, n, H):
                    if t < 168 or t + H >= n: continue
                    seg = lr[t-71:t+1]; vs = v[t-71:t+1]
                    sa = np.nansum(np.abs(seg))
                    if sa <= 0 or vs.sum() <= 0: continue
                    r72 = c[t]/c[t-72]-1; r24 = c[t]/c[t-24]-1
                    rows.append(dict(coin=coin, win=w, H=H, r24=r24, r72=r72,
                        eff=abs(np.nansum(seg))/sa,
                        jump=np.nanmax(np.abs(seg))/sa,
                        top3=np.sort(np.abs(seg))[-3:].sum()/sa,
                        vconc=np.sort(vs)[-3:].sum()/vs.sum(),
                        vol168=np.nanstd(lr[t-167:t+1]),
                        fwd=c[t+H]/c[t]-1, hour=hr[t], wd=wd[t]))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin","H"])["fwd"].transform("mean")
    R["sd"] = R.groupby(["coin","H"])["fwd"].transform("std")
    R["ex"] = (R["fwd"]-R["drift"])/R["sd"]
    R["dir"] = np.sign(R["r72"])
    R["cont"] = R["dir"]*R["ex"]
    R["absz"] = R["r72"].abs()/R.groupby(["coin","H"])["r72"].transform("std")
    for H in (24, 72):
        S = R[R.H == H].copy()
        S["effq"] = S.groupby("coin")["eff"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
        S["jq"] = S.groupby("coin")["top3"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
        S["vq"] = S.groupby("coin")["vconc"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
        S["sq"] = S.groupby("coin")["absz"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
        S["volq"] = S.groupby("coin")["vol168"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
        def tab(g):
            return S.groupby(g)["cont"].agg(["mean","count",lambda x: x.mean()/x.std()*np.sqrt(len(x))]).rename(columns={"<lambda_0>":"t"})
        out[f"H{H} cont by eff quintile"] = tab("effq")
        out[f"H{H} cont by top3 jump quintile"] = tab("jq")
        out[f"H{H} cont by vol-conc quintile"] = tab("vq")
        out[f"H{H} cont by size quintile"] = tab("sq")
        # regression cont ~ absz + eff + top3 + vconc (standardized within coin)
        X = S[["absz","eff","top3","vconc"]].copy()
        X = (X - X.groupby(S["coin"]).transform("mean"))/X.groupby(S["coin"]).transform("std")
        X = X.assign(const=1.0).values; y = S["cont"].values
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X@b; s2 = res@res/(len(y)-X.shape[1])
        se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        out[f"H{H} regression"] = pd.DataFrame({"b": b, "t": b/se}, index=["absz","eff","top3","vconc","const"])
        # fall rebound by vol level (24h fall)
        S["fall"] = -S["r24"]; S["rev24"] = -np.sign(S["r24"])*S["ex"]
        out[f"H{H} reversal of 24h move by vol quintile"] = S.groupby("volq")["rev24"].agg(["mean","count",lambda x: x.mean()/x.std()*np.sqrt(len(x))])
        out[f"H{H} by coin eff corr"] = S.groupby("coin").apply(lambda g: pd.Series({"corr_eff_cont": g["eff"].corr(g["cont"]), "corr_top3_cont": g["top3"].corr(g["cont"]), "n": len(g)}))
    Hh = pd.concat(hourly).dropna()
    Hh["rz"] = Hh.groupby("coin")["r"].transform(lambda x: (x - x.mean())/x.std())
    out["hour of day excess z"] = Hh.groupby("hour")["rz"].agg(["mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["weekday excess z"] = Hh.groupby("wd")["rz"].agg(["mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    return out
