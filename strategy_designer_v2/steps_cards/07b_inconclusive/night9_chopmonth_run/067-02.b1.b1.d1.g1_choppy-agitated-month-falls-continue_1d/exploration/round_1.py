def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    coin_mean = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in (3, 7, 14)}
        for w, df in wins.items():
            c = df["close"].values
            for h in (3, 7, 14):
                idx = np.arange(0, len(c) - h, h)
                allr[h] += list(c[idx + h] / c[idx] - 1)
        coin_mean[coin] = {h: np.mean(allr[h]) for h in allr}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            ts = pd.to_datetime(df["timestamp"])
            reg = df["regime"].values
            fc = df["forecast"].values
            n = len(c)
            for h in (3, 7, 14):
                for i in range(0, n - h, h):
                    if i < 30:
                        r30 = np.nan
                    else:
                        r30 = c[i] / c[i - 30] - 1
                    rows.append(dict(coin=coin, w=w, h=h, year=ts[i].year, day=ts[i].normalize(),
                                     inprof=reg[i] == "unknown", r30=r30, fc=fc[i],
                                     fwd=c[i + h] / c[i] - 1, mu=coin_mean[coin][h]))
    d = pd.DataFrame(rows)
    d["unus_short"] = -(d["fwd"] - d["mu"])
    out = {}
    def tclu(s):
        g = s.groupby(s.index.get_level_values(0) if False else None) if False else None
    def summ(x):
        if len(x) < 3:
            return pd.Series(dict(n=len(x), mean=np.nan, t=np.nan))
        per = x.groupby("day")["unus_short"].sum()
        nd = len(per)
        m = x["unus_short"].mean()
        se = per.std(ddof=1) * np.sqrt(nd) / len(x)
        return pd.Series(dict(n=len(x), days=nd, mean=m, t=m / se if se > 0 else np.nan, total_short=-x["fwd"].mean()))
    base = d[(d.inprof) & (d.r30 < 0)]
    out["by_horizon_falls"] = base.groupby("h").apply(summ)
    rises = d[(d.inprof) & (d.r30 > 0)].copy()
    out["by_horizon_rises_shortdir"] = rises.groupby("h").apply(summ)
    b7 = base[base.h == 7].copy()
    b7["q"] = pd.qcut(b7["r30"], 4, labels=["deepest", "q2", "q3", "shallowest"])
    out["h7_by_depth_quartile"] = b7.groupby("q").apply(summ)
    out["h7_by_coin"] = b7.groupby("coin").apply(summ)
    out["h7_by_year"] = b7.groupby("year").apply(summ)
    out["h7_by_window"] = b7.groupby("w").apply(summ)
    # all falls regardless of profile, h7, by depth
    allf = d[(d.h == 7) & (d.r30 < 0)].copy()
    allf["q"] = pd.qcut(allf["r30"], 4, labels=["deepest", "q2", "q3", "shallowest"])
    out["h7_falls_anyprofile_depth"] = allf.groupby(["inprof", "q"]).apply(summ)
    # correlation within profile of r30 and fwd at h7
    p7 = d[(d.h == 7) & d.inprof & d.r30.notna()]
    out["h7_inprof_corr_r30_fwd"] = float(p7[["r30", "fwd"]].corr().iloc[0, 1])
    out["h7_inprof_n"] = len(p7)
    b14 = base[base.h == 14].copy()
    b14["q"] = pd.qcut(b14["r30"], 2, labels=["deeper", "shallower"])
    out["h14_by_depth_half"] = b14.groupby("q").apply(summ)
    return out
