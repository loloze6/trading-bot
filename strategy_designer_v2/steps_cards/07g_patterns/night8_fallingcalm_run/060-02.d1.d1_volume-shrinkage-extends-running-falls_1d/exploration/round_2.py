def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = 5
    drift = {}
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            rs += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(rs)
    rows = []; drows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            agi = sd30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            vr = np.log(v.rolling(30).mean() / v.shift(30).rolling(30).mean())
            ret20 = c / c.shift(20) - 1
            ret60 = c / c.shift(60) - 1
            z1 = r1 / sd30.shift(1)
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            prof = np.where(ret60 > 0.1, "rising", np.where(ret60 < -0.1, "falling", np.where(ret60.notna(), "choppy", "na")))
            ag = np.where(agi > 0.5, "agit", np.where(agi.notna(), "calm", "na"))
            for i in range(len(b)):
                drows.append(dict(coin=coin, w=w, yr=ts.iloc[i].year, wd=ts.iloc[i].weekday(), prof=prof[i], ag=ag[i],
                                  r=(c.iloc[i+1]/c.iloc[i]-1) if i+1 < len(b) else np.nan))
            for i in range(0, len(b) - H, H):
                rows.append(dict(coin=coin, w=w, yr=ts.iloc[i].year, prof=prof[i], ag=ag[i], vr=vr.iloc[i], ret20=ret20.iloc[i],
                                 z1=z1.iloc[i], un=fwd.iloc[i]-drift[coin]))
    g = pd.DataFrame(rows); D = pd.DataFrame(drows).dropna(subset=["r"])
    def summ(df, key, col="un"):
        a = df.dropna(subset=[col]).groupby(key)[col]
        r = a.agg(["count", "mean"]); r["t"] = a.mean() / (a.std() / np.sqrt(a.count()))
        return r.round(4)
    # weekday by profile, next-day return from the bar (bar of weekday wd -> next day's return)
    for p in ["rising", "choppy", "falling"]:
        out[f"next-day ret by weekday of bar, {p}"] = summ(D[D.prof == p], "wd", "r")
    D["late"] = D.wd.isin([3, 4])  # bars Thu,Fri -> next-day Fri,Sat returns
    out["late-week (bar Thu/Fri) next-day, by prof x ag"] = summ(D, ["prof", "ag", "late"], "r")
    out["late-week by year (all)"] = summ(D[D.late], "yr", "r")
    out["late-week by year (falling)"] = summ(D[D.late & (D.prof == "falling")], "yr", "r")
    f = g[g.prof == "falling"].dropna(subset=["vr"]).copy()
    f["vrq"] = pd.qcut(f.vr, 3, labels=False)
    out["falling: vr tercile x agitation"] = summ(f, ["ag", "vrq"])
    out["falling: vr tercile x ret20 sign"] = summ(f.assign(s=np.sign(f.ret20)), ["s", "vrq"])
    f["v0"] = f.vrq == 0
    out["falling lowest vr tercile by year"] = summ(f[f.v0], "yr")
    fz = g[g.prof == "falling"].dropna(subset=["z1"]).copy()
    fz["zq"] = pd.qcut(fz.z1, 5, labels=False)
    out["falling: z1 quintile x agitation"] = summ(fz, ["ag", "zq"])
    out["falling z1 q0-1 by year"] = summ(fz[fz.zq <= 1], "yr")
    out["corr vr vs z1 in falling"] = float(g[g.prof=="falling"][["vr","z1"]].corr().iloc[0,1])
    return out
