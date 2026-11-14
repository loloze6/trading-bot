def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    allrecs = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            d = data["days"][coin][w].copy()
            d["day"] = pd.to_datetime(d["day"]).dt.floor("D") if not np.issubdtype(d["day"].dtype, np.datetime64) else d["day"].dt.floor("D")
            b["day"] = b["day"].dt.tz_localize(None) if b["day"].dt.tz is not None else b["day"]
            try:
                d["day"] = d["day"].dt.tz_localize(None)
            except Exception:
                pass
            bb = b.groupby("day").last()[["forecast", "postRebalance_current_allocation", "close"]]
            bb["fc_prev"] = bb["forecast"].shift(1)
            bb["alloc_prev"] = bb["postRebalance_current_allocation"].shift(1)
            c = bb["close"]
            bb["ret20"] = c / c.shift(20) - 1
            bb["ret60"] = c / c.shift(60) - 1
            bb["vol20"] = c.pct_change().rolling(20).std()
            # bars since forecast became positive
            pos = (bb["forecast"] > 0).astype(int)
            grp = (pos != pos.shift()).cumsum()
            bb["age"] = pos.groupby(grp).cumcount() + 1
            bb.loc[pos == 0, "age"] = 0
            m = d.set_index("day")[["book_return", "coin_return"]].join(bb, how="left")
            m["coin"] = coin; m["w"] = w
            # prior-day features
            for col in ["ret20", "ret60", "vol20", "age"]:
                m[col + "_p"] = m[col].shift(1)
            allrecs.append(m)
    A = pd.concat(allrecs)
    A = A.dropna(subset=["book_return"])
    def summ(x):
        return pd.Series({"n": len(x), "mean_book": x.book_return.mean(), "mean_coin": x.coin_return.mean(),
                          "sh_book": x.book_return.mean()/x.book_return.std()*np.sqrt(365),
                          "sh_coin": x.coin_return.mean()/x.coin_return.std()*np.sqrt(365),
                          "share_long": (x.alloc_prev.abs() > 1e-9).mean(), "mean_alloc": x.alloc_prev.mean()})
    out["per_coin"] = A.groupby("coin").apply(summ)
    # by forecast bucket of prior day
    A["fcb"] = pd.cut(A["fc_prev"], [-0.01, 0.001, 5, 10, 15, 19.99, 20.01], labels=["0", "0-5", "5-10", "10-15", "15-20", "20"])
    out["by_fc_bucket"] = A.groupby("fcb").apply(summ)
    L = A[A.alloc_prev.abs() > 1e-9].copy()
    L["agebin"] = pd.cut(L["age_p"], [0, 20, 60, 120, 250, 5000])
    out["long_by_age"] = L.groupby("agebin").apply(summ)
    L["r20bin"] = pd.qcut(L["ret20_p"], 5)
    out["long_by_ret20"] = L.groupby("r20bin").apply(summ)
    L["volbin"] = pd.qcut(L["vol20_p"], 5)
    out["long_by_vol20"] = L.groupby("volbin").apply(summ)
    A["year"] = A.index.year
    out["by_year"] = A.groupby("year").apply(summ)
    # drawdowns per coin: chained book within windows order
    dd = []
    for coin, g in A.groupby("coin", sort=False):
        eq = (1 + g.book_return.fillna(0)).cumprod()
        peak = eq.cummax(); ddr = eq/peak - 1
        trough = ddr.values.argmin()
        pk = eq.values[:trough+1].argmax()
        seg = g.iloc[pk:trough+1]
        dd.append({"coin": coin, "maxdd": ddr.min(), "days": trough-pk, "coin_ret_during": (1+seg.coin_return).prod()-1,
                   "mean_fc_during": seg.fc_prev.mean(), "share_long": (seg.alloc_prev.abs()>1e-9).mean(),
                   "mean_age_long": seg.loc[seg.alloc_prev.abs()>1e-9, "age_p"].mean(),
                   "ret60_at_peak": seg.ret60.iloc[0] if len(seg) else np.nan})
    out["deepest_falls"] = pd.DataFrame(dd)
    # trades fees
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    out["trades"] = pd.Series({"n": len(T), "mean_gross": T.profit_loss_percent.mean(), "mean_net": T.net_profit_loss_percent.mean(),
                               "mean_comm": T.total_commission.mean(), "median_dur_days": T.duration_minutes.median()/1440})
    return out
