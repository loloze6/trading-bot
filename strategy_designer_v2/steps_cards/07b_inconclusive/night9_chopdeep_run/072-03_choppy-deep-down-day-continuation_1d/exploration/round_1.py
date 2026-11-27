import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi = c.rolling(20, min_periods=20).max()
            sd = r1.rolling(20, min_periods=20).std()
            depth = (c - hi) / hi / sd
            reg = b["regime"].astype(str)
            choppy = reg.isin(["trending", "unknown"])
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                              "r1": r1, "depth": depth, "choppy": choppy,
                              "alloc": b["postRebalance_current_allocation"].astype(float),
                              "fc": b["forecast"].astype(float)})
            for h in [1, 2, 3, 5, 10]:
                d[f"f{h}"] = c.shift(-h) / c - 1 - ((1 + mu) ** h - 1)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D[D["choppy"] & D["depth"].notna()]
    D["down"] = D["r1"] < 0
    D["q"] = D.groupby("down")["depth"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out = {}
    # depth quintile x up/down: next-day excess (short gain = -f1)
    g = D.groupby(["down", "q"])
    out["quint_f1"] = g.agg(n=("f1", "count"), depth=("depth", "mean"), f1=("f1", "mean"),
                            t=("f1", lambda x: x.mean() / x.std() * np.sqrt(x.count())))
    # horizons, non-overlapping grid, down days, deepest 40% vs shallowest 40%
    hz = []
    for h in [1, 2, 3, 5, 10]:
        for dn in [True, False]:
            s = D[(D["pos"] % h == 0) & (D["down"] == dn)].dropna(subset=[f"f{h}"])
            deep = s[s["q"] <= 1][f"f{h}"]; sh = s[s["q"] >= 3][f"f{h}"]
            corr, p = stats.spearmanr(s["depth"], s[f"f{h}"])
            tt = stats.ttest_ind(deep, sh, equal_var=False)
            hz.append({"h": h, "down": dn, "n": len(s), "deep": deep.mean(), "shallow": sh.mean(),
                       "t_diff": tt.statistic, "spearman_depth_vs_ret": corr, "p": p})
    out["horizons"] = pd.DataFrame(hz)
    dd = D[D["down"]].dropna(subset=["f1"])
    out["by_coin_down"] = dd.groupby("coin").apply(lambda s: pd.Series({
        "n": len(s), "rho": stats.spearmanr(s["depth"], s["f1"])[0],
        "deep_f1": s[s["q"] <= 1]["f1"].mean(), "shallow_f1": s[s["q"] >= 3]["f1"].mean()}))
    out["by_win_down"] = dd.groupby("win").apply(lambda s: pd.Series({
        "n": len(s), "rho": stats.spearmanr(s["depth"], s["f1"])[0], "mean_f1": s["f1"].mean()}))
    act = D[D["alloc"].abs() > 0].dropna(subset=["f1"])
    out["active"] = pd.Series({"n": len(act), "gain": (act["alloc"] * act["f1"]).mean(),
                               "rho_fc_f1": stats.spearmanr(act["fc"], act["f1"])[0]})
    return out
