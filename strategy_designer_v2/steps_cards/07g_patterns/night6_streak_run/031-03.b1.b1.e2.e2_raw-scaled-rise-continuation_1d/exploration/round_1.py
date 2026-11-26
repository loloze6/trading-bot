import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    H = 5
    rows = []
    drift = {}; usual = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(allr); usual[coin] = np.std(allr, ddof=1)
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"]
            r1 = c.pct_change()
            vol = r1.rolling(60, min_periods=20).std()
            vsr = (c / c.shift(10) - 1) / (vol * np.sqrt(10))
            vsr3 = (c / c.shift(3) - 1) / (vol * np.sqrt(3))
            sgn = np.sign(r1).fillna(0)
            streak = np.zeros(len(d))
            for i in range(1, len(d)):
                if sgn[i] != 0 and sgn[i] == sgn[i-1]:
                    streak[i] = streak[i-1] + sgn[i]
                else:
                    streak[i] = sgn[i]
            fwd = c.shift(-H) / c - 1
            rng = (d["high"] - d["low"]) / c / vol
            vrel = vol / vol.rolling(60, min_periods=20).median()
            volu = d["volume"] / d["volume"].rolling(20, min_periods=10).mean()
            g = d.iloc[::H].copy()
            sel = g.index
            out = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(d.loc[sel, "timestamp"]).dt.floor("D").values,
                "wd": pd.to_datetime(d.loc[sel, "timestamp"]).dt.weekday.values,
                "year": pd.to_datetime(d.loc[sel, "timestamp"]).dt.year.values,
                "vsr": vsr[sel].values, "vsr3": vsr3[sel].values, "r1z": (r1 / vol)[sel].values,
                "streak": streak[sel], "rng": rng[sel].values, "vrel": vrel[sel].values,
                "volu": volu[sel].values,
                "fwd": fwd[sel].values,
            })
            out["unus"] = out["fwd"] - drift[coin]
            out["str"] = out["unus"] / usual[coin]
            rows.append(out)
    A = pd.concat(rows).dropna(subset=["fwd"])

    def ct(sub, col="unus"):
        sub = sub.dropna(subset=[col])
        if len(sub) < 10: return pd.Series({"n": len(sub), "mean": np.nan, "t": np.nan, "days": 0})
        dev = sub[col] - sub[col].mean()
        s = dev.groupby(sub["day"]).sum()
        D = len(s); se = np.sqrt((s**2).sum() * D / (D - 1)) / len(sub)
        return pd.Series({"n": len(sub), "mean": sub[col].mean(), "t": sub[col].mean() / se, "days": D,
                          "strength": sub["str"].mean()})

    res = {}
    A2 = A.dropna(subset=["vsr"])
    res["by_vsr_bin"] = A2.groupby(pd.cut(A2["vsr"], [-99, -2, -1, -0.5, 0, 0.5, 1, 2, 3, 99])).apply(ct)
    res["by_vsr3_bin"] = A2.groupby(pd.cut(A2["vsr3"], [-99, -2, -1, 0, 1, 2, 99])).apply(ct)
    res["by_r1z_bin"] = A2.groupby(pd.cut(A2["r1z"], [-99, -2, -1, 0, 1, 2, 99])).apply(ct)
    res["by_streak"] = A.groupby(A["streak"].clip(-5, 5)).apply(ct)
    res["by_volrel"] = A2.groupby(pd.qcut(A2["vrel"], 5)).apply(ct)
    res["by_volume_surge"] = A2.groupby(pd.qcut(A2["volu"], 5)).apply(ct)
    res["by_range"] = A2.groupby(pd.qcut(A2["rng"], 5)).apply(ct)
    res["by_weekday"] = A.groupby("wd").apply(ct)
    res["by_year"] = A.groupby("year").apply(ct)
    hi = A2[A2["vsr"] >= 2]
    res["vsr>=2_by_volu"] = hi.groupby(pd.qcut(hi["volu"], 3)).apply(ct)
    res["vsr>=2_by_vrel"] = hi.groupby(pd.qcut(hi["vrel"], 3)).apply(ct)
    lo = A2[A2["vsr"] <= -2]
    res["vsr<=-2_by_volu"] = lo.groupby(pd.qcut(lo["volu"], 3)).apply(ct)
    res["vsr>=2_by_year"] = hi.groupby("year").apply(ct)
    res["vsr>=2_by_coin"] = hi.groupby("coin").apply(ct)
    return res
