import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [18, 36]
    rows = []
    for coin, wins in bars.items():
        drift, sd = {}, {}
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            rs = np.array(rs); drift[h] = rs.mean(); sd[h] = rs.std()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values; reg = df["regime"].values
            q = df.get("debug_info.components.quiet.post_pipeline_value")
            q = q.values if q is not None else np.full(len(c), np.nan)
            p10 = pd.Series(c).pct_change(60).values
            p5 = pd.Series(c).pct_change(30).values
            p20 = pd.Series(c).pct_change(120).values
            low = None; seen = set()
            for t in range(len(c)):
                if f[t] <= 0:
                    low = 0.0; continue
                if low is None: low = 0.0
                if reg[t] == "trending" and f[t] - low >= 2:
                    low = f[t]
                    cell = t // 18
                    if cell in seen or t + 18 >= len(c): continue
                    seen.add(cell)
                    rec = dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[t]).year,
                               q=q[t], p10=p10[t], p5=p5[t], p20=p20[t], sd18=sd[18], drift18=drift[18])
                    for h in H:
                        if t + h < len(c):
                            rec[f"u{h}"] = c[t + h] / c[t] - 1 - drift[h]
                    rows.append(rec)
                else:
                    low = min(low, f[t])
    d = pd.DataFrame(rows)
    def summ(g, col="u18"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    dd = d.dropna(subset=["p10"]).copy()
    dd["p10q"] = pd.qcut(dd["p10"], 5, labels=False)
    out["by_p10_quintile"] = dd.groupby("p10q").apply(summ)
    out["by_p10_quintile_u36"] = dd.groupby("p10q").apply(lambda g: summ(g, "u36"))
    out["by_p5_sign"] = d.groupby(np.sign(d["p5"])).apply(summ)
    out["by_p20_sign"] = d.groupby(np.sign(d["p20"])).apply(summ)
    pos = dd[dd["p10"] > 0]; neg = dd[dd["p10"] < 0]
    out["pos_p10_by_coin"] = pos.groupby("coin").apply(summ)
    out["neg_p10_by_coin"] = neg.groupby("coin").apply(summ)
    out["pos_p10_by_year"] = pos.groupby("year").apply(summ)
    out["neg_p10_by_year"] = neg.groupby("year").apply(summ)
    out["pos_minus_neg_welch"] = pd.Series({"diff": pos["u18"].mean() - neg["u18"].mean(),
        "t": stats.ttest_ind(pos["u18"], neg["u18"], equal_var=False).statistic})
    # within pos p10, quiet halves
    m = pos["q"].median()
    hi_ = pos[pos["q"] > m]["u18"]; lo_ = pos[pos["q"] < m]["u18"]
    out["pos_p10_quiet_halves"] = pd.Series({"hi_mean": hi_.mean(), "lo_mean": lo_.mean(), "n_hi": len(hi_), "n_lo": len(lo_),
        "welch_t": stats.ttest_ind(hi_, lo_, equal_var=False).statistic})
    out["pos_p10_strength"] = (pos["u18"] / pos["sd18"]).mean()
    out["pos_p10_total_move"] = (pos["u18"] + pos["drift18"]).mean()
    # correlation of p10 with u18 (graded)
    out["spearman_p10_u18"] = pd.Series(stats.spearmanr(dd["p10"], dd["u18"]), index=["rho", "p"])
    out["spearman_p10_u18_pos"] = pd.Series(stats.spearmanr(pos["p10"], pos["u18"]), index=["rho", "p"])
    return out
