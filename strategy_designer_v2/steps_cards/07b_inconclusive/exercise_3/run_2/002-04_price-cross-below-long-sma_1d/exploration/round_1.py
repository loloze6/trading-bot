def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    # coin mean daily return over all windows
    cmean = {}
    for c in bars:
        rs = []
        for w, df in bars[c].items():
            rs.append(df["close"].pct_change().dropna())
        cmean[c] = pd.concat(rs).mean()
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            al = df["postRebalance_current_allocation"].values
            fc = df["forecast"].values
            dist = df.get("debug_info.components.below_ma.last_history_value")
            dist = dist.values if dist is not None else np.full(len(df), np.nan)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            for h in [1, 5, 10, 20, 40]:
                for i in range(0, n - h, h):
                    r = cl[i + h] / cl[i] - 1
                    past20 = cl[i] / cl[i - 20] - 1 if i >= 20 else np.nan
                    rv = np.nan
                    if i >= 20:
                        rv = np.std(np.diff(np.log(cl[i-20:i+1])))
                    rows.append(dict(coin=c, w=w, h=h, yr=yr[i], alloc=al[i], fc=fc[i], dist=dist[i],
                                     r=r, ex=r - h * cmean[c], past20=past20, rv=rv))
    d = pd.DataFrame(rows)
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    act = d[d.alloc < 0].copy()
    act["g"] = act.alloc * act.ex
    act["gr"] = act.alloc * act.r
    # by horizon: short-sign excess return (-ex) mean, and gain
    out["by_h_neg_ex"] = act.groupby("h").apply(lambda g: tt(-g.ex))
    out["by_h_gain_gross"] = act.groupby("h").apply(lambda g: tt(g.gr))
    a10 = act[act.h == 10].copy()
    out["coin_negex_h10"] = a10.groupby("coin").apply(lambda g: tt(-g.ex))
    out["year_negex_h10"] = a10.groupby("yr").apply(lambda g: tt(-g.ex))
    a10["fq"] = pd.qcut(a10.fc.rank(method="first"), 4, labels=["deepest", "q2", "q3", "shallow"])
    out["fc_quart_negex"] = a10.groupby("fq").apply(lambda g: tt(-g.ex))
    a10["pm"] = pd.qcut(a10.past20.rank(method="first"), 3, labels=["fell", "mid", "rose"])
    out["past20_negex"] = a10.groupby("pm").apply(lambda g: tt(-g.ex))
    a10["vq"] = pd.qcut(a10.rv.rank(method="first"), 3, labels=["lowvol", "mid", "highvol"])
    out["vol_negex"] = a10.groupby("vq").apply(lambda g: tt(-g.ex))
    # flat bars comparison
    fl = d[(d.h == 10) & (d.alloc == 0)]
    out["flat_ex_h10"] = tt(fl.ex)
    for h in [20, 40]:
        ah = act[act.h == h].copy()
        ah["pm"] = pd.qcut(ah.past20.rank(method="first"), 3, labels=["fell", "mid", "rose"])
        out[f"past20_negex_h{h}"] = ah.groupby("pm").apply(lambda g: tt(-g.ex))
    return out
