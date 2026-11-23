def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drift = {}
    usual = {}
    for coin, wins in data["bars"].items():
        g = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            g.extend(list(c[idx + 48] / c[idx] - 1))
        drift[coin] = np.mean(g); usual[coin] = np.std(g, ddof=1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].values; v = b["volume"].values
            f = b["forecast"].fillna(0).values
            last = -10**9
            for i in np.where(f != 0)[0]:
                if i + 48 >= len(c) or i - last < 48 or i < 168:
                    continue
                last = i
                r = c[i + 48] / c[i] - 1
                s = np.sign(f[i])
                wk = c[i] / c[i - 48] - 1
                vr = v[i - 47:i + 1].mean() / max(v[i - 167:i - 47].mean(), 1e-12)
                # first 24h vs second 24h of horizon
                r24 = c[i + 24] / c[i] - 1
                rows.append(dict(coin=coin, win=w, year=ts[i].year, f=f[i], af=abs(f[i]), side="long" if s > 0 else "short",
                                 u=s * (r - drift[coin]), u24=s * (r24 - drift[coin] / 2), u2448=s * (c[i+48]/c[i+24]-1 - drift[coin]/2),
                                 str_=s * (r - drift[coin]) / usual[coin], wkz=abs(wk) / usual[coin], vr=vr,
                                 ret_unsigned=r))
    d = pd.DataFrame(rows)
    def agg(x):
        return pd.Series(dict(n=len(x), mean=x.u.mean(), t=x.u.mean() / (x.u.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              str_=x.str_.mean(), u24=x.u24.mean(), u2448=x.u2448.mean()))
    out = {}
    out["all"] = agg(d).to_frame().T
    out["by_coin"] = d.groupby("coin").apply(agg)
    out["by_year"] = d.groupby("year").apply(agg)
    out["by_side"] = d.groupby("side").apply(agg)
    d["fq"] = pd.qcut(d.af.rank(method="first"), 5, labels=False)
    d["mq"] = pd.qcut(d.wkz.rank(method="first"), 5, labels=False)
    d["vq"] = pd.qcut(d.vr.rank(method="first"), 5, labels=False)
    out["by_absforecast_q"] = d.groupby("fq").apply(agg)
    out["by_movesize_q"] = d.groupby("mq").apply(agg)
    out["by_volratio_q"] = d.groupby("vq").apply(agg)
    out["vr_range"] = d.groupby("vq").vr.agg(["min", "max"])
    out["corr_u_vs"] = pd.Series(dict(af=stats.spearmanr(d.af, d.u)[0], wkz=stats.spearmanr(d.wkz, d.u)[0], vr=stats.spearmanr(d.vr, d.u)[0],
                                      corr_af_wkz=stats.spearmanr(d.af, d.wkz)[0], corr_af_vr=stats.spearmanr(d.af, d.vr)[0]))
    out["side_x_movesize"] = d.groupby(["side", "mq"]).u.agg(["count", "mean"])
    return out
