def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            raw = b.get("debug_info.components.vol30_vs_year.last_history_value")
            r30 = pd.Series(c).pct_change(30).values
            for h in (5, 10, 20):
                for i in range(0, n - h, h):
                    if b.loc[i, "regime"] != "mean_reversion" or b.loc[i, "forecast"] == 0:
                        continue
                    rows.append(dict(
                        coin=coin, win=w, h=h, fc=b.loc[i, "forecast"],
                        raw=raw.iloc[i] if raw is not None else np.nan,
                        r30=r30[i], ret=c[i + h] / c[i] - 1,
                        year=pd.Timestamp(b.loc[i, "timestamp"]).year))
    d = pd.DataFrame(rows)
    out = {}

    def diff(g):
        hv = g[g.fc > 0].ret
        q = g[g.fc < 0].ret
        t = stats.ttest_ind(hv, q, equal_var=False).statistic if len(hv) > 1 and len(q) > 1 else np.nan
        return pd.Series(dict(n_heavy=len(hv), n_quiet=len(q), m_heavy=hv.mean(), m_quiet=q.mean(),
                              diff=hv.mean() - q.mean(), t=t,
                              corr_fc_ret=g[["fc", "ret"]].corr().iloc[0, 1]))

    out["by_horizon"] = d.groupby("h").apply(diff)
    d5 = d[d.h == 5].copy()
    out["by_coin_h5"] = d5.groupby("coin").apply(diff)
    out["by_window_h5"] = d5.groupby("win").apply(diff)
    out["by_year_h5"] = d5.groupby("year").apply(diff)
    d5["fcq"] = pd.qcut(d5.fc, 5, duplicates="drop")
    out["by_fc_quintile_h5"] = d5.groupby("fcq").ret.agg(["count", "mean", "std"])
    d5["rawq"] = pd.qcut(d5.raw, 5, duplicates="drop")
    out["by_raw_quintile_h5"] = d5.groupby("rawq").ret.agg(["count", "mean", "std"])
    d5["r30q"] = pd.qcut(d5.r30, 3, duplicates="drop")
    out["by_r30_tercile_h5"] = d5.groupby("r30q").apply(diff)
    out["raw_vs_fc_sign_agree"] = float((np.sign(d5.raw) == np.sign(d5.fc)).mean())
    return out
