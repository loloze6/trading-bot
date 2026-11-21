def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    col = "debug_info.components.beyond_high.post_pipeline_value"
    H = 20
    drift = {}
    sd = {}
    for c, ws in bars.items():
        r = {h: [] for h in (5, 10, 20, 40)}
        for w, df in ws.items():
            cl = df["close"].values
            for h in r:
                for i in range(0, len(cl) - h, h):
                    r[h].append(cl[i + h] / cl[i] - 1)
        drift[c] = {h: np.mean(v) for h, v in r.items()}
        sd[c] = np.std(r[20])
    ev = []
    allfirst = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            f = df[col].fillna(0).values
            raw = df["debug_info.components.beyond_high.last_history_value"].values if "debug_info.components.beyond_high.last_history_value" in df else np.full(len(cl), np.nan)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(cl)
            last = -10**9
            for i in range(1, n):
                if f[i] > 0 and f[i - 1] <= 0:
                    # past 90-bar return if available
                    p90 = cl[i] / cl[i - 90] - 1 if i >= 90 else np.nan
                    p20 = cl[i] / cl[i - 20] - 1 if i >= 20 else np.nan
                    row = {"coin": c, "w": w, "yr": yr[i], "f": f[i], "raw": raw[i], "p90": p90, "p20": p20, "sep": i - last >= H}
                    for h in (5, 10, 20, 40):
                        if i + h < n:
                            row[f"a{h}"] = cl[i + h] / cl[i] - 1 - drift[c][h]
                            row[f"s{h}"] = row[f"a{h}"] / sd[c]
                    if row["sep"]:
                        last = i
                    ev.append(row)
    e = pd.DataFrame(ev)
    def tt(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "median": x.median(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 1 else np.nan})
    s = e[e.sep]
    out = {}
    out["sep_events_by_h"] = pd.DataFrame({h: tt(s[f"a{h}"]) for h in (5, 10, 20, 40)})
    out["sep_events_strength_by_h"] = pd.DataFrame({h: tt(s[f"s{h}"]) for h in (5, 10, 20, 40)})
    s = s.copy()
    s["fq"] = pd.qcut(s.f.rank(method="first"), 3, labels=["low", "mid", "high"])
    out["sep_by_ftercile"] = s.groupby("fq").agg(n=("a20", "count"), a5=("a5", "mean"), a10=("a10", "mean"), a20=("a20", "mean"), a40=("a40", "mean"), raw=("raw", "mean"))
    out["sep_spearman_f"] = pd.Series({h: stats.spearmanr(s.f, s[f"a{h}"], nan_policy="omit")[0] for h in (5, 10, 20, 40)})
    out["sep_by_coin_a10"] = s.groupby("coin")["a10"].apply(tt).unstack()
    out["sep_by_year_a10"] = s.groupby("yr")["a10"].apply(tt).unstack()
    s["p90q"] = pd.qcut(s.p90.rank(method="first"), 3, labels=["low", "mid", "high"])
    out["sep_by_p90tercile"] = s.groupby("p90q").agg(n=("a20", "count"), p90=("p90", "mean"), a5=("a5", "mean"), a10=("a10", "mean"), a20=("a20", "mean"))
    s["p20q"] = pd.qcut(s.p20.rank(method="first"), 3, labels=["low", "mid", "high"])
    out["sep_by_p20tercile"] = s.groupby("p20q").agg(n=("a20", "count"), p20=("p20", "mean"), a5=("a5", "mean"), a10=("a10", "mean"), a20=("a20", "mean"))
    out["share_events_sep"] = float(e.sep.mean())
    out["n_windows_with_event"] = int(s.groupby(["coin", "w"]).size().shape[0])
    return out
