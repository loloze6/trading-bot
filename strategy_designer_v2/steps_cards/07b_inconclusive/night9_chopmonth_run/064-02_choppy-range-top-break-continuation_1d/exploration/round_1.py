def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1,3,5,10]
    rows = []
    drift = {}
    usual = {}
    for coin, ws in bars.items():
        allr = {h: [] for h in H}
        for w, df in ws.items():
            c = df["close"].values
            for h in H:
                idx = np.arange(0, len(c)-h, h)
                allr[h] += list(c[idx+h]/c[idx]-1)
        drift[coin] = {h: np.mean(allr[h]) if allr[h] else np.nan for h in H}
        usual[coin] = {h: np.std(allr[h]) if allr[h] else np.nan for h in H}
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            c = df["close"].values
            raw = df.get("debug_info.components.brk.last_history_value")
            raw = raw.values if raw is not None else np.full(len(df), np.nan)
            pf = np.r_[0, f[:-1]]
            bet = (f > 0) & (f - pf > 0)
            seen = set()
            for i in np.where(bet)[0]:
                cell = i // 5
                if cell in seen: continue
                seen.add(cell)
                r = {"coin": coin, "w": w, "i": i, "f": f[i], "raw": raw[i],
                     "day": str(df["timestamp"].iloc[i])[:10],
                     "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "ret1d": c[i]/c[i-1]-1 if i > 0 else np.nan}
                # 60-bar trend inside window if available
                r["tr30"] = c[i]/c[i-30]-1 if i >= 30 else np.nan
                for h in H:
                    if i+h < len(c):
                        r[f"u{h}"] = c[i+h]/c[i]-1 - drift[coin][h]
                        r[f"s{h}"] = r[f"u{h}"]/usual[coin][h]
                    else:
                        r[f"u{h}"] = np.nan; r[f"s{h}"] = np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    def pooled(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 3: return (len(s), np.nan, np.nan, np.nan)
        dev = s[col] - 0
        g = dev.groupby(s["day"]).sum()
        G = len(g); n = len(s)
        m = dev.mean()
        se = np.sqrt((g**2).sum() * G/(G-1)) / n
        return (n, G, m, m/se)
    out = {}
    hz = []
    for h in H:
        n, G, m, t = pooled(d, f"u{h}")
        hz.append({"h": h, "n": n, "days": G, "mean": m, "t": t, "median": d[f"u{h}"].median(), "hit": (d[f"u{h}"] > 0).mean()})
    out["by_horizon"] = pd.DataFrame(hz)
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 4, labels=["q1","q2","q3","q4"])
    def tab(key):
        res = []
        for k, s in d.groupby(key):
            rr = {"k": k}
            for h in [3,5,10]:
                n, G, m, t = pooled(s, f"u{h}")
                rr[f"n{h}"] = n; rr[f"m{h}"] = m; rr[f"t{h}"] = t
            rr["med5"] = s["u5"].median(); rr["meanf"] = s["f"].mean(); rr["meanraw"]=s["raw"].mean()
            res.append(rr)
        return pd.DataFrame(res)
    out["by_forecast_q"] = tab("fq")
    out["by_coin"] = tab("coin")
    out["by_window"] = tab("w")
    out["by_year"] = tab("year")
    d["rq"] = pd.qcut(d["ret1d"].rank(method="first"), 4, labels=["r1","r2","r3","r4"])
    out["by_day_ret_q"] = tab("rq")
    out["n_cases"] = len(d)
    out["skew_u5"] = float(stats.skew(d["u5"].dropna()))
    out["trimmed_mean_u5_5pct"] = float(stats.trim_mean(d["u5"].dropna(), 0.05))
    sl = d.dropna(subset=["u5"])
    out["slope_u5_on_f"] = str(stats.linregress(sl["f"], sl["u5"])[:4])
    return out
