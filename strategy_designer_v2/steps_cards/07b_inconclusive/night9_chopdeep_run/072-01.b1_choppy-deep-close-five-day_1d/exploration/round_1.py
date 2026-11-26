def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    col = "debug_info.components.depth.last_history_value"
    # normal drift per coin per horizon, all windows together (visible ones)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            for h in (1, 3, 5, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, ret=c[i+h]/c[i]-1,
                                     fc=df["forecast"].iloc[i],
                                     depth=df[col].iloc[i] if col in df else np.nan,
                                     reg=df["regime"].iloc[i],
                                     up=float(c[i] > df["open"].iloc[i]),
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin", "h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["drift"]
    S = R[(R.reg == "unknown") & (R.depth < 0)].copy()

    def reg(d, x):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 10: return (len(d), np.nan, np.nan)
        r = stats.linregress(d[x], d["ex"])
        return (len(d), r.slope, r.slope / r.stderr)

    out = {}
    hz = []
    for h in (1, 3, 5, 10):
        d = S[S.h == h]
        n1, s1, t1 = reg(d[d.fc < 0], "fc")
        n2, s2, t2 = reg(d, "depth")
        q = d.depth.rank(pct=True)
        hz.append(dict(h=h, n_fc=n1, t_fc=t1, n_depth=n2, slope_depth=s2, t_depth=t2,
                       ex_deep3=d.ex[q <= 1/3].mean(), ex_shallow3=d.ex[q > 2/3].mean(),
                       tot_deep3=d.ret[q <= 1/3].mean()))
    out["by horizon"] = pd.DataFrame(hz)
    d5 = S[S.h == 5]
    g = []
    for key in ["coin", "w", "year", "up"]:
        for k, dd in d5.groupby(key):
            n, s, t = reg(dd, "depth")
            g.append(dict(by=key, grp=k, n=n, t_depth=t, mean_ex=dd.ex.mean(), mean_depth=dd.depth.mean()))
    out["h5 by group"] = pd.DataFrame(g)
    d1 = S[S.h == 1]
    g1 = []
    for key in ["coin", "up"]:
        for k, dd in d1.groupby(key):
            n, s, t = reg(dd, "depth")
            g1.append(dict(by=key, grp=k, n=n, t_depth=t, mean_ex=dd.ex.mean()))
    out["h1 by group"] = pd.DataFrame(g1)
    # deciles of depth at h5
    d5 = d5.copy(); d5["q"] = pd.qcut(d5.depth, 5, labels=False)
    out["h5 depth quintiles"] = d5.groupby("q").agg(n=("ex", "size"), depth=("depth", "mean"),
                                                   ex=("ex", "mean"), ret=("ret", "mean"))
    out["fc vs depth corr h5"] = float(d5[["fc", "depth"]].corr().iloc[0, 1])
    return out
