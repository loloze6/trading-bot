def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []; brows = []
    for coin, wins in data["bars"].items():
        g = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 24, 24)
            g.append(c[idx + 24] / c[idx] - 1)
        g = np.concatenate(g); drift = g.mean()
        r1all = []
        for w, b in wins.items():
            c = b["close"].values; r1all.append(c[1:] / c[:-1] - 1)
        hdrift = np.concatenate(r1all).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            ts = pd.to_datetime(b["timestamp"]); hr = ts.dt.hour.values; yr = ts.dt.year.values
            a = b["postRebalance_current_allocation"].fillna(0).values
            pa = b["previous_allocation"].fillna(0).values
            nxt = np.r_[c[1:] / c[:-1] - 1, np.nan]
            gain = a * nxt
            turn = np.abs(a - pa)
            brows.append(pd.DataFrame(dict(coin=coin, yr=yr, side=np.sign(a), gain=gain,
                                           timing=a * (nxt - hdrift), turn=turn)))
            ret1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol24 = pd.Series(ret1).rolling(480, min_periods=100).std().values * np.sqrt(24)
            vol_long = pd.Series(ret1).rolling(24 * 90, min_periods=500).std().values * np.sqrt(24)
            f = b["forecast"].fillna(0).values
            for t in np.where(hr == 0)[0]:
                if t < 25 or t + 24 >= n: continue
                r24 = c[t] / c[t - 24] - 1; h1 = ret1[t - 24]
                rows.append(dict(coin=coin, yr=yr[t], f=f[t], dis=np.sign(r24) != np.sign(h1),
                                 sig=-np.sign(r24), z=abs(r24) / vol24[t] if vol24[t] > 0 else np.nan,
                                 vol=vol24[t], vrel=vol24[t] / vol_long[t] if vol_long[t] > 0 else np.nan,
                                 u24=-np.sign(r24) * (c[t + 24] / c[t] - 1 - drift),
                                 tot=-np.sign(r24) * (c[t + 24] / c[t] - 1),
                                 alloc=abs(a[t]), turn=turn[t]))
    B = pd.concat(brows).dropna(subset=["gain"])
    out["bar_gain_by_side"] = B.groupby("side").agg(n=("gain", "size"), gain_bp=("gain", lambda x: x.mean() * 1e4),
                                                   timing_bp=("timing", lambda x: x.mean() * 1e4))
    out["turnover_per_coinday"] = pd.Series({"mean_abs_alloc_change_per_day": B.turn.sum() / (len(B) / 24),
                                             "cost_per_day_bp_at_0.095%_per_side": B.turn.sum() / (len(B) / 24) * 9.5})
    d = pd.DataFrame(rows)
    def summ(x, col="u24"):
        v = x[col].dropna()
        return pd.Series({"n": len(v), "mean%": v.mean() * 100, "t": v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan})
    d["volq"] = pd.qcut(d.vol, 3, labels=False)
    d["vrq"] = pd.qcut(d.vrel, 3, labels=False)
    d["zq"] = pd.qcut(d.z, 5, labels=False)
    act = d[d.dis & (d.f != 0)]; agr = d[~d.dis]
    out["vol_tercile_dis_vs_agree"] = pd.concat({"dis": act.groupby("volq").apply(summ), "agree": agr.groupby("volq").apply(summ)}, axis=1)
    out["relvol_tercile_dis_vs_agree"] = pd.concat({"dis": act.groupby("vrq").apply(summ), "agree": agr.groupby("vrq").apply(summ)}, axis=1)
    out["dis_vol2_by_zq"] = act[act.volq == 2].groupby("zq").apply(summ)
    out["dis_vol2_by_side"] = act[act.volq == 2].groupby("sig").apply(summ)
    out["dis_vol2_by_year"] = act[act.volq == 2].groupby("yr").apply(summ)
    out["dis_total_by_side"] = act.groupby("sig").apply(lambda x: summ(x, "tot"))
    out["alloc_by_volq"] = act.groupby("volq")[["alloc", "turn"]].mean()
    out["vol_tercile_edges"] = pd.Series(d.vol.quantile([1/3, 2/3]).values, index=["q33", "q67"])
    return out
