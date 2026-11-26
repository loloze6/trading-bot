def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3]
    drift = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs)
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; hi = df["high"].values; lo = df["low"].values; op = df["open"].values
            ret = pd.Series(cl).pct_change()
            sd30 = ret.rolling(30).std().values
            r60 = pd.Series(cl) / pd.Series(cl).shift(60) - 1
            r5 = pd.Series(cl) / pd.Series(cl).shift(5) - 1
            n = len(df)
            fc = df["forecast"].fillna(0).values
            prev = np.r_[0, fc[:-1]]
            sig = (fc - prev >= 2) & (fc > 0)
            seen = set()
            for i in np.where(sig)[0]:
                cell = i // 3
                if cell in seen: continue
                seen.add(cell)
                r = {"coin": c, "day": str(df["timestamp"].iloc[i])[:10],
                     "dayret_z": ret.iloc[i] / sd30[i] if sd30[i] > 0 else np.nan,
                     "body_z": ((cl[i] - op[i]) / op[i]) / sd30[i] if sd30[i] > 0 else np.nan,
                     "r60": r60.iloc[i], "r5": r5.iloc[i], "sd30": sd30[i],
                     "core": c in ["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"]}
                for h in H:
                    r[f"u{h}"] = cl[i + h] / cl[i] - 1 - drift[(c, h)] if i + h < n else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    def tday(col, sub):
        s = sub.dropna(subset=[col])
        g = s.groupby("day")[col].sum()
        m = s[col].mean()
        se = g.std(ddof=1) * np.sqrt(len(g)) / len(s) if len(g) > 1 else np.nan
        return pd.Series({"n": len(s), "days": len(g), "mean": m, "t": m / se if se else np.nan})
    out = {"all_stepdef": pd.DataFrame({h: tday(h, d) for h in ["u1", "u3"]}).T}
    for v in ["dayret_z", "body_z", "r60", "r5", "sd30"]:
        q = pd.qcut(d[v], 3, labels=["lo", "mid", "hi"])
        out[f"by_{v}"] = pd.concat({h: d.groupby(q).apply(lambda s: tday(h, s)) for h in ["u1", "u3"]})
    out["by_core"] = d.groupby("core").apply(lambda s: tday("u3", s))
    out["spearman"] = pd.Series({f"{a}_{h}": stats.spearmanr(d[a], d[h], nan_policy="omit")[0]
                                 for a in ["dayret_z", "body_z", "r60", "r5", "sd30"] for h in ["u1", "u3"]})
    return out
