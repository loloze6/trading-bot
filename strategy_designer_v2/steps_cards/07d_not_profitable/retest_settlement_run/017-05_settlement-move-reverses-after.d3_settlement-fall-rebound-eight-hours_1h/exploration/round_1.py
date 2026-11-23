def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [8, 16, 24]
    rows = []
    drift = {}; usual = {}
    for coin, wins in data["bars"].items():
        dr = {h: [] for h in H}
        for w, b in wins.items():
            c = b["close"].values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                dr[h].extend(list(c[idx + h] / c[idx] - 1))
        for h in H:
            drift[(coin, h)] = np.mean(dr[h]); usual[(coin, h)] = np.std(dr[h])
        for w, b in wins.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"]
            r2 = c / c.shift(2) - 1
            scale = r2.abs().rolling(720, min_periods=120).mean()
            z = r2 / scale
            r24 = c / c.shift(24) - 1
            r168 = c / c.shift(168) - 1
            sc24 = r24.abs().rolling(720, min_periods=120).mean()
            hr = ((ts + pd.Timedelta(hours=1)).dt.hour).values
            d = pd.DataFrame({"coin": coin, "win": w, "hour": hr, "z": z.values,
                              "fc": b["forecast"].values, "r24z": (r24 / sc24).values,
                              "r168": r168.values, "year": ts.dt.year.values})
            for h in H:
                d[f"f{h}"] = (c.shift(-h) / c - 1).values - drift[(coin, h)]
                d[f"s{h}"] = d[f"f{h}"] / usual[(coin, h)]
            # keep one bar per 8h-grid cell-like: every bar but we'll subsample by hour classes
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    S = D[D.hour.isin([0, 16])].dropna(subset=["z", "f24"])
    S = S.assign(zb=pd.cut(S.z, [-99, -3, -2, -1.5, -1, -0.5, 0, 99]))
    out["settle_by_fallz"] = S.groupby("zb").agg(n=("f8", "size"), ex8=("f8", "mean"),
        ex16=("f16", "mean"), ex24=("f24", "mean"), str8=("s8", "mean"), str24=("s24", "mean"))
    # same by any hour (fall z<-1) by settlement hour
    A = D.dropna(subset=["z", "f24"])
    A = A[A.z < -1]
    g = A.groupby("hour").agg(n=("f8", "size"), ex8=("f8", "mean"), ex24=("f24", "mean"))
    g["t8"] = A.groupby("hour")["f8"].apply(lambda x: x.mean() / x.std() * np.sqrt(len(x)))
    out["fall_z_lt_-1_by_close_hour"] = g
    # cases fc>=2 split by settlement and by trend
    C = S[S.fc >= 2]
    out["cases_by_hour"] = C.groupby("hour").agg(n=("f8", "size"), ex8=("f8", "mean"), ex24=("f24", "mean"))
    C = C.assign(tr=pd.cut(C.r168, [-9, -0.1, -0.03, 0.03, 0.1, 9]))
    out["cases_by_7d_trend"] = C.groupby("tr").agg(n=("f8", "size"), ex8=("f8", "mean"), ex24=("f24", "mean"))
    N = S[S.fc < 2].assign(tr=pd.cut(S.r168, [-9, -0.1, -0.03, 0.03, 0.1, 9]))
    out["noncases_settle_by_7d_trend"] = N.groupby("tr").agg(n=("f8", "size"), ex8=("f8", "mean"), ex24=("f24", "mean"))
    out["cases_by_year"] = C.groupby("year").agg(n=("f8", "size"), ex8=("f8", "mean"))
    # trades
    T = pd.concat([t.assign(coin=k) for k, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    T["fb"] = pd.cut(T.entry_forecast, [-1, 2, 5, 10, 15, 21])
    out["trades_by_entry_fc"] = T.groupby("fb").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda x: x.mean() / 60))
    out["trades_sides"] = T.side.value_counts()
    return out
