def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    h = 20
    drift = {}; usual = {}
    for c, ws in bars.items():
        rs = []
        for w, df in ws.items():
            cl = df["close"].values
            for i in range(0, len(cl) - h, h):
                rs.append(cl[i + h] / cl[i] - 1)
        drift[c] = np.mean(rs); usual[c] = np.std(rs, ddof=1)
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; fc = df["forecast"].fillna(0).values
            raw = df.get("debug_info.components.rally.last_history_value")
            raw = raw.values if raw is not None else np.full(len(df), np.nan)
            ts = pd.to_datetime(df["timestamp"]); n = len(df)
            lr = np.log(cl)
            for s in range(0, n, 20):
                idx = [i for i in range(s, min(s + 20, n)) if fc[i] <= -2]
                if not idx: continue
                i = idx[0]
                if i + h >= n: continue
                r = {"coin": c, "year": ts[i].year, "day": ts[i].normalize(), "fc": fc[i], "raw": raw[i],
                     "u20": -(cl[i + h] / cl[i] - 1 - drift[c])}
                r["ret10"] = cl[i] / cl[i - 10] - 1 if i >= 10 else np.nan
                r["ret20"] = cl[i] / cl[i - 20] - 1 if i >= 20 else np.nan
                r["vol20"] = np.std(np.diff(lr[i - 20:i + 1])) if i >= 20 else np.nan
                r["off_high20"] = cl[i] / cl[max(0, i - 19):i + 1].max() - 1 if i >= 19 else np.nan
                r["chg_next_after"] = np.nan
                rows.append(r)
    C = pd.DataFrame(rows)
    def ct(x, days):
        m = x.notna(); x = x[m]; d = days[m]
        if len(x) < 3: return (np.nan, np.nan, len(x))
        mu = x.mean(); g = (x - mu).groupby(d).sum(); G = len(g)
        se = np.sqrt(G / (G - 1) * (g ** 2).sum()) / len(x)
        return (mu, mu / se, len(x))
    out = {}
    out["overall"] = pd.Series(dict(zip(["u20", "t", "n"], ct(C["u20"], C["day"]))))
    for col in ["raw", "ret10", "ret20", "vol20", "off_high20"]:
        sub = C.dropna(subset=[col]).copy()
        sub["q"] = pd.qcut(sub[col].rank(method="first"), 3, labels=["low", "mid", "high"])
        res = []
        for k, g in sub.groupby("q"):
            mu, t, nn = ct(g["u20"], g["day"])
            res.append({"tercile": k, "mean_x": g[col].mean(), "u20_short": mu, "t": t, "n": nn})
        out[f"by {col} tercile"] = pd.DataFrame(res)
        out[f"spearman {col}"] = sub[col].corr(sub["u20"], method="spearman")
    # bear years vs others via coin's own window return before signal not available; split by year groups
    C["era"] = np.where(C.year <= 2022, "2018-2022", "2023-2025")
    res = []
    for k, g in C.groupby("era"):
        mu, t, nn = ct(g["u20"], g["day"]); res.append({"era": k, "u20": mu, "t": t, "n": nn})
    out["by era"] = pd.DataFrame(res)
    return out
