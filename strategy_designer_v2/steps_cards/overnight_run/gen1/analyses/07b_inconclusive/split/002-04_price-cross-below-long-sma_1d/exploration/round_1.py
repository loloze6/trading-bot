def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        rets = []
        for w, b in wins.items():
            c = b["close"].values
            if len(c) > 1:
                rets.append(np.diff(c) / c[:-1])
        mu = np.concatenate(rets).mean()
        for w, b in wins.items():
            c = b["close"].values
            a = b["postRebalance_current_allocation"].values
            f = b["forecast"].values
            raw = b["debug_info.components.below_ma.last_history_value"].values
            for i in range(0, len(b) - 10, 10):
                r = c[i + 10] / c[i] - 1
                ex = r - 10 * mu
                prior = c[i] / c[max(0, i - 30)] - 1
                rows.append(dict(coin=coin, w=w, alloc=a[i], fc=f[i], raw=raw[i], r=r, ex=ex,
                                 prod=a[i] * ex, prior30=prior,
                                 year=pd.Timestamp(b["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    act = d[d.alloc != 0].copy()
    act["short_gain"] = -act.ex

    def st(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), sd=x.std(),
                              t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              hit=(x > 0).mean()))

    out = {}
    out["all_active_shortgain"] = st(act.short_gain).to_frame().T
    out["prod_all"] = st(d["prod"]).to_frame().T
    out["by_coin"] = act.groupby("coin").short_gain.apply(st).unstack()
    out["by_year"] = act.groupby("year").short_gain.apply(st).unstack()
    out["by_window"] = act.groupby("w").short_gain.apply(st).unstack()
    act["fcq"] = pd.qcut(act.fc, 5, labels=False, duplicates="drop")
    out["by_fc_quintile(0=deepest)"] = act.groupby("fcq").agg(
        fc=("fc", "mean"), n=("ex", "size"), sg=("short_gain", "mean"),
        t=("short_gain", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))),
        hit=("short_gain", lambda x: (x > 0).mean()))
    act["rawq"] = pd.qcut(act.raw, 5, labels=False, duplicates="drop")
    out["by_raw_dist_quintile(0=deepest)"] = act.groupby("rawq").agg(
        raw=("raw", "mean"), n=("ex", "size"), sg=("short_gain", "mean"),
        t=("short_gain", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    act["prq"] = pd.qcut(act.prior30, 4, labels=False)
    out["by_prior30_quartile"] = act.groupby("prq").agg(
        prior=("prior30", "mean"), n=("ex", "size"), sg=("short_gain", "mean"),
        t=("short_gain", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    out["sd_excess_active_vs_flat"] = pd.Series(dict(
        sd_active=act.ex.std(), sd_flat=d[d.alloc == 0].ex.std(),
        mean_flat_ex=d[d.alloc == 0].ex.mean()))
    return out
