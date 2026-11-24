import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    res = {}
    def ct(sub, col, scol):
        sub = sub.dropna(subset=[col])
        if len(sub) < 10: return pd.Series({"n": len(sub), "mean": np.nan, "t": np.nan, "days": 0, "strength": np.nan})
        dev = sub[col] - sub[col].mean()
        s = dev.groupby(sub["day"]).sum(); D = len(s)
        se = np.sqrt((s**2).sum() * D / (D - 1)) / len(sub)
        return pd.Series({"n": len(sub), "mean": sub[col].mean(), "t": sub[col].mean() / se,
                          "days": D, "strength": sub[scol].mean()})
    def slope(sub, x, y):
        sub = sub.dropna(subset=[x, y]).copy()
        X = sub[x] - sub[x].mean(); b = (X * sub[y]).sum() / (X**2).sum()
        e = sub[y] - sub[y].mean() - b * X
        s = (X * e).groupby(sub["day"]).sum(); D = len(s)
        se = np.sqrt((s**2).sum() * D / (D - 1)) / (X**2).sum()
        return pd.Series({"n": len(sub), "days": D, "slope": b, "t": b / se})
    for H in [5, 10, 20]:
        rows = []
        for coin, wins in bars.items():
            allr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                allr += list(c[idx + H] / c[idx] - 1)
            drift = np.mean(allr); usual = np.std(allr, ddof=1)
            for w, df in wins.items():
                d = df.reset_index(drop=True)
                c = d["close"]; r1 = c.pct_change()
                vol = r1.rolling(60, min_periods=20).std()
                vsr = (c / c.shift(10) - 1) / (vol * np.sqrt(10))
                v = d["volume"]; volu = v / v.rolling(20, min_periods=10).mean()
                fwd = c.shift(-H) / c - 1
                sel = d.index[::H]
                out = pd.DataFrame({"coin": coin,
                    "day": pd.to_datetime(d.loc[sel, "timestamp"]).dt.floor("D").values,
                    "year": pd.to_datetime(d.loc[sel, "timestamp"]).dt.year.values,
                    "vsr": vsr[sel].values, "lv": np.log(volu[sel].values), "fwd": fwd[sel].values})
                out["unus"] = out["fwd"] - drift; out["str"] = out["unus"] / usual
                rows.append(out)
        A = pd.concat(rows).dropna(subset=["fwd", "vsr"])
        res[f"H{H}_by_vsr"] = A.groupby(pd.cut(A["vsr"], [-99, -2, -1, 0, 1, 2, 3, 99])).apply(lambda s: ct(s, "unus", "str"))
        hi = A[A["vsr"] >= 1].dropna(subset=["lv"])
        res[f"H{H}_slope_str_on_logvol_vsr>=1"] = slope(hi, "lv", "str")
        if H == 5:
            h2 = A[A["vsr"] >= 2].dropna(subset=["lv"])
            res["H5_slope_str_on_logvol_vsr>=2"] = slope(h2, "lv", "str")
            hi = hi.copy(); hi["half"] = np.where(hi["year"] <= 2021, "2018-2021", "2022-2025")
            res["H5_vsr>=1_logvol_slope_by_half"] = pd.DataFrame({k: slope(g, "lv", "str") for k, g in hi.groupby("half")}).T
    return res
