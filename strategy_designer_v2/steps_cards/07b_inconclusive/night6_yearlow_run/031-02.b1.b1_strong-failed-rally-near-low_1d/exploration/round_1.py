def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [5, 10, 20, 40]
    # coin normal drift per horizon (non-overlapping, all windows)
    drift = {}
    usual = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs, ddof=1)
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; fc = df["forecast"].fillna(0).values
            reg = (df["regime"] == "mean_reversion").values
            raw = df.get("debug_info.components.rally.last_history_value")
            raw = raw.values if raw is not None else np.full(len(df), np.nan)
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            # cases: first bar per 20-bar cell with forecast <= -2
            for s in range(0, n, 20):
                idx = [i for i in range(s, min(s + 20, n)) if fc[i] <= -2]
                if idx:
                    i = idx[0]
                    r = {"coin": c, "win": w, "year": ts[i].year, "day": ts[i].normalize(),
                         "fc": fc[i], "raw": raw[i], "kind": "case"}
                    for h in H:
                        r[f"u{h}"] = -(cl[i + h] / cl[i] - 1 - drift[(c, h)]) if i + h < n else np.nan
                        r[f"s{h}"] = r[f"u{h}"] / usual[(c, h)] if i + h < n else np.nan
                    rows.append(r)
            # grid bars for regime comparisons
            for i in range(0, n, 20):
                r = {"coin": c, "win": w, "year": ts[i].year, "day": ts[i].normalize(), "fc": fc[i],
                     "raw": raw[i], "kind": "grid", "reg": reg[i]}
                for h in H:
                    r[f"u{h}"] = -(cl[i + h] / cl[i] - 1 - drift[(c, h)]) if i + h < n else np.nan
                rows.append(r)
    D = pd.DataFrame(rows)
    def ct(x, days):
        m = x.notna(); x = x[m]; d = days[m]
        if len(x) < 3: return (np.nan, np.nan, len(x))
        mu = x.mean(); g = (x - mu).groupby(d).sum(); G = len(g)
        se = np.sqrt(G / (G - 1) * (g ** 2).sum()) / len(x)
        return (mu, mu / se, len(x))
    C = D[D.kind == "case"].copy()
    out = {}
    hz = []
    for h in H:
        mu, t, nn = ct(C[f"u{h}"], C["day"]); hz.append({"h": h, "mean_unusual_short": mu, "t": t, "n": nn, "strength": C[f"s{h}"].mean()})
    out["cases by horizon"] = pd.DataFrame(hz)
    def tab(key):
        res = []
        for k, g in C.groupby(key):
            mu, t, nn = ct(g["u20"], g["day"]); mu10, t10, _ = ct(g["u10"], g["day"])
            res.append({key: k, "n": nn, "u20": mu, "t20": t, "u10": mu10, "t10": t10})
        return pd.DataFrame(res)
    out["by coin"] = tab("coin"); out["by year"] = tab("year")
    C["fc_tercile"] = pd.qcut(C["fc"].abs().rank(method="first"), 3, labels=["small", "mid", "large"])
    out["by forecast tercile"] = tab("fc_tercile")
    rr = C[["raw", "u20", "u10", "u40"]].dropna()
    out["spearman raw rally vs short unusual u10/u20/u40"] = pd.Series({k: rr["raw"].corr(rr[k], method="spearman") for k in ["u10", "u20", "u40"]})
    Gd = D[D.kind == "grid"].copy()
    Gd["grp"] = np.where(~Gd.reg, "out_regime", np.where(Gd.fc < 0, "in_regime_rally", "in_regime_no_rally"))
    res = []
    for k, g in Gd.groupby("grp"):
        for h in [10, 20, 40]:
            mu, t, nn = ct(g[f"u{h}"], g["day"]); res.append({"grp": k, "h": h, "short_unusual": mu, "t": t, "n": nn})
    out["grid groups"] = pd.DataFrame(res)
    return out
