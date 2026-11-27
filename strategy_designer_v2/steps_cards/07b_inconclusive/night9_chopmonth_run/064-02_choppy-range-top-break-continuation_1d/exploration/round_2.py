def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [5, 10]
    drift, usual = {}, {}
    for coin, ws in bars.items():
        allr = {h: [] for h in H}
        for w, df in ws.items():
            c = df["close"].values
            for h in H:
                idx = np.arange(0, len(c)-h, h)
                allr[h] += list(c[idx+h]/c[idx]-1)
        drift[coin] = {h: np.mean(allr[h]) for h in H}
        usual[coin] = {h: np.std(allr[h]) for h in H}
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            c = df["close"].values
            lr = np.r_[np.nan, c[1:]/c[:-1]-1]
            sd30 = pd.Series(lr).rolling(30, min_periods=20).std().values
            sdmed = pd.Series(sd30).expanding(min_periods=20).median().values
            pf = np.r_[0, f[:-1]]
            bet = (f > 0) & (f - pf > 0)
            seen = set()
            for i in np.where(bet)[0]:
                cell = i // 5
                if cell in seen: continue
                seen.add(cell)
                r = {"coin": coin, "w": w, "f": f[i],
                     "day": str(df["timestamp"].iloc[i])[:10],
                     "zday": lr[i]/sd30[i] if i > 0 and sd30[i] > 0 else np.nan,
                     "agit": (sd30[i] > sdmed[i]) if not np.isnan(sdmed[i]) else np.nan,
                     "tr60": c[i]/c[i-60]-1 if i >= 60 else np.nan,
                     "tr20": c[i]/c[i-20]-1 if i >= 20 else np.nan}
                for h in H:
                    r[f"u{h}"] = c[i+h]/c[i]-1-drift[coin][h] if i+h < len(c) else np.nan
                    r[f"s{h}"] = r[f"u{h}"]/usual[coin][h] if i+h < len(c) else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    def pooled(s, col):
        s = s.dropna(subset=[col])
        n = len(s)
        if n < 3: return (n, np.nan, np.nan, np.nan)
        g = s[col].groupby(s["day"]).sum(); G = len(g)
        m = s[col].mean(); se = np.sqrt((g**2).sum()*G/(G-1))/n
        return (n, G, m, m/se)
    out = {}
    q = d["u5"].quantile([0.05, 0.95]).values
    d["u5w"] = d["u5"].clip(q[0], q[1])
    d["u5c"] = d["u5"] - d["u5"].groupby(d["day"]).transform("mean") * 0  # placeholder
    res = []
    for col in ["u5", "u5w", "s5", "u10", "s10"]:
        n, G, m, t = pooled(d, col)
        res.append({"col": col, "n": n, "days": G, "mean": m, "t": t})
    out["robust"] = pd.DataFrame(res)
    s5 = d.dropna(subset=["u5"]).sort_values("u5", ascending=False)
    out["top_contrib"] = pd.DataFrame({"top_k": [1, 3, 5, 10],
        "share_of_sum": [s5["u5"].head(k).sum()/s5["u5"].sum() for k in [1, 3, 5, 10]],
        "mean_without": [s5["u5"].iloc[k:].mean() for k in [1, 3, 5, 10]]})
    def tab(key, df_=d):
        res = []
        for k, s in df_.groupby(key):
            rr = {"k": k}
            for col in ["u5", "u5w", "s5", "u10"]:
                n, G, m, t = pooled(s, col)
                rr[f"n_{col}"] = n; rr[f"m_{col}"] = m; rr[f"t_{col}"] = t
            res.append(rr)
        return pd.DataFrame(res)
    d["agitq"] = d["agit"].map({True: "agit", False: "calm"})
    out["by_agitation"] = tab("agitq")
    d["tr60s"] = np.where(d["tr60"].isna(), "na", np.where(d["tr60"] > 0, "up60", "dn60"))
    out["by_tr60_sign"] = tab("tr60s")
    d["zq"] = pd.qcut(d["zday"].rank(method="first"), 3, labels=["z1", "z2", "z3"])
    out["by_zday_tercile"] = tab("zq")
    out["zday_tercile_means"] = d.groupby("zq")["zday"].mean()
    sl = d.dropna(subset=["s5", "f"])
    out["rank_corr_f_s5"] = str(stats.spearmanr(sl["f"], sl["s5"]))
    out["rank_corr_zday_s5"] = str(stats.spearmanr(d.dropna(subset=["zday", "s5"])["zday"], d.dropna(subset=["zday", "s5"])["s5"]))
    w = d.dropna(subset=["u5w"])
    out["slope_u5w_on_f"] = str(stats.linregress(w["f"], w["u5w"])[:4])
    return out
