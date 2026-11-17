def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; runs = []; post = []; deep = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            d = data["days"][coin][w]
            alloc = b["postRebalance_current_allocation"].fillna(0)
            act = (b["regime"] == "trending")
            nxt = b["close"].shift(-1) / b["close"] - 1
            gain = alloc * nxt
            rows.append(dict(coin=coin, w=w, n=len(b), act=act.sum(), inpos=(alloc.abs() > 1e-6).sum(),
                             meanalloc_act=alloc[act].mean() if act.any() else np.nan,
                             gain=gain.sum(), bookmean=d["book_return"].mean(), coinmean=d["coin_return"].mean()))
            # runs of trending
            a = act.values.astype(int)
            i = 0
            while i < len(a):
                if a[i]:
                    j = i
                    while j < len(a) and a[j]: j += 1
                    runs.append(j - i)
                    # coin return from run end (exit bar j) over next 10 and 30 bars, and from run start over 30
                    c = b["close"].values
                    r30s = c[i+30]/c[i]-1 if i+30 < len(c) else np.nan
                    e10 = c[j+10]/c[j]-1 if (j < len(c) and j+10 < len(c)) else np.nan
                    e30 = c[j+30]/c[j]-1 if (j < len(c) and j+30 < len(c)) else np.nan
                    inrun = c[j-1]/c[i]-1
                    post.append(dict(len=j-i, r30_from_start=r30s, after_exit10=e10, after_exit30=e30, inrun=inrun))
                    i = j
                else:
                    i += 1
            # drawdown of book in window
            bv = d["book_value"].values
            dd = bv / np.maximum.accumulate(bv) - 1
            deep.append(dict(coin=coin, w=w, maxdd=dd.min(), wret=bv[-1]/bv[0]-1,
                             coinret=d["close"].values[-1]/d["close"].values[0]-1))
    R = pd.DataFrame(rows); P = pd.DataFrame(post); D = pd.DataFrame(deep)
    out["share_active_bars"] = R["act"].sum() / R["n"].sum()
    out["share_inpos_bars"] = R["inpos"].sum() / R["n"].sum()
    out["mean_alloc_when_active"] = R["meanalloc_act"].mean()
    out["run_length_desc"] = pd.Series(runs).describe()
    out["run_len_buckets"] = pd.cut(P["len"], [0,1,3,7,15,30,1000]).value_counts().sort_index()
    out["post_run_stats"] = P[["r30_from_start","after_exit10","after_exit30","inrun"]].agg(["mean","median","count"])
    t = P["after_exit30"].dropna()
    out["after_exit30_t"] = stats.ttest_1samp(t, 0).statistic
    out["by_coin"] = R.groupby("coin")[["act","inpos","gain","bookmean","coinmean"]].agg({"act":"sum","inpos":"sum","gain":"sum","bookmean":"mean","coinmean":"mean"})
    out["worst_windows"] = D.sort_values("maxdd").head(12).drop(columns="w").reset_index(drop=True)
    out["by_window"] = D.groupby("w")[["maxdd","wret","coinret"]].mean()
    return out
