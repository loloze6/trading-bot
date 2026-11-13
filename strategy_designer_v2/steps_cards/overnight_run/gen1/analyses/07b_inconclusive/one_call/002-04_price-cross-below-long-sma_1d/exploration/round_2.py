import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        dr = []
        for w, b in wins.items():
            c = b["close"].values
            dr.append(np.diff(c) / c[:-1])
        mu = np.nanmean(np.concatenate(dr))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            raw = b["debug_info.components.below_ma.last_history_value"].values.astype(float)
            sma = c / (1 + raw / 100.0)
            alloc = b["postRebalance_current_allocation"].values
            ts = pd.to_datetime(b["timestamp"]).dt.floor("D")
            n = len(b)
            for s in range(0, n - 10, 10):
                r = c[s + 10] / c[s] - 1
                sl20 = sma[s] / sma[s - 20] - 1 if s >= 20 else np.nan
                rows.append(dict(coin=coin, win=w, ts=ts.iloc[s], alloc=alloc[s], below=raw[s] < 0,
                                 sl20=sl20, ex=r - 10 * mu, absret=abs(r)))
    d = pd.DataFrame(rows)
    # breadth: share of coins below SMA at same day (using all bars)
    br = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            br.append(pd.DataFrame({"ts": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                                    "below": (b["debug_info.components.below_ma.last_history_value"] < 0).astype(float)}))
    br = pd.concat(br).groupby("ts")["below"].mean()
    d["breadth"] = d["ts"].map(br)
    a = d[d["alloc"] != 0].copy()
    a["fall"] = -a["ex"]
    def summ(g):
        x = g["fall"]
        return pd.Series({"n": len(x), "mean_fall": x.mean(),
                          "t": stats.ttest_1samp(x, 0).statistic if len(x) > 2 else np.nan,
                          "hit": (x > 0).mean(), "sd": x.std()})
    out = {}
    out["by_sma_slope20"] = a.groupby(pd.cut(a["sl20"], [-1, -0.05, -0.02, 0, 0.02, 1])).apply(summ)
    out["slope_sign"] = a.groupby(a["sl20"] < 0).apply(summ)
    out["by_breadth"] = a.groupby(pd.cut(a["breadth"], [-0.01, 0.34, 0.67, 0.84, 1.0])).apply(summ)
    a["both"] = (a["sl20"] < 0) & (a["breadth"] > 0.67)
    out["slope_neg_and_breadth_high"] = a.groupby("both").apply(summ)
    out["both_by_coin"] = a[a["both"]].groupby("coin").apply(summ)
    out["both_by_year"] = a[a["both"]].groupby(a["ts"].dt.year).apply(summ)
    out["slope_neg_by_year"] = a[a["sl20"] < 0].groupby(a["ts"].dt.year).apply(summ)
    out["corr_absret_vs_mean"] = pd.Series({"sd_all_active": a["fall"].std(), "mean_abs_ex": a["fall"].abs().mean()})
    return out
