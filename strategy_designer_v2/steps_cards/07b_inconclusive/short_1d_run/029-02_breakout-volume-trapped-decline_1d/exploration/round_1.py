def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    rows = []
    drift = {}
    usual = {}
    for coin, ws in bars.items():
        for h in H:
            rs = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs)
            usual[(coin, h)] = np.std(rs)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            f = b["forecast"].fillna(0).values
            c = b["close"].values
            ts = pd.to_datetime(b["timestamp"])
            vr = b["debug_info.components.fb_vol.last_history_value"].values
            ret20 = pd.Series(c).pct_change(20).values
            ret60 = pd.Series(c).pct_change(60).values
            ref = 0.0
            used = set()
            for t in range(len(f)):
                if f[t] >= 0:
                    ref = 0.0
                    continue
                if f[t] <= ref - 2:
                    cell = t // 5
                    ref = f[t]
                    if cell in used or t + 5 >= len(c):
                        continue
                    used.add(cell)
                    r = {"coin": coin, "win": w, "year": ts[t].year, "f": f[t], "vr": vr[t],
                         "ret20": ret20[t], "ret60": ret60[t]}
                    for h in H:
                        if t + h < len(c):
                            raw = c[t + h] / c[t] - 1
                            r[f"u{h}"] = -(raw - drift[(coin, h)])
                            r[f"tot{h}"] = -raw
                    rows.append(r)
                else:
                    ref = max(ref, f[t]) if False else ref
    d = pd.DataFrame(rows)
    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["by horizon"] = pd.DataFrame({h: summ(d, f"u{h}") for h in H}).T
    out["by horizon total"] = pd.DataFrame({h: summ(d, f"tot{h}") for h in H}).T
    out["by coin"] = d.groupby("coin").apply(summ)
    out["by year"] = d.groupby("year").apply(summ)
    d["vrq"] = pd.qcut(d["vr"], 3, labels=["low", "mid", "high"])
    out["by vol ratio tercile u5"] = d.groupby("vrq").apply(summ)
    out["by vol ratio tercile u10"] = d.groupby("vrq").apply(lambda g: summ(g, "u10"))
    d["r60s"] = np.where(d["ret60"] > 0, "up60", "down60")
    out["by 60d trend u5"] = d.groupby("r60s").apply(summ)
    out["by 60d trend u10"] = d.groupby("r60s").apply(lambda g: summ(g, "u10"))
    d["r60q"] = pd.qcut(d["ret60"], 4, labels=False)
    out["by 60d ret quartile u5"] = d.groupby("r60q").apply(summ)
    out["by 20d ret quartile u5"] = d.groupby(pd.qcut(d["ret20"], 4, labels=False)).apply(summ)
    out["corr vr u5"] = float(d[["vr", "u5"]].corr().iloc[0, 1])
    out["n cases"] = len(d)
    return out
