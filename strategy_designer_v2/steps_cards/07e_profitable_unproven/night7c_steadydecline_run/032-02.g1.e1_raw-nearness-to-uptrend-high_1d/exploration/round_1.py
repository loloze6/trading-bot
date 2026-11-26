def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # coin mean daily return over all windows
    rows = []
    for c in bars:
        allr = []
        for w, b in bars[c].items():
            r = b["close"].pct_change().shift(-1)
            allr.append(r.dropna())
        mu = pd.concat(allr).mean()
        for w, b in bars[c].items():
            b = b.copy()
            fr = b["close"].shift(-1) / b["close"] - 1
            a = b["postRebalance_current_allocation"].fillna(0)
            g = a * fr
            yr = pd.to_datetime(b["timestamp"]).dt.year
            ret28 = b["close"] / b["close"].shift(28) - 1
            df = pd.DataFrame({"coin": c, "w": w, "yr": yr, "gain": g, "mkt": a * mu, "a": a,
                               "fr": fr, "ret28": ret28, "fc": b["forecast"]})
            rows.append(df.dropna(subset=["gain"]))
    D = pd.concat(rows)
    D["timing"] = D["gain"] - D["mkt"]
    out["decomp_overall"] = pd.Series({"mean_gain": D.gain.mean(), "mkt_part": D.mkt.mean(),
                                       "timing": D.timing.mean(),
                                       "t_timing": D.timing.mean() / (D.timing.std() / np.sqrt(len(D))),
                                       "share_in_pos": (D.a.abs() > 0).mean()})
    out["by_coin"] = D.groupby("coin")[["gain", "mkt", "timing"]].mean() * 1e4
    out["by_window"] = D.groupby("w")[["gain", "mkt", "timing"]].mean() * 1e4
    out["by_year"] = D.groupby("yr")[["gain", "mkt", "timing"]].mean() * 1e4
    # concentration: top days
    g = D.groupby(["w", "yr"]).size()
    s = D.gain.sort_values(ascending=False)
    out["top_share"] = pd.Series({"sum_all": s.sum(), "top20_days_sum": s.head(20).sum(),
                                  "top50_sum": s.head(50).sum(), "n": len(s)})
    # trades
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(p), "sum": p.sum(), "top10": p.head(10).sum(),
                               "win_share": (p > 0).mean(), "median": p.median()})
    # forward returns on grid by horizon: trending vs not, and slopes on ret28 and forecast
    res = []
    for h in [5, 10, 20]:
        recs = []
        for c in bars:
            for w, b in bars[c].items():
                cl = b["close"].reset_index(drop=True)
                fr = cl.shift(-h) / cl - 1
                r28 = cl / cl.shift(28) - 1
                hi = cl.rolling(28, min_periods=28).max()
                prox = 1 / (1 + 100 * (1 - cl / hi))
                idx = np.arange(0, len(cl), h)
                recs.append(pd.DataFrame({"coin": c, "fr": fr.iloc[idx].values, "r28": r28.iloc[idx].values,
                                          "prox": prox.iloc[idx].values,
                                          "fc": b["forecast"].reset_index(drop=True).iloc[idx].values}))
        R = pd.concat(recs).dropna(subset=["fr"])
        R["ex"] = R.fr - R.groupby("coin").fr.transform("mean")
        R = R.dropna()
        up = R[R.r28 > 0]; dn = R[R.r28 <= 0]
        tt = stats.ttest_ind(up.ex, dn.ex, equal_var=False)
        sl_r = stats.linregress(R.r28, R.ex)
        sl_ru = stats.linregress(up.r28, up.ex)
        sl_p = stats.linregress(up.prox, up.ex)
        sl_f = stats.linregress(up.fc, up.ex)
        res.append({"h": h, "n_up": len(up), "ex_up": up.ex.mean(), "n_dn": len(dn), "ex_dn": dn.ex.mean(),
                    "t_up_minus_dn": tt.statistic, "t_slope_r28_all": sl_r.slope / sl_r.stderr,
                    "t_slope_r28_up": sl_ru.slope / sl_ru.stderr, "t_slope_prox_up": sl_p.slope / sl_p.stderr,
                    "t_slope_fc_up": sl_f.slope / sl_f.stderr})
    out["horizons"] = pd.DataFrame(res)
    return out
