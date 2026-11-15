def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        # coin mean daily return over all windows
        dr = []
        for w, df in wins.items():
            dr.append(df["close"].pct_change().dropna())
        mu = pd.concat(dr).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            dist = df["debug_info.components.below_ma.last_history_value"].values
            fc = df["forecast"].values
            al = df["postRebalance_current_allocation"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r20 = np.full(n, np.nan)
            r20[20:] = c[20:] / c[:-20] - 1
            vol = df["sizing_realised_vol"].values
            for h in [1, 3, 5, 10, 20, 40]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, yr=yr[i], dist=dist[i], fc=fc[i], al=al[i],
                                     ex=c[i + h] / c[i] - 1 - h * mu, r20=r20[i], vol=vol[i]))
    d = pd.DataFrame(rows)
    def summ(g):
        s = g["ex"]
        return pd.Series({"n": len(s), "mean_ex": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan,
                          "share_down": (s < 0).mean()})
    out = {}
    d["below"] = d["fc"] < 0
    out["by_h_below"] = d.groupby(["h", "below"]).apply(summ)
    b10 = d[(d.h == 10) & d.below].copy()
    out["h10_below_by_coin"] = b10.groupby("coin").apply(summ)
    out["h10_below_by_year"] = b10.groupby("yr").apply(summ)
    b10["fq"] = pd.qcut(b10["fc"], 4, labels=["deep", "q2", "q3", "shallow"])
    out["h10_below_by_fc_quart"] = b10.groupby("fq").apply(summ)
    b10["r20s"] = np.where(b10["r20"].isna(), "na", np.where(b10["r20"] < 0, "r20neg", "r20pos"))
    out["h10_below_by_r20sign"] = b10.groupby("r20s").apply(summ)
    b10["vq"] = pd.qcut(b10["vol"], 3, labels=["lowvol", "midvol", "highvol"])
    out["h10_below_by_vol"] = b10.groupby("vq").apply(summ)
    a10 = d[(d.h == 10) & ~d.below].copy()
    a10["r20s"] = np.where(a10["r20"].isna(), "na", np.where(a10["r20"] < 0, "r20neg", "r20pos"))
    out["h10_above_by_r20sign"] = a10.groupby("r20s").apply(summ)
    b20 = d[(d.h == 20) & d.below].copy()
    b20["fq"] = pd.qcut(b20["fc"], 4, labels=["deep", "q2", "q3", "shallow"])
    out["h20_below_by_fc_quart"] = b20.groupby("fq").apply(summ)
    b1 = d[(d.h == 1) & d.below].copy()
    b1["r20s"] = np.where(b1["r20"].isna(), "na", np.where(b1["r20"] < 0, "r20neg", "r20pos"))
    out["h1_below_by_r20sign"] = b1.groupby("r20s").apply(summ)
    return out
