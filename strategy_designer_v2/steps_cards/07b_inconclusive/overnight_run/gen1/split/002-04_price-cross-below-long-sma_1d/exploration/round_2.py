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
            raw = b["debug_info.components.below_ma.last_history_value"].values.astype(float)
            sma = c / (1 + raw / 100.0)
            below = raw < 0
            run = np.zeros(len(b))
            for k in range(len(b)):
                run[k] = (run[k-1] + 1 if k > 0 else 1) if below[k] else 0
            ts = pd.to_datetime(b["timestamp"]).values
            for i in range(0, len(b) - 10, 10):
                r = c[i + 10] / c[i] - 1
                slope = sma[i] / sma[max(0, i - 20)] - 1 if i >= 20 else np.nan
                rows.append(dict(coin=coin, w=w, ts=ts[i], alloc=a[i], raw=raw[i], r=r,
                                 ex=r - 10 * mu, slope=slope, run=run[i], below=below[i]))
    d = pd.DataFrame(rows)
    # breadth and market return by timestamp
    d["breadth"] = d.groupby("ts").below.transform("mean")
    d["ncoin"] = d.groupby("ts").below.transform("size")
    d["mkt"] = d.groupby("ts").r.transform("mean")
    d["rel"] = d.r - d.mkt
    act = d[d.alloc != 0].copy()
    act["sg"] = -act.ex
    act["sg_rel"] = -act.rel

    def agg(g):
        return g.agg(n=("sg", "size"), sg=("sg", "mean"),
                     t=("sg", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))),
                     sg_rel=("sg_rel", "mean"),
                     t_rel=("sg_rel", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))),
                     hit=("sg", lambda x: (x > 0).mean()))
    out = {}
    out["overall_rel_to_market"] = agg(act.assign(k=0).groupby("k"))
    out["share_var_explained_by_mkt"] = pd.Series(dict(
        corr_r_mkt=act[["r", "mkt"]].corr().iloc[0, 1], sd_r=act.r.std(), sd_rel=act.rel.std()))
    act["slope_sign"] = np.where(act.slope.isna(), "na", np.where(act.slope < 0, "sma_falling", "sma_rising"))
    out["by_sma_slope"] = agg(act.groupby("slope_sign"))
    act["runb"] = pd.cut(act.run, [0, 20, 60, 150, 10000], labels=["<=20", "21-60", "61-150", ">150"])
    out["by_days_below"] = agg(act.groupby("runb", observed=True))
    act["brb"] = pd.cut(act.breadth, [0, 0.34, 0.67, 0.99, 1.01], labels=["<=1/3", "1/3-2/3", "2/3-<1", "all"])
    out["by_breadth"] = agg(act.groupby("brb", observed=True))
    act["sl_q"] = pd.qcut(act.slope, 4, labels=False)
    out["by_slope_quartile(0=most falling)"] = agg(act.groupby("sl_q")).join(
        act.groupby("sl_q").slope.mean().rename("slope"))
    out["slope_falling_x_breadth"] = agg(act[act.slope < 0].groupby("brb", observed=True))
    return out
