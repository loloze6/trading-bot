import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            r5 = c / c.shift(5) - 1
            r10 = c / c.shift(10) - 1
            r20 = c / c.shift(20) - 1
            vol20 = r1.rolling(20).std()
            vol120 = r1.rolling(120, min_periods=60).std()
            f5 = c.shift(-5) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            idx = np.arange(0, len(df), 5)
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "r5": r5.values[idx], "r10": r10.values[idx], "r20": r20.values[idx],
                "vr": (vol20 / vol120).values[idx], "f5": f5.values[idx], "fc": df["forecast"].values[idx],
                "year": ts.dt.year.values[idx], "dkey": ts.dt.floor("D").values[idx].astype("int64"),
            }))
    g = pd.concat(rows, ignore_index=True).dropna(subset=["f5", "r5", "r20"])
    g["ex"] = g.f5 - g.groupby("coin")["f5"].transform("mean")
    g["z"] = g.ex / g.groupby("coin")["f5"].transform("std")
    for k in ["r5", "r10", "r20"]:
        g[k + "s"] = g[k] / g.groupby("coin")[k].transform("std")
    out = {}
    def clus(s, key):
        m = s.groupby(key).mean()
        return f"mean {m.mean():.4f} t_dates {m.mean()/(m.std()/np.sqrt(len(m))):.2f} n_dates {len(m)} n {len(s)}"
    dn = g[g.r20 < 0].copy()
    dn["p"] = (dn.r5s - dn.r5s.mean()) * dn.z
    out["down20_r5_prod_clustered"] = clus(dn.p, dn.dkey)
    up = g[g.r20 >= 0].copy()
    up["p"] = (up.r5s - up.r5s.mean()) * up.z
    out["up20_r5_prod_clustered"] = clus(up.p, up.dkey)
    allg = g.copy(); allg["p"] = (allg.r5s - allg.r5s.mean()) * allg.z
    out["all_r5_prod_clustered"] = clus(allg.p, allg.dkey)
    dn["q"] = pd.qcut(dn.r5s.rank(method="first"), 5, labels=False)
    a = dn.groupby("q")["z"].agg(["mean", "count", "std"]); a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    a["ex_pct"] = dn.groupby("q")["ex"].mean() * 100
    out["down20_by_r5_quintile"] = a.drop(columns="std")
    act = g[g.fc < 0].copy()
    out["active_z_clustered"] = clus(act.z, act.dkey)
    out["active_z_clustered_ex2025"] = clus(act[act.year != 2025].z, act[act.year != 2025].dkey)
    act["p"] = (-act.fc / 10) * act.ex
    out["main_prod_clustered"] = clus(act.p, act.dkey)
    out["main_prod_clustered_ex2025"] = clus(act[act.year != 2025].p, act[act.year != 2025].dkey)
    b = g[(g.r20 < 0) & (g.r5 > 0)].copy()
    b = b.dropna(subset=["vr"])
    b["vq"] = pd.qcut(b.vr.rank(method="first"), 3, labels=False)
    out["bounce_by_volratio_tercile_active"] = b.groupby(["vq", b.fc < 0])["z"].agg(["mean", "count"])
    dn["r10q"] = pd.qcut(dn.r10s.rank(method="first"), 5, labels=False)
    out["down20_by_r10_quintile"] = dn.groupby("r10q")["z"].agg(["mean", "count"])
    return out
