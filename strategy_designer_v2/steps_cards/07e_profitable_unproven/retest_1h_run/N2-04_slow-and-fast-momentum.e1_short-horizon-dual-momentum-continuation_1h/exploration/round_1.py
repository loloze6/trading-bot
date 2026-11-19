import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    coins = list(bars.keys())
    # --- book decomposition per coin
    rows = []
    allday = []
    for c in coins:
        dd = []
        for w, b in bars[c].items():
            b = b.copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            al = b.groupby("day")["postRebalance_current_allocation"].mean()
            d = days[c][w].copy()
            d["day"] = pd.to_datetime(d["day"]).dt.floor("D")
            d = d.set_index("day")
            d["alloc"] = al.reindex(d.index).shift(1)
            d["w"] = w
            d["year"] = d.index.year
            dd.append(d.reset_index())
        dd = pd.concat(dd)
        mu = dd["coin_return"].mean()
        dd["mkt"] = dd["alloc"] * mu
        dd["timing"] = dd["book_return"] - dd["mkt"]
        dd["coin"] = c
        allday.append(dd)
        rows.append(dict(coin=c, book_mean=dd.book_return.mean(), mkt_part=dd.mkt.mean(),
                         timing=dd.timing.mean(), coin_mean=mu, avg_alloc=dd.alloc.mean(),
                         t_book=dd.book_return.mean()/dd.book_return.std()*np.sqrt(dd.book_return.count())))
    out["per_coin"] = pd.DataFrame(rows).round(5)
    A = pd.concat(allday)
    out["per_year"] = A.groupby("year")[["book_return","mkt","timing","coin_return","alloc"]].mean().round(5)
    pw = A.groupby("w")[["book_return","mkt","timing","coin_return"]].mean()
    out["per_window"] = pw.round(5)
    out["share_top3_windows"] = float(pw.book_return.sort_values(ascending=False).head(3).sum()/pw.book_return.sum())
    # --- trades concentration
    T = pd.concat([trades[c][w].assign(coin=c) for c in coins for w in trades[c]])
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series(dict(n=len(T), sum=p.sum(), top10_sum=p.head(10).sum(), top5pct_sum=p.head(int(len(p)*0.05)).sum(),
                                   winrate=(p>0).mean(), med_dur_h=T.duration_minutes.median()/60))
    # --- forward excess returns at multiple horizons, graded by forecast
    res = []; grade = []
    for h in [24, 72, 168, 480]:
        recs = []
        for c in coins:
            g = []
            for w, b in bars[c].items():
                cl = b["close"].values; f = b["forecast"].values
                idx = np.arange(0, len(b)-h, h)
                g.append(pd.DataFrame({"r": cl[idx+h]/cl[idx]-1, "f": f[idx]}))
            g = pd.concat(g); g["ex"] = g.r - g.r.mean(); g["coin"]=c
            recs.append(g)
        R = pd.concat(recs)
        on = R[R.f > 0]; off = R[R.f <= 0]
        res.append(dict(h=h, n_on=len(on), ex_on=on.ex.mean(), t_on=stats.ttest_1samp(on.ex,0).statistic,
                        n_off=len(off), ex_off=off.ex.mean(), t_on_minus_off=stats.ttest_ind(on.r, off.r, equal_var=False).statistic))
        if h in (72, 168):
            on = on.copy(); on["q"] = pd.qcut(on.f.rank(method="first"), 3, labels=["lo","mid","hi"])
            gg = on.groupby("q").ex.agg(["count","mean","std"]); gg["t"]=gg["mean"]/(gg["std"]/np.sqrt(gg["count"]))
            gg.index = [f"h{h}_{i}" for i in gg.index]; grade.append(gg)
            if h == 72:
                pc = on.groupby("coin").ex.agg(["count","mean","std"]); pc["t"]=pc["mean"]/(pc["std"]/np.sqrt(pc["count"]))
                out["h72_on_by_coin"] = pc.round(4)
    out["fwd_by_h"] = pd.DataFrame(res).round(4)
    out["grade_by_forecast"] = pd.concat(grade).round(4)
    return out
