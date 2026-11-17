def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 30
    # coin mean h-bar return over non-overlapping grid pooled across windows
    def coin_mean(coin, h):
        r = []
        for w, df in bars[coin].items():
            c = df["close"].values
            for i in range(0, len(c) - h, h):
                r.append(c[i+h]/c[i]-1)
        return np.mean(r) if r else np.nan
    rows = []
    for coin in bars:
        cm = {h: coin_mean(coin, h) for h in (10, 20, 30, 60)}
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values
            prevmax = pd.Series(hi).cummax().shift(1).values
            trend = (df["regime"] == "trending").values
            ok = trend & (c > np.nan_to_num(prevmax, nan=-np.inf))
            last = -10**9
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in np.where(ok)[0]:
                if i - last < H or i + H >= len(c):
                    continue
                last = i
                rec = dict(coin=coin, w=int(w[1:]), year=yr[i], fc=df["forecast"].iloc[i])
                for h in (10, 20, 30, 60):
                    rec[f"x{h}"] = (c[i+h]/c[i]-1 - cm[h]) if i + h < len(c) else np.nan
                rows.append(rec)
    ev = pd.DataFrame(rows)
    ev = ev.sort_values("fc").reset_index(drop=True)
    n = len(ev); k = n//2
    ev["half"] = "mid"
    ev.loc[:k-1, "half"] = "bot"; ev.loc[n-k:, "half"] = "top"
    out = {}
    out["n_events"] = n
    hz = {}
    for h in (10, 20, 30, 60):
        t = ev[ev.half=="top"][f"x{h}"].dropna(); b = ev[ev.half=="bot"][f"x{h}"].dropna()
        tt = stats.ttest_ind(t, b, equal_var=False)
        sp = stats.spearmanr(ev["fc"], ev[f"x{h}"], nan_policy="omit")
        hz[h] = dict(top=t.mean(), bot=b.mean(), diff=t.mean()-b.mean(), welch=tt.statistic, n_t=len(t), n_b=len(b), spear=sp.correlation, all_mean=ev[f"x{h}"].mean(), all_t=stats.ttest_1samp(ev[f"x{h}"].dropna(),0).statistic)
    out["by_horizon"] = pd.DataFrame(hz).T
    g = ev.groupby(["coin","half"])["x30"].agg(["count","mean"]).unstack()
    out["by_coin_half"] = g
    out["by_year_half"] = ev.groupby(["year","half"])["x30"].agg(["count","mean","median"]).unstack()
    ev["q"] = pd.qcut(ev["fc"].rank(method="first"), 4, labels=False)
    out["by_quartile"] = ev.groupby("q").agg(n=("x30","count"), fc=("fc","mean"), mean=("x30","mean"), median=("x30","median"), hit=("x30", lambda s:(s>0).mean()))
    # outlier sensitivity
    t = ev[ev.half=="top"]["x30"]; b = ev[ev.half=="bot"]["x30"]
    out["top_desc"] = t.describe()
    out["bot_desc"] = b.describe()
    tr = t.drop(t.idxmax()); 
    out["welch_drop_top_max"] = stats.ttest_ind(tr, b, equal_var=False).statistic
    out["mannwhitney_p"] = stats.mannwhitneyu(t, b).pvalue
    return out
