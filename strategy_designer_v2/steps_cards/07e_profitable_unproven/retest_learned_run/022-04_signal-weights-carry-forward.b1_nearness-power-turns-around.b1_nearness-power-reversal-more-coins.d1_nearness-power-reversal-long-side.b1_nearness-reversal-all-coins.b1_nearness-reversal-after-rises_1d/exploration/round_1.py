def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]
    out = {}
    # per-bar frame
    rows = []
    for c, wd in bars.items():
        for w, b in wd.items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"].astype(float)
            b["coin"] = c; b["win"] = w
            b["pos"] = pd.to_numeric(b["postRebalance_current_allocation"], errors="coerce").fillna(0)
            b["r1"] = cl.shift(-1) / cl - 1
            for h in (1, 5, 10, 20):
                b[f"f{h}"] = cl.shift(-h) / cl - 1
            b["r30"] = cl / cl.shift(30) - 1
            b["r90"] = cl / cl.shift(90) - 1
            b["near90"] = cl / b["high"].astype(float).rolling(90, min_periods=30).max() - 1
            b["i"] = np.arange(len(b))
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            b["fc"] = pd.to_numeric(b["forecast"], errors="coerce").fillna(0)
            rows.append(b[["coin","win","i","yr","pos","r1","f1","f5","f10","f20","r30","r90","near90","fc","regime"]])
    B = pd.concat(rows, ignore_index=True)
    mu1 = B.groupby("coin")["r1"].mean()
    B["mu1"] = B["coin"].map(mu1)
    B["gain"] = B["pos"] * B["r1"]
    B["mkt"] = B["pos"] * B["mu1"]
    B["key"] = B["win"] + "_" + B["i"].astype(str)
    d = B.groupby("key")[["gain","mkt"]].mean()
    out["book_decomp_daily"] = pd.Series({"gain": d.gain.mean(), "mkt_part": d.mkt.mean(), "timing": (d.gain-d.mkt).mean(),
        "t_timing": (d.gain-d.mkt).mean()/((d.gain-d.mkt).std()/np.sqrt(len(d))), "days": len(d)})
    # per coin contribution
    pc = B.groupby("coin").agg(gain_sum=("gain","sum"), mkt_sum=("mkt","sum"), share_in=("pos", lambda x:(x>0).mean()))
    pc["timing_sum"] = pc.gain_sum - pc.mkt_sum
    pc["share_of_gain"] = pc.gain_sum / pc.gain_sum.sum()
    out["per_coin"] = pc.sort_values("gain_sum", ascending=False).round(4)
    py = B.groupby("yr").agg(gain_sum=("gain","sum"), mkt_sum=("mkt","sum"), in_share=("pos", lambda x:(x>0).mean()))
    py["timing_sum"] = py.gain_sum - py.mkt_sum
    out["per_year"] = py.round(4)
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c, wd in trades.items() for w, t in wd.items() if len(t)], ignore_index=True)
    pl = pd.to_numeric(T["net_profit_loss_percent"], errors="coerce").dropna().sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(pl), "mean": pl.mean(), "median": pl.median(), "win_rate": (pl>0).mean(),
        "top10_share_of_sum": pl.head(10).sum()/pl.sum(), "top5pct_share": pl.head(max(1,len(pl)//20)).sum()/pl.sum(),
        "sum_without_top10": pl.iloc[10:].sum(), "sum": pl.sum()})
    # 5-day grid analysis
    mu = {}
    G = {}
    for h in (1,5,10,20):
        g = B[B["i"] % h == 0].dropna(subset=[f"f{h}"]).copy()
        drift = g.groupby("coin")[f"f{h}"].mean()
        g["ex"] = g[f"f{h}"] - g["coin"].map(drift)
        G[h] = g
    res = []
    for h, g in G.items():
        tr = g[g["regime"]=="trending"]
        a = tr[tr.fc>0]["ex"]; z = tr[tr.fc==0]["ex"]; nt = g[g["regime"]!="trending"]["ex"]
        tt = stats.ttest_ind(a, z, equal_var=False)
        tt2 = stats.ttest_ind(tr["ex"], nt, equal_var=False)
        r = stats.linregress(tr["fc"], tr["ex"])
        res.append({"h":h,"n_fc>0":len(a),"ex_fc>0":a.mean(),"n_trend_fc0":len(z),"ex_trend_fc0":z.mean(),"t_fc>0_vs_0":tt.statistic,
                    "n_nontrend":len(nt),"ex_trend":tr["ex"].mean(),"ex_nontrend":nt.mean(),"t_trend_vs_non":tt2.statistic,
                    "slope_in_trend":r.slope,"t_slope_in_trend":r.slope/r.stderr})
    out["horizons"] = pd.DataFrame(res).round(4)
    # graded by r30 and near90 on 5-day grid, all bars
    g = G[5].dropna(subset=["r30"]).copy()
    g["q_r30"] = pd.qcut(g["r30"], 5, labels=False)
    out["r30_quintiles_5d"] = g.groupby("q_r30")["ex"].agg(["count","mean"]).round(4)
    for h in (5,20):
        gg = G[h].dropna(subset=["r30"])
        r = stats.linregress(gg["r30"].clip(-1,3), gg["ex"]); out[f"r30_slope_h{h}"] = f"slope {r.slope:.4f} t {r.slope/r.stderr:.2f} n {len(gg)}"
    g2 = G[5].dropna(subset=["near90"]).copy()
    g2["q_near"] = pd.qcut(g2["near90"], 5, labels=False, duplicates="drop")
    out["near90_quintiles_5d"] = g2.groupby("q_near")["ex"].agg(["count","mean"]).round(4)
    # within active forecast>0: near90 levels
    a = G[5][(G[5].fc>0)].dropna(subset=["near90"]).copy()
    a["q_near"] = pd.qcut(a["near90"], 3, labels=False, duplicates="drop")
    out["fc>0_by_near90_tercile"] = a.groupby("q_near")[["ex","near90","r30","fc"]].mean().round(4)
    return out
