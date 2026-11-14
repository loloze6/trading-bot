import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        # coin mean daily return over all windows
        dr = []
        for w, b in wins.items():
            c = b["close"].values
            dr.append(np.diff(c) / c[:-1])
        mu = np.nanmean(np.concatenate(dr))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            alloc = b["postRebalance_current_allocation"].values
            fc = b["forecast"].values
            raw = b["debug_info.components.below_ma.last_history_value"].values
            n = len(b)
            # bars since forecast turned negative
            since = np.full(n, np.nan); cnt = 0
            for i in range(n):
                if fc[i] < 0:
                    cnt += 1; since[i] = cnt
                else:
                    cnt = 0
            for s in range(0, n - 10, 10):
                r = c[s + 10] / c[s] - 1
                mom20 = c[s] / c[s - 20] - 1 if s >= 20 else np.nan
                rows.append(dict(coin=coin, win=w, year=pd.Timestamp(b["timestamp"].iloc[s]).year,
                                 alloc=alloc[s], fc=fc[s], raw=raw[s], since=since[s],
                                 ex=r - 10 * mu, ret=r, mom20=mom20))
    d = pd.DataFrame(rows)
    a = d[d["alloc"] != 0].copy()
    a["gain"] = a["alloc"] * a["ex"]
    a["shortex"] = -a["ex"]  # excess fall
    def summ(g):
        x = g["shortex"]
        return pd.Series({"n": len(x), "mean_fall": x.mean(), "t": stats.ttest_1samp(x, 0).statistic if len(x) > 2 else np.nan,
                          "hit": (x > 0).mean(), "sd": x.std(), "mean_alloc": g["alloc"].mean()})
    out = {}
    out["all_active"] = summ(a)
    out["by_coin"] = a.groupby("coin").apply(summ)
    out["by_year"] = a.groupby("year").apply(summ)
    out["by_fc_bucket"] = a.groupby(pd.cut(a["fc"], [-20.01, -10, -5, -2, -1, 0])).apply(summ)
    out["by_raw_bucket"] = a.groupby(pd.qcut(a["raw"], 5, duplicates="drop")).apply(summ)
    out["by_since_cross"] = a.groupby(pd.cut(a["since"], [0, 10, 30, 60, 120, 1e4])).apply(summ)
    out["by_mom20"] = a.groupby(pd.qcut(a["mom20"], 4)).apply(summ)
    out["by_window"] = a.groupby("win").apply(summ)
    out["flat_blocks_mean_ex"] = pd.Series({"n": (d["alloc"] == 0).sum(), "mean_ex": d.loc[d["alloc"] == 0, "ex"].mean()})
    return out
