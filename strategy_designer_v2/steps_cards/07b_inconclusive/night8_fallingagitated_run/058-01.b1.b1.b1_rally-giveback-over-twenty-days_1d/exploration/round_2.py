import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [10, 20]
    drift = {}
    for coin, wins in bars.items():
        drift[coin] = {}
        for h in H:
            r = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    r.append(c[i + h] / c[i] - 1)
            drift[coin][h] = np.mean(r) if r else np.nan
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].values
            rg = df["regime"].astype(str).values
            ts = pd.to_datetime(df["timestamp"]).astype(str).str[:10].values
            n = len(c)
            r3 = np.full(n, np.nan)
            r3[3:] = c[3:] / c[:-3] - 1
            for i in range(0, n - 20, 20):
                rec = dict(coin=coin, w=w, f=f[i], reg=rg[i], day=ts[i], r3=r3[i])
                for h in H:
                    rec["x%d" % h] = c[i + h] / c[i] - 1 - drift[coin][h]
                    rec["raw%d" % h] = c[i + h] / c[i] - 1
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    out["regime_counts"] = d["reg"].value_counts()

    def cl_t(s, days):
        m = pd.DataFrame({"s": s, "d": days}).dropna()
        if len(m) < 3:
            return np.nan
        mu = m["s"].mean()
        dev = (m["s"] - mu).groupby(m["d"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(m)
        return mu / se if se > 0 else np.nan

    inprof = d[d["reg"] == "unknown"].copy()
    inprof["grp"] = np.where(inprof["f"] < 0, "rally", np.where(inprof["r3"] > 0, "rise_f0", "no_rise"))
    g = []
    for k, s in inprof.groupby("grp"):
        g.append(dict(grp=k, n=len(s), days=s["day"].nunique(), x10=s["x10"].mean(), x20=s["x20"].mean(),
                      t20=cl_t(s["x20"], s["day"]), raw20=s["raw20"].mean()))
    out["in_profile_groups"] = pd.DataFrame(g)
    out["out_profile_x20"] = pd.Series(dict(n=int((d["reg"] != "unknown").sum()),
                                            x20=d.loc[d["reg"] != "unknown", "x20"].mean()))
    a, b = inprof.loc[inprof["grp"] == "rally", "x20"], inprof.loc[inprof["grp"] != "rally", "x20"]
    tt = stats.ttest_ind(a, b, equal_var=False)
    out["rally_minus_other_in_profile_x20"] = pd.Series(dict(diff=a.mean() - b.mean(), t=tt.statistic, na=len(a), nb=len(b)))
    # in-profile regression of x20 on r3 scaled? use r3 directly, all in-profile cells
    ok = inprof[["r3", "x20"]].dropna()
    lr = stats.linregress(ok["r3"], ok["x20"])
    out["in_profile_x20_on_r3"] = pd.Series(dict(n=len(ok), slope=lr.slope, t=lr.slope / lr.stderr))
    ral = inprof[inprof["grp"] == "rally"]
    out["rally_ex_w18"] = pd.Series(dict(n=int((ral["w"] != "w18").sum()),
                                         x20=ral.loc[ral["w"] != "w18", "x20"].mean(),
                                         t=cl_t(ral.loc[ral["w"] != "w18", "x20"], ral.loc[ral["w"] != "w18", "day"])))
    oth = inprof[inprof["grp"] != "rally"]
    out["other_by_window_x20"] = oth.groupby("w")["x20"].agg(["count", "mean"])
    return out
