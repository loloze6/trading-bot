def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    for coin, ws in bars.items():
        allr = {h: [] for h in (1, 3, 5, 10)}
        for w, df in ws.items():
            c = df["close"].values
            for h in allr:
                for i in range(0, len(c) - h, h):
                    allr[h].append(c[i + h] / c[i] - 1)
        drift[coin] = {h: np.mean(v) for h, v in allr.items()}
        usual[coin] = {h: np.std(v, ddof=1) for h, v in allr.items()}
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            raw = df.get("debug_info.components.scaled_fall.last_history_value")
            post = df.get("debug_info.components.scaled_fall.post_pipeline_value")
            reg = df["regime"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            for i in range(0, n - 3, 3):
                if reg[i] != "unknown" or raw is None or pd.isna(raw.iloc[i]):
                    continue
                if raw.iloc[i] >= 0:
                    continue
                r = {"coin": coin, "w": w, "yr": yr[i], "raw": raw.iloc[i],
                     "post": post.iloc[i] if post is not None else np.nan,
                     "fc": df["forecast"].iloc[i]}
                for h in (1, 3, 5, 10):
                    if i + h < n:
                        ret = c[i + h] / c[i] - 1
                        r[f"u{h}"] = -(ret - drift[coin][h])
                        r[f"t{h}"] = -ret
                rows.append(r)
    d = pd.DataFrame(rows)
    out = {}
    def summ(g, col="u3"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["all_by_horizon"] = pd.DataFrame({h: summ(d, f"u{h}") for h in (1, 3, 5, 10)}).T
    out["total_by_horizon"] = pd.DataFrame({h: summ(d, f"t{h}") for h in (1, 3, 5, 10)}).T
    out["by_coin_u3"] = d.groupby("coin").apply(summ)
    out["by_window_u3"] = d.groupby("w").apply(summ)
    out["by_year_u3"] = d.groupby("yr").apply(summ)
    d["q_raw"] = pd.qcut(d["raw"], 4, labels=["q1_bigfall", "q2", "q3", "q4_smallfall"])
    out["by_raw_quartile_u3"] = d.groupby("q_raw").apply(summ)
    out["by_raw_quartile_u5"] = d.groupby("q_raw").apply(lambda g: summ(g, "u5"))
    out["by_raw_quartile_u10"] = d.groupby("q_raw").apply(lambda g: summ(g, "u10"))
    dd = d.dropna(subset=["post"])
    dd = dd[dd["post"] < 0]
    if len(dd) > 20:
        dd = dd.copy()
        dd["q_post"] = pd.qcut(dd["post"], 4, labels=["q1_strong", "q2", "q3", "q4_weak"], duplicates="drop")
        out["by_post_quartile_u3"] = dd.groupby("q_post").apply(summ)
    out["corr_raw_u3_spearman"] = float(stats.spearmanr(d["raw"], d["u3"], nan_policy="omit")[0])
    out["usual_move"] = pd.DataFrame(usual).T
    out["drift"] = pd.DataFrame(drift).T
    return out
