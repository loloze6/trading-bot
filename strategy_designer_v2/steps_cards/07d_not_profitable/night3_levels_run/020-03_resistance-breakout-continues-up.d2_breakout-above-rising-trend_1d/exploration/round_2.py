def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    drift = {}
    for c in data["bars"]:
        rs = []
        for w, b in data["bars"][c].items():
            cl = b["close"].values
            rs.append(pd.Series(cl).shift(-1)/pd.Series(cl)-1)
        drift[c] = pd.concat(rs).mean()
    cases = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = pd.Series(b["close"].values.astype(float))
            f = b["forecast"].fillna(0).values
            n = len(b)
            sma50 = cl.rolling(50, min_periods=50).mean()
            hi90 = cl.rolling(90, min_periods=60).max()
            lr = np.log(cl).diff()
            vol20 = lr.rolling(20).std()
            for i in range(1, n):
                if f[i] > 0 and f[i-1] <= 0:
                    rec = {"coin": c, "year": pd.Timestamp(b["timestamp"].iloc[i]).year}
                    for h in [5, 10, 20, 40]:
                        rec[f"x{h}"] = (cl[i+h]/cl[i]-1 - drift[c]*h) if i+h < n else np.nan
                    rec["sma_slope20"] = sma50[i]/sma50[i-20]-1 if i >= 20 and pd.notna(sma50[i-20]) else np.nan
                    rec["r60"] = cl[i]/cl[i-60]-1 if i >= 60 else np.nan
                    rec["near_hi90"] = cl[i]/hi90[i]-1 if pd.notna(hi90[i]) else np.nan
                    rec["day_ret"] = cl[i]/cl[i-1]-1
                    rec["vol20"] = vol20[i]
                    cases.append(rec)
    C = pd.DataFrame(cases)
    for g in ["sma_slope20", "r60", "near_hi90", "day_ret", "vol20"]:
        s = C.dropna(subset=[g])
        q = pd.qcut(s[g], 4, labels=False, duplicates="drop")
        t = s.groupby(q).agg(val=(g, "mean"), x5=("x5", "mean"), x10=("x10", "mean"),
                             x20=("x20", "mean"), x40=("x40", "mean"), n=("x10", "count"))
        lo, hi = s.loc[q == q.min(), "x20"].dropna(), s.loc[q == q.max(), "x20"].dropna()
        t["t_x20_top_minus_bottom"] = stats.ttest_ind(hi, lo, equal_var=False).statistic
        out[g] = t
    out["x20_by_year"] = C.groupby("year").agg(x10=("x10", "mean"), x20=("x20", "mean"), n=("x20", "count"))
    out["x20_by_coin"] = C.groupby("coin").agg(x10=("x10", "mean"), x20=("x20", "mean"), n=("x20", "count"))
    return out
