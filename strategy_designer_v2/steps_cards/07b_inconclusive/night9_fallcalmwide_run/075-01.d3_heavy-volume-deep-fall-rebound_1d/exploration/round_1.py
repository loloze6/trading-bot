import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    coin_mean = {}
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            rs.append(pd.Series(c).pct_change().dropna())
        coin_mean[coin] = pd.concat(rs).mean()
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            v = b["volume"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            vr = v / v.rolling(20, min_periods=10).mean()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "fc": b["forecast"].astype(float),
                "r": r, "z": r / sd30, "vr": vr,
                "tr60": c / c.shift(60) - 1,
                "n1": c.shift(-1) / c - 1,
                "n2": c.shift(-2) / c - 1,
                "n3": c.shift(-3) / c - 1,
                "n5": c.shift(-5) / c - 1,
            })
            df["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            m = coin_mean[coin]
            for h in [1, 2, 3, 5]:
                df["x%d" % h] = df["n%d" % h] - h * m
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    a = d[(d.fc > 0) & d.x1.notna()].copy()

    def clus(g, col="x1", wcol="fc"):
        g = g.dropna(subset=[col])
        w = g[wcol]; mu = (g[col] * w).sum() / w.sum()
        s = (w * (g[col] - mu)).groupby(g["day"]).sum()
        D = len(s)
        se = np.sqrt((s ** 2).sum() * D / max(D - 1, 1)) / w.sum()
        return pd.Series({"n": len(g), "days": D, "wmean": mu, "t": mu / se if se > 0 else np.nan,
                          "mean": g[col].mean()})

    out = {}
    out["all_BC"] = clus(a).to_frame().T
    out["by_coin"] = a.groupby("coin").apply(clus)
    out["by_win"] = a.groupby("win").apply(clus)
    out["by_year"] = a.groupby("year").apply(clus)
    a["fcq"] = pd.qcut(a.fc.rank(method="first"), 5, labels=False)
    out["by_fc_quint"] = a.groupby("fcq").apply(clus)
    a["vrq"] = pd.qcut(a.vr.rank(method="first"), 5, labels=False)
    out["by_volratio_quint"] = a.groupby("vrq").apply(clus)
    a["zq"] = pd.qcut(a.z.rank(method="first"), 5, labels=False)
    out["by_fall_quint(0=deepest)"] = a.groupby("zq").apply(clus)
    a["trend"] = np.where(a.tr60 > 0.1, "rising", np.where(a.tr60 < -0.1, "falling", np.where(a.tr60.notna(), "choppy", "na")))
    out["by_trend"] = a.groupby("trend").apply(clus)
    hz = {}
    for h in [1, 2, 3, 5]:
        hz["h%d" % h] = clus(a, "x%d" % h)
    out["horizons"] = pd.DataFrame(hz).T
    # all down days (unweighted), graded by vr and z separately
    dn = d[(d.r < 0) & d.x1.notna() & d.vr.notna() & d.z.notna()]
    out["downday_corr"] = pd.Series({
        "n": len(dn),
        "spearman_vr_x1": stats.spearmanr(dn.vr, dn.x1)[0],
        "spearman_negz_x1": stats.spearmanr(-dn.z, dn.x1)[0],
        "spearman_prod_x1": stats.spearmanr(-dn.z * dn.vr, dn.x1)[0],
    })
    return out
