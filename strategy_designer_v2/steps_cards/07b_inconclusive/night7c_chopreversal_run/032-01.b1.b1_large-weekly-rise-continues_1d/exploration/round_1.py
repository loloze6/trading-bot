def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        for h in (3, 7, 14):
            allr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(allr), np.std(allr, ddof=1))
        for w, b in wins.items():
            c = b["close"].reset_index(drop=True)
            r = c.pct_change()
            sd = r.rolling(30).std()
            z = (c / c.shift(7) - 1) / (sd * np.sqrt(7))
            eff = (c / c.shift(30) - 1).abs() / r.abs().rolling(30).sum()
            agit = sd / r.rolling(30).std().rolling(120, min_periods=30).median()
            fc = b["forecast"].reset_index(drop=True)
            day = pd.to_datetime(b["timestamp"]).dt.floor("D").reset_index(drop=True)
            yr = day.dt.year
            for h in (3, 7, 14):
                for i in range(0, len(c) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=yr[i], day=day[i],
                                     z=z[i], fc=fc[i], eff=eff[i], agit=agit[i],
                                     ret=c[i + h] / c[i] - 1,
                                     un=c[i + h] / c[i] - 1 - drift[(coin, h)][0],
                                     usual=drift[(coin, h)][1]))
    d = pd.DataFrame(rows)
    def tclust(s):
        s = s.dropna()
        if len(s) < 3: return pd.Series(dict(n=len(s), mean=np.nan, t=np.nan, days=0))
        dev = (s["un"] - s["un"].mean()).groupby(s["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / max(D - 1, 1)) / len(s)
        return pd.Series(dict(n=len(s), mean=s["un"].mean(), t=s["un"].mean() / se if se > 0 else np.nan, days=D,
                              strength=(s["un"] / s["usual"]).mean()))
    out = {}
    fcase = d[d.fc > 0]
    out["by_horizon_fc>0"] = fcase.groupby("h")[["un", "day", "usual"]].apply(tclust)
    zc = d[d.z >= 2]
    out["by_horizon_z>=2"] = zc.groupby("h")[["un", "day", "usual"]].apply(tclust)
    # graded: z buckets at h=7 over all bars
    d7 = d[(d.h == 7) & d.z.notna()].copy()
    d7["zb"] = pd.cut(d7.z, [-10, -2, -1, 0, 1, 2, 2.5, 3, 10])
    out["h7_by_zbucket"] = d7.groupby("zb", observed=True)[["un", "day", "usual"]].apply(tclust)
    c7 = fcase[fcase.h == 7]
    out["h7_fc>0_by_coin"] = c7.groupby("coin")[["un", "day", "usual"]].apply(tclust)
    out["h7_fc>0_by_window"] = c7.groupby("w")[["un", "day", "usual"]].apply(tclust)
    out["h7_fc>0_by_year"] = c7.groupby("year")[["un", "day", "usual"]].apply(tclust)
    z7 = zc[zc.h == 7].copy()
    z7["effb"] = pd.qcut(z7.eff, 2, labels=["choppy", "trendy"])
    z7["agb"] = pd.qcut(z7.agit, 2, labels=["calm", "agitated"])
    out["h7_z>=2_by_eff"] = z7.groupby("effb", observed=True)[["un", "day", "usual"]].apply(tclust)
    out["h7_z>=2_by_agit"] = z7.groupby("agb", observed=True)[["un", "day", "usual"]].apply(tclust)
    z7["zb"] = pd.qcut(z7.z, 3)
    out["h7_z>=2_by_ztercile"] = z7.groupby("zb", observed=True)[["un", "day", "usual"]].apply(tclust)
    out["h7_z>=2_corr_z_un"] = float(z7[["z", "un"]].corr().iloc[0, 1])
    return out
