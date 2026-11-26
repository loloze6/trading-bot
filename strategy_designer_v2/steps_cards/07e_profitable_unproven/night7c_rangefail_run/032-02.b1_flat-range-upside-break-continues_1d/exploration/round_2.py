def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    H = [5, 10]
    drift = {}
    for c in bars:
        for h in H:
            r = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                r += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(r)
    cases = []
    for c in bars:
        for w, b in bars[c].items():
            f = b["forecast"].fillna(0).values; cl = b["close"].values
            hi = b["high"].values; lo = b["low"].values; vol = b["volume"].values
            s = pd.Series(cl)
            er = (s - s.shift(60)).abs() / s.diff().abs().rolling(60).sum()
            rng = pd.Series(hi - lo)
            comp = (rng.rolling(10).mean() / rng.rolling(60).mean()).values
            volr = (pd.Series(vol) / pd.Series(vol).rolling(60).mean()).values
            hi60 = pd.Series(hi).shift(1).rolling(60).max().values
            lo60 = pd.Series(lo).shift(1).rolling(60).min().values
            width = (hi60 - lo60) / cl
            raw = b["debug_info.components.break_up.last_history_value"].values
            ret1 = s.pct_change(1).values
            for i in range(1, len(f)):
                if f[i] > 0 and f[i - 1] <= 0:
                    rec = {"coin": c, "w": w, "raw": raw[i], "er": er.iloc[i], "comp": comp[i], "volr": volr[i],
                           "width": width[i], "ret1": ret1[i], "year": pd.Timestamp(b["timestamp"].iloc[i]).year}
                    for h in H:
                        rec[f"u{h}"] = cl[i + h] / cl[i] - 1 - drift[(c, h)] if i + h < len(cl) else np.nan
                    cases.append(rec)
    C = pd.DataFrame(cases)
    def grp(col, q=3):
        C["_b"] = pd.qcut(C[col], q, duplicates="drop")
        g = C.groupby("_b")
        r = g[[col, "u5", "u10"]].mean()
        r["n"] = g.size()
        r["t10"] = g["u10"].apply(lambda x: x.mean() / (x.std() / np.sqrt(x.count())))
        return r.reset_index(drop=True)
    for col in ["er", "comp", "volr", "width", "ret1"]:
        out[f"by_{col}"] = grp(col)
    out["spearman_u10"] = pd.Series({col: stats.spearmanr(C[col], C["u10"], nan_policy="omit")[0] for col in ["er", "comp", "volr", "width", "ret1", "raw"]})
    out["by_year"] = C.groupby("year")[["u5", "u10"]].agg(["mean", "count"])
    out["u10_without_XRP"] = pd.Series({"mean": C[C.coin != "XRPUSD"].u10.mean(), "n": C[C.coin != "XRPUSD"].u10.count(),
                                         "t": (lambda x: x.mean() / (x.std() / np.sqrt(x.count())))(C[C.coin != "XRPUSD"].u10.dropna())})
    x = C.u10.dropna().sort_values()
    out["u10_trimmed"] = pd.Series({"drop_top5_mean": x.iloc[:-5].mean(), "drop_top5_t": x.iloc[:-5].mean() / (x.iloc[:-5].std() / np.sqrt(len(x) - 5)), "median": x.median()})
    # book leave one coin out
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return"]].copy(); dd["coin"] = c; dd["w"] = w; rows.append(dd)
    D = pd.concat(rows).dropna()
    loo = {}
    for c in list(days) + ["none"]:
        bk = D[D.coin != c].groupby(["w", "day"]).book_return.mean()
        loo[c] = {"mean": bk.mean(), "sharpe": bk.mean() / bk.std() * np.sqrt(365)}
    out["book_leave_coin_out"] = pd.DataFrame(loo).T
    return out
