def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    allb = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy().reset_index(drop=True)
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["alloc"] = b["postRebalance_current_allocation"].fillna(0)
            b["gain"] = b["alloc"] * b["ret1"]
            b["bv_ret"] = b["postRebalance_total_value"].shift(-1) / b["postRebalance_total_value"] - 1
            b["r20past"] = b["close"] / b["close"].shift(20) - 1
            b["r60past"] = b["close"] / b["close"].shift(60) - 1
            b["coin"] = coin; b["w"] = w; b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["fc"] = b["forecast"].fillna(0)
            allb.append(b)
    B = pd.concat(allb, ignore_index=True)
    B = B.dropna(subset=["ret1"])
    B["inmkt"] = (B["alloc"].abs() > 1e-9).astype(int)
    g = B.groupby("coin")
    out["by_coin"] = pd.DataFrame({
        "mean_bookret_bps": g["bv_ret"].mean() * 1e4,
        "mean_gain_bps": g["gain"].mean() * 1e4,
        "coin_drift_bps": g["ret1"].mean() * 1e4,
        "time_in_mkt": g["inmkt"].mean(),
        "mean_alloc": g["alloc"].mean(),
        "drift_part_bps": g["alloc"].mean() * g["ret1"].mean() * 1e4,
        "ret_when_in_bps": B[B.inmkt == 1].groupby("coin")["ret1"].mean() * 1e4,
        "ret_when_out_bps": B[B.inmkt == 0].groupby("coin")["ret1"].mean() * 1e4,
    })
    gy = B.groupby("year")
    out["by_year"] = pd.DataFrame({"gain_bps": gy["gain"].mean() * 1e4, "coin_bps": gy["ret1"].mean() * 1e4,
                                   "in_mkt": gy["inmkt"].mean(), "sum_gain": gy["gain"].sum(), "n": gy.size()})
    gw = B.groupby("w")
    out["by_window"] = pd.DataFrame({"sum_gain": gw["gain"].sum(), "coin_mean_bps": gw["ret1"].mean() * 1e4,
                                     "in_mkt": gw["inmkt"].mean()})
    # forecast buckets among in-market
    I = B[B.inmkt == 1].copy()
    I["fcq"] = pd.qcut(I["fc"].rank(method="first"), 5, labels=False)
    gq = I.groupby("fcq")
    out["fc_quintile_in_mkt"] = pd.DataFrame({"fc_mean": gq["fc"].mean(), "ret1_bps": gq["ret1"].mean() * 1e4,
                                               "alloc": gq["alloc"].mean(), "gain_bps": gq["gain"].mean() * 1e4, "n": gq.size()})
    # market state: past 60d coin return bucket
    B2 = B.dropna(subset=["r60past"]).copy()
    B2["st"] = pd.cut(B2["r60past"], [-np.inf, -0.2, 0, 0.2, 0.5, np.inf])
    gs = B2.groupby("st", observed=True)
    out["state_r60"] = pd.DataFrame({"share_gain": gs["gain"].sum() / B2["gain"].sum(), "in_mkt": gs["inmkt"].mean(),
                                     "ret_in_bps": B2[B2.inmkt == 1].groupby("st", observed=True)["ret1"].mean() * 1e4,
                                     "ret_all_bps": gs["ret1"].mean() * 1e4, "n": gs.size()})
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()], ignore_index=True)
    p = T["profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "sum_pl": p.sum(), "top10_sum": p.head(10).sum(), "top5pct_sum": p.head(int(len(p) * 0.05)).sum(),
                               "win_rate": (p > 0).mean(), "median": p.median(), "mean_dur_days": T["duration_minutes"].mean() / 1440})
    out["total"] = pd.Series({"gain_bps": B["gain"].mean() * 1e4, "drift_bps": B["ret1"].mean() * 1e4, "mean_alloc": B["alloc"].mean(),
                              "in_mkt": B["inmkt"].mean(), "ret_in_bps": I["ret1"].mean() * 1e4,
                              "ret_out_bps": B[B.inmkt == 0]["ret1"].mean() * 1e4,
                              "t_in_vs_out": __import__("scipy.stats").stats.ttest_ind(I["ret1"], B[B.inmkt == 0]["ret1"], equal_var=False)[0]})
    return out
