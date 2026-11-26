def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 2, 3]
    drift = {}
    for c in bars:
        drift[c] = {}
        for h in H:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[c][h] = np.mean(rs) if rs else np.nan
    rows = []; base = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            r1 = pd.Series(cl).pct_change()
            sd = r1.rolling(30).std()
            z = (r1 / sd).values
            f = b["forecast"].values
            reg = b["regime"].values
            n = len(b)
            for i in range(n - 1):
                if reg[i] == "unknown":
                    base.append({"coin": c, "up": r1.iloc[i] > 0, "z": z[i],
                                 "u1": -(cl[i+1]/cl[i]-1-drift[c][1]), "t1": -(cl[i+1]/cl[i]-1),
                                 "day": str(b["timestamp"].iloc[i])[:10]})
            for s in range(0, n, 3):
                for i in range(s, min(s + 3, n)):
                    if f[i] <= -2:
                        d = {"coin": c, "win": w, "f": -f[i], "z": z[i], "day": str(b["timestamp"].iloc[i])[:10]}
                        for h in H:
                            d["u%d" % h] = -(cl[i+h]/cl[i]-1-drift[c][h]) if i+h < n else np.nan
                            d["t%d" % h] = -(cl[i+h]/cl[i]-1) if i+h < n else np.nan
                        rows.append(d); break
    df = pd.DataFrame(rows); bs = pd.DataFrame(base)
    def ct(x, days):
        m = pd.DataFrame({"x": x, "d": days}).dropna()
        dev = m["x"] - m["x"].mean()
        s = dev.groupby(m["d"]).sum()
        return m["x"].mean() / (np.sqrt((s**2).sum()) / len(m)) if len(m) > 2 else np.nan
    res = {}
    tot = {}
    for h in H:
        tot["tot%d" % h] = df["t%d" % h].mean(); tot["t_tot%d" % h] = ct(df["t%d" % h].values, df["day"].values)
        m = df[["f", "u%d" % h]].dropna(); r = stats.linregress(m["f"], m["u%d" % h])
        tot["f_slope_t%d" % h] = r.slope / r.stderr
    res["cases_total_and_fslopes"] = pd.Series(tot)
    g = bs.dropna().groupby("up").agg(n=("u1", "size"), u1=("u1", "mean"), t1=("t1", "mean"))
    res["profile_days_up_vs_not_1d"] = g
    up = bs[bs["up"]].dropna().copy()
    up["zq"] = pd.qcut(up["z"], 5, labels=False, duplicates="drop")
    res["profile_up_days_by_z_quintile_1d"] = up.groupby("zq").agg(n=("u1","size"), zmean=("z","mean"), u1=("u1","mean"), t1=("t1","mean"))
    r = stats.linregress(up["z"], up["u1"])
    res["profile_up_days_z_slope_1d"] = pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(up)})
    nu = bs[~bs["up"]].dropna()
    res["up_minus_notup_u1_welch_t"] = stats.ttest_ind(up["u1"], nu["u1"], equal_var=False).statistic
    return res
