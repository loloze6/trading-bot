import numpy as np
import pandas as pd

def explore(data):
    bars = data["bars"]
    H = [2, 6]
    drift = {}
    for coin in bars:
        for h in H:
            rs = []
            for w, df in bars[coin].items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.concatenate(rs).mean()
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"]; r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std().shift(1)
            vm = df["volume"].rolling(720, min_periods=240).mean().shift(1)
            n = len(df); cv = c.values
            d = pd.DataFrame({"coin": coin, "win": w, "z": r / sd, "vr": df["volume"] / vm,
                              "f": df["forecast"].fillna(0).values,
                              "tr30": c / c.shift(720) - 1,
                              "tr7": c / c.shift(168) - 1,
                              "volreg": sd / sd.rolling(2160, min_periods=500).median(),
                              "hour": pd.to_datetime(df["timestamp"]).dt.hour,
                              "cell": np.arange(n) // 6})
            for h in H:
                fwd = np.full(n, np.nan); fwd[: n - h] = cv[h:] / cv[: n - h] - 1
                d[f"x{h}"] = fwd - drift[(coin, h)]
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def summ(g, col):
        v = g[col].dropna()
        if len(v) < 5: return pd.Series({"n": len(v), "bp": np.nan, "t": np.nan})
        return pd.Series({"n": len(v), "bp": v.mean() * 1e4, "t": v.mean() / (v.std() / np.sqrt(len(v)))})
    C = A[A["f"] >= 2].groupby(["coin", "win", "cell"]).head(1).copy()
    C["trend30"] = np.where(C["tr30"] > 0, "up30", "down30")
    C.loc[C["tr30"].isna(), "trend30"] = "na"
    C["trend7"] = np.where(C["tr7"] > 0, "up7", "down7")
    C["volq"] = pd.qcut(C["volreg"], 3, labels=["lowvol", "midvol", "highvol"])
    C["vrq"] = pd.qcut(C["vr"], 4, labels=["vr_q1", "vr_q2", "vr_q3", "vr_q4"])
    C["zq"] = pd.qcut(C["z"], 4, labels=["z_q1", "z_q2", "z_q3", "z_q4"])
    C["session"] = pd.cut(C["hour"], [-1, 7, 15, 23], labels=["asia", "europe", "us"])
    for k in ["trend30", "trend7", "volq", "vrq", "zq", "session"]:
        out[f"cases_by_{k}"] = pd.concat({h: C.groupby(k).apply(lambda g: summ(g, f"x{h}")) for h in ["x2", "x6"]}, axis=1)
    # volume ratio quartile within z quartile top only
    top = C[C["zq"] == "z_q4"]
    out["topz_by_vrq_x6"] = top.groupby("vrq").apply(lambda g: summ(g, "x6"))
    # down surges, signed (reversal check), by trend30
    A["absz"] = A["z"].abs()
    E = A.dropna(subset=["z", "vr"])
    E = E.loc[E.groupby(["coin", "win", "cell"])["absz"].idxmax()]
    dn = E[(E["z"] <= -3) & (E["vr"] >= 1.5)].copy()
    dn["trend30"] = np.where(dn["tr30"] > 0, "up30", "down30")
    out["down_surge_raw_excess_by_trend30"] = pd.concat({h: dn.groupby("trend30").apply(lambda g: summ(g, f"x{h}")) for h in ["x2", "x6"]}, axis=1)
    return out
