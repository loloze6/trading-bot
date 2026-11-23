def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []      # anchor-bar events (Sunday 23:00 and weekday 23:00 analogues)
    hrs = []       # 1h returns by hour of day
    grid24 = []    # 24h grid: past 24h return vs next 24h return
    for coin, wins in data["bars"].items():
        # coin's usual 48h and 12h moves from non-overlapping grids
        r48, r12, r24 = [], [], []
        for w, b in wins.items():
            c = b["close"].values
            r48 += list(c[48::48] / c[:-48:48][:len(c[48::48])] - 1)
            r12 += list(c[12::12] / c[:-12:12][:len(c[12::12])] - 1)
            r24 += list(c[24::24] / c[:-24:24][:len(c[24::24])] - 1)
        sd48, sd12, sd24 = np.std(r48), np.std(r12), np.std(r24)
        m12, m24 = np.mean(r12), np.mean(r24)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values; v = b["volume"].values
            n = len(c)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            hrs.append(pd.DataFrame({"hour": ts.dt.hour, "wd": ts.dt.weekday, "r": r1 / sd12}))
            idx = np.where(ts.dt.hour.values == 23)[0]
            for i in idx:
                if i < 168 or i + 48 >= n:
                    continue
                past48 = c[i] / c[i-48] - 1
                vr = v[i-47:i+1].mean() / max(v[i-167:i-47].mean(), 1e-12)
                past24 = c[i] / c[i-24] - 1
                rows.append(dict(coin=coin, wd=ts.iloc[i].weekday(),
                                 p48=past48 / sd48, p24=past24 / sd24, vr=vr,
                                 f12=(c[i+12]/c[i]-1 - m12) / sd12,
                                 f24=(c[i+24]/c[i]-1 - m24) / sd24,
                                 f12b=(c[i+24]/c[i+12]-1 - m12) / sd12,
                                 f48=(c[i+48]/c[i]-1 - 2*m24) / sd24))
            for i in range(24, n - 24, 24):
                grid24.append(dict(coin=coin, p=(c[i]/c[i-24]-1)/sd24,
                                   f=(c[i+24]/c[i]-1 - m24)/sd24))
    E = pd.DataFrame(rows)
    def summ(df, key):
        s = np.sign(df[key])
        res = {}
        for f in ["f12", "f12b", "f24", "f48"]:
            x = (s * df[f]).dropna()
            res[f] = (x.mean(), x.mean() / (x.std() / np.sqrt(len(x))), len(x))
        return res
    tab = []
    for wd in range(7):
        d = E[E.wd == wd]
        for q, lab in [(0, "all"), (0.8, "top|p48|x vr")]:
            dd = d
            if q:
                sc = (d.p48.abs() * d.vr)
                dd = d[sc >= sc.quantile(q)]
            s = summ(dd, "p48")
            tab.append(dict(anchor_wd=wd, sel=lab, n=s["f12"][2],
                            f12=s["f12"][0], t12=s["f12"][1],
                            f12b=s["f12b"][0], t12b=s["f12b"][1],
                            f24=s["f24"][0], t24=s["f24"][1],
                            f48=s["f48"][0], t48=s["f48"][1]))
    out["signed fwd (units of usual move) after 48h move, by anchor weekday 23h"] = pd.DataFrame(tab).round(3)
    # Sunday by volume-ratio quintile
    S = E[E.wd == 6].copy()
    S["vq"] = pd.qcut(S.vr, 5, labels=False)
    S["s12"] = np.sign(S.p48) * S.f12; S["s24"] = np.sign(S.p48) * S.f24
    out["Sunday: signed fwd by vol-ratio quintile"] = S.groupby("vq").agg(
        vr=("vr", "mean"), n=("s12", "size"), s12=("s12", "mean"), s24=("s24", "mean")).round(3)
    S["pq"] = pd.qcut(S.p48.abs(), 5, labels=False)
    out["Sunday: signed fwd by |move| quintile"] = S.groupby("pq").agg(
        n=("s12", "size"), s12=("s12", "mean"), s24=("s24", "mean")).round(3)
    H = pd.concat(hrs).dropna()
    g = H.groupby("hour").r
    out["1h return by hour (units of usual 12h move)"] = pd.DataFrame(
        {"mean": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.size())), "n": g.size()}).round(4)
    g = H.groupby("wd").r
    out["1h return by weekday"] = pd.DataFrame(
        {"mean": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.size()))}).round(4)
    G = pd.DataFrame(grid24)
    G["pq"] = pd.qcut(G.p, 10, labels=False)
    gg = G.groupby("pq").f
    out["24h grid: next 24h by past-24h decile"] = pd.DataFrame(
        {"p": G.groupby("pq").p.mean(), "f": gg.mean(), "t": gg.mean() / (gg.std()/np.sqrt(gg.size())), "n": gg.size()}).round(3)
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy(); dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday; dd["coin"] = coin
            D.append(dd)
    D = pd.concat(D).dropna(subset=["book_return"])
    out["book daily return by weekday"] = D.groupby("wd").book_return.agg(["mean", "std", "count"])
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    T = pd.concat(T)
    out["trades by side"] = T.groupby("side").net_profit_loss_percent.agg(["mean", "count", "std"])
    out["trades by coin"] = T.groupby("coin").net_profit_loss_percent.agg(["mean", "count"])
    T["y"] = pd.to_datetime(T.entry_time).dt.year
    out["trades by year"] = T.groupby("y").net_profit_loss_percent.agg(["mean", "count"])
    return out
