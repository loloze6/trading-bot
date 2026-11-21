def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    sd = {}
    for coin, ws in bars.items():
        rets = []
        for w, b in ws.items():
            c = b["close"].values
            for i in range(0, len(c) - 26, 26):
                rets.append(c[i + 26] / c[i] - 1)
        drift[coin] = np.mean(rets); sd[coin] = np.std(rets)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            for i in range(0, n - 26, 26):
                if b.loc[i, "regime"] == "trending" and b.loc[i, "forecast"] < 0:
                    r = c[i + 26] / c[i] - 1
                    r10 = c[min(i + 10, n - 1)] / c[i] - 1
                    r52 = c[i + 52] / c[i] - 1 if i + 52 < n else np.nan
                    rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b.loc[i, "timestamp"]).year,
                                     ex=-(r - drift[coin]), tot=-r, r10=-r10, r52=-r52,
                                     raw=b.loc[i, "debug_info.components.slow_fall.last_history_value"],
                                     post=b.loc[i, "debug_info.components.slow_fall.post_pipeline_value"],
                                     fc=b.loc[i, "forecast"], strength=-(r - drift[coin]) / sd[coin]))
    d = pd.DataFrame(rows)
    def summ(g):
        return pd.Series(dict(n=len(g), mean_ex=g.ex.mean(), t=g.ex.mean() / (g.ex.std(ddof=1) / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                              mean_tot=g.tot.mean(), share_pos=(g.ex > 0).mean()))
    out = {}
    out["all"] = summ(d)
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["q_raw"] = pd.qcut(d.raw.rank(method="first"), 4, labels=["q1_fast", "q2", "q3", "q4_slow"])
    out["by_raw_quartile"] = d.groupby("q_raw").apply(summ)
    d["q_fc"] = pd.qcut(d.fc.rank(method="first"), 4, labels=["q1_most_short", "q2", "q3", "q4_least"])
    out["by_forecast_quartile"] = d.groupby("q_fc").apply(summ)
    out["raw_desc"] = d.raw.describe()
    out["corr_raw_ex_spearman"] = stats.spearmanr(d.raw, d.ex, nan_policy="omit")[0]
    hi = d[d.raw > d.raw.median()].ex; lo = d[d.raw <= d.raw.median()].ex
    out["welch_slow_minus_fast"] = pd.Series(dict(diff=hi.mean() - lo.mean(), t=stats.ttest_ind(hi, lo, equal_var=False)[0]))
    out["horizons_short_dir_raw"] = pd.Series(dict(r10=d.r10.mean(), r10_t=d.r10.mean() / (d.r10.std() / np.sqrt(d.r10.notna().sum())),
                                                    r52=d.r52.mean(), r52_t=d.r52.mean() / (d.r52.std() / np.sqrt(d.r52.notna().sum())), n52=d.r52.notna().sum()))
    out["drift"] = pd.Series(drift)
    return out
