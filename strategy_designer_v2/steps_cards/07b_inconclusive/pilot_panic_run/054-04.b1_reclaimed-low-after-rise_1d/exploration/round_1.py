def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    sd = {}
    for coin in bars:
        for H in (5, 10, 20):
            rets = []
            for w, df in bars[coin].items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rets.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = np.mean(rets) if rets else np.nan
            sd[(coin, H)] = np.std(rets, ddof=1) if len(rets) > 1 else np.nan
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            lo = df["low"]; c = df["close"].values
            pm = lo.shift(1).rolling(30, min_periods=30).min()
            rec = (lo < pm) & (df["close"] >= pm)
            r60 = df["close"] / df["close"].shift(60) - 1
            for i in np.where(rec.values)[0]:
                row = {"coin": coin, "win": w, "i": i, "regime": df["regime"].iloc[i],
                       "fc": df["forecast"].iloc[i], "r60": r60.iloc[i],
                       "depth": (pm.iloc[i] - lo.iloc[i]) / pm.iloc[i],
                       "ts": str(df["timestamp"].iloc[i])[:10], "year": str(df["timestamp"].iloc[i])[:4]}
                for H in (5, 10, 20):
                    if i + H < len(c):
                        row[f"ab{H}"] = c[i + H] / c[i] - 1 - drift[(coin, H)]
                        row[f"st{H}"] = row[f"ab{H}"] / sd[(coin, H)]
                    else:
                        row[f"ab{H}"] = np.nan
                rows.append(row)
    ev = pd.DataFrame(rows)
    ev["agit"] = ev["regime"] != "chop"
    ev["short_bet"] = ev["fc"] <= -2
    ev["r60pos"] = ev["r60"] > 0
    def summ(g):
        out = {}
        for H in (5, 10, 20):
            x = g[f"ab{H}"].dropna()
            out[f"n{H}"] = len(x)
            out[f"mean_ab{H}"] = x.mean()
            out[f"t{H}"] = x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(out)
    res = {}
    res["all_reclaims_by_agit"] = ev.groupby("agit").apply(summ)
    res["by_agit_r60pos"] = ev.groupby(["agit", "r60pos"]).apply(summ)
    res["agit_by_shortbet"] = ev[ev.agit].groupby("short_bet").apply(summ)
    res["agit_by_coin"] = ev[ev.agit].groupby("coin").apply(summ)
    res["agit_by_year"] = ev[ev.agit].groupby("year").apply(summ)
    a = ev[ev.agit & ev.r60.notna()]
    res["agit_corr_r60_ab10"] = pd.Series({"spearman": stats.spearmanr(a.r60, a.ab10, nan_policy="omit")[0], "n": len(a)})
    a2 = ev[ev.agit]
    res["agit_corr_depth_ab10"] = pd.Series({"spearman": stats.spearmanr(a2.depth, a2.ab10, nan_policy="omit")[0], "n": len(a2)})
    ev["r60q"] = pd.qcut(ev["r60"], 4, labels=False, duplicates="drop")
    res["all_by_r60quart"] = ev.groupby("r60q").apply(summ)
    res["counts"] = pd.Series({"reclaims": len(ev), "agit": int(ev.agit.sum()), "r60_missing": int(ev.r60.isna().sum())})
    return res
