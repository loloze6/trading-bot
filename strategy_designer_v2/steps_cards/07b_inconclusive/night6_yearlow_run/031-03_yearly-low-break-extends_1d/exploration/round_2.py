def explore(data):
    import numpy as np, pandas as pd, json, ast
    from scipy import stats
    bars = data["bars"]
    out = {}
    # inspect components format
    sample = None
    for coin, ws in bars.items():
        for w, df in ws.items():
            s = df.loc[df["regime"] == "trending", "debug_info.components"]
            if len(s):
                sample = s.iloc[0]; break
        if sample is not None: break
    out["comp_type"] = str(type(sample))
    out["comp_sample"] = str(sample)[:300]
    def parse(v):
        if isinstance(v, dict): return v
        if isinstance(v, str):
            for f in (json.loads, ast.literal_eval):
                try: return f(v)
                except Exception: pass
        return {}
    drift = {}; usual = {}
    for coin, ws in bars.items():
        r10 = []
        for w, df in ws.items():
            c = df["close"].values
            for i in range(0, len(c) - 10, 10):
                r10.append(c[i + 10] / c[i] - 1)
        drift[coin] = np.mean(r10); usual[coin] = np.std(r10, ddof=1)
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c)
            act = (df["regime"] == "trending").values
            fc = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            for i in range(n):
                if not act[i]: continue
                d = parse(df["debug_info.components"].iloc[i]).get("depth", {})
                raw = d.get("last_history_value", np.nan) if isinstance(d, dict) else np.nan
                # deepening: |fc| larger than min |fc| over previous run / previous bar
                prevfc = fc[i - 1] if i > 0 else 0.0
                rec = {"coin": coin, "w": w, "i": i, "cell": i // 10, "fc": fc[i], "raw": raw,
                       "deepen": abs(fc[i]) - abs(prevfc) >= 0.05,
                       "ret10back": c[i] / c[i - 10] - 1 if i >= 10 else np.nan,
                       "day": ts.iloc[i].normalize(), "year": ts.iloc[i].year}
                for h in [2, 5, 10, 20]:
                    rec[f"r{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(rec)
    A = pd.DataFrame(rows)
    A["u10"] = -(A["r10"] - A["coin"].map(drift))
    A["u5"] = -(A["r5"] - A["coin"].map(drift) / 2)
    A["u20"] = -(A["r20"] - A["coin"].map(drift) * 2)
    def tday(s, days):
        s = s.dropna(); days = days.loc[s.index]
        m = s.mean(); n = len(s)
        dev = (s - m).groupby(days).sum()
        se = np.sqrt((dev ** 2).sum()) / n
        return pd.Series({"mean": m, "t_day": m / se if se > 0 else np.nan, "n": n, "days": days.nunique()})
    out["raw_nonnull"] = int(A["raw"].notna().sum())
    out["raw_desc"] = A["raw"].describe()
    F = A.dropna(subset=["r10"]).sort_values("i").groupby(["coin", "w", "cell"]).first().reset_index()
    D = A[A["deepen"]].dropna(subset=["r10"]).sort_values("i").groupby(["coin", "w", "cell"]).first().reset_index()
    res = {}
    for name, X in [("first_per_cell", F), ("deepening_cases", D)]:
        for u in ["u5", "u10", "u20"]:
            res[f"{name}_{u}"] = tday(X[u], X["day"])
    out["short_side_unusual_by_set"] = pd.DataFrame(res).T
    F["fcq"] = pd.qcut(F["fc"].abs().rank(method="first"), 3, labels=["small", "mid", "large"])
    out["first_cell_by_fc_tercile"] = F.groupby("fcq")[["u5", "u10", "u20", "fc", "raw", "ret10back"]].mean().join(F.groupby("fcq").size().rename("n"))
    if F["raw"].notna().sum() > 10:
        F["rq"] = pd.qcut(F["raw"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
        out["first_cell_by_rawdepth"] = F.groupby("rq")[["u5", "u10", "u20", "raw"]].mean().join(F.groupby("rq").size().rename("n"))
    F["mq"] = pd.qcut(F["ret10back"].rank(method="first"), 3, labels=["fell_most", "mid", "fell_least"])
    out["first_cell_by_prior10d"] = F.groupby("mq")[["u5", "u10", "u20", "ret10back"]].mean().join(F.groupby("mq").size().rename("n"))
    out["spearman_F"] = F[["fc", "raw", "ret10back", "u5", "u10", "u20"]].corr(method="spearman")[["u5", "u10", "u20"]]
    out["deepen_by_coin"] = D.groupby("coin")["u10"].agg(["mean", "count"])
    out["deepen_by_year"] = D.groupby("year")["u10"].agg(["mean", "count"])
    return out
