def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [5, 10]
    drift = {}
    for coin, ws in bars.items():
        for h in H:
            rs = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs)
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            f = b["forecast"].fillna(0).values
            c = b["close"].values; hi = b["high"].values; lo = b["low"].values
            ts = pd.to_datetime(b["timestamp"])
            vr = b["debug_info.components.fb_vol.last_history_value"].values
            ret60 = pd.Series(c).pct_change(60).values
            ret120 = pd.Series(c).pct_change(120).values
            ph = pd.Series(hi).shift(1).rolling(20).max().values
            ref = 0.0; used = set()
            for t in range(len(f)):
                if f[t] >= 0:
                    ref = 0.0; continue
                if f[t] <= ref - 2:
                    ref = f[t]; cell = t // 5
                    if cell in used or t + 5 >= len(c):
                        continue
                    used.add(cell)
                    k = None
                    for j in range(t - 1, max(t - 4, 0) - 1, -1):
                        if not np.isnan(ph[j]) and c[j] > ph[j] and c[t] < ph[j]:
                            k = j; break
                    r = {"coin": coin, "year": ts[t].year, "vr": vr[t], "ret60": ret60[t], "ret120": ret120[t]}
                    if k is not None:
                        r["lag"] = t - k
                        r["depth"] = c[t] / ph[k] - 1
                        r["below_low"] = c[t] < lo[k]
                        r["bo_size"] = c[k] / ph[k] - 1
                    for h in H:
                        if t + h < len(c):
                            r[f"u{h}"] = -(c[t + h] / c[t] - 1 - drift[(coin, h)])
                    rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["matched breakout share"] = float(d["lag"].notna().mean())
    out["by lag u5"] = d.groupby("lag").apply(summ)
    out["by depth tercile u5"] = d.groupby(pd.qcut(d["depth"], 3, labels=False)).apply(summ)
    out["by depth tercile u10"] = d.groupby(pd.qcut(d["depth"], 3, labels=False)).apply(lambda g: summ(g, "u10"))
    out["below breakout low u5"] = d.groupby("below_low").apply(summ)
    out["below breakout low u10"] = d.groupby("below_low").apply(lambda g: summ(g, "u10"))
    out["by breakout size tercile u5"] = d.groupby(pd.qcut(d["bo_size"], 3, labels=False)).apply(summ)
    d["r120s"] = np.where(d["ret120"] > 0, "up120", np.where(d["ret120"] <= 0, "down120", "na"))
    out["by 120d trend u5"] = d.groupby("r120s").apply(summ)
    out["by 120d trend u10"] = d.groupby("r120s").apply(lambda g: summ(g, "u10"))
    d["vrq"] = pd.qcut(d["vr"], 3, labels=["low", "mid", "high"])
    d["r60s"] = np.where(d["ret60"] > 0, "up60", "down60")
    out["vol x 60d trend u10"] = d.groupby(["r60s", "vrq"]).apply(lambda g: summ(g, "u10"))
    out["vol x 120d trend u5"] = d[d.r120s != "na"].groupby(["r120s", "vrq"]).apply(summ)
    for h in H:
        x = d[["vr", f"u{h}"]].dropna()
        sl = stats.linregress(x["vr"], x[f"u{h}"])
        out[f"slope u{h} on vr"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(x)})
    return out
