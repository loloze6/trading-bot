def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    comp_info = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            allr.append(b["close"].pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            dc = b["debug_info.components"]
            comp_info.append(dict(coin=coin, w=w, nonnull=int(dc.notna().sum()),
                                  nonempty=int(dc.dropna().astype(str).str.len().gt(2).sum()),
                                  active=int((b["regime"] == "mean_reversion").sum())))
            c = b["close"]; h = b["high"]; l = b["low"]
            rng = h - l
            mr30 = rng.rolling(30).mean()
            low10 = l.shift(1).rolling(10).min()
            depth = (low10 - c).clip(lower=0) / mr30
            nxt = c.shift(-1) / c - 1
            f = b["forecast"].fillna(0)
            reg = b["regime"] == "mean_reversion"
            low_since = 0.0
            bet = np.zeros(len(b), bool)
            for i in range(len(b)):
                fi = f.iloc[i]
                if fi - low_since >= 2 and fi > 0:
                    bet[i] = True
                    low_since = fi
                else:
                    low_since = min(low_since, fi)
            for i in range(len(b)):
                if np.isnan(nxt.iloc[i]) or not reg.iloc[i]:
                    continue
                rows.append(dict(coin=coin, w=w, bet=bet[i], brk=depth.iloc[i] > 0,
                                 depth=depth.iloc[i], fc=f.iloc[i], u=nxt.iloc[i] - mu,
                                 day=pd.Timestamp(b["timestamp"].iloc[i]).normalize()))
    d = pd.DataFrame(rows)
    ci = pd.DataFrame(comp_info)
    out["components_recorded"] = ci[["nonnull", "nonempty", "active"]].sum()
    def stat(g):
        s = g.groupby("day")["u"].sum(); n = len(g); G = len(s); m = g["u"].mean()
        se = np.sqrt((s - g.groupby("day").size() * m).pow(2).sum() * G / (G - 1)) / n if G > 1 else np.nan
        return pd.Series(dict(n=n, days=G, mean=m, t=m / se, median=g["u"].median()))
    out["regime_days_by_kind"] = d.groupby(["bet", "brk"]).apply(stat)
    bt = d[d.bet]
    med = bt["depth"].median()
    deep = bt[bt.depth > med]["u"]; sh = bt[bt.depth <= med]["u"]
    tw = stats.ttest_ind(deep, sh, equal_var=False)
    out["median_split_recomputed_depth"] = pd.Series(dict(n_deep=len(deep), n_shallow=len(sh),
        mean_deep=deep.mean(), mean_shallow=sh.mean(), diff=deep.mean() - sh.mean(), welch_t=tw.statistic))
    medf = bt["fc"].median()
    deepf = bt[bt.fc > medf]["u"]; shf = bt[bt.fc <= medf]["u"]
    out["median_split_forecast"] = pd.Series(dict(diff=deepf.mean() - shf.mean(),
        welch_t=stats.ttest_ind(deepf, shf, equal_var=False).statistic))
    out["spearman_depth_u_bets"] = float(stats.spearmanr(bt["depth"], bt["u"]).correlation)
    br = d[d.brk]
    out["spearman_depth_u_allbreaks"] = float(stats.spearmanr(br["depth"], br["u"]).correlation)
    br = br.copy()
    br["dq"] = pd.qcut(br["depth"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["all_breaks_by_depth_quartile"] = br.groupby("dq").apply(stat)
    # excluding top outliers
    trim = bt[bt.u < bt.u.quantile(0.95)]
    out["bets_trim_top5pct"] = stat(trim)
    return out
