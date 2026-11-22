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
            pos = {t: i for i, t in enumerate(ts)}
            # signal bars: close at 00:00 of the next day; day-of-week of the day that just ended
            for i in np.where(ts.dt.hour == 23)[0]:
                t = ts.iloc[i]
                js = pos.get(t - pd.Timedelta(hours=24)); k48 = pos.get(t + pd.Timedelta(hours=48))
                if js is None or k48 is None:
                    continue
                r1 = c[i] / c[js] - 1
                u = c[k48] / c[i] - 1 - dr
                rows.append({"coin": coin, "win": w, "dow": t.dayofweek, "year": (t + pd.Timedelta(hours=1)).year,
                             "r1": r1, "z1": r1 / sd, "u48": u, "s48": u / sd, "sd": sd})
    d = pd.DataFrame(rows)
    out = {}
    sl = {}
    for dw, g in d.groupby("dow"):
        s = stats.linregress(g["z1"], g["s48"])
        sl[dw] = pd.Series({"slope_s_on_z": s.slope, "t": s.slope / s.stderr, "n": len(g)})
    out["slope_by_day_ended(0=Mon..6=Sun)"] = pd.DataFrame(sl).T
    sun = d[d.dow == 6].copy()
    # signal against the Sunday move: case direction = -sign(r1)
    sun["dir"] = -np.sign(sun["r1"])
    sun["cu"] = sun["dir"] * sun["u48"]; sun["cs"] = sun["dir"] * sun["s48"]
    sun["q"] = sun.groupby("coin")["r1"].transform(lambda s: pd.qcut(s, 5, labels=False))
    def agg(g):
        return pd.Series({"n": len(g), "u48": g["u48"].mean(), "t_u48": g["u48"].mean() / (g["u48"].std() / np.sqrt(len(g))),
                          "against_u": g["cu"].mean(), "against_strength": g["cs"].mean(),
                          "t_against": g["cu"].mean() / (g["cu"].std() / np.sqrt(len(g)))})
    out["sun_by_quintile"] = sun.groupby("q").apply(agg)
    sun["side"] = np.where(sun.r1 < 0, "sun_fall(long)", "sun_rise(short)")
    out["sun_by_side"] = sun.groupby("side").apply(agg)
    out["sun_by_coin"] = sun.groupby("coin").apply(agg)
    out["sun_by_year"] = sun.groupby("year").apply(agg)
    big = sun[sun.q.isin([0, 4])]
    out["sun_extreme_quintiles_by_side"] = big.groupby("side").apply(agg)
    wk = d[d.dow.isin([0, 1, 2, 3])].copy()
    wk["dir"] = -np.sign(wk["r1"]); wk["cu"] = wk["dir"] * wk["u48"]; wk["cs"] = wk["dir"] * wk["s48"]
    wk["q"] = wk.groupby("coin")["r1"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["weekday_control_by_quintile"] = wk.groupby("q").apply(agg)
    return out
