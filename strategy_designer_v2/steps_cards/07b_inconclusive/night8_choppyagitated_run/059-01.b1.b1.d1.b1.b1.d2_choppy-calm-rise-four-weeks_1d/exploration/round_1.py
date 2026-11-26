def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    # drift per coin per horizon over visible windows
    H = [7, 14, 28]
    rows = []
    drift = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
    for c, ws in bars.items():
        for w, df in ws.items():
            cl = df["close"].values
            f = df["forecast"].values
            raw = df.get("debug_info.components.scaled_week_rise.last_history_value")
            raw = raw.values if raw is not None else np.full(len(cl), np.nan)
            ret60 = pd.Series(cl).pct_change(60).values
            ret7 = pd.Series(cl).pct_change(7).values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            for h in H:
                for i in range(0, len(cl) - h, h):
                    if f[i] > 0:
                        r = cl[i + h] / cl[i] - 1
                        rows.append(dict(coin=c, win=w, h=h, f=f[i], raw=raw[i], r60=ret60[i], r7=ret7[i],
                                         ex=r - drift[(c, h)], tot=r, day=day[i],
                                         year=pd.Timestamp(day[i]).year))
    d = pd.DataFrame(rows)
    out = {}
    def summ(g):
        n = len(g); m = g.ex.mean(); s = g.ex.std(ddof=1)
        wm = (g.ex * g.f).sum() / g.f.sum()
        return pd.Series(dict(n=n, days=g.day.nunique(), mean_ex=m, wmean_ex=wm, mean_tot=g.tot.mean(),
                              t=m / (s / np.sqrt(n)) if n > 1 and s > 0 else np.nan, hit=(g.ex > 0).mean()))
    out["by_h"] = d.groupby("h").apply(summ)
    d28 = d[d.h == 28].copy()
    out["28_by_coin"] = d28.groupby("coin").apply(summ)
    out["28_by_win"] = d28.groupby("win").apply(summ)
    out["28_by_year"] = d28.groupby("year").apply(summ)
    for h in H:
        dh = d[d.h == h].copy()
        dh["fq"] = pd.qcut(dh.f.rank(method="first"), 3, labels=["lo", "mid", "hi"])
        out[f"{h}_by_fterc"] = dh.groupby("fq").apply(summ)
        dh["tr"] = np.where(dh.r60 > 0, "60d_up", "60d_down")
        out[f"{h}_by_60dsign"] = dh.groupby("tr").apply(summ)
    out["corr_f_ex_by_h"] = d.groupby("h").apply(lambda g: pd.Series(dict(spearman=g[["f", "ex"]].corr("spearman").iloc[0, 1])))
    return out
