def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    Hs = [3, 10]
    drift, usual = {}, {}
    base = []
    cases = []
    for coin, wins in bars.items():
        rets = {h: [] for h in Hs}
        for w, df in wins.items():
            c = df["close"].values; n = len(c)
            for h in Hs:
                idx = np.arange(0, n - h, h)
                rets[h].extend(list(c[idx + h] / c[idx] - 1))
        drift[coin] = {h: np.mean(rets[h]) for h in Hs}
        usual[coin] = {h: np.std(rets[h]) for h in Hs}
        for w, df in wins.items():
            c = df["close"].values; n = len(c)
            f = df["forecast"].fillna(0).values
            # baseline: all bars on the 10-bar grid with 30 days of past
            for t in range(30, n - 10, 10):
                base.append({"coin": coin, "p30": c[t] / c[t - 30] - 1,
                             "u10": c[t + 10] / c[t] - 1 - drift[coin][10],
                             "s10": (c[t + 10] / c[t] - 1 - drift[coin][10]) / usual[coin][10],
                             "brk": 0})
            floor = 0.0; taken = set()
            for t in range(n):
                if f[t] <= 0: floor = 0.0
                cell = t // 10
                if f[t] - floor >= 2 and cell not in taken:
                    taken.add(cell); floor = f[t]
                    if t >= 30 and t + 10 < n:
                        u = c[t + 10] / c[t] - 1 - drift[coin][10]
                        cases.append({"coin": coin, "p30": c[t] / c[t - 30] - 1, "u10": u,
                                      "s10": u / usual[coin][10], "brk": 1,
                                      "p30s": (c[t] / c[t - 30] - 1) / usual[coin][10]})
    b = pd.DataFrame(base); d = pd.DataFrame(cases)
    edges = b["p30"].quantile([0, .25, .5, .75, 1]).values
    edges[0] = -np.inf; edges[-1] = np.inf
    b["q"] = pd.cut(b["p30"], edges, labels=False); d["q"] = pd.cut(d["p30"], edges, labels=False)
    def summ(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out = {}
    out["base_by_p30q"] = b.groupby("q")["u10"].apply(summ).unstack()
    out["brk_by_p30q"] = d.groupby("q")["u10"].apply(summ).unstack()
    rows = {}
    for q in range(4):
        x = d.loc[d.q == q, "u10"].dropna(); y = b.loc[b.q == q, "u10"].dropna()
        tt = stats.ttest_ind(x, y, equal_var=False)
        rows[q] = {"brk_minus_base": x.mean() - y.mean(), "welch_t": tt.statistic}
    out["brk_minus_base_by_q"] = pd.DataFrame(rows).T
    out["edges_base"] = pd.Series(edges[1:-1])
    # graded: correlation of past30 (scaled) with strength within breakouts
    dd = d.dropna(subset=["p30s", "s10"])
    r, p = stats.spearmanr(dd["p30s"], dd["s10"])
    out["brk_spearman_p30_vs_s10"] = pd.Series({"rho": r, "p": p, "n": len(dd)})
    bb = b.dropna(); bb = bb.assign(p30s=bb["p30"] / bb["coin"].map(lambda k: usual[k][10]))
    r2, p2 = stats.spearmanr(bb["p30s"], bb["s10"])
    out["base_spearman_p30_vs_s10"] = pd.Series({"rho": r2, "p": p2, "n": len(bb)})
    # breakouts with positive vs non-positive 30d return
    pos = d.loc[d.p30 > 0, "u10"]; neg = d.loc[d.p30 <= 0, "u10"]
    out["brk_pos_vs_neg_p30"] = pd.DataFrame({"pos": summ(pos), "neg": summ(neg)})
    bpos = b.loc[b.p30 > 0, "u10"]; bneg = b.loc[b.p30 <= 0, "u10"]
    out["base_pos_vs_neg_p30"] = pd.DataFrame({"pos": summ(bpos), "neg": summ(bneg)})
    return out
