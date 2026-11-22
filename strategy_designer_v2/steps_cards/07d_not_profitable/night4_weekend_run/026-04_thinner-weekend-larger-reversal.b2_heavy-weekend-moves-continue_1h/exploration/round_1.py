def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # exposure and allocation
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            a = b["postRebalance_current_allocation"].fillna(0)
            rows.append(dict(coin=c, w=w, n=len(b), inpos=(a.abs() > 1e-6).mean(),
                             absalloc_in=a[a.abs() > 1e-6].abs().mean()))
    r = pd.DataFrame(rows)
    out["exposure_by_coin"] = r.groupby("coin")[["inpos", "absalloc_in"]].mean()
    # book daily returns: per day mean across coins, per window
    dd = []
    for c in days:
        for w, d in days[c].items():
            x = d[["day", "book_return", "coin_return"]].copy(); x["w"] = w; x["coin"] = c
            dd.append(x)
    D = pd.concat(dd)
    B = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    B["wn"] = B["w"].str[1:].astype(int)
    B = B.sort_values(["wn", "day"])
    out["book_by_window"] = B.groupby("wn").agg(book_mean=("book_return", "mean"),
                                                 coin_mean=("coin_return", "mean"),
                                                 ndays=("book_return", "size"))
    eq = (1 + B["book_return"].fillna(0)).cumprod().values
    peak = np.maximum.accumulate(eq); ddn = eq / peak - 1
    i = ddn.argmin(); j = eq[:i + 1].argmax()
    out["deepest_fall"] = f"depth {ddn[i]:.4f}, from window {B['wn'].iloc[j]} to window {B['wn'].iloc[i]}, length {i-j} days"
    # cases: Sunday 23:00 bars with forecast != 0; forward path
    cs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values; v = b["volume"].values
            idx = np.where((ts.dt.dayofweek == 6) & (ts.dt.hour == 23) & (b["forecast"].fillna(0) != 0))[0]
            for k in idx:
                s = np.sign(b["forecast"].iloc[k])
                rec = dict(coin=c, wn=int(w[1:]), f=b["forecast"].iloc[k], s=s,
                           alloc=b["postRebalance_current_allocation"].iloc[k])
                if k >= 48:
                    rec["wk_ret"] = cl[k] / cl[k - 48] - 1
                    rec["vr"] = v[k-47:k+1].mean() / v[max(0,k-167):k-47].mean() if k >= 167 else np.nan
                for h in [6, 12, 24, 48, 72, 96, 120]:
                    rec[f"r{h}"] = s * (cl[k + h] / cl[k] - 1) if k + h < len(cl) else np.nan
                if k >= 48:
                    # Friday move preceding weekend (24h before weekend) as context
                    rec["fri_ret_signed"] = s * (cl[k-48] / cl[k-72] - 1) if k >= 72 else np.nan
                cs.append(rec)
    C = pd.DataFrame(cs)
    def tt(x):
        x = x.dropna(); return pd.Series(dict(mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))), n=len(x)))
    out["signed_path_by_h"] = pd.DataFrame({h: tt(C[f"r{h}"]) for h in [6,12,24,48,72,96,120]}).T
    C["incr_48_120"] = C["r120"] - C["r48"]
    out["signed_48_to_120_increment"] = tt(C["incr_48_120"])
    C["fq"] = pd.qcut(C["f"].abs(), 4, labels=False, duplicates="drop")
    out["r48_by_absforecast_q"] = C.groupby("fq")["r48"].apply(tt).unstack()
    out["r48_by_vr_q"] = C.groupby(pd.qcut(C["vr"], 4, labels=False))["r48"].apply(tt).unstack()
    C["mq"] = pd.qcut(C["wk_ret"].abs(), 4, labels=False)
    out["r48_by_absmove_q"] = C.groupby("mq")["r48"].apply(tt).unstack()
    out["r48_by_side"] = C.groupby("s")["r48"].apply(tt).unstack()
    out["r48_by_coin"] = C.groupby("coin")["r48"].apply(tt).unstack()
    out["r48_by_fri_signed_sign"] = C.groupby(np.sign(C["fri_ret_signed"]))["r48"].apply(tt).unstack()
    out["mean_absalloc_cases"] = C["alloc"].abs().mean()
    # trades
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values() if len(t)])
    out["trades"] = pd.Series(dict(n=len(T), mean_gross=T["profit_loss_percent"].mean(),
                                   mean_net=T["net_profit_loss_percent"].mean(),
                                   win=(T["net_profit_loss_percent"] > 0).mean(),
                                   dur_h=T["duration_minutes"].mean()/60,
                                   worst=T["net_profit_loss_percent"].min()))
    return out
