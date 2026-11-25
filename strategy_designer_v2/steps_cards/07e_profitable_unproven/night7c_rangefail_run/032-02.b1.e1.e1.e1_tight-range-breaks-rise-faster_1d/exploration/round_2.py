import numpy as np, pandas as pd
from scipy import stats

def welch(a, b):
    a = pd.Series(a).dropna(); b = pd.Series(b).dropna()
    if len(a) < 3 or len(b) < 3: return np.nan
    return stats.ttest_ind(a, b, equal_var=False).statistic

def tone(x):
    x = pd.Series(x).dropna()
    return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    H = [5, 10, 20]
    # drift per coin, horizon (non-overlapping)
    dr = {}
    for h in H:
        for c in coins:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            dr[(c, h)] = np.mean(rs)
    res = {}; grads = {}
    for h in H:
        cases = []
        for c in coins:
            for w, b in bars[c].items():
                cl = b["close"].values; n = len(cl)
                lr = np.abs(np.diff(np.log(cl)))
                for g in range(0, n, h):
                    for t in range(max(g, 60), min(g + h, n)):
                        pm = cl[t-60:t].max(); pmin = cl[t-60:t].min()
                        if cl[t] > pm:
                            if t + h < n:
                                cases.append({"coin": c, "window": w,
                                              "dist": cl[t]/pm - 1,
                                              "ret60": cl[t]/cl[t-60] - 1,
                                              "W": (np.log(pm) - np.log(pmin)) / lr[t-60:t].mean(),
                                              "fresh": int(cl[t-1] <= cl[max(0, t-61):t-1].max()),
                                              "u": cl[t+h]/cl[t] - 1 - dr[(c, h)]})
                            break
        C = pd.DataFrame(cases)
        res[(h, "all")] = {"n": len(C), "mean_u": C.u.mean(), "t": tone(C.u)}
        nx = C[C.coin != "XRPUSD"]
        res[(h, "noXRP")] = {"n": len(nx), "mean_u": nx.u.mean(), "t": tone(nx.u)}
        nw = C[C.window != "w17"]
        res[(h, "no_w17")] = {"n": len(nw), "mean_u": nw.u.mean(), "t": tone(nw.u)}
        for f in ["dist", "ret60", "W"]:
            med = C.groupby("coin")[f].transform("median")
            lo = C[C[f] <= med].u; hi = C[C[f] > med].u
            grads[(h, f)] = {"low_half_u": lo.mean(), "high_half_u": hi.mean(),
                             "high_minus_low": hi.mean() - lo.mean(), "welch_t": welch(hi, lo), "n": len(C)}
            nxm = nx.groupby("coin")[f].transform("median")
            grads[(h, f + "_noXRP")] = {"low_half_u": nx[nx[f] <= nxm].u.mean(), "high_half_u": nx[nx[f] > nxm].u.mean(),
                                        "high_minus_low": nx[nx[f] > nxm].u.mean() - nx[nx[f] <= nxm].u.mean(),
                                        "welch_t": welch(nx[nx[f] > nxm].u, nx[nx[f] <= nxm].u), "n": len(nx)}
        if h == 10:
            C["dq"] = C.groupby("coin")["dist"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
            out["h10_by_dist_tercile"] = C.groupby("dq").agg(n=("u", "count"), dist=("dist", "mean"), u=("u", "mean"))
            C["rq"] = C.groupby("coin")["ret60"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
            out["h10_by_ret60_tercile"] = C.groupby("rq").agg(n=("u", "count"), ret60=("ret60", "mean"), u=("u", "mean"))
            out["h10_by_coin"] = C.groupby("coin").agg(n=("u", "count"), u=("u", "mean"))
            out["h10_fresh"] = C.groupby("fresh").agg(n=("u", "count"), u=("u", "mean"))
    out["grid_horizons"] = pd.DataFrame(res).T
    out["grid_grading"] = pd.DataFrame(grads).T
    # book robustness
    rows = []
    for c in coins:
        for w, d in days[c].items():
            rows.append(d.assign(coin=c, window=w))
    D = pd.concat(rows).dropna(subset=["book_return"])
    D["day"] = pd.to_datetime(D["day"]).dt.floor("D")
    def sharpe(sub):
        bk = sub.groupby(["window", "day"])["book_return"].mean()
        return bk.mean() / bk.std() * np.sqrt(365)
    out["book_sharpe"] = pd.Series({"all": sharpe(D), "noXRP": sharpe(D[D.coin != "XRPUSD"]),
                                    "noETH": sharpe(D[D.coin != "ETHUSD"]),
                                    "no_w17": sharpe(D[D.window != "w17"]),
                                    "no_w11": sharpe(D[D.window != "w11"])})
    bk = D.groupby(["window", "day"])["book_return"].mean().sort_values(ascending=False)
    out["book_days"] = pd.Series({"n_days": len(bk), "sum": bk.sum(), "top10_days_sum": bk.head(10).sum(),
                                  "top30_days_sum": bk.head(30).sum()})
    return out
