def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    trd = []
    for coin, wins in data["bars"].items():
        # drift and usual move per coin, 24h grid
        g = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 24, 24)
            g.append(c[idx + 24] / c[idx] - 1)
        g = np.concatenate(g)
        drift, usual = g.mean(), g.std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            ts = pd.to_datetime(b["timestamp"])
            hr = ts.dt.hour.values
            yr = ts.dt.year.values
            f = b["forecast"].fillna(0).values
            n = len(c)
            ret1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol24 = pd.Series(ret1).rolling(480, min_periods=100).std().values * np.sqrt(24)
            for t in np.where(hr == 0)[0]:
                if t < 25 or t + 72 >= n:
                    continue
                r24 = c[t] / c[t - 24] - 1
                h1 = ret1[t - 24]
                fw = {h: c[t + h] / c[t] - 1 for h in (6, 12, 24, 48, 72)}
                rows.append(dict(coin=coin, w=w, yr=yr[t], f=f[t], r24=r24, h1=h1,
                                 z=r24 / vol24[t] if vol24[t] > 0 else np.nan,
                                 vol=vol24[t], drift=drift, usual=usual, **{f"f{h}": v for h, v in fw.items()}))
        for w, tr in data["trades"][coin].items():
            if len(tr):
                t2 = tr[["side", "net_profit_loss_percent", "profit_loss_percent", "duration_minutes"]].copy()
                t2["coin"] = coin
                trd.append(t2)
    d = pd.DataFrame(rows)
    d["dis"] = np.sign(d.r24) != np.sign(d.h1)
    d["sig"] = -np.sign(d.r24)
    for h in (6, 12, 24, 48, 72):
        d[f"u{h}"] = d.sig * (d[f"f{h}"] - d.drift * h / 24)
    d["tot24"] = d.sig * d.f24
    act = d[(d.f != 0) & d.dis].copy()
    def summ(x, col="u24"):
        v = x[col].dropna()
        return pd.Series({"n": len(v), "mean%": v.mean() * 100, "t": v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan})
    out = {}
    out["active_vs_condition_alone"] = pd.DataFrame({
        "active(dis)": summ(act), "hour0_agree": summ(d[~d.dis]), "hour0_all": summ(d)})
    act["zq"] = pd.qcut(act.z.abs(), 5, labels=False)
    out["by_absz_quintile"] = act.groupby("zq").apply(summ)
    act["volq"] = pd.qcut(act.vol, 3, labels=False)
    out["by_vol_tercile"] = act.groupby("volq").apply(summ)
    d["zq"] = pd.qcut(d.z.abs(), 5, labels=False)
    out["agree_by_absz"] = d[~d.dis].groupby("zq").apply(summ)
    out["by_side"] = act.groupby("sig").apply(summ)
    out["by_coin"] = act.groupby("coin").apply(summ)
    out["by_year"] = act.groupby("yr").apply(summ)
    out["horizons"] = pd.DataFrame({f"u{h}": summ(act, f"u{h}") for h in (6, 12, 24, 48, 72)})
    out["horizons_top2quint"] = pd.DataFrame({f"u{h}": summ(act[act.zq >= 3], f"u{h}") for h in (6, 12, 24, 48, 72)})
    T = pd.concat(trd)
    out["trades"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"),
                                          gross=("profit_loss_percent", "mean"),
                                          net=("net_profit_loss_percent", "mean"),
                                          dur_h=("duration_minutes", lambda x: x.mean() / 60))
    # book by year
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w
            dd.append(x)
    D = pd.concat(dd)
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    out["book_by_year"] = D.groupby("yr").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    return out
