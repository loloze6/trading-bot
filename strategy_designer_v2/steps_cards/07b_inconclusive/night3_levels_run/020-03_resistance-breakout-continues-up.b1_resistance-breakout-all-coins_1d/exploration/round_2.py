def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wd in bars.items():
        rr = []; rr10 = []
        for w, df in wd.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 5, 5); rr += list(c[idx + 5] / c[idx] - 1)
            idx = np.arange(0, len(c) - 10, 10); rr10 += list(c[idx + 10] / c[idx] - 1)
        dr5, sd5 = np.mean(rr), np.std(rr); dr10 = np.mean(rr10)
        for w, df in wd.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c)
            f = df["forecast"].fillna(0).values
            raw = df["debug_info.components.break_touches.last_history_value"].values
            ret30 = pd.Series(c).pct_change(30).values
            ret90 = pd.Series(c).pct_change(90).values
            seen = set()
            for t in range(n):
                prev = f[t - 1] if t > 0 else 0
                if f[t] >= 2 and prev < 2 and t + 5 < n:
                    cell = t // 5
                    if cell in seen: continue
                    seen.add(cell)
                    # touch count recomputed: swing highs in last 90 closes within 2% of level crossed
                    lo = max(0, t - 90)
                    sw = []
                    for k in range(lo + 2, t - 2 + 1):
                        if k + 2 <= t - 1 and c[k] >= c[k-1] and c[k] >= c[k-2] and c[k] > c[k+1] and c[k] > c[k+2]:
                            sw.append(c[k])
                    lv = [s for s in sw if c[t-1] <= s < c[t]]
                    N = np.nan; margin = np.nan
                    if lv:
                        L = max(lv)
                        N = sum(abs(s / L - 1) <= 0.02 for s in sw)
                        margin = c[t] / L - 1
                    rows.append({"coin": coin, "year": pd.Timestamp(df["timestamp"].iloc[t]).year,
                                 "raw": raw[t], "ret30": ret30[t], "ret90": ret90[t], "N": N, "margin": margin,
                                 "u5": c[t+5]/c[t]-1-dr5,
                                 "u10": (c[t+10]/c[t]-1-dr10) if t + 10 < n else np.nan})
    d = pd.DataFrame(rows)
    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["N_dist"] = d["N"].value_counts().sort_index().head(12)
    d["Ng"] = d["N"].clip(upper=4)
    out["by_N"] = d.groupby("Ng").apply(summ)
    d["mq"] = pd.qcut(d["margin"].rank(method="first"), 4, labels=False)
    out["by_margin_q"] = d.groupby("mq").apply(summ)
    d["trq"] = pd.qcut(d["ret30"].rank(method="first"), 4, labels=False)
    d["rawh"] = (d["raw"] > d["raw"].median()).astype(int)
    out["ret30q_x_rawhalf"] = d.groupby(["trq", "rawh"]).apply(summ)
    d["t90q"] = pd.qcut(d["ret90"].rank(method="first"), 4, labels=False)
    out["by_ret90q"] = d.groupby("t90q").apply(summ)
    up = d[d["ret30"] > 0]; dn = d[d["ret30"] <= 0]
    out["ret30_pos_vs_neg"] = pd.DataFrame({"pos": summ(up), "neg": summ(dn)}).T
    out["pos_ret30_by_year"] = up.groupby("year").apply(summ)
    out["neg_ret30_by_year"] = dn.groupby("year").apply(summ)
    out["corr_ret30_u5_spearman"] = float(stats.spearmanr(d["ret30"], d["u5"], nan_policy="omit")[0])
    out["pos_ret30_by_coin_sign"] = up.groupby("coin").apply(summ)["mean"].gt(0).sum()
    return out
