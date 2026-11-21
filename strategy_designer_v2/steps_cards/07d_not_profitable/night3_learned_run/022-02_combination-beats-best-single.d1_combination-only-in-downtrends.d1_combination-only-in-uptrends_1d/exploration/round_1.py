def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    gain = []
    for coin, wins in data["bars"].items():
        # coin mean 5d return over all windows on grid
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        mu = np.nanmean(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            # daily gain of position
            pos = b["postRebalance_current_allocation"].values
            r1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            for i in range(n - 1):
                gain.append((coin, w, pos[i], r1[i], b["regime"].iloc[i]))
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year,
                                 reg=b["regime"].iloc[i], fc=b["forecast"].iloc[i],
                                 pos=pos[i],
                                 comb=b.get("debug_info.components.combined.post_pipeline_value", pd.Series([np.nan]*n)).iloc[i],
                                 combraw=b.get("debug_info.components.combined.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                                 best=b.get("debug_info.components.best.post_pipeline_value", pd.Series([np.nan]*n)).iloc[i],
                                 r90=b.get("debug_info.components.ret90.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                                 fwd=c[i + H] / c[i] - 1, ex=c[i + H] / c[i] - 1 - mu))
    d = pd.DataFrame(rows)
    t = d[d.reg == "trending"].dropna(subset=["comb"])
    out = {}
    def summ(g):
        return pd.Series({"n": len(g), "mean_fwd": g.fwd.mean(), "mean_ex": g.ex.mean(),
                          "t_ex": g.ex.mean() / (g.ex.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    t = t.copy()
    t["side"] = np.sign(t.comb)
    out["trend_by_side"] = t.groupby("side").apply(summ)
    t["cq"] = pd.qcut(t.comb, 5, labels=False)
    out["trend_by_comb_quintile"] = t.groupby("cq").apply(summ)
    t["bq"] = pd.qcut(t.best, 5, labels=False, duplicates="drop")
    out["trend_by_best_quintile"] = t.groupby("bq").apply(summ)
    t["rq"] = pd.qcut(t.r90, 4, labels=False)
    out["trend_by_r90_quartile"] = t.groupby("rq").apply(summ)
    out["corr_spearman"] = pd.Series({"comb": stats.spearmanr(t.comb, t.ex)[0],
                                      "best": stats.spearmanr(t.best, t.ex)[0],
                                      "r90": stats.spearmanr(t.r90, t.ex)[0],
                                      "comb_vs_best": stats.spearmanr(t.comb, t.best)[0],
                                      "sign_raw_ne_std": (np.sign(t.combraw) != np.sign(t.comb)).mean(),
                                      "share_short": (t.comb < 0).mean()})
    out["by_regime_all"] = d.groupby("reg").apply(summ)
    t["signed_ex"] = t.side * t.ex
    out["signed_by_year"] = t.groupby("year").apply(lambda g: pd.Series({"n": len(g), "signed_ex": g.signed_ex.mean(), "share_short": (g.side < 0).mean(), "mean_ex": g.ex.mean()}))
    out["signed_by_coin"] = t.groupby("coin").apply(lambda g: pd.Series({"n": len(g), "signed_ex": g.signed_ex.mean(), "long_ex": g.ex[g.side > 0].mean(), "short_ex": g.ex[g.side < 0].mean()}))
    G = pd.DataFrame(gain, columns=["coin", "w", "pos", "r1", "reg"]).dropna()
    G["pg"] = G.pos * G.r1
    G["ps"] = np.sign(G.pos)
    out["gain_by_pos_sign"] = G.groupby("ps").agg(n=("pg", "size"), sum_pg=("pg", "sum"), mean_pg=("pg", "mean"), mean_abs_pos=("pos", lambda x: x.abs().mean()))
    tr = []
    for coin, wins in data["trades"].items():
        for w, x in wins.items():
            if len(x): tr.append(x.assign(coin=coin))
    T = pd.concat(tr)
    out["trades"] = T.groupby("side").agg(n=("side", "size"), pl=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"), dur_days=("duration_minutes", lambda x: x.mean() / 1440))
    return out
