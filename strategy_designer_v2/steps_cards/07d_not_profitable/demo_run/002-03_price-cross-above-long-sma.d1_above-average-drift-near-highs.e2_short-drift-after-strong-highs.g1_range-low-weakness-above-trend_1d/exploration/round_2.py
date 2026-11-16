def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    mus = {}
    for coin in data["days"]:
        dd = pd.concat(list(data["days"][coin].values()))
        mus[coin] = dd["coin_return"].mean()
        for w, b in data["bars"][coin].items():
            b = b.copy()
            c = b["close"]
            b["pos"] = b["postRebalance_current_allocation"]
            b["ret1"] = c.shift(-1) / c - 1
            b["gain"] = b["pos"] * b["ret1"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["net"] = b["gain"] - b["fee"].shift(-1).fillna(0)
            b["r60"] = c / c.shift(60) - 1
            b["r30"] = c / c.shift(30) - 1
            lo = c.rolling(20).min(); hi = c.rolling(20).max()
            b["rp"] = (c - lo) / (hi - lo)
            b["fwd5"] = c.shift(-5) / c - 1
            b["mu"] = mus[coin]
            b["coin"] = coin; b["window"] = w
            b["grid"] = (np.arange(len(b)) % 5) == 0
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    s = B[B.pos < 0].copy()
    s["r60b"] = pd.cut(s["r60"], [-1, 0, 0.13, 0.4, 100])
    agg = s.groupby("r60b").agg(n=("gain", "size"), gain=("gain", "mean"), net=("net", "mean"),
                                drift=("pos", lambda x: (x * s.loc[x.index, "mu"]).mean()),
                                pos=("pos", "mean"))
    out["short_bars_by_r60"] = agg
    t = s.groupby("r60b")["gain"].apply(lambda x: x.mean() / x.std() * np.sqrt(len(x)))
    out["t_gain_by_r60"] = t
    out["fee_on_short_or_change_bars_sum_share"] = float(B["fee"].sum() / B["gain"].sum())
    out["sum_gain"] = float(B["gain"].sum()); out["sum_fee"] = float(B["fee"].sum())
    g = B[B.grid & (B.regime == "trending")].copy()
    g["ex5"] = g["fwd5"] - 5 * g["mu"]
    g["rpb"] = pd.cut(g["rp"], [-0.01, 0.1, 0.25, 0.5, 1.01])
    g["r60s"] = np.where(g["r60"] <= 0.13, "low", "high")
    out["ex5_by_r60_rp"] = g.groupby(["r60s", "rpb"])["ex5"].agg(["mean", "count"])
    out["fwd5_by_r60_rp"] = g.groupby(["r60s", "rpb"])["fwd5"].agg(["mean", "count"])
    # graded within low r60: corr of r60 and fwd5 among short grid
    sg = g[g.forecast < 0].dropna(subset=["r60", "fwd5"])
    r, p = stats.spearmanr(sg["r60"], sg["fwd5"])
    out["spearman_r60_fwd5_short_grid"] = f"{r:.3f} p={p:.4f} n={len(sg)}"
    out["share_short_bars_r60_gt_013"] = float((s["r60"] > 0.13).mean())
    return out
