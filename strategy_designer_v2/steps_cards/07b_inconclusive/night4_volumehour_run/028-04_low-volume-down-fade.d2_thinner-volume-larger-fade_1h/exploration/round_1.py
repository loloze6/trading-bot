import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = [1, 2, 3, 6, 12, 24]
    rows = []
    drift = {}
    for coin, ws in data["bars"].items():
        for h in H:
            rs = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.concatenate(rs).mean()
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].values
            fl = b["debug_info.components.fall.last_history_value"].values
            fv = b["debug_info.components.fall_x_volume.last_history_value"].values
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            n = len(b)
            for s in range(0, n, 6):
                cell = np.where(f[s:s+6] >= 2)[0]
                if len(cell) == 0:
                    continue
                t = s + cell[0]
                d = {"coin": coin, "w": w, "year": yr[t], "fc": f[t],
                     "fall": fl[t], "v": fv[t] / fl[t] if fl[t] not in (0, np.nan) else np.nan,
                     "r1": r1[t]}
                for h in H:
                    d[f"u{h}"] = (c[t+h] / c[t] - 1 - drift[(coin, h)]) if t + h < n else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    df["v"] = df["v"].replace([np.inf, -np.inf], np.nan)

    def summ(g):
        out = {}
        for h in H:
            x = g[f"u{h}"].dropna()
            out[f"m{h}_bp"] = x.mean() * 1e4
            out[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        out["n"] = len(g)
        return pd.Series(out)

    res = {}
    res["all"] = summ(df).to_frame().T
    res["by_coin"] = df.groupby("coin").apply(summ)
    res["by_year"] = df.groupby("year").apply(summ)
    df["vq"] = pd.qcut(df["v"], 5, labels=False, duplicates="drop")
    res["by_vol_quintile"] = df.groupby("vq").apply(summ)
    res["vq_vmean"] = df.groupby("vq")["v"].agg(["mean", "min", "max"])
    df["fq"] = pd.qcut(df["fall"], 5, labels=False, duplicates="drop")
    res["by_fall_quintile(0=deepest)"] = df.groupby("fq").apply(summ)
    df["fcq"] = pd.qcut(df["fc"], 5, labels=False, duplicates="drop")
    res["by_forecast_quintile"] = df.groupby("fcq").apply(summ)
    res["forecast_q_desc"] = df.groupby("fcq")[["fc", "fall", "v"]].mean()
    res["by_window"] = df.groupby("w").apply(summ)[["m6_bp", "t6", "n"]]
    return res
