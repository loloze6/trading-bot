def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            b["hour"] = ts.dt.hour.values
            b["year"] = ts.dt.year.values
            c = b["close"].astype(float)
            lr = np.log(c).diff()
            b["r1"] = c.shift(-1) / c - 1
            b["f2"] = c.shift(-2) / c - 1
            b["f4"] = c.shift(-4) / c - 1
            vol = lr.rolling(20).std()
            b["z24"] = (np.log(c) - np.log(c.shift(24))) / (vol * np.sqrt(24))
            b["z6"] = (np.log(c) - np.log(c.shift(6))) / (vol * np.sqrt(6))
            b["pos_i"] = np.arange(len(b))
            b["coin"] = coin; b["win"] = w
            b["fc"] = b["forecast"].astype(float)
            rows.append(b[["coin","win","year","hour","r1","f2","f4","z24","z6","pos_i","fc"]])
    d = pd.concat(rows, ignore_index=True)
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean_bp": x.mean()*1e4, "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    # evening drift: 2-bar return from bar stamped 20 (close 21:00 -> 23:00)
    e = d[d.hour == 20].copy()
    mu2 = d[d.pos_i % 2 == 0]["f2"].mean()
    e["x2"] = e.f2 - mu2
    out["eve_x2_by_coin"] = e.groupby("coin")["x2"].apply(tt).unstack().round(2)
    out["eve_x2_by_year"] = e.groupby("year")["x2"].apply(tt).unstack().round(2)
    out["eve_x2_fc_zero_vs_pos"] = e.groupby(e.fc > 0)["x2"].apply(tt).unstack().round(2)
    wm = e.groupby(["coin","win"])["x2"].mean()
    out["eve_share_coinwindows_positive"] = float((wm > 0).mean())
    # pooled 2-bar reversal on z24 and z6, non-overlapping grid, by year
    g = d[d.pos_i % 2 == 0].dropna(subset=["f2","z24","z6"])
    res = []
    for yr, s in list(g.groupby("year")) + [("all", g)]:
        for v in ["z24","z6"]:
            sl = stats.linregress(s[v], s.f2)
            res.append({"year": yr, "var": v, "n": len(s), "slope_bp": sl.slope*1e4, "t": sl.slope/sl.stderr})
    out["f2_reversal_by_year"] = pd.DataFrame(res).round(2)
    res = []
    for coin, s in g.groupby("coin"):
        sl = stats.linregress(s["z6"], s.f2)
        res.append({"coin": coin, "n": len(s), "slope_bp": sl.slope*1e4, "t": sl.slope/sl.stderr})
    out["f2_on_z6_by_coin"] = pd.DataFrame(res).round(2)
    # 4-bar horizon on z6, quintiles
    g4 = d[d.pos_i % 4 == 0].dropna(subset=["f4","z6"]).copy()
    g4["q"] = pd.qcut(g4.z6, 5, labels=False)
    out["f4_by_z6_quintile"] = g4.groupby("q")["f4"].apply(tt).unstack().round(2)
    # book: daily gross vs fees
    fee = []; 
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            fee.append(t["total_commission"].astype(float).sum())
    out["total_commission_sum"] = float(np.sum(fee))
    dd = pd.concat([x.assign(coin=c) for c, ws in data["days"].items() for x in ws.values()])
    out["book_daily"] = tt(dd.groupby(["coin"])["book_return"].mean()).round(3)
    tr = pd.concat([x for ws in data["trades"].values() for x in ws.values()])
    out["trade_pl_bp"] = pd.DataFrame({"gross": tt(tr.profit_loss_percent.astype(float)/100), "net": tt(tr.net_profit_loss_percent.astype(float)/100)}).round(2)
    return out
