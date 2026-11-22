def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        g48 = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            g48.extend(list(c[idx + 48] / c[idx] - 1))
        dr = np.mean(g48); sd = np.std(g48)
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"].values
            v = df["volume"].values
            pos = {t: i for i, t in enumerate(ts)}
            for i in np.where((ts.dt.hour == 23) & (ts.dt.dayofweek == 6))[0]:
                t = ts.iloc[i]
                j = pos.get(t - pd.Timedelta(hours=48)); js = pos.get(t - pd.Timedelta(hours=24))
                k24 = pos.get(t + pd.Timedelta(hours=24)); k48 = pos.get(t + pd.Timedelta(hours=48))
                jp = pos.get(t - pd.Timedelta(hours=216))
                if None in (j, js, k24, k48):
                    continue
                past = c[i] / c[j] - 1
                prior = c[j] / c[jp] - 1 if jp is not None else np.nan
                rows.append({"coin": coin, "week": (t + pd.Timedelta(hours=1)).normalize(),
                             "past": past, "z": past / sd, "sun": c[i] / c[js] - 1, "sat": c[js] / c[j] - 1,
                             "prior7d": prior,
                             "mon": c[k24] / c[i] - 1 - dr / 2, "tue": c[k48] / c[k24] - 1 - dr / 2,
                             "u48": c[k48] / c[i] - 1 - dr, "s48": (c[k48] / c[i] - 1 - dr) / sd})
    d = pd.DataFrame(rows)
    out = {}
    f = d[d.past < 0].copy()
    wk = f.groupby("week")["u48"].mean()
    out["fall_u48_over_weeks"] = pd.Series({"mean": wk.mean(), "t": wk.mean() / (wk.std() / np.sqrt(len(wk))), "weeks": len(wk),
                                            "strength": f["s48"].mean(), "mon": f["mon"].mean(), "tue": f["tue"].mean(),
                                            "t_mon": stats.ttest_1samp(f["mon"], 0).statistic, "t_tue": stats.ttest_1samp(f["tue"], 0).statistic})
    f["zb"] = pd.cut(f["z"], [-10, -1, -0.5, -0.25, 0])
    out["fall_by_zbin"] = f.groupby("zb").agg(n=("u48", "size"), u48=("u48", "mean"), s48=("s48", "mean"),
                                              t=("u48", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    d["zb"] = pd.cut(d["z"], [-10, -1, -0.5, -0.25, 0, 0.25, 0.5, 1, 10])
    out["all_by_zbin"] = d.groupby("zb").agg(n=("u48", "size"), u48=("u48", "mean"), mon=("mon", "mean"),
                                             t=("u48", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    # prior trend: weekend fall within a falling vs rising week
    f["prior_side"] = np.where(f["prior7d"] < 0, "prior_fall", "prior_rise")
    out["fall_by_prior"] = f.dropna(subset=["prior7d"]).groupby("prior_side").agg(n=("u48", "size"), u48=("u48", "mean"),
                                             t=("u48", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    reg = {}
    for col in ["past", "sun", "sat", "prior7d"]:
        x = d[[col, "u48"]].dropna()
        s = stats.linregress(x[col], x["u48"])
        reg[col] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(x)})
    x = f[["past", "u48"]]
    s = stats.linregress(x["past"], x["u48"]); reg["past_falls_only"] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(x)})
    out["slopes_u48"] = pd.DataFrame(reg).T
    return out
