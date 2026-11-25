def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    rows = []
    case_rows = []
    fc_vals = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year
            reg = df["regime"].astype(str)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0)
            close = df["close"].astype(float)
            low = df["low"].astype(float)
            prevlow = low.shift(1).rolling(30, min_periods=30).min()
            brk = close / prevlow - 1
            ret30 = close / close.shift(30) - 1
            rng = (df["high"] - df["low"]) / df["close"]
            # cheap recompute of short/long range ratio within window (long limited)
            r30 = rng.rolling(30, min_periods=30).mean()
            rall = rng.expanding(min_periods=60).mean()
            rows.append({
                "coin": coin, "window": w, "year": int(yr.iloc[0]), "bars": n,
                "trending_bars": int((reg == "trending").sum()),
                "fc_neg_bars": int((fc < 0).sum()),
                "brk_bars": int((brk < 0).sum()),
                "brk_and_down30": int(((brk < 0) & (ret30 < 0)).sum()),
                "brk_down30_wide(approx)": int(((brk < 0) & (ret30 < 0) & (r30 > rall)).sum()),
                "bars_with_30_prior": int(prevlow.notna().sum()),
            })
            fc_vals.extend(fc[fc < 0].tolist())
            # cases per plan: forecast falls by >=2, once per 5-bar grid cell
            dfc = fc.diff()
            for start in range(0, n, 5):
                cell = range(start, min(start + 5, n))
                sig = [i for i in cell if dfc.iloc[i] <= -2]
                if sig:
                    i = sig[0]
                    if i + 5 < n:
                        r = close.iloc[i + 5] / close.iloc[i] - 1
                        case_rows.append({"coin": coin, "window": w, "year": int(yr.iloc[i]),
                                          "fc": fc.iloc[i], "ret5": r})
    t = pd.DataFrame(rows)
    c = pd.DataFrame(case_rows)
    out = {}
    out["per coin"] = t.groupby("coin")[["bars", "trending_bars", "fc_neg_bars", "brk_bars", "brk_and_down30", "brk_down30_wide(approx)", "bars_with_30_prior"]].sum()
    out["per window"] = t.groupby("window")[["bars", "trending_bars", "fc_neg_bars", "brk_bars", "brk_and_down30", "brk_down30_wide(approx)"]].sum()
    out["per year"] = t.groupby("year")[["bars", "trending_bars", "fc_neg_bars", "brk_bars", "brk_and_down30"]].sum()
    out["bars per window stats"] = t["bars"].describe()
    out["neg forecast distribution"] = pd.Series(fc_vals).describe()
    if len(c):
        out["cases per coin"] = c.groupby("coin")["ret5"].agg(["count", "mean", "std"])
        out["cases per year"] = c.groupby("year")["ret5"].agg(["count", "mean", "std"])
        out["cases total"] = len(c)
        out["case fc"] = c["fc"].describe()
        out["case ret5 short-signed"] = (-c["ret5"]).describe()
    return out
