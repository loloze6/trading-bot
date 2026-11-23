def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    wk = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            s = pd.Series(c)
            for H in (24, 72):
                past = s / s.shift(H) - 1
                scale = past.abs().rolling(720, min_periods=240).mean()
                hv = s.pct_change().rolling(720, min_periods=240).std()
                fwd = s.shift(-H) / s - 1
                idx = np.arange(0, n, H)
                for i in idx:
                    if np.isnan(fwd.iloc[i]) or np.isnan(past.iloc[i]) or np.isnan(scale.iloc[i]):
                        continue
                    rows.append((coin, w, H, past.iloc[i] / scale.iloc[i], hv.iloc[i],
                                 fwd.iloc[i], ts.iloc[i].dayofweek, ts.iloc[i].hour))
            # weekend: close at Fri 24:00 -> Sun 24:00, then Mon-Tue
            d = pd.DataFrame({"ts": ts, "c": c})
            d["day"] = d["ts"].dt.floor("D")
            daily = d.groupby("day")["c"].last()
            dd = pd.DataFrame({"c": daily})
            dd["dow"] = dd.index.dayofweek
            dd["r"] = dd["c"].pct_change()
            # consecutive daily check
            dd["gap"] = dd.index.to_series().diff().dt.days
            dd = dd[dd["gap"] == 1]
            for coinw in [0]:
                pass
            # 2-day blocks ending on each day: return of prev 2 days vs next 2 days
            dd2 = pd.DataFrame({"c": daily})
            dd2["r2p"] = dd2["c"] / dd2["c"].shift(2) - 1
            dd2["r2f"] = dd2["c"].shift(-2) / dd2["c"] - 1
            dd2["dow"] = dd2.index.dayofweek
            dd2["coin"] = coin
            # one per week per dow -> non-overlapping per dow
            wk.append(dd2.dropna())
    R = pd.DataFrame(rows, columns=["coin", "w", "H", "z", "hv", "fwd", "dow", "hour"])
    R["drift"] = R.groupby(["coin", "H"])["fwd"].transform("mean")
    R["usual"] = R.groupby(["coin", "H"])["fwd"].transform("std")
    R["ex"] = R["fwd"] - R["drift"]
    R["str"] = R["ex"] / R["usual"]
    out = {}
    def summ(g):
        return pd.Series({"n": len(g), "mean_ex": g["ex"].mean(), "t": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))),
                          "strength": g["str"].mean()})
    for H in (24, 72):
        sub = R[R.H == H].copy()
        sub["zq"] = sub.groupby("coin")["z"].transform(lambda x: pd.qcut(x, 5, labels=False))
        out[f"H{H} by past-move quintile"] = sub.groupby("zq").apply(summ)
        sub["vq"] = sub.groupby("coin")["hv"].transform(lambda x: pd.qcut(x, 3, labels=False))
        out[f"H{H} by vol tercile x top/bottom zq"] = sub[sub.zq.isin([0, 4])].groupby(["vq", "zq"]).apply(summ)
        sub["sz"] = np.sign(sub["z"])
        out[f"H{H} by coin top/bottom"] = sub[sub.zq.isin([0, 4])].groupby(["coin", "zq"]).apply(summ)
        sub["yr"] = sub["w"]
    # regression slope of ex on z, per H
    for H in (24, 72):
        sub = R[R.H == H]
        sl = stats.linregress(sub["z"].clip(-6, 6), sub["str"])
        out[f"H{H} slope str on z"] = f"slope {sl.slope:.4f} t {sl.slope/sl.stderr:.2f} n {len(sub)}"
    W = pd.concat(wk)
    W["drift"] = W.groupby("coin")["r2f"].transform("mean")
    W["ex"] = W["r2f"] - W["drift"]
    res = []
    for dow, g in W.groupby("dow"):
        sl = stats.linregress(g["r2p"], g["ex"])
        res.append((dow, len(g), sl.slope, sl.slope / sl.stderr))
    out["2d past vs 2d next by end-dow (6=Sun:weekend->MonTue)"] = pd.DataFrame(res, columns=["dow", "n", "slope", "t"])
    return out
