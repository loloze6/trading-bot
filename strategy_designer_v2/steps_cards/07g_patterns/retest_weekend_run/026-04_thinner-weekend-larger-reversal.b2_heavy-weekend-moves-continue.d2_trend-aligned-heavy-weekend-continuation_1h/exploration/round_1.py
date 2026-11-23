def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []      # per anchor-bar cases
    hr_rows = []
    for coin, wins in data["bars"].items():
        # usual 48h move: std of non-overlapping 48-bar returns over all windows
        r48 = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            r48.extend(c[idx + 48] / c[idx] - 1)
        r48 = np.array(r48); sd48 = np.nanstd(r48); mu48 = np.nanmean(r48)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values; v = b["volume"].values
            n = len(c)
            lr = np.log(c)
            # hourly returns by hour/weekday
            r1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            hr_rows.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                                         "r1": r1, "absr1_prev": np.abs(np.r_[np.nan, r1[:-1]])}))
            # anchor bars at 23:00 each day
            anchors = np.where(ts.dt.hour.values == 23)[0]
            for i in anchors:
                if i - 720 < 0 or i + 48 >= n:
                    continue
                past = c[i] / c[i - 48] - 1
                fut = c[i + 48] / c[i] - 1
                fut24 = c[i + 24] / c[i] - 1
                vr = np.nanmean(v[i - 47:i + 1]) / np.nanmean(v[i - 167:i - 47])
                tr = c[i - 48] / c[i - 720] - 1
                rows.append((coin, w, ts.iloc[i].weekday(), past / sd48, (fut - mu48) / sd48,
                             fut24 / sd48, vr, np.sign(tr), fut - mu48, ts.iloc[i].year))
    df = pd.DataFrame(rows, columns=["coin", "win", "wd", "past", "fut", "fut24", "vr", "trs", "futraw", "year"])
    # anchors non-overlapping within each weekday group (one per week)
    def slope_t(g):
        g = g.dropna()
        if len(g) < 30:
            return pd.Series({"n": len(g)})
        s = stats.linregress(g["past"], g["fut"])
        sg = np.sign(g["past"]) * g["fut"]
        return pd.Series({"n": len(g), "slope": s.slope, "t_slope": s.slope / s.stderr,
                          "signed_fut_mean": sg.mean(), "t_signed": sg.mean() / (sg.std() / np.sqrt(len(sg)))})
    out["by_anchor_weekday(6=Sun23h)"] = df.groupby("wd").apply(slope_t)
    sun = df[df.wd == 6].copy()
    sun["vr_hi"] = sun["vr"] >= 1
    sun["aligned"] = np.sign(sun["past"]) == sun["trs"]
    out["sun_by_vr_aligned"] = sun.groupby(["vr_hi", "aligned"]).apply(slope_t)
    sun["pq"] = pd.qcut(sun["past"].abs(), 4, labels=False)
    out["sun_by_absmove_quartile"] = sun.groupby("pq").apply(slope_t)
    out["sun_by_coin"] = sun.groupby("coin").apply(slope_t)
    out["sun_by_year"] = sun.groupby("year").apply(slope_t)
    # all weekdays, by vol ratio quartile, aligned
    df["aligned"] = np.sign(df["past"]) == df["trs"]
    out["all_days_aligned"] = df.groupby(["aligned"]).apply(slope_t)
    out["weekday_aligned_vrhi"] = df[(df.vr >= 1) & df.aligned].groupby("wd").apply(slope_t)
    H = pd.concat(hr_rows)
    def mt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean_bp": x.mean() * 1e4, "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["hour_ret"] = H.groupby("hour")["r1"].apply(mt).unstack()
    out["weekday_hour_ret"] = H.groupby("wd")["r1"].apply(mt).unstack()
    return out
