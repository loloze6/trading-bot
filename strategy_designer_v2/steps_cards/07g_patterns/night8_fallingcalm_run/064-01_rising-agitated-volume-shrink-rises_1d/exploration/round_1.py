def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            vr = np.log(v.rolling(30).mean() / v.shift(30).rolling(30).mean())
            ret20 = c / c.shift(20) - 1
            ret5p = c / c.shift(5) - 1
            ret1 = r1
            vol20 = r1.rolling(20).std()
            vol20rel = vol20 / r1.rolling(60).std()
            rng = (b["high"] - b["low"]) / c
            closepos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            fwd5 = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for i in range(0, n, 5):
                rows.append(dict(coin=coin, w=w, i=i, inprof=b["regime"].iat[i] == "unknown",
                                 fc=b["forecast"].iat[i], vr=vr.iat[i], ret20=ret20.iat[i], ret5p=ret5p.iat[i],
                                 ret1=ret1.iat[i], vol20=vol20.iat[i], vrel=vol20rel.iat[i], rng=rng.iat[i],
                                 cpos=closepos.iat[i], fwd5=fwd5.iat[i], fwd1=fwd1.iat[i],
                                 wd=ts.iat[i].weekday(), year=ts.iat[i].year,
                                 vchg5=np.log(v.iloc[max(0,i-4):i+1].mean() / v.iloc[max(0,i-34):max(1,i-4)].mean()) if i >= 34 else np.nan))
    df = pd.DataFrame(rows)
    df = df.dropna(subset=["fwd5"])
    mean5 = df.groupby("coin")["fwd5"].mean()
    df["ex5"] = df["fwd5"] - df["coin"].map(mean5)
    # z-score within coin for a few predictors
    def reg(sub, x):
        s = sub.dropna(subset=[x, "ex5"])
        if len(s) < 30: return (len(s), np.nan, np.nan)
        z = (s[x] - s[x].mean()) / s[x].std()
        sl = stats.linregress(z, s["ex5"])
        return (len(s), sl.slope, sl.slope / sl.stderr)
    out = {}
    preds = ["vr", "ret20", "ret5p", "ret1", "vol20", "vrel", "rng", "cpos", "vchg5"]
    res = []
    for x in preds:
        for lab, sub in [("all", df), ("inprof", df[df.inprof]), ("outprof", df[~df.inprof]),
                         ("up20", df[df.ret20 > 0.1]), ("down20", df[df.ret20 < -0.1]), ("flat20", df[df.ret20.abs() <= 0.1])]:
            n, s, t = reg(sub, x)
            res.append(dict(pred=x, set=lab, n=n, slope_per_sd=s, t=t))
    out["regressions ex5 on z(pred)"] = pd.DataFrame(res)
    # quintiles of vr in profile and out
    q = []
    for lab, sub in [("inprof", df[df.inprof]), ("outprof", df[~df.inprof])]:
        s = sub.dropna(subset=["vr"]).copy()
        s["qq"] = pd.qcut(s["vr"], 5, labels=False)
        g = s.groupby("qq")["ex5"].agg(["count", "mean"]); g["set"] = lab
        q.append(g.reset_index())
    out["vr quintiles"] = pd.concat(q)
    out["weekday ex5"] = df.groupby("wd")["ex5"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["year ex5 inprof fc>0"] = df[df.inprof & (df.fc > 0)].groupby("year")["ex5"].agg(["count", "mean"])
    out["coin inprof fc>0"] = df[df.inprof & (df.fc > 0)].groupby("coin")["ex5"].agg(["count", "mean"])
    out["share inprof"] = float(df.inprof.mean())
    return out
