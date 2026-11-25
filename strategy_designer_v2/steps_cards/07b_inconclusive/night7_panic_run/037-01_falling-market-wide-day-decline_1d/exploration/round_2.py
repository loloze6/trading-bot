def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    def stat(x, col):
        x = x.dropna(subset=[col])
        n = len(x)
        if n < 3: return pd.Series({"n": n, "days": x["day"].nunique(), "mean": x[col].mean() if n else np.nan, "t": np.nan})
        s = x.groupby("day")[col].sum() - x[col].mean() * x.groupby("day")[col].size()
        D = len(s)
        se = np.sqrt((s ** 2).sum() * D / max(D - 1, 1)) / n
        return pd.Series({"n": n, "days": D, "mean": x[col].mean(), "t": x[col].mean() / se if se else np.nan})
    res_h = {}
    per_h = {}
    for H in (3, 5, 7, 10):
        rows = []
        for coin, ws in bars.items():
            rets = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - H, H)
                rets += list(c[idx + H] / c[idx] - 1)
            m, sd = np.mean(rets), np.std(rets, ddof=1)
            for w, b in ws.items():
                b = b.reset_index(drop=True)
                c = b["close"]; r = c.pct_change()
                sd30 = r.rolling(30).std()
                ratio = ((b["high"] - b["low"]) / c) / sd30
                tr60 = c / c.shift(60) - 1
                n = len(b)
                seen = set()
                for i in range(n - H):
                    if not (tr60.iloc[i] < -0.10 and ratio.iloc[i] >= 2.0): continue
                    cell = i // H
                    if cell in seen: continue
                    seen.add(cell)
                    fr = c.iloc[i + H] / c.iloc[i] - 1
                    ts = pd.Timestamp(b["timestamp"].iloc[i])
                    rows.append({"coin": coin, "w": w, "day": ts.normalize(), "year": ts.year,
                                 "ratio": ratio.iloc[i], "closedown": bool(c.iloc[i] < b["open"].iloc[i]),
                                 "dayret": r.iloc[i], "tr60": tr60.iloc[i],
                                 "u": -(fr - m), "tot": -fr, "s": -(fr - m) / sd})
        df = pd.DataFrame(rows)
        per_h[H] = df
        res_h[f"h{H}"] = pd.concat([stat(df, "u"), pd.Series({"total": df["tot"].mean(), "strength": df["s"].mean(),
                                    "corr_ratio_u": df[["ratio", "u"]].corr().iloc[0, 1]})])
    out["nonoverlap_by_horizon"] = pd.DataFrame(res_h).T
    d10 = per_h[10].copy()
    d10["rq"] = pd.qcut(d10["ratio"], 3, labels=False)
    out["h10_by_ratio_tercile"] = d10.groupby("rq").apply(lambda x: pd.concat([stat(x, "u"), pd.Series({"rmed": x["ratio"].median()})]))
    out["h10_by_closedown"] = d10.groupby("closedown").apply(lambda x: stat(x, "u"))
    out["h10_by_year"] = d10.groupby("year").apply(lambda x: stat(x, "u"))
    out["h10_by_coin"] = d10.groupby("coin").apply(lambda x: stat(x, "u"))
    d10["tq"] = pd.qcut(d10["tr60"], 3, labels=False)
    out["h10_by_trend_tercile"] = d10.groupby("tq").apply(lambda x: pd.concat([stat(x, "u"), pd.Series({"tmed": x["tr60"].median()})]))
    d3 = per_h[3].copy()
    out["h3_by_closedown"] = d3.groupby("closedown").apply(lambda x: stat(x, "u"))
    out["h3_by_coin"] = d3.groupby("coin").apply(lambda x: stat(x, "u"))
    return out
