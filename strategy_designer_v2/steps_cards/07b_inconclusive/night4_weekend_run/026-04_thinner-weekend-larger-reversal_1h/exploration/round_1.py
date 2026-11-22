def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].values.astype(float); v = b["volume"].values.astype(float)
            n = len(b)
            fc = b["forecast"].values
            for i in range(n):
                t = ts.iloc[i]
                if not (t.weekday() == 6 and t.hour == 23):
                    continue
                if i < 168 or i + 120 >= n:
                    continue
                # check contiguity
                if (ts.iloc[i] - ts.iloc[i-168]) != pd.Timedelta(hours=168):
                    continue
                if (ts.iloc[i+120] - ts.iloc[i]) != pd.Timedelta(hours=120):
                    continue
                wk = c[i]/c[i-48]-1
                volr = np.nanmean(v[i-167:i-47]) / max(np.nanmean(v[i-47:i+1]), 1e-12)
                r = {"coin": coin, "win": w, "year": t.year, "wk": wk, "volr": volr, "fc": fc[i],
                     "wd_move": c[i-48]/c[i-168]-1}
                for h in (12, 24, 48, 72, 120):
                    r[f"f{h}"] = c[i+h]/c[i]-1
                rows.append(r)
    df = pd.DataFrame(rows)
    # normalise weekend move by coin's std of weekend moves
    df["wkz"] = df.groupby("coin")["wk"].transform(lambda s: s/s.std())
    for h in (12, 24, 48, 72, 120):
        df[f"u{h}"] = df[f"f{h}"] - df.groupby("coin")[f"f{h}"].transform("mean")
    def reg(d, y, x="wkz"):
        d = d[[x, y]].dropna()
        if len(d) < 10: return (np.nan, np.nan, len(d))
        s = stats.linregress(d[x], d[y])
        return (s.slope, s.slope/s.stderr, len(d))
    out = {}
    out["horizon: slope of unusual fwd on weekend z"] = pd.DataFrame(
        {h: reg(df, f"u{h}") for h in (12, 24, 48, 72, 120)}, index=["slope", "t", "n"]).T
    # by coin
    out["by coin, 48h"] = pd.DataFrame({c: reg(g, "u48") for c, g in df.groupby("coin")}, index=["slope","t","n"]).T
    out["by year, 48h"] = pd.DataFrame({y: reg(g, "u48") for y, g in df.groupby("year")}, index=["slope","t","n"]).T
    df["vq"] = pd.qcut(df["volr"], 3, labels=["thickwk", "mid", "thinwk"])
    out["by volume tercile, 48h & 24h"] = pd.DataFrame({q: reg(g, "u48") + reg(g, "u24")[:2] for q, g in df.groupby("vq")},
                                                        index=["slope48","t48","n","slope24","t24"]).T
    df["mq"] = pd.qcut(df["wkz"].abs(), 3, labels=["small", "mid", "large"])
    sg = np.sign(df["wkz"])
    df["rev48"] = -sg*df["u48"]; df["rev24"] = -sg*df["u24"]
    out["reversal mean by |move| tercile"] = df.groupby("mq").agg(rev48=("rev48","mean"), rev24=("rev24","mean"), n=("rev48","size"),
        t48=("rev48", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))))
    out["reversal by side"] = df.groupby(sg).agg(rev48=("rev48","mean"), n=("rev48","size"),
        t48=("rev48", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))))
    # weekday move (Mon-Fri 120h) continuation over next 48 (weekend) for comparison: not available fwd; skip
    df["wdz"] = df.groupby("coin")["wd_move"].transform(lambda s: s/s.std())
    out["weekday 5d move vs next 48h (control)"] = pd.DataFrame({"u48": reg(df, "u48", "wdz")}, index=["slope","t","n"]).T
    out["vol ratio summary"] = df["volr"].describe()
    out["corr volr with wkz abs"] = float(np.corrcoef(df["volr"], df["wkz"].abs())[0,1])
    return out
