def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            h, l, c, o = b["high"], b["low"], b["close"], b["open"]
            rng = (h - l)
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "rm": rng / rng.rolling(20).mean(),
                "cl": (c - l) / rng.replace(0, np.nan),
                "r0": c / c.shift(1) - 1,
                "r5": c / c.shift(5) - 1,
                "tr60": c / c.shift(60) - 1,
                "nxt": c.shift(-1) / c - 1,
                "nxt3": c.shift(-3) / c - 1,
                "agit": (b["regime"] != "chop").astype(int),
                "regime": b["regime"],
                "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
            })
            df["vol20"] = df["r0"].rolling(20).std()
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    d["u"] = d["nxt"] - d["coin"].map(drift)
    d["uz"] = d["u"] / d["vol20"]

    def tstat(sub, col="u"):
        sub = sub.dropna(subset=[col])
        if len(sub) < 10:
            return pd.Series({"n": len(sub), "mean": np.nan, "t": np.nan})
        m = sub[col].mean()
        dev = (sub[col] - m).groupby(sub["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev**2).sum() * D / (D - 1)) / len(sub)
        return pd.Series({"n": len(sub), "days": D, "mean": m, "t": m / se})

    out = {}
    d["clq"] = pd.cut(d["cl"], [0, .2, .4, .6, .8, 1.0001], include_lowest=True, labels=["c1","c2","c3","c4","c5"])
    d["rmq"] = pd.cut(d["rm"], [0, .8, 1.2, 1.7, 99], labels=["narrow","norm","wide","vwide"])
    out["agit_cl_rm"] = d[d.agit==1].groupby(["rmq","clq"]).apply(tstat).unstack(0)["t"]
    out["agit_cl_rm_mean"] = d[d.agit==1].groupby(["rmq","clq"]).apply(tstat).unstack(0)["mean"]
    out["calm_cl_rm_t"] = d[d.agit==0].groupby(["rmq","clq"]).apply(tstat).unstack(0)["t"]
    d["trend"] = np.where(d.tr60 > .1, "rising", np.where(d.tr60 < -.1, "falling", "choppy"))
    d.loc[d.tr60.isna(), "trend"] = "na"
    d["r0q"] = pd.qcut(d["r0"] / d["vol20"], 5, labels=["q1","q2","q3","q4","q5"])
    out["r0z_by_trend_agit"] = d.groupby(["trend","agit","r0q"]).apply(tstat)[["n","mean","t"]].unstack(2)["t"]
    d["r5q"] = pd.qcut(d["r5"] / (d["vol20"]*np.sqrt(5)), 5, labels=["q1","q2","q3","q4","q5"])
    out["r5z_by_agit"] = d.groupby(["agit","r5q"]).apply(tstat)[["mean","t"]].unstack(0)
    out["weekday"] = d.groupby("wd").apply(tstat)
    out["weekday_agit"] = d.groupby(["agit","wd"]).apply(tstat)["t"].unstack(0)
    out["trend_agit_all"] = d.groupby(["trend","agit"]).apply(tstat)
    # correlation of regime features with next
    a = d[(d.agit==1)].dropna(subset=["rm","cl","u"])
    out["corr_agit"] = pd.Series({"rm*cl": a["u"].corr(a.rm*a.cl), "cl": a["u"].corr(a.cl), "rm": a["u"].corr(a.rm), "r0z": a["u"].corr(a.r0/a.vol20)})
    # book by window
    bk = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            bk.append(x.assign(coin=coin, win=w))
    bk = pd.concat(bk)
    out["book_by_win"] = bk.groupby("win")[["book_return","coin_return"]].mean()
    return out
