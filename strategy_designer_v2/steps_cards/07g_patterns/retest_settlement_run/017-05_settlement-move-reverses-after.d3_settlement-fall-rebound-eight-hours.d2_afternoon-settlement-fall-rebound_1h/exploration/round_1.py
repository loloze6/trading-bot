def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    hourly = []
    for coin, wins in data["bars"].items():
        # drift over 8 bars, non-overlapping, all windows
        nn = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 8, 8)
            nn.append(c[idx + 8] / c[idx] - 1)
        nn = np.concatenate(nn); drift = nn.mean(); usual = nn.std()
        for w, b in wins.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            ch = ((ts + pd.Timedelta(hours=1)).dt.hour).values
            c = b["close"]
            r2 = c / c.shift(2) - 1
            sc = r2.abs().rolling(720, min_periods=240).mean()
            z = r2 / sc
            f8 = c.shift(-8) / c - 1
            f1 = c.shift(-1) / c - 1
            r24 = c / c.shift(24) - 1
            vol = b["volume"]
            vrel = vol / vol.rolling(720, min_periods=240).median()
            d = pd.DataFrame({"coin": coin, "w": w, "ch": ch, "z": z.values,
                              "f8": (f8 - drift).values, "f8s": ((f8 - drift) / usual).values,
                              "f1": f1.values, "r24": r24.values, "vrel": vrel.values,
                              "wd": (ts + pd.Timedelta(hours=1)).dt.weekday.values,
                              "yr": ts.dt.year.values})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # by close hour: falls only, product -z * f8s; and rises
    res = []
    for h, g in D.dropna(subset=["z", "f8s"]).groupby("ch"):
        fa = g[g.z < 0]; ri = g[g.z > 0]
        p = (-fa.z) * fa.f8s
        q = (ri.z) * ri.f8s
        res.append({"ch": h, "n_fall": len(fa), "fall_strength": fa.f8s.mean(),
                    "fall_prod_t": p.mean() / p.std() * np.sqrt(len(p)),
                    "rise_strength": ri.f8s.mean(),
                    "rise_prod_t": q.mean() / q.std() * np.sqrt(len(q)),
                    "corr_z_f8": np.corrcoef(g.z, g.f8s)[0, 1]})
    out["reversal_by_close_hour"] = pd.DataFrame(res).round(4)
    # 1h return by close hour
    g1 = D.dropna(subset=["f1"]).groupby("ch")["f1"]
    out["next1h_by_close_hour_bp"] = pd.DataFrame({"mean_bp": g1.mean() * 1e4,
                                                   "t": g1.mean() / g1.std() * np.sqrt(g1.count())}).round(2)
    out["vol_rel_by_close_hour"] = D.groupby("ch")["vrel"].median().round(3)
    # z deciles at all hours vs f8s
    E = D.dropna(subset=["z", "f8s"]).copy()
    E["dec"] = pd.qcut(E.z, 10, labels=False)
    out["f8s_by_z_decile_all_hours"] = E.groupby("dec").agg(z=("z", "mean"), f8s=("f8s", "mean"), n=("f8s", "size")).round(4)
    # 24h return deciles vs f8s at hour 16 only vs all
    E2 = D[D.ch == 16].dropna(subset=["r24", "f8s"]).copy()
    E2["dec"] = pd.qcut(E2.r24, 5, labels=False)
    out["f8s_by_r24_quintile_at16"] = E2.groupby("dec").agg(r24=("r24", "mean"), f8s=("f8s", "mean"), n=("f8s", "size")).round(4)
    # book daily by weekday and year
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; dd.append(x)
    DD = pd.concat(dd); DD["day"] = pd.to_datetime(DD["day"])
    bk = DD.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    bk["wd"] = bk.index.weekday; bk["yr"] = bk.index.year
    out["book_by_weekday_bp"] = (bk.groupby("wd")[["book_return", "coin_return"]].mean() * 1e4).round(2)
    out["book_by_year_bp"] = (bk.groupby("yr")[["book_return", "coin_return"]].mean() * 1e4).round(2)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades_by_coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"),
                                                  gross=("profit_loss_percent", "mean"),
                                                  net=("net_profit_loss_percent", "mean"),
                                                  dur_h=("duration_minutes", lambda s: s.mean() / 60)).round(3)
    return out
