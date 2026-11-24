def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    H_list = [5, 10, 20, 40]
    rows = []
    coin_mean = {}
    for coin, wins in bars.items():
        for H in H_list:
            rets = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rets.append(c[i + H] / c[i] - 1)
            coin_mean[(coin, H)] = np.mean(rets) if rets else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            reg = df["regime"].values
            dl = df.get("debug_info.components.dist_low.post_pipeline_value")
            raw = df.get("debug_info.components.dist_low.last_history_value")
            ts = pd.to_datetime(df["timestamp"])
            for H in H_list:
                for i in range(0, len(c) - H, H):
                    if reg[i] != "trending" or f[i] == 0 or pd.isna(f[i]):
                        continue
                    r = c[i + H] / c[i] - 1
                    ex = r - coin_mean[(coin, H)]
                    rows.append(dict(coin=coin, win=w, H=H, f=f[i], ex=ex, r=r,
                                     prod=f[i] / 10 * ex,
                                     dl=dl.iloc[i] if dl is not None else np.nan,
                                     raw=raw.iloc[i] if raw is not None else np.nan,
                                     year=ts.iloc[i].year, day=ts.iloc[i].normalize()))
    d = pd.DataFrame(rows)

    def tday(sub, col):
        s = sub.groupby("day")[col].sum()
        if len(s) < 3: return (np.nan, len(s))
        return (s.mean() / (s.std(ddof=1) / np.sqrt(len(s))), len(s))

    out = {}
    hz = []
    for H in H_list:
        s = d[d.H == H]
        t, nd = tday(s, "prod")
        sh = s[s.f < 0]; lo = s[s.f > 0]
        ts_, nds = tday(sh, "ex"); tl, ndl = tday(lo, "ex")
        hz.append(dict(H=H, n=len(s), days=nd, prod_mean=s["prod"].mean(), t_prod=t,
                       n_short=len(sh), ex_short=sh.ex.mean(), t_short=ts_,
                       n_long=len(lo), ex_long=lo.ex.mean(), t_long=tl))
    out["by horizon"] = pd.DataFrame(hz)
    s = d[d.H == 20].copy()
    s["fb"] = pd.cut(s.f, [-5.01, -3, -1.5, 0, 1.5, 3, 5.01])
    g = s.groupby("fb", observed=True).agg(n=("ex", "size"), ex=("ex", "mean"), r=("r", "mean"), prod=("prod", "mean"))
    out["H20 by forecast bucket"] = g
    out["H20 by year"] = s.groupby("year").agg(n=("ex", "size"), prod=("prod", "mean"),
        ex_short=("ex", lambda x: x[s.loc[x.index, "f"] < 0].mean()),
        ex_long=("ex", lambda x: x[s.loc[x.index, "f"] > 0].mean()))
    out["H20 by coin"] = s.groupby("coin").agg(n=("ex", "size"), prod=("prod", "mean"),
        ex_short=("ex", lambda x: x[s.loc[x.index, "f"] < 0].mean()),
        ex_long=("ex", lambda x: x[s.loc[x.index, "f"] > 0].mean()))
    # raw distance quintiles (percent above yearly low)
    s["rq"] = pd.qcut(s.raw, 5, duplicates="drop")
    out["H20 by raw distance quintile"] = s.groupby("rq", observed=True).agg(n=("ex", "size"), ex=("ex", "mean"), f=("f", "mean"))
    out["H20 corr f ex (spearman)"] = float(stats.spearmanr(s.f, s.ex).correlation)
    out["H20 corr raw ex (spearman)"] = float(stats.spearmanr(s.raw, s.ex, nan_policy="omit").correlation)
    return out
