def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20).std().shift(1)
            z = r / vol
            vr = v / v.rolling(30).mean().shift(1)
            vr_inc = v / v.rolling(30).mean()
            fwd = c.shift(-5) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "z": z, "vr": vr, "vri": vr_inc, "fwd": fwd,
                               "fc": b["forecast"].astype(float), "pos": np.arange(len(b))})
            grid = fwd.iloc[::5]
            df["coinmean_part"] = np.nan
            rows.append((df, grid))
    all_df = pd.concat([d for d, g in rows])
    gridall = pd.concat([g for d, g in rows]).dropna()
    cm = pd.concat([g.to_frame("f").assign(coin=d["coin"].iloc[0]) for d, g in rows]).dropna().groupby("coin")["f"].mean()
    all_df["ex"] = all_df["fwd"] - all_df["coin"].map(cm)
    out = {}
    out["n bars"] = len(all_df)
    out["forecast>0 bars"] = int((all_df["fc"] > 0).sum())
    out["share z<=-2"] = float((all_df["z"] <= -2).mean())
    out["share vr<=0.5 (incl)"] = float((all_df["vri"] <= 0.5).mean())
    out["share vr<=0.5 (prior avg)"] = float((all_df["vr"] <= 0.5).mean())
    falls = all_df[all_df["z"] <= -1].dropna(subset=["ex", "vri"]).copy()
    out["vri quantiles on z<=-2"] = all_df.loc[all_df["z"] <= -2, "vri"].describe()
    # dedupe: keep events >=5 bars apart within coin/window
    def dedupe(d):
        keep = []; last = -10
        for p in d["pos"]:
            keep.append(p - last >= 5)
            if keep[-1]: last = p
        return d[keep]
    def table(d, col):
        d = d.sort_values(["coin", "w", "pos"])
        d = d.groupby(["coin", "w"], group_keys=False).apply(dedupe)
        d["q"] = pd.qcut(d[col], 4, labels=False, duplicates="drop")
        g = d.groupby("q")["ex"].agg(["count", "mean", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g[col + "_mean"] = d.groupby("q")[col].mean()
        return g, d
    g1, d1 = table(falls, "vri")
    out["falls z<=-1 by vol ratio quartile (excess 5d)"] = g1
    g2, d2 = table(all_df[all_df["z"] <= -2].dropna(subset=["ex", "vri"]), "vri")
    out["falls z<=-2 by vol ratio quartile"] = g2
    d1b = d1.dropna(subset=["vri", "z"])
    s = stats.linregress(d1b["vri"], d1b["ex"])
    out["slope ex on vri (z<=-1)"] = f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(d1b)}"
    s2 = stats.linregress(d1b["z"], d1b["ex"])
    out["slope ex on z (z<=-1)"] = f"slope {s2.slope:.4f} t {s2.slope/s2.stderr:.2f}"
    # all bars: volume ratio below 1 on down days, quartile of z
    dd = all_df[all_df["z"] < 0].dropna(subset=["ex", "vri"])
    dd = dd.sort_values(["coin","w","pos"]).groupby(["coin","w"], group_keys=False).apply(dedupe)
    dd["thin"] = dd["vri"] < 1
    dd["zq"] = pd.qcut(dd["z"], 4, labels=False)
    g3 = dd.groupby(["zq", "thin"])["ex"].agg(["count", "mean", "std"])
    g3["t"] = g3["mean"] / (g3["std"] / np.sqrt(g3["count"]))
    out["down days: z quartile x thin"] = g3
    return out
