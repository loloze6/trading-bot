def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    H = [3, 10]
    drift = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            fc = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            s = pd.Series(cl)
            r30 = s.pct_change(30).values
            r7 = s.pct_change(7).values
            vol = s.pct_change().rolling(30).std().values
            n = len(df)
            for start in range(0, n, 10):
                idx = [i for i in range(start, min(start + 10, n)) if fc[i] <= -2]
                if not idx:
                    continue
                i = idx[0]
                rec = {"coin": c, "window": w, "day": ts[i].normalize(), "fc": fc[i],
                       "r30": r30[i], "r7": r7[i], "z30": r30[i] / (vol[i] * np.sqrt(30)) if vol[i] > 0 else np.nan}
                for h in H:
                    rec[f"un{h}"] = (-(cl[i + h] / cl[i] - 1) + drift[(c, h)]) if i + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)

    def ct(sub, col):
        x = sub[[col, "day"]].dropna()
        if len(x) < 3:
            return pd.Series({"mean": x[col].mean() if len(x) else np.nan, "t": np.nan, "n": len(x), "days": x["day"].nunique()})
        m = x[col].mean()
        g = (x[col] - m).groupby(x["day"]).sum()
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return pd.Series({"mean": m, "t": m / se, "n": len(x), "days": G})

    out["all_un10"] = ct(d, "un10")
    out["excl_w16_un10"] = ct(d[d["window"] != "w16"], "un10")
    out["all_un3"] = ct(d, "un3")
    out["windows_positive_share"] = float((d.groupby("window")["un10"].mean() > 0).mean())
    out["median_un10"] = float(d["un10"].median())
    out["share_un10_pos"] = float((d["un10"] > 0).mean())
    d["r7s"] = np.where(d["r7"] < 0, "week_down", "week_up")
    out["by_r7_sign"] = d.groupby("r7s").apply(lambda s: ct(s, "un10")).round(4)
    d["z30q"] = pd.qcut(d["z30"], 3, labels=False, duplicates="drop")
    out["by_z30_tercile"] = d.groupby("z30q").apply(lambda s: ct(s, "un10")).round(4)
    out["spearman_r30_un10"] = float(d[["r30", "un10"]].dropna().corr("spearman").iloc[0, 1])
    out["spearman_z30_un10"] = float(d[["z30", "un10"]].dropna().corr("spearman").iloc[0, 1])
    out["spearman_r30_un10_excl_w16"] = float(d[d["window"] != "w16"][["r30", "un10"]].dropna().corr("spearman").iloc[0, 1])
    return out
