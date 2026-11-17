def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    parts = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            z = r / r.rolling(20).std().shift(1)
            vri = v / v.rolling(30).mean()
            df = pd.DataFrame({"coin": coin, "w": w, "z": z, "vri": vri,
                               "year": pd.to_datetime(b["timestamp"]).dt.year, "pos": np.arange(len(b))})
            for h in (3, 5, 10):
                df[f"f{h}"] = c.shift(-h) / c - 1
                df[f"g{h}"] = np.where(np.arange(len(b)) % h == 0, df[f"f{h}"], np.nan)
            df["fc"] = b["forecast"].astype(float)
            df["alloc"] = b["postRebalance_current_allocation"].astype(float)
            parts.append(df)
    a = pd.concat(parts)
    out = {}
    for h in (3, 5, 10):
        cm = a.groupby("coin")[f"g{h}"].mean()
        a[f"ex{h}"] = a[f"f{h}"] - a["coin"].map(cm)
    zz = a[a["z"] <= -2]
    out["z<=-2: share vri<=0.5, <=0.8, <1"] = f"{(zz.vri<=0.5).mean():.3f} {(zz.vri<=0.8).mean():.3f} {(zz.vri<1).mean():.3f} n {len(zz)}"
    out["share bars with alloc!=0"] = float((a["alloc"].abs() > 1e-9).mean())
    def dedupe(d, h):
        keep = []; last = -100
        for p in d["pos"]:
            k = p - last >= h; keep.append(k)
            if k: last = p
        return d[keep]
    falls = a[a["z"] <= -1].dropna(subset=["vri"]).sort_values(["coin","w","pos"])
    res = []
    for h in (3, 5, 10):
        d = falls.dropna(subset=[f"ex{h}"]).groupby(["coin","w"], group_keys=False).apply(lambda x: dedupe(x, h))
        d = d.copy(); d["s"] = (-d["z"]) * np.log(d["vri"])
        sl = stats.linregress(d["s"], d[f"ex{h}"])
        sv = stats.linregress(np.log(d["vri"]), d[f"ex{h}"])
        heavy = d[d.vri >= 1.5][f"ex{h}"]; thin = d[d.vri < 1][f"ex{h}"]
        tt = stats.ttest_ind(heavy, thin, equal_var=False)
        res.append({"h_days": h, "n": len(d), "slope_on_-z*logvr": sl.slope, "t1": sl.slope/sl.stderr,
                    "slope_on_logvr": sv.slope, "t2": sv.slope/sv.stderr,
                    "heavy_mean": heavy.mean(), "n_heavy": len(heavy), "thin_mean": thin.mean(), "n_thin": len(thin),
                    "welch_t_heavy_minus_thin": tt.statistic})
    out["falls z<=-1 graded by volume"] = pd.DataFrame(res)
    d = falls.dropna(subset=["ex5"]).groupby(["coin","w"], group_keys=False).apply(lambda x: dedupe(x, 5))
    d = d.copy(); d["heavy"] = d["vri"] >= 1.5
    g = d.groupby(["year","heavy"])["ex5"].agg(["count","mean"]).unstack()
    out["by year ex5 heavy vs not"] = g
    g2 = d.groupby(["coin","heavy"])["ex5"].agg(["count","mean"]).unstack()
    out["by coin ex5 heavy vs not"] = g2
    return out
