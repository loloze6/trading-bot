def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 10
    rows = []
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            rets += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(rets)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            n = len(c)
            prev = np.r_[0, f[:-1]]
            sig = (f < 0) & ((-f) - np.maximum(-prev, 0) >= 2)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            brkcol = df.get("debug_info.components.break.last_history_value", pd.Series(np.nan, index=df.index))
            taken = set()
            for t in np.where(sig)[0]:
                cell = t // H
                if cell in taken or t + H >= n: continue
                taken.add(cell)
                r = {}
                for h in (5, 10, 20):
                    r["r%d" % h] = (-(c[t + h] / c[t] - 1 - drift[coin] * h / 10)) if t + h < n else np.nan
                # close relative to 90-bar max close (excluding today), and 90-day return
                lo = max(0, t - 90)
                mx = c[lo:t].max() if t > lo else np.nan
                rows.append(dict(coin=coin, year=yr[t], brk=brkcol.iloc[t],
                                 day1=c[t] / c[t - 1] - 1 if t >= 1 else np.nan,
                                 below_max=c[t] / mx - 1,
                                 ret90=c[t] / c[t - 90] - 1 if t >= 90 else np.nan, **r))
    d = pd.DataFrame(rows)
    def summ(g, col="r10"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    d["q_brk"] = pd.qcut(d["brk"].rank(method="first"), 4, labels=False)
    out["brk_q_r20"] = d.groupby("q_brk").apply(lambda g: summ(g, "r20"))
    out["brk_q_r5"] = d.groupby("q_brk").apply(lambda g: summ(g, "r5"))
    out["brk_q_mean_brk_day1"] = d.groupby("q_brk")[["brk", "day1", "below_max"]].mean()
    out["spearman_brk_r10"] = pd.Series(stats.spearmanr(d["brk"], d["r10"], nan_policy="omit"), index=["rho", "p"])
    out["spearman_day1_r10"] = pd.Series(stats.spearmanr(d["day1"], d["r10"], nan_policy="omit"), index=["rho", "p"])
    d["q_day1"] = pd.qcut(d["day1"], 4, labels=False)
    out["day1_q"] = d.groupby("q_day1").apply(summ)
    out["day1_q_range"] = d.groupby("q_day1")["day1"].agg(["min", "max"])
    q0 = d[d.q_brk == 0]
    out["q0_by_coin"] = q0.groupby("coin").apply(summ)
    out["q0_by_year"] = q0.groupby("year").apply(summ)
    d["q_ret90"] = pd.qcut(d["ret90"], 3, labels=False)
    out["ret90_t"] = d.groupby("q_ret90").apply(summ)
    out["ret90_t_q0brk"] = d[d.q_brk == 0].groupby("q_ret90").apply(summ)
    return out
