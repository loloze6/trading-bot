def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True).copy()
            b["coin"] = coin; b["win"] = w
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"].fillna(0)
            b["gain"] = b["pos"] * b["r1"]
            pm = b["close"].shift(1).rolling(20, min_periods=20).max()
            sd = b["close"].pct_change().rolling(20, min_periods=20).std()
            b["dist"] = (b["close"] / pm - 1) / sd
            for h in (1, 5, 10, 20):
                b[f"f{h}"] = b["close"].shift(-h) / b["close"] - 1
            b["pos_in_win"] = np.arange(len(b))
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    cm = B.groupby("coin")["r1"].mean()
    B["mkt"] = B["pos"] * B["coin"].map(cm)
    B["timing"] = B["gain"] - B["mkt"]
    B["date"] = pd.to_datetime(B["timestamp"]).dt.floor("D")
    D = B.groupby("date")[["gain", "mkt", "timing"]].mean()
    out["book_daily_mean_gain_mkt_timing"] = D.mean()
    out["t_timing"] = float(D["timing"].mean() / (D["timing"].std() / np.sqrt(len(D))))
    out["t_gain"] = float(D["gain"].mean() / (D["gain"].std() / np.sqrt(len(D))))
    out["n_days"] = len(D)
    out["share_long_short_flat"] = pd.Series({
        "long": (B["pos"] > 0).mean(), "short": (B["pos"] < 0).mean(), "flat": (B["pos"] == 0).mean(),
        "mean_pos_when_in": B.loc[B["pos"] != 0, "pos"].mean()})
    g = B.groupby("coin").agg(gain_sum=("gain", "sum"), mkt_sum=("mkt", "sum"), timing_sum=("timing", "sum"), n=("gain", "size"))
    out["by_coin"] = g.sort_values("gain_sum")
    out["by_window"] = B.groupby("win").agg(gain_sum=("gain", "sum"), mkt_sum=("mkt", "sum"), timing_sum=("timing", "sum"),
                                           coin_r1_mean=("r1", "mean"), in_pos=("pos", lambda s: (s != 0).mean()))
    out["by_side_gain"] = B.assign(side=np.sign(B["pos"])).groupby("side").agg(gain_sum=("gain", "sum"), timing_sum=("timing", "sum"), n=("gain", "size"))
    # forecast buckets on in-profile bars, 5d grid, drift removed
    A = B[B["regime"] == "unknown"].copy()
    for h in (1, 5, 10, 20):
        dm = B[B["pos_in_win"] % h == 0].groupby("coin")[f"f{h}"].mean()
        A[f"u{h}"] = A[f"f{h}"] - A["coin"].map(dm)
    G5 = A[A["pos_in_win"] % 5 == 0].dropna(subset=["u5", "forecast"])
    G5["fq"] = pd.qcut(G5["forecast"], 5, labels=False, duplicates="drop")
    out["fcst_quintile_u5"] = G5.groupby("fq").agg(fc=("forecast", "mean"), u5=("u5", "mean"), n=("u5", "size"),
                                                  pos=("pos", "mean"))
    Gd = G5.dropna(subset=["dist"]).copy()
    Gd["dq"] = pd.qcut(Gd["dist"], 5, labels=False, duplicates="drop")
    out["dist_quintile_u5"] = Gd.groupby("dq").agg(dist=("dist", "mean"), u5=("u5", "mean"), n=("u5", "size"))
    hz = {}
    for h in (1, 5, 10, 20):
        G = A[A["pos_in_win"] % h == 0].dropna(subset=[f"u{h}", "dist"])
        r, p = stats.pearsonr(G["dist"], G[f"u{h}"])
        top = G[G["dist"] >= G["dist"].quantile(0.8)][f"u{h}"]; bot = G[G["dist"] <= G["dist"].quantile(0.2)][f"u{h}"]
        hz[h] = {"corr": r, "p": p, "n": len(G), "top_minus_bot": top.mean() - bot.mean(),
                 "t_welch": stats.ttest_ind(top, bot, equal_var=False).statistic, "all_mean_u": G[f"u{h}"].mean(),
                 "t_all": G[f"u{h}"].mean() / (G[f"u{h}"].std() / np.sqrt(len(G)))}
    out["horizon_dist_vs_u"] = pd.DataFrame(hz).T
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    pl = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "sum": pl.sum(), "top10_sum": pl.head(10).sum(), "top5pct_sum": pl.head(max(1, len(pl)//20)).sum(),
                               "win_rate": (pl > 0).mean(), "long_share": (T["side"] == "LONG").mean(),
                               "mean_dur_days": T["duration_minutes"].mean() / 1440})
    out["by_year_gain"] = B.groupby("yr").agg(gain_sum=("gain", "sum"), timing_sum=("timing", "sum"))
    return out
