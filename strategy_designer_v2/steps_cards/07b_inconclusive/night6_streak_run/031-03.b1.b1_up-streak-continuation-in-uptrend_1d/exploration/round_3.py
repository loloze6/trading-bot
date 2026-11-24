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

    def slope_t(x, col, xc):
        x = x.dropna(subset=[col, xc])
        X = x[xc] - x[xc].mean()
        b = (X * x[col]).sum() / (X ** 2).sum()
        e = x[col] - x[col].mean() - b * X
        g = (X * e).groupby(x["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / (X ** 2).sum()
        return pd.Series({"slope": b, "t": b / se, "n": len(x)})

    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            f = b["forecast"].fillna(0).values
            cl = b["close"].values
            raw = b.get("debug_info.components.streak.last_history_value")
            raw = raw.values if raw is not None else np.full(len(b), np.nan)
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            low, last_cell = 0.0, -1
            for i in range(n):
                if f[i] <= 0:
                    low = 0.0; continue
                if f[i] - low >= 2:
                    cell = i // 5
                    if cell != last_cell:
                        last_cell = cell
                        r = {"coin": c, "day": ts[i].normalize(), "fc": f[i], "raw": raw[i],
                             "ret60": cl[i] / cl[i - 60] - 1 if i >= 60 else np.nan,
                             "ret10": cl[i] / cl[i - 10] - 1 if i >= 10 else np.nan}
                        for h in H:
                            if i + h < n:
                                r[f"u{h}"] = cl[i + h] / cl[i] - 1 - drift[(c, h)]
                        rows.append(r)
                    low = f[i]
                else:
                    low = min(low, f[i]) if low > 0 else f[i]
    d = pd.DataFrame(rows)
    out = {}
    out["slope_fc_t"] = pd.DataFrame({h: slope_t(d, f"u{h}", "fc") for h in H}).T
    out["slope_raw_t"] = pd.DataFrame({h: slope_t(d, f"u{h}", "raw") for h in H}).T
    d["s60"] = np.where(d["ret60"].isna(), "na", np.where(d["ret60"] > 0, "pos", "neg"))
    out["by_ret60_sign_u10"] = d.groupby("s60").apply(lambda x: ct(x, "u10"))
    out["by_ret60_sign_u20"] = d.groupby("s60").apply(lambda x: ct(x, "u20"))
    out["by_ret60_sign_u5"] = d.groupby("s60").apply(lambda x: ct(x, "u5"))
    pos = d[d.s60 == "pos"].copy()
    pos["fcq"] = pd.qcut(pos["fc"].rank(method="first"), 3, labels=False)
    out["ret60pos_fc_tercile_u10"] = pos.groupby("fcq").apply(lambda x: ct(x, "u10"))
    out["ret60pos_slope_fc"] = pd.DataFrame({h: slope_t(pos, f"u{h}", "fc") for h in H}).T
    d["rawq"] = pd.qcut(d["raw"].rank(method="first"), 3, labels=False)
    out["raw_tercile_u10"] = d.groupby("rawq").apply(lambda x: ct(x, "u10"))
    return out
