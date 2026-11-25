def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r7 = c / c.shift(7) - 1
            s7 = r7 / (sd30 * np.sqrt(7))
            r3 = c / c.shift(3) - 1
            s3 = r3 / (sd30 * np.sqrt(3))
            r14 = c / c.shift(14) - 1
            s14 = r14 / (sd30 * np.sqrt(14))
            r30 = c / c.shift(30) - 1
            s30 = r30 / (sd30 * np.sqrt(30))
            fwd = c.shift(-H) / c - 1
            fwd3 = c.shift(-3) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "s7": s7, "s3": s3, "s14": s14, "s30": s30,
                               "fwd": fwd, "fwd3": fwd3, "regime": b["regime"].astype(str),
                               "year": ts.dt.year, "day": ts.dt.floor("D"), "sd30": sd30})
            df = df.iloc[::H]
            rows.append(df)
    g = pd.concat(rows).dropna(subset=["fwd"])
    drift = g.groupby("coin")["fwd"].mean()
    g["u"] = g["fwd"] - g["coin"].map(drift)
    g["usual"] = g.groupby("coin")["fwd"].transform("std")
    g["calm"] = np.where(g["regime"] == "chop", "agitated", "calm")
    out = {}

    def reg(sub, x, y="u"):
        sub = sub.dropna(subset=[x, y])
        if len(sub) < 30: return pd.Series({"n": len(sub)})
        sl = stats.linregress(sub[x], sub[y])
        return pd.Series({"n": len(sub), "slope": sl.slope, "t": sl.slope / sl.stderr})

    def daytm(sub):
        s = sub.groupby("day")["dev"].sum()
        n = sub.groupby("day").size()
        m = s.sum() / n.sum()
        # day-clustered t of mean
        e = (sub["dev"] - m).groupby(sub["day"]).sum()
        se = np.sqrt((e ** 2).sum()) / n.sum()
        return m, m / se, len(s)

    calm = g[g["calm"] == "calm"]
    neg = calm[calm["s7"] < 0].copy()
    out["calm fall s7<0 slope by year"] = pd.DataFrame({y: reg(s, "s7") for y, s in neg.groupby("year")}).T
    out["calm fall s7<0 slope by coin"] = pd.DataFrame({k: reg(s, "s7") for k, s in neg.groupby("coin")}).T
    out["calm fall s3<0 slope by year"] = pd.DataFrame({y: reg(s, "s3") for y, s in calm[calm["s3"] < 0].groupby("year")}).T
    # size of falls in short direction, day-clustered
    sz = {}
    for nm, sub in [("calm s7<0", neg), ("calm s3<0", calm[calm["s3"] < 0]), ("agit s7<0", g[(g["calm"] == "agitated") & (g["s7"] < 0)]),
                    ("calm s7>0", calm[calm["s7"] > 0])]:
        sub = sub.copy()
        sgn = -1 if "<0" in nm else 1
        sub["dev"] = sgn * sub["u"]
        m, t, nd = daytm(sub)
        sub["dev"] = sgn * sub["fwd"]
        mt, tt, _ = daytm(sub)
        sz[nm] = {"cases": len(sub), "days": nd, "unusual": m, "t_day": t, "total": mt, "t_total": tt,
                  "strength": (sgn * sub["u"] / sub["usual"]).mean()}
    out["size in signal direction"] = pd.DataFrame(sz).T
    # other lookbacks in calm, all signs
    lk = {}
    for x in ["s3", "s7", "s14", "s30"]:
        lk[("calm", x)] = reg(calm, x)
        lk[("calm", x, "neg")] = reg(calm[calm[x] < 0], x)
        lk[("agit", x)] = reg(g[g["calm"] == "agitated"], x)
    out["lookbacks slope"] = pd.DataFrame(lk).T
    # calm s7 quintile within negative side, by year halves
    neg["q"] = pd.qcut(neg["s7"], 3, labels=False)
    out["calm fall tercile x year"] = neg.groupby(["year", "q"])["u"].mean().unstack()
    # interaction test calm vs agitated slope difference for s7
    a = g.dropna(subset=["s7"]).copy()
    a["c"] = (a["calm"] == "calm").astype(float)
    X = np.column_stack([np.ones(len(a)), a["s7"], a["c"], a["s7"] * a["c"]])
    beta, *_ = np.linalg.lstsq(X, a["u"].values, rcond=None)
    res = a["u"].values - X @ beta
    cov = np.linalg.inv(X.T @ X) * (res @ res) / (len(a) - 4)
    out["interaction s7 x calm"] = pd.Series({"beta_int": beta[3], "t_int": beta[3] / np.sqrt(cov[3, 3]), "n": len(a)})
    return out
