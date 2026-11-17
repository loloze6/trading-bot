def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(0, n - 7, 7):
                r30 = c[i]/c[i-30]-1 if i >= 30 else np.nan
                hi = np.max(c[max(0, i-30):i+1])
                rows.append(dict(coin=coin, win=w, year=yr[i], fc=df["forecast"].iat[i],
                                 ret=c[i+7]/c[i]-1, r30=r30, dd30=c[i]/hi-1))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby("coin")["ret"].transform("mean")
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x)))})
    out = {}
    act = d[d.fc > 0].copy(); flat = d[d.fc == 0]
    out["active_minus_flat"] = pd.Series({"diff": act.ex.mean()-flat.ex.mean(),
        "welch_t": stats.ttest_ind(act.ex, flat.ex, equal_var=False)[0],
        "n_act": len(act), "n_flat": len(flat)})
    med = act.fc.median()
    out["upper_half"] = tt(act[act.fc > med].ex)
    out["lower_half"] = tt(act[act.fc <= med].ex)
    out["top_quint"] = tt(act[act.fc >= act.fc.quantile(0.8)].ex)
    # leave-one-year-out t
    out["loyo_t"] = pd.Series({y: tt(act[act.year != y].ex)["t"] for y in sorted(act.year.unique())})
    # trimmed (winsorise 1%) t to see outlier dependence
    lo, hi = act.ex.quantile([0.01, 0.99])
    out["winsor_t"] = tt(act.ex.clip(lo, hi))
    out["median_ex_active"] = act.ex.median()
    out["share_pos_active"] = (act.ex > 0).mean()
    # window-level mean of active excess: how many windows positive
    wm = act.groupby(["coin", "win"]).ex.mean()
    out["windows_pos_share"] = pd.Series({"n_coin_windows": len(wm), "share_pos": (wm > 0).mean()})
    return out
