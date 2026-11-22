def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    # coin drift / usual move per horizon
    drift, usual = {}, {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
            usual[(c, h)] = np.std(rs) if rs else np.nan
    rows = []
    col = "debug_info.components.fail_depth.last_history_value"
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            raw = df[col].fillna(0).values if col in df else np.zeros(len(df))
            ts = pd.to_datetime(df["timestamp"])
            r60 = pd.Series(cl).pct_change(60).values
            r20 = pd.Series(cl).pct_change(20).values
            for h in H:
                for start in range(0, len(cl) - h, h):
                    seg = np.where(raw[start:start + h] != 0)[0]
                    if len(seg) == 0:
                        continue
                    t = start + seg[0]
                    if t + h >= len(cl):
                        continue
                    ret = cl[t + h] / cl[t] - 1
                    rows.append(dict(coin=c, win=w, h=h, year=ts[t].year,
                                     depth=abs(raw[t]), r60=r60[t], r20=r20[t],
                                     tot=-ret, unus=-(ret - drift[(c, h)]),
                                     strength=-(ret - drift[(c, h)]) / usual[(c, h)]))
    d = pd.DataFrame(rows)
    def summ(g):
        n = len(g); m = g["unus"].mean(); s = g["unus"].std()
        return pd.Series(dict(n=n, unus=m, t=m / (s / np.sqrt(n)) if n > 1 else np.nan,
                              tot=g["tot"].mean(), strength=g["strength"].mean(),
                              hit=(g["unus"] > 0).mean()))
    out = {}
    out["by_horizon"] = d.groupby("h").apply(summ)
    d5 = d[d.h == 5].copy()
    out["h5_by_coin"] = d5.groupby("coin").apply(summ)
    out["h5_by_year"] = d5.groupby("year").apply(summ)
    d5["dq"] = pd.qcut(d5["depth"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["h5_by_depthq"] = d5.groupby("dq").apply(summ)
    d5["trend60"] = np.where(d5["r60"] > 0, "up60", np.where(d5["r60"] <= 0, "down60", "na"))
    out["h5_by_trend60"] = d5.groupby("trend60").apply(summ)
    d5["r20q"] = pd.qcut(d5["r20"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["h5_by_r20tercile"] = d5.groupby("r20q").apply(summ)
    out["h5_outlier"] = pd.Series(dict(median=d5["unus"].median(), max=d5["unus"].max(),
                                        min=d5["unus"].min(),
                                        mean_trim5=stats.trim_mean(d5["unus"], 0.05),
                                        spearman_depth=stats.spearmanr(d5["depth"], d5["unus"])[0]))
    d10 = d[d.h == 10].copy()
    d10["trend60"] = np.where(d10["r60"] > 0, "up60", "down60")
    out["h10_by_trend60"] = d10.groupby("trend60").apply(summ)
    return out
