def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20, min_periods=15).std()
            z = r / sd
            df = pd.DataFrame({
                "coin": coin, "w": w,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "falling": (b["regime"] != "chop").values,
                "fc": b["debug_info.components.fade_move.post_pipeline_value"].astype(float),
                "z": z, "r1": c.shift(-1) / c - 1, "r2": c.shift(-2) / c - 1, "r3": c.shift(-3) / c - 1,
                "r5": c.shift(-5) / c - 1, "sd": sd,
                "ret60": c / c.shift(60) - 1, "sd30": r.rolling(30).std(),
            })
            df["pos"] = np.arange(len(df))
            df["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    means = d.groupby("coin")["r1"].mean()
    d["ex1"] = d["r1"] - d["coin"].map(means)
    for h in [2, 3, 5]:
        mh = d[d.pos % h == 0].groupby("coin")[f"r{h}"].mean()
        d[f"ex{h}"] = d[f"r{h}"] - d["coin"].map(mh)
    out = {}

    def tday(sub, col):
        s = sub.dropna(subset=[col]).groupby("day")[col].sum()
        if len(s) < 3:
            return (np.nan, len(s))
        return (s.mean() / (s.std() / np.sqrt(len(s))), len(s))

    # main measure analog, falling vs not falling (fade signal = -z)
    res = []
    for name, sub in [("falling", d[d.falling]), ("notfalling", d[~d.falling]), ("all", d)]:
        for h in [1, 2, 3, 5]:
            s = sub[sub.pos % h == 0].copy()
            s["v"] = -s["z"].clip(-4, 4) * s[f"ex{h}"]
            t, n = tday(s, "v")
            res.append({"set": name, "h": h, "mean_v": s["v"].mean(), "t_day": t, "days": n})
    out["fade_score_by_set_horizon"] = pd.DataFrame(res)

    f = d[d.falling].dropna(subset=["z", "ex1"]).copy()
    f["side"] = np.where(f.z > 0, "after_up", "after_down")
    f["dirmove"] = np.where(f.z > 0, -f.ex1, f.ex1)
    f["zq"] = pd.qcut(f.z, 10, labels=False)
    g = f.groupby("zq").agg(z=("z", "mean"), ex1=("ex1", "mean"), n=("ex1", "size"),
                            t=("ex1", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    out["falling_next_excess_by_z_decile"] = g
    out["falling_by_side"] = f.groupby("side").agg(dirmove=("dirmove", "mean"), n=("dirmove", "size"),
        t=("dirmove", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    f["absq"] = pd.qcut(f.z.abs(), 5, labels=False)
    out["falling_dirmove_by_absz_side"] = f.groupby(["side", "absq"]).agg(absz=("z", lambda x: x.abs().mean()),
        dirmove=("dirmove", "mean"), n=("dirmove", "size"),
        t=("dirmove", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    f["v"] = -f.z.clip(-4, 4) * f.ex1
    out["falling_v_by_coin"] = f.groupby("coin").agg(v=("v", "mean"), n=("v", "size"),
        t=("v", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    out["falling_v_by_window"] = f.groupby("w").agg(v=("v", "mean"), n=("v", "size"),
        t=("v", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    # agitation within falling: sd30 vs coin's median sd30 over visible data (proxy)
    med = d.groupby("coin")["sd30"].median()
    f["agit"] = np.where(f["sd30"] > f["coin"].map(med), "agitated", "calm")
    f["depth"] = pd.qcut(f["ret60"], 3, labels=["deep", "mid", "shallow"])
    for col in ["agit", "depth"]:
        out[f"falling_v_by_{col}"] = f.groupby([col, "side"]).agg(dirmove=("dirmove", "mean"),
            n=("dirmove", "size"), t=("dirmove", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    # forecast-based main measure on visible folds
    fm = d[d.fc.notna() & (d.fc != 0)].copy()
    fm["v"] = fm.fc * fm.ex1
    out["main_measure_visible"] = pd.Series({"t_day": tday(fm, "v")[0], "days": tday(fm, "v")[1],
        "corr_fc_negz": fm[["fc", "z"]].corr().iloc[0, 1]})
    return out
