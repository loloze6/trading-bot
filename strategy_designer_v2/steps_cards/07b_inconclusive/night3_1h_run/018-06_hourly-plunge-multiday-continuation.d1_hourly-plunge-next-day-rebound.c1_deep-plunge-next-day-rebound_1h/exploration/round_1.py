def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    H = [24, 72, 120]
    for coin, wins in bars.items():
        # drift per horizon
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
            # 30-day trend before signal, and 24h return
            lowest = 0.0
            cell_taken = set()
            for i in range(n):
                if f[i] - lowest >= 2:
                    cell = i // 24
                    lowest = f[i]
                    if cell in cell_taken:
                        continue
                    cell_taken.add(cell)
                    r = {"coin": coin, "win": w, "year": ts.iloc[i].year, "hour": ts.iloc[i].hour,
                         "fc": f[i],
                         "tr30": c[i] / c[i - 720] - 1 if i >= 720 else np.nan}
                    for h in H:
                        r[f"x{h}"] = (c[i + h] / c[i] - 1 - drift[(coin, h)]) if i + h < n else np.nan
                    rows.append(r)
                else:
                    lowest = min(lowest, f[i])
    d = pd.DataFrame(rows)

    def summ(g, col="x24"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["all_by_horizon"] = pd.DataFrame({h: summ(d, f"x{h}") for h in H}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fcb"] = pd.cut(d["fc"], [0, 4, 10, 19.99, 20.01])
    out["by_fc"] = pd.concat({h: d.groupby("fcb").apply(lambda g: summ(g, f"x{h}")) for h in H}, axis=1)
    d["trb"] = pd.qcut(d["tr30"], 4)
    out["by_trend30_q"] = pd.concat({h: d.groupby("trb").apply(lambda g: summ(g, f"x{h}")) for h in H}, axis=1)
    d["hb"] = d["hour"] // 6
    out["by_hour6"] = d.groupby("hb").apply(summ)
    out["usual"] = pd.Series({f"{k[0]}_{k[1]}": v for k, v in usual.items() if k[1] == 24})
    out["fc20_by_trend"] = d[d.fc >= 19.99].groupby("trb").apply(summ)
    return out
