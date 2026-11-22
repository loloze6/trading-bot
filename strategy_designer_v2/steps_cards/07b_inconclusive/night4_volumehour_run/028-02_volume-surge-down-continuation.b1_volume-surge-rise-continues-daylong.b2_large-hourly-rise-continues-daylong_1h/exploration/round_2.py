def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [6, 24]
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
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"]; v = df["volume"]
            r1 = c.pct_change()
            mabs = r1.abs().rolling(720, min_periods=720).mean()
            z = r1 / mabs
            vr = v / v.shift(1).rolling(720, min_periods=720).mean()
            fc = df["forecast"].fillna(0)
            for h in H:
                fwd = c.shift(-h) / c - 1
                ex = fwd - drift[(coin, h)][0]
                cell = np.arange(len(df)) // h
                d = pd.DataFrame({"z": z, "vr": vr, "ex": ex, "fwd": fwd, "cell": cell, "fc": fc,
                                  "coin": coin, "w": w, "h": h, "usual": drift[(coin, h)][1]})
                d = d.dropna(subset=["z", "vr", "ex"])
                d = d[(d["z"] >= 3) & (d["vr"] >= 1)]
                d = d.sort_values("vr", ascending=False).groupby("cell").head(1)
                rows.append(d)
    A = pd.concat(rows)
    A["vb"] = pd.cut(A["vr"], [1, 2, 3, 5, 8, np.inf], labels=["1-2", "2-3", "3-5", "5-8", ">=8"], include_lowest=True)
    A["zb"] = pd.cut(A["z"], [3, 5, 8, np.inf], labels=["3-5", "5-8", ">=8"], include_lowest=True)
    def agg(g):
        x = g["ex"]
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "total%": 100 * g["fwd"].mean(),
                          "strength": (x / g["usual"]).mean()})
    out = {}
    out["by_h_vb"] = A.groupby(["h", "vb"], observed=True).apply(agg)
    out["by_h_vb_zb"] = A.groupby(["h", "vb", "zb"], observed=True).apply(agg)
    res = {}
    for h in H:
        B = A[A["h"] == h]
        res[f"spearman_ex_vr_h{h}"] = B["ex"].corr(B["vr"], method="spearman")
        res[f"spearman_ex_z_h{h}"] = B["ex"].corr(B["z"], method="spearman")
        C = B[B["vr"] >= 3]
        res[f"spearman_ex_vr_vr3_h{h}"] = C["ex"].corr(np.log(C["vr"]), method="spearman")
    out["corr"] = pd.Series(res)
    out["by_coin_h24_vr3"] = A[(A["h"] == 24) & (A["vr"] >= 3)].groupby("coin").apply(agg)
    out["fc_pos_share_by_vb_h24"] = A[A["h"] == 24].groupby("vb", observed=True)["fc"].apply(lambda s: (s >= 2).mean())
    return out
