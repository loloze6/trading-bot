def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r1 = pd.Series(c).pct_change()
            ret14 = pd.Series(c).pct_change(14)
            sd30 = r1.rolling(30).std()
            z = ret14 / (sd30 * np.sqrt(14))
            ret60 = pd.Series(c).pct_change(60)
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for h in (1, 3, 5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, year=yr[i],
                                     day=str(b["timestamp"].iloc[i])[:10],
                                     ret=c[i+h]/c[i]-1, fc=float(b["forecast"].iloc[i]),
                                     reg=b["regime"].iloc[i], z=z.iloc[i], r60=ret60.iloc[i]))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby(["coin","h"])["ret"].transform("mean")
    df["ex"] = -(df["ret"] - df["drift"])  # signed short
    df["tot"] = -df["ret"]
    cases = df[(df.reg=="unknown") & (df.fc < 0)].copy()
    def dt(s, days):
        g = pd.DataFrame({"v": s.values, "d": days.values}).groupby("d")["v"].sum()
        n = len(s); m = s.mean()
        dev = pd.DataFrame({"v": (s - m).values, "d": days.values}).groupby("d")["v"].sum()
        se = np.sqrt((dev**2).sum()) / n
        return m, m/se if se > 0 else np.nan, n, g.shape[0]
    out = {}
    hr = []
    for h, g in cases.groupby("h"):
        m, t, n, d = dt(g["ex"], g["day"])
        wm = (g["ex"]*g["fc"].abs()).sum()/g["fc"].abs().sum()
        hr.append(dict(h=h, mean_ex=m, t=t, n=n, days=d, wmean=wm, tot=g["tot"].mean()))
    out["by_horizon"] = pd.DataFrame(hr)
    c5 = cases[cases.h==5].copy()
    def tab(g):
        m, t, n, d = dt(g["ex"], g["day"])
        return pd.Series(dict(mean_ex=m, t=t, n=n, tot=g["tot"].mean()))
    out["by_coin"] = c5.groupby("coin").apply(tab)
    out["by_window"] = c5.groupby("w").apply(tab)
    out["by_year"] = c5.groupby("year").apply(tab)
    c5["fq"] = pd.qcut(c5["fc"].abs().rank(method="first"), 4, labels=["q1_shallow","q2","q3","q4_deep"])
    out["by_fc_quartile"] = c5.groupby("fq").apply(tab)
    c5z = c5.dropna(subset=["z"]).copy()
    c5z["zq"] = pd.qcut(c5z["z"].rank(method="first"), 4, labels=["z_deepest","z2","z3","z_shallow"])
    out["by_rawz_quartile"] = c5z.groupby("zq").apply(tab)
    c5t = c5.dropna(subset=["r60"]).copy()
    c5t["trend"] = np.where(c5t.r60 > 0.10, "rising", np.where(c5t.r60 < -0.10, "falling", "choppy"))
    out["by_trend"] = c5t.groupby("trend").apply(tab)
    out["corr_absfc_ex"] = float(stats.spearmanr(c5["fc"].abs(), c5["ex"])[0])
    out["corr_z_ex"] = float(stats.spearmanr(c5z["z"], c5z["ex"])[0])
    # agitated side for comparison: forecast not recorded in chop; use z<0
    ag = df[(df.h==5) & (df.reg=="chop") & (df.z < 0)]
    m, t, n, d = dt(ag["ex"], ag["day"])
    out["agitated_z_neg_h5"] = pd.Series(dict(mean_ex=m, t=t, n=n))
    return out
