def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].values.astype(float); v = b["volume"].values.astype(float)
            n = len(b); fc = b["forecast"].values
            idx = np.where((ts.dt.weekday.values == 6) & (ts.dt.hour.values == 23))[0]
            for i in idx:
                if i < 168 or i + 48 >= n: continue
                if (ts.iloc[i] - ts.iloc[i-168]) != pd.Timedelta(hours=168): continue
                if (ts.iloc[i+48] - ts.iloc[i]) != pd.Timedelta(hours=48): continue
                wk = c[i]/c[i-48]-1
                volr = np.nanmean(v[i-167:i-47]) / max(np.nanmean(v[i-47:i+1]), 1e-12)
                rows.append({"coin": coin, "win": w, "year": ts.iloc[i].year, "wk": wk, "volr": volr,
                             "fc": fc[i], "f24": c[i+24]/c[i]-1, "f48": c[i+48]/c[i]-1})
    df = pd.DataFrame(rows)
    df["wkz"] = df.groupby("coin")["wk"].transform(lambda s: s/s.std())
    for h in (24, 48):
        df[f"u{h}"] = df[f"f{h}"] - df.groupby("coin")[f"f{h}"].transform("mean")
    df["lvr"] = np.log(df["volr"])
    df["lvrc"] = df["lvr"] - df["lvr"].mean()
    out = {}
    # interaction regression
    X = np.column_stack([np.ones(len(df)), df["wkz"], df["lvrc"], df["wkz"]*df["lvrc"]])
    y = df["u48"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X@beta; s2 = res@res/(len(y)-4)
    se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["u48 ~ wkz + logvolr + wkz*logvolr"] = pd.DataFrame({"beta": beta, "t": beta/se},
        index=["const", "wkz", "logvolr", "wkz_x_logvolr"])
    # forecast sign agreement with -wkz
    nz = df[df["fc"] != 0]
    out["share forecast sign = -sign(weekend move)"] = float((np.sign(nz["fc"]) == -np.sign(nz["wk"])).mean())
    out["corr fc with -wkz*volr, with -wkz"] = pd.Series({"fc~-wkz*volr": np.corrcoef(nz["fc"], -nz["wkz"]*nz["volr"])[0,1],
                                                        "fc~-wkz": np.corrcoef(nz["fc"], -nz["wkz"])[0,1]})
    df["vq"] = pd.qcut(df["volr"], 3, labels=["thickwk", "mid", "thinwk"])
    df["rev48"] = -np.sign(df["wkz"])*df["u48"]
    def reg(d, y="u48", x="wkz"):
        d = d[[x, y]].dropna()
        if len(d) < 15: return (np.nan, np.nan, len(d))
        s = stats.linregress(d[x], d[y]); return (s.slope, s.slope/s.stderr, len(d))
    th = df[df["vq"] == "thinwk"]
    out["thin tercile: by year"] = pd.DataFrame({yv: reg(g) for yv, g in th.groupby("year")}, index=["slope","t","n"]).T
    out["thin tercile: by coin"] = pd.DataFrame({cv: reg(g) for cv, g in th.groupby("coin")}, index=["slope","t","n"]).T
    out["rev48 mean by vol tercile"] = df.groupby("vq").agg(rev48=("rev48","mean"), n=("rev48","size"),
        t=("rev48", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))), absmove=("wk", lambda s: s.abs().mean()))
    # graded within: quintiles of volr, slope
    df["v5"] = pd.qcut(df["volr"], 5, labels=False)
    out["slope by volr quintile"] = pd.DataFrame({q: reg(g) + (g["volr"].median(),) for q, g in df.groupby("v5")},
        index=["slope","t","n","median volr"]).T
    # thin tercile reversal by |move| tercile
    th = th.copy(); th["mq"] = pd.qcut(th["wkz"].abs(), 3, labels=["small","mid","large"])
    out["thin tercile: rev48 by |move|"] = th.groupby("mq").agg(rev48=("rev48","mean"), n=("rev48","size"),
        t=("rev48", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))))
    return out
