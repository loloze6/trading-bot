import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    res = []; grad = []; age = []; coinr = []
    for h in [1, 5, 10, 20]:
        allA = []
        for c, wb in data["bars"].items():
            parts = []
            for w, b in wb.items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                r = cl[idx + h] / cl[idx] - 1
                bir = pd.to_numeric(b["debug_info.bars_in_regime"], errors="coerce").values[idx]
                s = b["debug_info.components.slow.post_pipeline_value"].values[idx] if "debug_info.components.slow.post_pipeline_value" in b else np.full(len(idx), np.nan)
                m = b["debug_info.components.medium.post_pipeline_value"].values[idx] if "debug_info.components.medium.post_pipeline_value" in b else np.full(len(idx), np.nan)
                parts.append(pd.DataFrame({"r": r, "f": b["forecast"].values[idx], "bir": bir,
                                           "slow": s, "med": m, "window": w}))
            A = pd.concat(parts); A["ex"] = A.r - A.r.mean(); A["coin"] = c
            allA.append(A)
        A = pd.concat(allA)
        act = A[A.f > 0].copy()
        # forecast terciles
        act["fq"] = pd.qcut(act.f.rank(method="first"), 3, labels=["low", "mid", "high"])
        for q, g in act.groupby("fq", observed=True):
            grad.append({"h": h, "fq": str(q), "mean_ex": g.ex.mean(),
                         "t": g.ex.mean()/(g.ex.std()/np.sqrt(len(g))), "n": len(g), "mean_f": g.f.mean()})
        # trend age
        act["age"] = pd.cut(act.bir, [-1, 10, 30, 60, 10000], labels=["0-10", "11-30", "31-60", ">60"])
        for q, g in act.groupby("age", observed=True):
            age.append({"h": h, "age": str(q), "mean_ex": g.ex.mean(),
                        "t": g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g) > 2 else np.nan, "n": len(g)})
        if h == 5:
            for c, g in act.groupby("coin"):
                coinr.append({"coin": c, "mean_ex": g.ex.mean(), "t": g.ex.mean()/(g.ex.std()/np.sqrt(len(g))), "n": len(g)})
            sl = act.dropna(subset=["slow", "med"])
            out["h5_slow_vs_med_corr"] = pd.Series({"corr_ex_slow": stats.spearmanr(sl.ex, sl.slow).correlation,
                                                    "corr_ex_med": stats.spearmanr(sl.ex, sl.med).correlation,
                                                    "corr_ex_f": stats.spearmanr(act.ex, act.f).correlation, "n": len(sl)})
    out["graded_by_forecast"] = pd.DataFrame(grad)
    out["by_trend_age"] = pd.DataFrame(age)
    out["h5_per_coin"] = pd.DataFrame(coinr)
    # book without the top trades: share of book days carried by top-decile book days
    rows = []
    for c, wd in data["days"].items():
        for w, d in wd.items():
            rows.append(d.assign(coin=c, window=w))
    D = pd.concat(rows).dropna(subset=["book_return"])
    book = D.groupby(["window", "day"]).book_return.mean().sort_values(ascending=False)
    tot = book.sum()
    out["book_day_conc"] = pd.Series({"total": tot, "top1pct_share": book.head(int(len(book)*0.01)).sum()/tot,
                                      "top5pct_share": book.head(int(len(book)*0.05)).sum()/tot,
                                      "mean_ex_top29": book.iloc[29:].mean(), "n": len(book)})
    return out
