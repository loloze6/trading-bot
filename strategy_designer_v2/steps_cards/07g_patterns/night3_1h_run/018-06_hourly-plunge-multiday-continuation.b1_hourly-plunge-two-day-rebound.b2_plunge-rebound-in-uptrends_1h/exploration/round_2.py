def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            if len(c) < 900: continue
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=360).mean()
            z = r24 / mabs
            r30 = c / c.shift(720) - 1
            for h in (6, 12, 24, 48):
                idx = np.arange(0, len(c) - h, h)
                fr = (c.shift(-h) / c - 1).iloc[idx]
                rows.append(pd.DataFrame({"coin": coin, "win": w, "h": h, "fwd": fr.values,
                    "z": z.iloc[idx].values, "r30": r30.iloc[idx].values,
                    "year": ts.iloc[idx].dt.year.values, "wd": ts.iloc[idx].dt.weekday.values}))
    A = pd.concat(rows, ignore_index=True)
    A["unus"] = A["fwd"] - A.groupby(["coin", "h"])["fwd"].transform("mean")
    A = A.dropna(subset=["z", "r30", "unus"])
    def summ(g):
        x = g["unus"]
        return pd.Series({"n": len(x), "mean_bps": x.mean() * 1e4,
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    # fall rebound by horizon, graded
    A["zb"] = pd.cut(A["z"], [-np.inf, -4, -3, -2, -1, np.inf])
    out["fall_by_h"] = A[A.z < -1].groupby(["h", "zb"], observed=True).apply(summ).round(2)
    S = A[(A.h == 24) & (A.z <= -2.5)]
    out["fall24_by_coin"] = S.groupby("coin").apply(summ).round(2)
    out["fall24_by_year"] = S.groupby("year").apply(summ).round(2)
    S2 = A[(A.h == 24) & (A.z < 0)]
    rho, p = stats.spearmanr(-S2["z"], S2["unus"])
    out["spearman_fall_depth_vs_next24"] = f"rho {rho:.3f} p {p:.2g} n {len(S2)}"
    # rally fade in downtrend
    D = A[(A.h == 24) & (A.r30 < 0) & (A.z >= 1)]
    out["downrally24_by_coin"] = D.groupby("coin").apply(summ).round(2)
    out["downrally24_by_year"] = D.groupby("year").apply(summ).round(2)
    D2 = A[(A.h == 24) & (A.r30 < 0) & (A.z > 0)]
    rho, p = stats.spearmanr(D2["z"], D2["unus"])
    out["spearman_downrally_vs_next24"] = f"rho {rho:.3f} p {p:.2g} n {len(D2)}"
    U2 = A[(A.h == 24) & (A.r30 > 0) & (A.z > 0)]
    rho, p = stats.spearmanr(U2["z"], U2["unus"])
    out["spearman_uprally_vs_next24"] = f"rho {rho:.3f} p {p:.2g} n {len(U2)}"
    D3 = A[(A.r30 < 0) & (A.z >= 1)]
    out["downrally_by_h"] = D3.groupby("h").apply(summ).round(2)
    # weekday by coin/year
    W = A[A.h == 24]
    out["wd_fri_thu_by_year"] = W[W.wd.isin([3, 4])].groupby(["year", "wd"]).apply(summ).round(2)
    return out
