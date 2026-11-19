def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    grid = []
    for coin in data["bars"]:
        # coin mean daily return over all windows
        cr = pd.concat([data["days"][coin][w]["coin_return"] for w in data["days"][coin]]).dropna()
        mu_d = cr.mean()
        br = pd.concat([data["days"][coin][w]["book_return"] for w in data["days"][coin]]).dropna()
        # mean held position per day (last bar) approx -> use bar mean allocation
        allocs = []; fees = 0; pv0 = []
        gross = []; 
        for w, b in data["bars"][coin].items():
            a = b["postRebalance_current_allocation"].fillna(0)
            r = b["close"].shift(-1) / b["close"] - 1
            gross.append((a * r).dropna())
            allocs.append(a)
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            fees += fee.clip(lower=0).sum()
            c = b["close"].values
            ret72 = b["close"] / b["close"].shift(72) - 1
            vs = b["debug_info.components.vol_share.post_pipeline_value"]
            raw = b["debug_info.components.vol_share.last_history_value"]
            for i in range(0, len(b) - 72, 72):
                grid.append(dict(coin=coin, w=w, fwd=c[i+72]/c[i]-1, past=ret72.iloc[i],
                                 reg=b["regime"].iloc[i], pp=vs.iloc[i], raw=raw.iloc[i]))
        A = pd.concat(allocs); G = pd.concat(gross)
        nbars = len(A)
        rows.append(dict(coin=coin, book_mean_d=br.mean(), coin_mean_d=mu_d,
                         mean_alloc=A.mean(), share_short=(A < 0).mean(),
                         gross_per_day=G.mean()*24, fee_per_day=fees/nbars*24,
                         drift_part_d=A.mean()*mu_d))
    out["per_coin"] = pd.DataFrame(rows).set_index("coin")
    g = pd.DataFrame(grid)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    out["fwd_by_regime"] = g.groupby("reg")["ex"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    r = g[g["reg"] == "mean_reversion"].dropna(subset=["past"]).copy()
    r["past_q"] = pd.qcut(r["past"], 5, labels=False)
    out["risen_by_pastret_q"] = r.groupby("past_q")["ex"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    r2 = r.dropna(subset=["raw"]).copy()
    r2["raw_q"] = pd.qcut(r2["raw"], 5, labels=False)
    out["risen_by_rawshare_q"] = r2.groupby("raw_q")["ex"].agg(["mean", "count"])
    r2["pp_q"] = pd.qcut(r2["pp"], 5, labels=False, duplicates="drop")
    out["risen_by_pp_q"] = r2.groupby("pp_q")["ex"].agg(["mean", "count"])
    allg = g.dropna(subset=["past"]).copy()
    allg["past_q"] = pd.qcut(allg["past"], 5, labels=False)
    out["all_by_pastret_q"] = allg.groupby("past_q")[["past", "ex"]].mean()
    return out
