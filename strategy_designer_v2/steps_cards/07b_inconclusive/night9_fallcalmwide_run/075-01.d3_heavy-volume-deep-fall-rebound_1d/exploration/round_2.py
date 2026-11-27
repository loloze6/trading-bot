import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    coin_mean = {}
    for coin, wins in data["bars"].items():
        rs = [pd.Series(b["close"].astype(float).values).pct_change().dropna() for w, b in wins.items()]
        coin_mean[coin] = pd.concat(rs).mean()
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            sdlong = sd30.expanding(min_periods=30).median()
            df = pd.DataFrame({"coin": coin, "win": w, "fc": b["forecast"].astype(float),
                               "r": r, "z": r / sd30, "vr": v / v.rolling(20, min_periods=10).mean(),
                               "agit": (sd30 > sdlong).astype(float).where(sdlong.notna()),
                               "r5": c / c.shift(5) - 1,
                               "x1": c.shift(-1) / c - 1 - coin_mean[coin]})
            df["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)

    def clus(g, col="x1", wcol=None):
        g = g.dropna(subset=[col])
        w = g[wcol] if wcol else pd.Series(1.0, index=g.index)
        mu = (g[col] * w).sum() / w.sum()
        s = (w * (g[col] - mu)).groupby(g["day"]).sum(); D = len(s)
        se = np.sqrt((s ** 2).sum() * D / max(D - 1, 1)) / w.sum()
        return pd.Series({"n": len(g), "days": D, "mean": mu, "t": mu / se if se > 0 else np.nan})

    out = {}
    dn = d[(d.r < 0) & d.x1.notna() & d.vr.notna() & d.z.notna()].copy()
    dn["vt"] = pd.qcut(dn.vr.rank(method="first"), 3, labels=["vlow", "vmid", "vhigh"])
    dn["zt"] = pd.qcut((-dn.z).rank(method="first"), 3, labels=["fshallow", "fmid", "fdeep"])
    out["grid_vol_x_fall"] = dn.groupby(["vt", "zt"]).apply(clus)
    out["by_agitation"] = dn[dn.fc > 0].groupby("agit").apply(lambda g: clus(g, wcol="fc"))
    dn["r5s"] = np.where(dn.r5 < 0, "5d_down", "5d_up")
    out["by_5d_sign"] = dn[dn.fc > 0].groupby("r5s").apply(lambda g: clus(g, wcol="fc"))
    # up days, high volume: does volume alone grade?
    up = d[(d.r > 0) & d.x1.notna() & d.vr.notna()].copy()
    up["vt"] = pd.qcut(up.vr.rank(method="first"), 3, labels=False)
    out["updays_by_vol_tercile"] = up.groupby("vt").apply(clus)
    # top fc quintile by coin
    a = d[(d.fc > 0) & d.x1.notna()].copy()
    a["fcq"] = pd.qcut(a.fc.rank(method="first"), 5, labels=False)
    top = a[a.fcq >= 3]
    out["top2quint_by_win"] = top.groupby("win").apply(clus)
    out["top2quint_pos_coins_share"] = pd.Series({"share_coins_pos": (top.groupby("coin").x1.mean() > 0).mean(),
                                                  "share_wins_pos": (top.groupby("win").x1.mean() > 0).mean()})
    return out
