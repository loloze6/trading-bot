def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - 7, 7):
                rs.append(c[i + 7] / c[i] - 1)
        drift = np.mean(rs)
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            reg = df["regime"].values
            fc = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            for i in range(30, n - 7, 7):
                if reg[i] != "unknown":
                    continue
                r30 = c[i] / c[i - 30] - 1
                if r30 >= 0:
                    continue
                r7p = c[i] / c[i - 7] - 1
                lo30 = c[i - 30:i + 1].min()
                hi30 = c[i - 30:i + 1].max()
                pos = (c[i] - lo30) / (hi30 - lo30) if hi30 > lo30 else np.nan
                x = -(c[i + 7] / c[i] - 1 - drift)
                rows.append({"coin": coin, "win": w, "day": ts[i], "r30": r30, "r7p": r7p,
                             "pos": pos, "fc": fc[i], "x": x})
    d = pd.DataFrame(rows)
    out = {}
    def tday(g):
        s = g.groupby("day")["x"].sum()
        cnt = g.groupby("day").size()
        m = g["x"].mean()
        dev = (g["x"] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(g)
        return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean": m, "t_day": m / se if se > 0 else np.nan})
    out["all"] = tday(d)
    out["no_w16"] = tday(d[d.win != "w16"])
    w = d["fc"].abs()
    out["weighted_mean_fc"] = float((d["x"] * w).sum() / w.sum()) if w.sum() > 0 else np.nan
    out["share_fc_nonzero"] = float((d["fc"] < 0).mean())
    d["last_week"] = np.where(d["r7p"] < 0, "still_falling", "bounced")
    out["by_last_week"] = d.groupby("last_week").apply(tday)
    d["near_low"] = pd.cut(d["pos"], [-0.01, 0.25, 0.6, 1.01], labels=["near_low", "mid", "near_high"])
    out["by_pos_in_range"] = d.groupby("near_low").apply(tday)
    d["year"] = pd.to_datetime(d["day"]).dt.year
    out["by_year"] = d.groupby("year").apply(tday)
    return out
