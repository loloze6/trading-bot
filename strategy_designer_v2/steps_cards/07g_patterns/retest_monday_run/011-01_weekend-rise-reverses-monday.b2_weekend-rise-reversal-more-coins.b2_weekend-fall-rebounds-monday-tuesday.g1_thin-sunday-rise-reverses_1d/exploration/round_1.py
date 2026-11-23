def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        # coin drift over 2 bars, non-overlapping, all windows pooled
        d2 = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - 2, 2):
                d2.append(c[i+2]/c[i]-1)
        drift2 = np.mean(d2) if d2 else 0.0
        usual2 = np.std(d2) if d2 else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"]; v = b["volume"]
            r1 = c/c.shift(1)-1
            r2b = c/c.shift(2)-1
            mabs = r1.abs().rolling(60, min_periods=20).mean().shift(1)
            vr = v.rolling(60, min_periods=20).mean().shift(1)/v
            f1 = c.shift(-1)/c-1
            f2 = c.shift(-2)/c-1
            f2n = c.shift(-3)/c.shift(-1)-1  # day+1 to day+3
            df = pd.DataFrame({"coin": coin, "win": w, "wd": ts.dt.weekday, "year": ts.dt.year,
                               "z": r1/mabs, "z2": r2b/mabs, "vr": vr, "f1": f1, "f2": f2, "f2n": f2n,
                               "u2": (f2-drift2)/usual2, "f2x": f2-drift2,
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    D = pd.concat(rows).dropna(subset=["z", "f2x"])
    def tt(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    # reversal by weekday: move in direction opposite the day's return
    D["rev"] = -np.sign(D["z"]) * D["f2x"]
    out["reversal_by_weekday_and_side"] = D.groupby(["wd", D["z"] > 0])["rev"].apply(tt).unstack()
    # graded: Sunday rises by z quintile
    S = D[(D.wd == 6) & (D.z > 0)].copy()
    S["zq"] = pd.qcut(S["z"], 5, labels=False)
    S["vq"] = pd.qcut(S["vr"], 5, labels=False)
    out["sun_rise_by_size_quintile"] = S.groupby("zq")["rev"].apply(tt).unstack()
    out["sun_rise_by_volratio_quintile(4=thinnest)"] = S.groupby("vq")["rev"].apply(tt).unstack()
    out["sun_rise_by_year"] = S.groupby("year")["rev"].apply(tt).unstack()
    # Sunday fall: rebound?
    F = D[(D.wd == 6) & (D.z < 0)].copy()
    F["zq"] = pd.qcut(-F["z"], 5, labels=False)
    out["sun_fall_rebound_by_size_quintile"] = F.groupby("zq")["rev"].apply(tt).unstack()
    # weekend 2-day move (Fri close->Sun close) on Sunday
    W = D[D.wd == 6].copy()
    W["rev2"] = -np.sign(W["z2"]) * W["f2x"]
    W["q"] = pd.qcut(W["z2"], 5, labels=False)
    out["weekend2d_move_quintile_fwd2_excess"] = W.groupby("q")["f2x"].apply(tt).unstack()
    # split monday vs tuesday for sunday rises
    out["sun_rise_monday_only_raw"] = tt(-S["f1"])
    out["sun_rise_tue_wed_raw"] = tt(-S["f2n"])
    # Saturday rises: forward
    Sa = D[(D.wd == 5)].copy()
    Sa["q"] = pd.qcut(Sa["z"], 5, labels=False)
    out["saturday_move_quintile_fwd2_excess"] = Sa.groupby("q")["f2x"].apply(tt).unstack()
    # by coin
    out["sun_rise_by_coin"] = S.groupby("coin")["rev"].apply(tt).unstack()
    return out
