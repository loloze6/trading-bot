def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 72
    rows = []
    grid_rows = []
    drift = {}; usd = {}
    for coin, ws in bars.items():
        rr = []
        for w, b in ws.items():
            c = b["close"].values
            n = len(c)
            for i in range(0, n - H, H):
                rr.append(c[i + H] / c[i] - 1)
        rr = np.array(rr)
        drift[coin] = rr.mean() if len(rr) else np.nan
        usd[coin] = rr.std() if len(rr) > 1 else np.nan
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; hi = b["high"]; lo = b["low"]
            n = len(b)
            ph = hi.shift(1).rolling(12).max(); pl = lo.shift(1).rolling(12).min()
            up = (c > ph).values; dn = (c < pl).values
            r180 = (c / c.shift(180) - 1).values
            r18p = (c / c.shift(18) - 1).values
            rng = (ph - pl) / c
            narrow = (rng / rng.rolling(180, min_periods=60).median()).values
            vol = np.log(c).diff().rolling(180, min_periods=60).std().values
            cv = c.values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            fw = {}
            for h in (18, 36, 72, 144):
                f = np.full(n, np.nan)
                f[:n - h] = cv[h:] / cv[:n - h] - 1
                fw[h] = f
            cells = np.arange(n) // H
            types = {
                "up_neg": up & (r180 < 0), "up_pos": up & (r180 > 0),
                "dn_neg": dn & (r180 < 0), "dn_pos": dn & (r180 > 0),
            }
            for tname, m in types.items():
                seen = set()
                for i in np.where(m)[0]:
                    if cells[i] in seen: continue
                    seen.add(cells[i])
                    if np.isnan(fw[72][i]): continue
                    rows.append(dict(coin=coin, w=w, t=tname, yr=yr[i], r180=r180[i], narrow=narrow[i],
                                     vol=vol[i], r18p=r18p[i],
                                     **{f"u{h}": fw[h][i] - drift[coin] * h / 72 for h in fw},
                                     s72=(fw[72][i] - drift[coin]) / usd[coin]))
            for i in range(0, n - H, H):
                grid_rows.append(dict(coin=coin, r180=r180[i], r18p=r18p[i], narrow=narrow[i], vol=vol[i],
                                      yr=yr[i], u72=fw[72][i] - drift[coin], s72=(fw[72][i] - drift[coin]) / usd[coin]))
    E = pd.DataFrame(rows); G = pd.DataFrame(grid_rows)
    def agg(df, col="u72"):
        x = df[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              strength=df["s72"].mean()))
    out = {}
    out["by_type"] = E.groupby("t").apply(agg)
    hz = []
    for t in ["up_neg", "up_pos", "dn_neg", "dn_pos"]:
        d = E[E.t == t]
        for h in (18, 36, 72, 144):
            x = d[f"u{h}"].dropna()
            hz.append(dict(t=t, h=h, n=len(x), mean=x.mean(), t_=x.mean() / (x.std() / np.sqrt(len(x)))))
    out["by_type_horizon"] = pd.DataFrame(hz)
    d = E[E.t == "up_neg"].copy()
    d["q_r180"] = pd.qcut(d.r180, 5, labels=False)
    out["upneg_by_depth_q"] = d.groupby("q_r180").apply(agg)
    d["q_nar"] = pd.qcut(d.narrow, 5, labels=False, duplicates="drop")
    out["upneg_by_narrow_q"] = d.groupby("q_nar").apply(agg)
    d["q_vol"] = pd.qcut(d.vol, 5, labels=False, duplicates="drop")
    out["upneg_by_vol_q"] = d.groupby("q_vol").apply(agg)
    out["upneg_by_year"] = d.groupby("yr").apply(agg)
    out["upneg_by_coin"] = d.groupby("coin").apply(agg)
    G["q_r180"] = pd.qcut(G.r180, 5, labels=False)
    out["grid_by_r180_q"] = G.groupby("q_r180").apply(agg)
    G["q_vol"] = pd.qcut(G.vol, 5, labels=False, duplicates="drop")
    out["grid_by_vol_q"] = G.groupby("q_vol").apply(agg)
    G["q_nar"] = pd.qcut(G.narrow, 5, labels=False, duplicates="drop")
    gn = G.groupby("q_nar").apply(agg)
    gn["mean_abs_u"] = G.groupby("q_nar")["u72"].apply(lambda x: x.abs().mean())
    out["grid_by_narrow_q"] = gn
    E["absu"] = E.u72.abs()
    E["q_nar"] = pd.qcut(E.narrow, 5, labels=False, duplicates="drop")
    out["all_brk_absmove_by_narrow"] = E.groupby("q_nar")["absu"].agg(["count", "mean"])
    # book
    dy = []
    for coin, ws in data["days"].items():
        for w, x in ws.items():
            x = x.copy(); x["yr"] = pd.to_datetime(x["day"]).dt.year; x["coin"] = coin
            dy.append(x)
    D = pd.concat(dy)
    out["book_by_year"] = D.groupby("yr").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    T = []
    for coin, ws in data["trades"].items():
        for w, x in ws.items():
            if len(x): T.append(x.assign(coin=coin))
    T = pd.concat(T)
    T["yr"] = pd.to_datetime(T["entry_time"]).dt.year
    out["trades_by_year"] = T.groupby("yr").agg(n=("net_profit_loss_percent", "count"), mean_net=("net_profit_loss_percent", "mean"),
                                                 win=("net_profit_loss_percent", lambda s: (s > 0).mean()))
    out["trades_dur_days"] = T["duration_minutes"].describe() / 1440
    return out
