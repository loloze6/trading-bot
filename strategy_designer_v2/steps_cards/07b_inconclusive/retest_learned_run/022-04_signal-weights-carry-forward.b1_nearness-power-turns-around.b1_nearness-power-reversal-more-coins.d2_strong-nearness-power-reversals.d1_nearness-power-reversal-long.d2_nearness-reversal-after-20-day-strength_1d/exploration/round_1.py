def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    def grid_rows(h):
        rows = []
        for coin, wins in bars.items():
            # coin mean h-return over all windows
            allr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr.extend(list(c[idx + h] / c[idx] - 1))
            mu = np.mean(allr) if allr else np.nan
            sd = np.std(allr, ddof=1) if len(allr) > 1 else np.nan
            for w, df in wins.items():
                c = df["close"].values
                f = df["forecast"].values
                yr = pd.to_datetime(df["timestamp"]).dt.year.values
                raw = df.get("debug_info.components.npower_rev.last_history_value")
                raw = raw.values if raw is not None else np.full(len(c), np.nan)
                for i in range(0, len(c) - h, h):
                    r20 = c[i] / c[i - 20] - 1 if i >= 20 else np.nan
                    r60 = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                    rows.append(dict(coin=coin, w=w, year=yr[i], f=f[i], raw=raw[i],
                                     ret=c[i + h] / c[i] - 1, mu=mu, sd=sd, r20=r20, r60=r60))
        d = pd.DataFrame(rows)
        d["ex"] = d["ret"] - d["mu"]
        d["fx"] = d["f"] * d["ex"]
        return d
    def tt(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    # horizons
    hz = {}
    for h in [1, 3, 5, 10, 20]:
        d = grid_rows(h)
        a = d[d.f > 0]
        b = d[d.f == 0]
        r = tt(a.fx); r2 = tt(a.ex)
        hz[f"h{h}"] = {"n": r["n"], "fx_mean": r["mean"], "fx_t": r["t"], "ex_mean": r2["mean"], "ex_t": r2["t"],
                      "ret_mean": a.ret.mean(), "ex_flat_mean": b.ex.mean(),
                      "corr_f_ex_t": stats.pearsonr(a.f, a.ex)[0] * np.sqrt(len(a))}
    out["by_horizon"] = pd.DataFrame(hz).T
    d = grid_rows(5)
    a = d[d.f > 0].copy()
    a["fq"] = pd.qcut(a.f.rank(method="first"), 5, labels=False)
    out["by_forecast_quintile"] = a.groupby("fq").apply(lambda g: pd.Series({"fmean": g.f.mean(), **tt(g.ex).to_dict(), "fx_t": tt(g.fx)["t"]}))
    a["r20q"] = pd.qcut(a.r20.rank(method="first"), 4, labels=False)
    out["by_r20_quartile"] = a.groupby("r20q").apply(lambda g: pd.Series({"r20": g.r20.mean(), **tt(g.ex).to_dict(), "fx_t": tt(g.fx)["t"]}))
    a["r60s"] = np.sign(a.r60)
    out["by_r60_sign"] = a.groupby("r60s").apply(lambda g: pd.Series({**tt(g.ex).to_dict(), "fx_t": tt(g.fx)["t"]}))
    out["by_coin"] = a.groupby("coin").apply(lambda g: pd.Series({**tt(g.fx).to_dict(), "ex_mean": g.ex.mean()}))
    out["by_year"] = a.groupby("year").apply(lambda g: pd.Series({**tt(g.fx).to_dict(), "ex_mean": g.ex.mean(), "ret_mean": g.ret.mean()}))
    # all grid bars, r20>0: does forecast size grade vs nothing
    allg = d[d.r20 > 0]
    out["r20pos_f0_vs_fpos"] = pd.DataFrame({"f0": tt(allg[allg.f == 0].ex), "fpos": tt(allg[allg.f > 0].ex)}).T
    # fx without top 1% forecast
    q = a.f.quantile(0.99)
    out["fx_drop_top1pct"] = tt(a[a.f < q].fx).to_frame().T
    out["fx_top_contrib_share"] = float(a[a.f >= q].fx.sum() / a.fx.sum())
    return out
