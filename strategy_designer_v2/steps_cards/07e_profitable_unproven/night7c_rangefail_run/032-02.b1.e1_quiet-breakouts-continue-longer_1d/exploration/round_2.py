def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    H = [10, 20]
    normal = {h: [] for h in H}
    cases = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True); cl = b["close"].astype(float); n = len(cl)
            for h in H:
                for i in range(0, n - h, h):
                    normal[h].append((c, cl.iloc[i+h]/cl.iloc[i]-1))
            pm = cl.shift(1).rolling(60, min_periods=60).max()
            pmin = cl.shift(1).rolling(60, min_periods=60).min()
            er = (cl.diff(60).abs() / cl.diff().abs().rolling(60).sum()).rolling(5).mean()
            ret = cl.pct_change()
            sd = ret.rolling(60).std()
            r20 = cl.pct_change(20)
            r60 = cl.pct_change(60)
            rng = pm / pmin - 1
            brk = cl / pm - 1
            for g in range(0, n, 10):
                idx = [i for i in range(g, min(g+10, n)) if brk.iloc[i] > 0]
                if not idx: continue
                i = idx[0]
                rec = {"coin": c, "w": w, "day": pd.to_datetime(b["timestamp"].iloc[i]).floor("D"),
                       "er": er.iloc[i], "brk": brk.iloc[i], "brkz": brk.iloc[i]/sd.iloc[i] if sd.iloc[i] > 0 else np.nan,
                       "r1": ret.iloc[i], "r20": r20.iloc[i], "r60": r60.iloc[i], "rng": rng.iloc[i],
                       "rngz": rng.iloc[i]/(sd.iloc[i]*np.sqrt(60)) if sd.iloc[i] > 0 else np.nan}
                for h in H:
                    rec[f"f{h}"] = cl.iloc[i+h]/cl.iloc[i]-1 if i+h < n else np.nan
                cases.append(rec)
    C = pd.DataFrame(cases)
    nd = {h: pd.DataFrame(normal[h], columns=["coin", "r"]).groupby("coin")["r"].mean() for h in H}
    for h in H:
        C[f"u{h}"] = C[f"f{h}"] - C["coin"].map(nd[h])
    def tday(x, col):
        x = x[["day", col]].dropna()
        if len(x) < 3: return (np.nan, np.nan, len(x))
        m = x[col].mean(); s = (x[col]-m).groupby(x["day"]).sum(); G = len(s)
        se = np.sqrt((s**2).sum()*G/(G-1))/len(x)
        return (m, m/se, len(x))
    out["all_breakouts"] = pd.DataFrame({h: tday(C, f"u{h}") for h in H}, index=["mean", "t", "n"]).T
    C["choppy"] = C["er"] < 0.3
    out["choppy_vs_not"] = pd.DataFrame({(k, h): tday(C[C["choppy"] == k], f"u{h}") for k in [True, False] for h in H}, index=["mean", "t", "n"]).T
    for col in ["er", "brk", "brkz", "r20", "r60", "rngz", "r1"]:
        q = pd.qcut(C[col], 4, labels=False, duplicates="drop")
        res = {}
        for k in sorted(q.dropna().unique()):
            sub = C[q == k]
            m10 = tday(sub, "u10"); m20 = tday(sub, "u20")
            res[k] = {"lo": sub[col].min(), "hi": sub[col].max(), "n": m10[2], "u10": m10[0], "t10": m10[1], "u20": m20[0], "t20": m20[1]}
        out[f"q_{col}"] = pd.DataFrame(res).T
        x = C[[col, "u10", "u20"]].dropna()
        out.setdefault("spearman", {})[col] = (stats.spearmanr(x[col], x["u10"])[0], stats.spearmanr(x[col], x["u20"])[0], len(x))
    out["spearman"] = pd.DataFrame(out["spearman"], index=["rho_u10", "rho_u20", "n"]).T
    ch = C[C["choppy"]]
    for col in ["brkz", "r60"]:
        q = pd.qcut(ch[col], 3, labels=False, duplicates="drop")
        out[f"choppy_q_{col}"] = pd.DataFrame({k: {"lo": ch[q == k][col].min(), "hi": ch[q == k][col].max(), "n": tday(ch[q == k], "u20")[2],
                                                   "u10": tday(ch[q == k], "u10")[0], "t10": tday(ch[q == k], "u10")[1],
                                                   "u20": tday(ch[q == k], "u20")[0], "t20": tday(ch[q == k], "u20")[1]} for k in sorted(q.dropna().unique())}).T
    out["by_coin_u20"] = C.groupby("coin")[["u10", "u20"]].mean()
    return out
