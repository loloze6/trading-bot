def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        g = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            g.extend(list(c[idx + 48] / c[idx] - 1))
        dr = np.mean(g); us = np.std(g, ddof=1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].values; v = b["volume"].values
            m = ((ts.dt.dayofweek == 6) & (ts.dt.hour == 23)).values
            for i in np.where(m)[0]:
                if i < 168 or i + 48 >= len(c):
                    continue
                wk = c[i] / c[i - 48] - 1
                if wk == 0:
                    continue
                s = np.sign(wk)
                vr = v[i - 47:i + 1].mean() / max(v[i - 167:i - 47].mean(), 1e-12)
                r = c[i + 48] / c[i] - 1
                rows.append(dict(coin=coin, year=ts[i].year, s=s, wkz=abs(wk) / us, vr=vr,
                                 u=s * (r - dr), strn=s * (r - dr) / us, active=b["forecast"].fillna(0).values[i] != 0))
    d = pd.DataFrame(rows)
    def agg(x):
        n = len(x)
        return pd.Series(dict(n=n, mean=x.u.mean(), t=x.u.mean() / (x.u.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan, str_=x.strn.mean()))
    out = {}
    out["all_sundays"] = agg(d).to_frame().T
    out["by_vr_gt1"] = d.groupby(d.vr > 1).apply(agg)
    out["by_active"] = d.groupby("active").apply(agg)
    d["vq"] = pd.qcut(d.vr.rank(method="first"), 6, labels=False)
    out["by_vr_sextile_all"] = d.groupby("vq").apply(agg)
    out["vr_sextile_range"] = d.groupby("vq").vr.agg(["min", "max"])
    d["mq"] = pd.qcut(d.wkz.rank(method="first"), 5, labels=False)
    out["by_move_q_all"] = d.groupby("mq").apply(agg)
    out["move_q_range"] = d.groupby("mq").wkz.agg(["min", "max"])
    out["vr_gt1_by_coin"] = d[d.vr > 1].groupby("coin").apply(agg)
    out["vr_le1_by_coin"] = d[d.vr <= 1].groupby("coin").apply(agg)
    h = d[d.vr > 1]
    out["spearman_vr_u_heavy"] = stats.spearmanr(h.vr, h.u)[0]
    out["spearman_vr_u_all"] = stats.spearmanr(d.vr, d.u)[0]
    out["spearman_wkz_u_all"] = stats.spearmanr(d.wkz, d.u)[0]
    out["heavy_noXRP"] = agg(h[h.coin != "XRPUSD"]).to_frame().T
    return out
