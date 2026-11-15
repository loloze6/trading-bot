def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    dc = "debug_info.components.below_ma.last_history_value"
    mdr = {c: pd.concat([df["close"].pct_change().dropna() for df in bars[c].values()]).mean() for c in bars}
    rows = []
    h = 10
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            d = df[dc].values if dc in df else np.full(len(df), np.nan)
            sma = cl / (1 + d / 100.0)
            lr = np.log(cl)
            for i in range(0, len(df) - h, h):
                ex = cl[i + h] / cl[i] - 1 - h * mdr[c]
                sl50 = sma[i] / sma[i - 50] - 1 if i >= 50 else np.nan
                vol = np.std(np.diff(lr[i - 30:i + 1])) if i >= 30 else np.nan
                d10 = d[i] - d[i - 10] if i >= 10 else np.nan
                rows.append(dict(coin=c, f=df["forecast"].iloc[i], d=d[i], ex=ex, sl50=sl50, vol=vol, d10=d10,
                                 a=df["postRebalance_current_allocation"].iloc[i]))
    R = pd.DataFrame(rows)
    def tt(s):
        s = s.dropna()
        return pd.Series(dict(n=len(s), mean=s.mean(), t=s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan))
    out = {}
    act = R[R.f < 0].copy()
    med = act["d"].median()
    act["depth"] = np.where(act["d"] > med, "shallow", "deep")
    act["sl50q"] = pd.qcut(act["sl50"], 3, labels=["fall_fast", "fall_mid", "rise_or_flat"])
    out["ex_by_sl50_depth"] = act.groupby(["sl50q", "depth"])["ex"].apply(tt).unstack()
    act["volq"] = pd.qcut(act["vol"], 3, labels=["lowvol", "midvol", "highvol"])
    out["ex_by_vol_depth"] = act.groupby(["volq", "depth"])["ex"].apply(tt).unstack()
    act["d10s"] = np.where(act["d10"] < 0, "sinking", "recovering")
    out["ex_by_d10_depth"] = act.groupby(["d10s", "depth"])["ex"].apply(tt).unstack()
    # book: market part vs timing
    b = []
    for c in days:
        cm = pd.concat([df["coin_return"].dropna() for df in days[c].values()]).mean()
        for w, df in days[c].items():
            bdf = bars[c][w]
            pos = bdf.groupby(pd.to_datetime(bdf["timestamp"]).dt.floor("D"))["postRebalance_current_allocation"].last()
            pos = pos.shift(1).reindex(pd.to_datetime(df["day"]).dt.floor("D")).values
            b.append(pd.DataFrame(dict(br=df["book_return"].values, pos=pos, cm=cm)))
    B = pd.concat(b).dropna()
    out["book_mean"] = B["br"].mean()
    out["book_market_part"] = (B["pos"] * B["cm"]).mean()
    out["book_timing_part"] = B["br"].mean() - (B["pos"] * B["cm"]).mean()
    return out
