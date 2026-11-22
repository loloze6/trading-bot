def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; h = b["high"].values; l = b["low"].values
            n = len(b)
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            prev = b["previous_allocation"].fillna(0).values
            cs = pd.Series(c)
            ma180 = cs.rolling(180).mean().values
            ma540 = cs.rolling(540, min_periods=300).mean().values
            r84 = (cs / cs.shift(84) - 1).values
            r42 = (cs / cs.shift(42) - 1).values
            r540 = (cs / cs.shift(540) - 1).values
            for t in range(n):
                if prev[t] <= 1e-9 and alloc[t] > 1e-9:
                    j = t
                    while j + 1 < n and alloc[j + 1] > 1e-9:
                        j += 1
                    hold = c[min(j + 1, n - 1)] / c[t] - 1
                    f84 = c[t + 84] / c[t] - 1 if t + 84 < n else np.nan
                    rows.append(dict(coin=coin, wn=int(w[1:]), hold=hold, f84=f84,
                                     gap180=c[t] / ma180[t] - 1 if not np.isnan(ma180[t]) else np.nan,
                                     gap540=c[t] / ma540[t] - 1 if not np.isnan(ma540[t]) else np.nan,
                                     r84=r84[t], r42=r42[t], r540=r540[t], bars=j - t + 1))
    e = pd.DataFrame(rows)
    e["fallwin"] = e["wn"].between(12, 14)
    out["entries_fall_vs_rest"] = e.groupby("fallwin")[["hold", "f84", "gap180", "gap540", "r84", "r42", "r540", "bars"]].mean()
    out["entries_fall_count"] = e.groupby("fallwin").agg(n=("hold", "size"), win=("hold", lambda x: (x > 0).mean()))
    for col in ["gap180", "gap540", "r84", "r540"]:
        x = e[[col, "hold", "f84"]].dropna().copy()
        x["q"] = pd.qcut(x[col], 3, labels=False, duplicates="drop")
        g = x.groupby("q").agg(n=("hold", "size"), lo=(col, "min"), hi=(col, "max"),
                               hold=("hold", "mean"), f84=("f84", "mean"), win=("hold", lambda s: (s > 0).mean()))
        out["by_" + col] = g
        xx = x.dropna()
        sl = stats.linregress(xx[col], xx["f84"])
        out["slope_f84_on_" + col] = pd.Series(dict(slope=sl.slope, t=sl.slope / sl.stderr, n=len(xx)))
    # book: share of mean daily return in fall windows, and exposure when in position
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["wn"] = int(w[1:]); dd.append(d)
    D = pd.concat(dd).dropna(subset=["book_return"])
    D["inpos"] = D["book_return"].abs() > 1e-9
    out["coin_day_stats"] = pd.Series(dict(mean_in_pos=D.loc[D.inpos, "book_return"].mean(),
                                           coin_in_pos=D.loc[D.inpos, "coin_return"].mean(),
                                           share_in_pos=D.inpos.mean(),
                                           coin_mean_all=D["coin_return"].mean()))
    D["fallwin"] = D["wn"].between(12, 14)
    out["book_coin_by_fallwin"] = D.groupby("fallwin").agg(b=("book_return", "mean"), c=("coin_return", "mean"),
                                                           inpos=("inpos", "mean"))
    return out
