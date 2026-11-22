def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std()
            mv = v.rolling(720, min_periods=240).mean()
            zr = r / sd; vr = v / mv
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in (1, 2, 4, 6):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(df), h)
                sub = pd.DataFrame({"coin": coin, "win": w, "h": h, "zr": zr.values[idx], "vr": vr.values[idx],
                                    "fwd": fwd.values[idx], "fc": df["forecast"].values[idx], "year": yr.values[idx]})
                rows.append(sub)
    A = pd.concat(rows).dropna(subset=["zr", "vr", "fwd"])
    A["drift"] = A.groupby(["coin", "h"])["fwd"].transform("mean")
    A["u"] = A["fwd"] - A["drift"]
    def summ(g):
        n = len(g); m = g["u"].mean(); s = g["u"].std()
        return pd.Series({"n": n, "mean_u_bp": m * 1e4, "t": m / (s / np.sqrt(n)) if n > 1 else np.nan})
    A["zbin"] = pd.cut(A["zr"], [-np.inf, -6, -4, -3, -2, 2, 3, 4, 6, np.inf])
    A["vbin"] = pd.cut(A["vr"], [0, 1, 2, 3, 5, np.inf])
    out = {}
    fall = A[A["zr"] <= -3]
    out["falls_z<=-3_by_h_vbin"] = fall.groupby(["h", "vbin"]).apply(summ).reset_index()
    rise = A[A["zr"] >= 3]
    out["rises_z>=3_by_h_vbin"] = rise.groupby(["h", "vbin"]).apply(summ).reset_index()
    hv = A[A["vr"] >= 3]
    out["vr>=3_by_h_zbin"] = hv.groupby(["h", "zbin"]).apply(summ).reset_index()
    act = A[A["fc"] > 0]
    out["fc>0_by_h"] = act.groupby("h").apply(summ).reset_index()
    act["fcb"] = pd.qcut(act["fc"], 5, duplicates="drop")
    out["fc>0_h2_by_fc_quintile"] = act[act["h"] == 2].groupby("fcb").apply(summ).reset_index()
    out["fc>0_h2_by_coin_year"] = act[act["h"] == 2].groupby(["coin", "year"]).apply(summ).reset_index()
    return out
