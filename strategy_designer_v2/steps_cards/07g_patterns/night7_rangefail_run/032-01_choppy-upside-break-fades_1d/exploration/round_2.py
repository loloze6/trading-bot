def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            ph = hi.shift(1).rolling(20).max(); pl = lo.shift(1).rolling(20).min()
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "ts": ts, "pos": np.arange(len(b)),
                "dh": (c / ph - 1) * 100,
                "rp": (c - pl) / (ph - pl),
                "tr60": c / c.shift(60) - 1,
                "f5": c.shift(-5) / c - 1, "f10": c.shift(-10) / c - 1, "f3": c.shift(-3) / c - 1,
            }))
    d = pd.concat(rows, ignore_index=True)
    out = {}
    def clt(x, col):
        x = x.dropna(subset=[col]); n = len(x)
        if n < 3: return pd.Series({"n": n})
        m = x[col].mean(); ds = (x[col] - m).groupby(x["ts"]).sum()
        se = np.sqrt((ds ** 2).sum()) / n
        return pd.Series({"n": n, "days": ds.size, "mean%": 100 * m, "t_cl": m / se})
    res = {}
    for H, col in [(3, "f3"), (5, "f5"), (10, "f10")]:
        g = d[d["pos"] % H == 0].dropna(subset=[col, "rp"]).copy()
        g["u"] = g[col] - g["coin"].map(g.groupby("coin")[col].mean())
        g["us"] = g["u"] / g["coin"].map(g.groupby("coin")[col].std())
        g["rq"] = pd.cut(g["rp"], [-10, 0, 0.25, 0.5, 0.75, 1.0, 10])
        out[f"by_range_pos_h{H}"] = g.groupby("rq").apply(lambda x: clt(x, "u"))
        sl = stats.linregress(g["rp"].clip(-0.5, 1.5), g["us"])
        res[f"h{H}"] = {"slope_strength_per_rangepos": sl.slope, "t_ols": sl.slope / sl.stderr, "n": len(g)}
        if H == 5:
            g5 = g
    out["slope_rangepos"] = pd.DataFrame(res).T
    # per coin and per window: top quarter of range (rp>0.75) minus bottom quarter (rp<0.25)
    g5 = g5.copy()
    g5["top"] = g5["rp"] > 0.75; g5["bot"] = g5["rp"] < 0.25
    def diff(x):
        a = x.loc[x["top"], "us"]; b = x.loc[x["bot"], "us"]
        return pd.Series({"n_top": len(a), "n_bot": len(b), "top_minus_bot": a.mean() - b.mean()})
    out["coin_top_minus_bot_strength_h5"] = g5.groupby("coin").apply(diff)
    out["win_top_minus_bot_strength_h5"] = g5.groupby("win").apply(diff)
    # top of range by profile where known
    def prof(t):
        if pd.isna(t): return "na"
        return "rising" if t > 0.10 else ("falling" if t < -0.10 else "choppy")
    g5["prof"] = g5["tr60"].map(prof)
    out["top_by_prof_h5"] = g5[g5["top"]].groupby("prof").apply(lambda x: clt(x, "u"))
    out["bot_by_prof_h5"] = g5[g5["bot"]].groupby("prof").apply(lambda x: clt(x, "u"))
    return out
