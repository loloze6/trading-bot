def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book decomposition per bar: gross gain, fee drag, turnover
    g = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].values
            a = b["postRebalance_current_allocation"].fillna(0).values
            pre = b["total_portfolio_value"].values
            post = b["postRebalance_total_value"].values
            r = np.r_[c[1:] / c[:-1] - 1, np.nan]
            gross = a * r
            fee = (pre - post) / pre
            turn = np.abs(b["postRebalance_current_allocation"].fillna(0).values - b["previous_allocation"].fillna(0).values)
            g.append(pd.DataFrame(dict(coin=coin, w=w, gross=gross, fee=fee, turn=turn, a=a, inpos=(a != 0))))
    G = pd.concat(g)
    out["book_bar_sums"] = G.groupby("coin").agg(bars=("gross", "size"), gross_sum=("gross", "sum"), fee_sum=("fee", "sum"),
                                                 turnover_sum=("turn", "sum"), share_in_pos=("inpos", "mean"),
                                                 mean_abs_alloc_in_pos=("a", lambda x: x[x != 0].abs().mean()))
    G["chg"] = G["turn"] > 0
    out["rebalances"] = G.groupby("coin").agg(n_rebal=("chg", "sum"))
    # cases joint grouping r7d x rise24 and volratio, using recomputed case set
    rows = []
    for coin, wins in data["bars"].items():
        dr = []
        for w, b in wins.items():
            c = b["close"].values; idx = np.arange(0, len(c) - 6, 6); dr.append(c[idx + 6] / c[idx] - 1)
        d6 = np.concatenate(dr).mean()
        for w, b in wins.items():
            c = b["close"].values; f = b["forecast"].fillna(0).values; n = len(c)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            r24 = pd.Series(c).pct_change(24).values
            r7d = pd.Series(c).pct_change(168).values
            v7 = pd.Series(r1).rolling(168, min_periods=50).std().values
            v30 = pd.Series(r1).rolling(720, min_periods=200).std().values
            lm = 0.0; cd = -1
            for i in range(n):
                if f[i] <= 0:
                    lm = 0.0; continue
                if f[i] - lm >= 2:
                    if i // 6 != cd and i + 6 < n:
                        cd = i // 6
                        rows.append(dict(coin=coin, r24=r24[i - 1], r7d=r7d[i], vr=v7[i] / v30[i], t6=c[i + 6] / c[i] - 1, u6=c[i + 6] / c[i] - 1 - d6))
                    lm = f[i]
                else:
                    lm = min(lm, f[i])
    D = pd.DataFrame(rows).dropna()
    D["r7d_pos"] = np.where(D["r7d"] > 0, "r7d>0", "r7d<=0")
    D["r24q"] = pd.qcut(D["r24"], 3, labels=["lo", "mid", "hi"])
    def agg(x):
        return pd.Series(dict(n=len(x), t6=x["t6"].mean(), u6=x["u6"].mean(), t=x["u6"].mean() / (x["u6"].std() / np.sqrt(len(x)))))
    out["r7dsign_x_r24"] = D.groupby(["r7d_pos", "r24q"]).apply(agg)
    D["prod"] = D["r24"] * D["r7d"].clip(lower=0)
    D["pq"] = pd.qcut(D["prod"].rank(method="first"), 5, labels=False)
    out["by_r24_times_r7dpos_q"] = D.groupby("pq").apply(agg)
    D["vrq"] = pd.qcut(D["vr"], 3, labels=["calm", "mid", "agitated"])
    out["vr_x_r7d"] = D.groupby(["vrq", "r7d_pos"]).apply(agg)
    return out
