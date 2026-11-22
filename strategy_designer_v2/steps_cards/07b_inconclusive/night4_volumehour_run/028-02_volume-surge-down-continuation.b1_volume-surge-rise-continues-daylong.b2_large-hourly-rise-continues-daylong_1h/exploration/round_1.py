def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [2, 6, 24]
    rows = []
    drift = {}
    for coin in bars:
        for h in H:
            rs = []
            for w, df in bars[coin].items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs)
            drift[(coin, h)] = (rs.mean(), rs.std())
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"]; v = df["volume"]
            r1 = c.pct_change()
            mabs = r1.abs().rolling(720, min_periods=720).mean()
            z = r1 / mabs
            vr = v / v.shift(1).rolling(720, min_periods=720).mean()
            yr = pd.to_datetime(df["timestamp"]).dt.year
            fc = df["forecast"].fillna(0)
            for h in H:
                fwd = c.shift(-h) / c - 1
                ex = fwd - drift[(coin, h)][0]
                cell = np.arange(len(df)) // h
                d = pd.DataFrame({"z": z, "vr": vr, "ex": ex, "fwd": fwd, "cell": cell,
                                  "yr": yr, "fc": fc, "w": w, "coin": coin, "h": h,
                                  "usual": drift[(coin, h)][1]})
                d = d.dropna(subset=["z", "vr", "ex"])
                d = d[d["z"].abs() >= 3]
                d["side"] = np.where(d["z"] > 0, "up", "down")
                d["vol"] = pd.cut(d["vr"], [0, 1, 3, np.inf], labels=["<1", "1-3", ">=3"])
                d["zb"] = pd.cut(d["z"].abs(), [3, 5, 8, np.inf], labels=["3-5", "5-8", ">=8"], include_lowest=True)
                d = d.groupby(["side", "vol", "cell"], observed=True).head(1)
                rows.append(d)
    A = pd.concat(rows)
    A["dirx"] = np.where(A["side"] == "up", A["ex"], -A["ex"])
    def agg(g):
        x = g["dirx"]
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "strength": (x / g["usual"]).mean()})
    out = {}
    out["by_h_side_vol"] = A.groupby(["h", "side", "vol"], observed=True).apply(agg)
    B = A[A["h"].isin([6, 24])]
    out["by_h_side_vol_zb"] = B.groupby(["h", "side", "vol", "zb"], observed=True).apply(agg)
    out["by_coin_h_side_highvol"] = A[A["vol"] != "<1"].groupby(["coin", "h", "side"]).apply(agg)
    out["by_year_h24_up_highvol"] = A[(A["vol"] != "<1") & (A["h"] == 24) & (A["side"] == "up")].groupby("yr").apply(agg)
    out["by_year_h6_up_highvol"] = A[(A["vol"] != "<1") & (A["h"] == 6) & (A["side"] == "up")].groupby("yr").apply(agg)
    return out
