def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]
    out = {}
    H = 10
    cs = []
    for c in bars:
        allr = []
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            hi = cl.rolling(60, min_periods=20).max()
            D = (1-cl/hi)*100
            r28 = cl/cl.shift(28)-1
            r7 = cl/cl.shift(7)-1
            vol = cl.pct_change().rolling(20, min_periods=10).std()
            raw = b.get("debug_info.components.hp_mom.last_history_value", pd.Series(np.nan, index=b.index))
            pos = b["postRebalance_current_allocation"]
            idx = np.arange(0, len(cl)-H, H)
            fr = cl.values[idx+H]/cl.values[idx]-1
            allr.append(pd.DataFrame({"coin": c, "win": w, "fc": b["forecast"].values[idx], "fr": fr,
                                      "D": D.values[idx], "r28": r28.values[idx], "r7": r7.values[idx],
                                      "vol": vol.values[idx], "raw": raw.values[idx], "pos": pos.values[idx]}))
        d = pd.concat(allr); d["ex"] = d.fr-d.fr.mean()
        d["sd"] = d.fr.std(); cs.append(d)
    d = pd.concat(cs, ignore_index=True)
    d["z"] = d.ex/d.sd
    d["near"] = 1/(1+d.D)**2
    d["mom_near"] = d.r28*d.near
    d["Dq"] = pd.cut(d.D, [-0.01, 0.5, 5, 15, 30, 1000], labels=["at_high", "0.5-5", "5-15", "15-30", ">30"])
    d["r28q"] = pd.qcut(d.r28, 4, labels=["r28_q1", "r28_q2", "r28_q3", "r28_q4"])
    # mean 10-day excess return by distance to high and 28-day return
    g = d.groupby("Dq")
    out["ex_by_dist"] = pd.DataFrame({"n": g.size(), "ex_mean_%": g.ex.mean()*100, "fr_mean_%": g.fr.mean()*100,
                                      "t": g.ex.mean()/(g.ex.std()/np.sqrt(g.size())),
                                      "median_fr_%": g.fr.median()*100}).round(3)
    out["ex_by_dist_r28"] = (d.pivot_table(index="Dq", columns="r28q", values="ex", aggfunc="mean")*100).round(3)
    out["n_by_dist_r28"] = d.pivot_table(index="Dq", columns="r28q", values="ex", aggfunc="size")
    # slopes on single variables (standardized excess z)
    res = []
    for v in ["fc", "raw", "near", "r28", "mom_near", "r7", "D", "pos"]:
        s = d.dropna(subset=[v, "z"])
        lr = stats.linregress(s[v], s.z)
        sp = stats.spearmanr(s[v], s.z)
        res.append({"var": v, "n": len(s), "ols_t": lr.slope/lr.stderr, "spearman": sp.correlation, "spearman_p": sp.pvalue})
    out["single_slopes"] = pd.DataFrame(res).round(4)
    # within r28>0: does nearness grade the move?
    up = d[d.r28 > 0].dropna(subset=["near"])
    lr = stats.linregress(up.near, up.z)
    out["near_within_r28pos"] = pd.Series({"n": len(up), "t": lr.slope/lr.stderr})
    dn = d[d.r28 < 0].dropna(subset=["near"])
    lr2 = stats.linregress(dn.near, dn.z)
    out["near_within_r28neg"] = pd.Series({"n": len(dn), "t": lr2.slope/lr2.stderr})
    # tails: distribution of 10-day returns near high vs far
    q = d.groupby("Dq").fr.quantile([0.1, 0.5, 0.9]).unstack()*100
    out["fr_quantiles_by_dist_%"] = q.round(2)
    # trades: entry distance and concentration
    rows = []
    for c in trades:
        for w, t in trades[c].items():
            if not len(t): continue
            b = bars[c][w].reset_index(drop=True)
            cl = b["close"]; hi = cl.rolling(60, min_periods=20).max()
            Dd = pd.Series(((1-cl/hi)*100).values, index=pd.to_datetime(b.timestamp))
            et = pd.to_datetime(t.entry_time)
            Dv = Dd.reindex(et, method="ffill").values
            rows.append(t.assign(coin=c, win=w, Dent=Dv))
    T = pd.concat(rows, ignore_index=True)
    T["Dq"] = pd.cut(T.Dent, [-0.01, 0.5, 5, 15, 30, 1000], labels=["at_high", "0.5-5", "5-15", "15-30", ">30"])
    g = T.groupby(["side", "Dq"]).net_profit_loss_percent
    out["trades_side_dist"] = pd.DataFrame({"n": g.size(), "sum": g.sum(), "mean": g.mean(), "median": g.median(),
                                            "win": g.apply(lambda s: (s > 0).mean()),
                                            "days": T.groupby(["side", "Dq"]).duration_minutes.mean()/1440}).round(2)
    L = T[T.side == "LONG"].sort_values("net_profit_loss_percent", ascending=False)
    top = L.head(30)
    out["top30_long"] = pd.DataFrame({"by_coin": top.coin.value_counts()}).T
    out["top30_long_win_count"] = pd.Series({"distinct_windows": top.win.nunique(),
                                             "share_of_long_sum": top.net_profit_loss_percent.sum()/L.net_profit_loss_percent.sum(),
                                             "median_days": top.duration_minutes.median()/1440,
                                             "median_Dent": top.Dent.median()})
    return out
