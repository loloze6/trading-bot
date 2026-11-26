import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    H = [5, 10, 20]
    drift, sd = {}, {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, b in ws.items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); sd[(c, h)] = np.std(rs, ddof=1)

    def ct(df, col):
        x = df.dropna(subset=[col])
        if len(x) < 5:
            return pd.Series({"n": len(x), "mean": np.nan, "t": np.nan, "days": 0})
        g = x.groupby("day")[col].apply(lambda v: (v - x[col].mean()).sum())
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return pd.Series({"n": len(x), "mean": x[col].mean(), "t": x[col].mean() / se, "days": G})

    rows, base = [], []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            f = b["forecast"].fillna(0).values
            cl = b["close"].values
            raw = b.get("debug_info.components.streak.last_history_value")
            raw = raw.values if raw is not None else np.full(len(b), np.nan)
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            up = np.r_[False, cl[1:] > cl[:-1]]
            streak = np.zeros(n)
            for i in range(1, n):
                streak[i] = streak[i - 1] + 1 if up[i] else 0
            # baseline: every 20-bar grid point with ret30>0 (regime, any streak)
            for h in H:
                for i in range(0, n - h, h):
                    if i >= 30 and cl[i] / cl[i - 30] - 1 > 0:
                        base.append({"h": h, "coin": c, "day": ts[i].normalize(), "year": ts[i].year,
                                     "u": cl[i + h] / cl[i] - 1 - drift[(c, h)],
                                     "upclose": int(up[i]), "streak": streak[i]})
            low, last_cell = 0.0, -1
            for i in range(n):
                if f[i] <= 0:
                    low = 0.0; continue
                if f[i] - low >= 2:
                    cell = i // 5
                    if cell != last_cell:
                        last_cell = cell
                        r = {"coin": c, "year": ts[i].year, "day": ts[i].normalize(), "fc": f[i],
                             "raw": raw[i], "streak": streak[i]}
                        for h in H:
                            if i + h < n:
                                r[f"u{h}"] = cl[i + h] / cl[i] - 1 - drift[(c, h)]
                        rows.append(r)
                    low = f[i]
                else:
                    low = min(low, f[i]) if low > 0 else f[i]
    d = pd.DataFrame(rows); B = pd.DataFrame(base)
    out = {}
    out["baseline_regime_all_gridpoints"] = B.groupby("h").apply(lambda x: ct(x, "u"))
    out["baseline_by_streak_len_h20"] = B[B.h == 20].assign(
        sl=lambda x: x["streak"].clip(upper=4)).groupby("sl").apply(lambda x: ct(x, "u"))
    out["baseline_by_streak_len_h10"] = B[B.h == 10].assign(
        sl=lambda x: x["streak"].clip(upper=4)).groupby("sl").apply(lambda x: ct(x, "u"))
    out["cases_by_year_u20"] = d.groupby("year").apply(lambda x: ct(x, "u20"))
    out["cases_by_year_u10"] = d.groupby("year").apply(lambda x: ct(x, "u10"))
    sl = {}
    for h in H:
        x = d.dropna(subset=[f"u{h}"])
        sl[h] = pd.Series({"slope_fc": np.polyfit(x["fc"], x[f"u{h}"], 1)[0],
                           "slope_raw": np.polyfit(x["raw"].fillna(x["raw"].median()), x[f"u{h}"], 1)[0],
                           "corr_raw": x[["raw", f"u{h}"]].corr().iloc[0, 1]})
    out["slopes"] = pd.DataFrame(sl).T
    out["cases_by_streaklen_u20"] = d.assign(sl=d["streak"].clip(upper=6)).groupby("sl").apply(lambda x: ct(x, "u20"))
    out["coins_positive_u20"] = (d.groupby("coin")["u20"].mean() > 0).mean()
    return out
