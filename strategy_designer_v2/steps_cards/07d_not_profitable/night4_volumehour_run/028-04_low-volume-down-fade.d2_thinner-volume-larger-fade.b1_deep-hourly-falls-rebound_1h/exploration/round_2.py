def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book daily stats by coin and year
    dd = []
    for coin in data["days"]:
        for w, d in data["days"][coin].items():
            x = d.copy(); x["coin"] = coin; x["w"] = w
            x["yr"] = pd.to_datetime(x["day"]).dt.year
            dd.append(x)
    D = pd.concat(dd)
    out["book_daily_by_year"] = D.groupby("yr").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"),
                                                   n=("book_return", "count"))
    # trades
    tr = []
    for coin in data["trades"]:
        for w, t in data["trades"][coin].items():
            t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr)
    T["efc"] = pd.cut(T["entry_forecast"], [-0.01, 1, 2, 5, 10, 20.01])
    out["trades_by_entry_forecast"] = T.groupby("efc", observed=True).agg(
        n=("profit_loss_percent", "size"), gross_pct=("profit_loss_percent", "mean"),
        net_pct=("net_profit_loss_percent", "mean"), dur_min=("duration_minutes", "median"))
    out["trades_all"] = pd.Series(dict(n=len(T), gross_pct=T.profit_loss_percent.mean(),
                                       net_pct=T.net_profit_loss_percent.mean(),
                                       dur_med=T.duration_minutes.median()))
    # where the position sits: by hour z of the bar that set it
    rows = []; ev = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            c = b["close"].astype(float)
            r = c.pct_change()
            typ = r.abs().rolling(720, min_periods=240).mean()
            z = r / typ
            vr = b["volume"] / b["volume"].rolling(720, min_periods=240).mean()
            pos = b["postRebalance_current_allocation"].fillna(0)
            turn = (pos - b["previous_allocation"].fillna(0)).abs()
            r1 = c.shift(-1) / c - 1
            rows.append(pd.DataFrame(dict(z=z, pos=pos, turn=turn, g=pos * r1)))
            for h in (3, 6):
                idx = np.arange(0, len(c) - h, h)
                fr = c.values[idx + h] / c.values[idx] - 1
                ev.append(pd.DataFrame(dict(h=h, z=z.values[idx], vr=vr.values[idx], f=fr, coin=coin)))
    R = pd.concat(rows).dropna()
    R["zbin"] = pd.cut(R["z"], [-np.inf, -4, -2, -1, -0.5, 0, np.inf])
    out["position_turnover_gain_by_hour_z"] = R.groupby("zbin", observed=True).agg(
        bars=("pos", "size"), mean_pos=("pos", "mean"), turnover=("turn", "sum"), gross=("g", "sum"))
    G = pd.concat(ev).dropna()
    res = []
    for h in (3, 6):
        g = G[G.h == h]
        drift = g.groupby("coin")["f"].transform("mean")
        g = g.assign(u=g.f - drift)
        sd = g["f"].std()
        for zl, zh in [(-99, -4), (-4, -2), (-2, -1)]:
            s = g[(g.z > zl) & (g.z <= zh)]
            for vl, vh, nm in [(0, 1.5, "vol<1.5x"), (1.5, 3, "1.5-3x"), (3, 999, ">3x")]:
                q = s[(s.vr > vl) & (s.vr <= vh)]
                if len(q) > 5:
                    res.append(dict(h=h, z=f"{zl},{zh}", vol=nm, n=len(q), total=q.f.mean(), unusual=q.u.mean(),
                                    t=q.u.mean() / (q.u.std() / np.sqrt(len(q))), strength=q.u.mean() / sd))
    out["grid_falls_by_depth_and_volume"] = pd.DataFrame(res)
    return out
