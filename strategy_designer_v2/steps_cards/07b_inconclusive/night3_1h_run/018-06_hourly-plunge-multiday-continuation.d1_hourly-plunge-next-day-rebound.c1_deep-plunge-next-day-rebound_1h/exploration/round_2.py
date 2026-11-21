def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    H = [24, 72, 120]
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            rs = np.array(rs)
            drift[(coin, h)] = rs.mean()
            usual[(coin, h)] = rs.std()
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            lowest = 0.0
            taken = {24: set(), 120: set()}
            for i in range(n):
                if f[i] - lowest >= 2:
                    lowest = f[i]
                    first24 = (i // 24) not in taken[24]
                    first120 = (i // 120) not in taken[120]
                    taken[24].add(i // 24)
                    taken[120].add(i // 120)
                    if not (first24 or first120):
                        continue
                    r = {"coin": coin, "win": w, "year": ts.iloc[i].year, "hour": ts.iloc[i].hour,
                         "fc": f[i], "first24": first24, "first120": first120,
                         "tr30": c[i] / c[i - 720] - 1 if i >= 720 else np.nan,
                         "u120": usual[(coin, 120)]}
                    for h in H:
                        r[f"x{h}"] = (c[i + h] / c[i] - 1 - drift[(coin, h)]) if i + h < n else np.nan
                        r[f"t{h}"] = (c[i + h] / c[i] - 1) if i + h < n else np.nan
                    rows.append(r)
                else:
                    lowest = min(lowest, f[i])
    d = pd.DataFrame(rows)

    def summ(g, col="x120"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    nd = d[d.first120].copy()  # non-overlapping 120h cases
    nd["up"] = nd["tr30"] > 0
    out["nonoverlap120_all"] = pd.DataFrame({c: summ(nd, c) for c in ["x24", "x72", "x120", "t120"]}).T
    out["nonoverlap120_by_up"] = pd.concat({c: nd.groupby("up").apply(lambda g: summ(g, c)) for c in ["x120", "t120"]}, axis=1)
    up = nd[nd.up].copy()
    up["fcb"] = pd.cut(up["fc"], [0, 4, 10, 19.99, 20.01])
    out["up_by_fc_x120"] = up.groupby("fcb").apply(summ)
    up["trb"] = pd.qcut(up["tr30"], 3)
    out["up_by_trend_tercile_x120"] = up.groupby("trb").apply(summ)
    out["up_by_coin_x120"] = up.groupby("coin").apply(summ)
    out["up_by_year_x120"] = up.groupby("year").apply(summ)
    out["up_strength120"] = pd.Series({"mean_strength": (up["x120"] / up["u120"]).mean(),
                                       "unusual%": 100 * up["x120"].mean(),
                                       "total%": 100 * up["t120"].mean()})
    # graded: drop multiple x trend; correlation within up
    out["up_corr"] = pd.Series({"corr_fc_x120": up[["fc", "x120"]].corr().iloc[0, 1],
                                "corr_tr30_x120": up[["tr30", "x120"]].corr().iloc[0, 1]})
    # hour effect stability (24h cases)
    d24 = d[d.first24].copy()
    d24["hb"] = d24["hour"] // 6
    d24["half"] = np.where(d24["year"] <= 2021, "2018-21", "2022-25")
    out["hour6_by_half_x24"] = d24.groupby(["half", "hb"]).apply(lambda g: summ(g, "x24"))
    return out
