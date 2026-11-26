import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    drift = {}
    for c in bars:
        rs = []
        for w, df in bars[c].items():
            cl = df["close"].values
            idx = np.arange(0, len(cl) - 5, 5)
            rs += list(cl[idx + 5] / cl[idx] - 1)
        drift[c] = np.mean(rs) if rs else np.nan
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = pd.Series(df["close"].values)
            r = cl.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            sr = r / sd
            r3 = cl.pct_change(3)
            s3 = r3 / (sd * np.sqrt(3))
            r10 = cl.pct_change(10)
            tr = cl.pct_change(min(60, len(cl) - 1))
            ts = pd.to_datetime(df["timestamp"])
            mr = (df["regime"] == "mean_reversion").values
            fc = df["forecast"].values
            for i in np.where(mr)[0]:
                if i + 5 >= len(cl):
                    continue
                tot = cl[i + 5] / cl[i] - 1
                rec = {"coin": c, "win": w, "i": i, "day": ts.dt.floor("D").values[i],
                       "sr": sr[i], "s3": s3[i], "r10": r10[i], "fc": abs(fc[i]),
                       "sd": sd[i], "u5": -(tot - drift[c]), "t5": -tot,
                       "wd": ts.dt.weekday.values[i]}
                rows.append(rec)
    d = pd.DataFrame(rows)
    d = d.assign(cell=d["i"] // 5).drop_duplicates(["coin", "win", "cell"]).copy()

    def tday(x, col="u5"):
        x = x.dropna(subset=[col]); n = len(x)
        if n < 3: return np.nan
        m = x[col].mean(); dev = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / n
        return m / se if se > 0 else np.nan

    def grp(key):
        g = []
        for k, x in d.groupby(key):
            g.append({"key": k, "n": len(x), "mean_u5": x["u5"].mean(), "t": tday(x),
                      "mean_t5": x["t5"].mean(), "std_u5": x["u5"].std()})
        return pd.DataFrame(g)

    out = {}
    out["all"] = pd.DataFrame([{"n": len(d), "mean_u5": d["u5"].mean(), "t": tday(d),
                                "std_u5": d["u5"].std(), "median_u5": d["u5"].median(),
                                "share_pos": (d["u5"] > 0).mean()}])
    for col in ["s3", "r10", "fc", "sd"]:
        d[col + "_q"] = pd.qcut(d[col], 3, labels=False, duplicates="drop")
        out["by_" + col + "_tercile"] = grp(col + "_q")
        out[col + "_edges"] = d.groupby(col + "_q")[col].agg(["min", "max"])
    d["s3_pos"] = (d["s3"] > d["sr"] / np.sqrt(3)).astype(int)
    out["by_3day_rise_above_1day"] = grp("s3_pos")
    out["spearman"] = pd.Series({k: d[[k, "u5"]].dropna().corr(method="spearman").iloc[0, 1]
                                 for k in ["sr", "s3", "r10", "fc", "sd"]})
    d["trim"] = (d["u5"].abs() < d["u5"].abs().quantile(0.95)).astype(int)
    out["trimmed_top5pct"] = grp("trim")
    return out
