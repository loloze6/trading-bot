def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    def tod(s):
        return pd.to_datetime(s, utc=True).dt.tz_localize(None).dt.floor("D")
    allrecs = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy()
            b["day"] = tod(b["timestamp"])
            d = data["days"][coin][w].copy()
            d["day"] = tod(d["day"])
            bb = b.groupby("day").last()[["forecast", "postRebalance_current_allocation", "close"]]
            c = bb["close"]
            bb["ret20"] = c / c.shift(20) - 1
            bb["ret60"] = c / c.shift(60) - 1
            bb["vol20"] = c.pct_change().rolling(20).std()
            bb["dd60"] = c / c.rolling(60, min_periods=10).max() - 1
            pos = (bb["forecast"] > 0).astype(int)
            grp = (pos != pos.shift()).cumsum()
            bb["age"] = pos.groupby(grp).cumcount() + 1
            bb.loc[pos == 0, "age"] = 0
            feats = ["forecast", "postRebalance_current_allocation", "ret20", "ret60", "vol20", "dd60", "age"]
            bp = bb[feats].shift(1)
            bp.columns = [x + "_p" for x in feats]
            m = d.set_index("day")[["book_return", "coin_return"]].join(bp, how="left")
            m["coin"] = coin; m["w"] = w
            allrecs.append(m)
    A = pd.concat(allrecs)
    A = A.dropna(subset=["book_return", "coin_return"])
    A["alloc_prev"] = A["postRebalance_current_allocation_p"]
    def summ(x):
        sb = x.book_return.std(); sc = x.coin_return.std()
        return pd.Series({"n": len(x), "mean_book": x.book_return.mean(), "mean_coin": x.coin_return.mean(),
                          "sh_book": x.book_return.mean()/sb*np.sqrt(365) if sb > 0 else np.nan,
                          "sh_coin": x.coin_return.mean()/sc*np.sqrt(365),
                          "t_coin": x.coin_return.mean()/(sc/np.sqrt(len(x))),
                          "share_long": (x.alloc_prev.abs() > 1e-9).mean(), "mean_alloc": x.alloc_prev.mean()})
    out["per_coin"] = A.groupby("coin").apply(summ)
    A["fcb"] = pd.cut(A["forecast_p"], [-0.01, 0.001, 5, 10, 15, 19.99, 20.01], labels=["0", "0-5", "5-10", "10-15", "15-20", "20"])
    out["by_fc_bucket"] = A.groupby("fcb", observed=True).apply(summ)
    L = A[A.alloc_prev.abs() > 1e-9].copy()
    L["agebin"] = pd.cut(L["age_p"], [0, 20, 60, 120, 250, 5000])
    out["long_by_age"] = L.groupby("agebin", observed=True).apply(summ)
    L["r20bin"] = pd.qcut(L["ret20_p"], 5)
    out["long_by_ret20"] = L.groupby("r20bin", observed=True).apply(summ)
    L["volbin"] = pd.qcut(L["vol20_p"], 5)
    out["long_by_vol20"] = L.groupby("volbin", observed=True).apply(summ)
    L["ddbin"] = pd.qcut(L["dd60_p"], 5)
    out["long_by_dd60"] = L.groupby("ddbin", observed=True).apply(summ)
    F = A[A.alloc_prev.abs() <= 1e-9].copy()
    F["r20bin"] = pd.qcut(F["ret20_p"], 5)
    out["flat_by_ret20"] = F.groupby("r20bin", observed=True).apply(summ)
    A["year"] = A.index.year
    out["by_year"] = A.groupby("year").apply(summ)
    dd = []
    for coin, g in A.groupby("coin", sort=False):
        eq = (1 + g.book_return).cumprod()
        ddr = eq / eq.cummax() - 1
        tr = int(ddr.values.argmin()); pk = int(eq.values[:tr+1].argmax())
        seg = g.iloc[pk:tr+1]
        dd.append({"coin": coin, "maxdd": ddr.min(), "days": tr-pk, "book_ret": (1+seg.book_return).prod()-1,
                   "coin_ret_during": (1+seg.coin_return).prod()-1,
                   "share_long": (seg.alloc_prev.abs() > 1e-9).mean(), "mean_alloc": seg.alloc_prev.mean(),
                   "mean_fc": seg.forecast_p.mean(), "mean_age_long": seg.loc[seg.alloc_prev.abs() > 1e-9, "age_p"].mean(),
                   "ret60_at_peak": seg.ret60_p.iloc[0], "vol20_at_peak": seg.vol20_p.iloc[0]})
    out["deepest_falls"] = pd.DataFrame(dd)
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    out["trades"] = pd.Series({"n": len(T), "mean_gross": T.profit_loss_percent.mean(), "mean_net": T.net_profit_loss_percent.mean(),
                               "mean_comm": T.total_commission.mean(), "median_dur_days": T.duration_minutes.median()/1440,
                               "share_win_net": (T.net_profit_loss_percent > 0).mean()})
    out["alloc_by_fc"] = A.groupby("fcb", observed=True)["alloc_prev"].describe()
    return out
