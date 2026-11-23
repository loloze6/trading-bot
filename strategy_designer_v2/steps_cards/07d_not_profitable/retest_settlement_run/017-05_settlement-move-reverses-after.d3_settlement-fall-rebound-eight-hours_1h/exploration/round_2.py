def explore(data):
    import numpy as np, pandas as pd
    H = [8, 24]
    rows = []; drift = {}; usual = {}
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
            ts = pd.to_datetime(b["timestamp"]); c = b["close"]
            r2 = c / c.shift(2) - 1
            z = r2 / r2.abs().rolling(720, min_periods=120).mean()
            hr = ((ts + pd.Timedelta(hours=1)).dt.hour).values
            al = b["postRebalance_current_allocation"].values
            ch = np.abs(b["postRebalance_current_allocation"] - b["previous_allocation"]).values
            d = pd.DataFrame({"coin": coin, "win": w, "hour": hr, "z": z.values, "fc": b["forecast"].values,
                              "year": ts.dt.year.values, "alloc": al, "turn": ch})
            for h in H:
                d[f"f{h}"] = (c.shift(-h) / c - 1).values - drift[(coin, h)]
                d[f"tot{h}"] = (c.shift(-h) / c - 1).values
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    def agg(g):
        return pd.Series({"n": len(g), "ex8": g.f8.mean(), "t8": g.f8.mean()/g.f8.std()*np.sqrt(len(g)),
                          "ex24": g.ex24.mean() if "ex24" in g else np.nan})
    S = D[D.hour.isin([0, 16, 8])].dropna(subset=["z", "f24"])
    S = S.assign(zb=pd.cut(S.z, [-99, -3, -2, -1, 99]))
    g = S.groupby(["hour", "zb"])
    r = g.agg(n=("f8", "size"), ex8=("f8", "mean"), ex24=("f24", "mean"), tot24=("tot24", "mean"),
              sd8=("f8", "std"), sd24=("f24", "std"))
    r["t8"] = r.ex8 / r.sd8 * np.sqrt(r.n); r["t24"] = r.ex24 / r.sd24 * np.sqrt(r.n)
    out["by_hour_and_fall"] = r.drop(columns=["sd8", "sd24"])
    St = S[(S.z <= -2) & S.hour.isin([0, 16])]
    y = St.groupby("year").agg(n=("f8", "size"), ex8=("f8", "mean"), ex24=("f24", "mean"))
    out["strong_falls_z_le_-2_by_year"] = y
    out["strong_falls_z_le_-2_by_coin"] = St.groupby("coin").agg(n=("f8", "size"), ex8=("f8", "mean"), ex24=("f24", "mean"))
    # book turnover: share of turnover on non-settlement bars
    D["settle"] = D.hour.isin([0, 16])
    out["turnover_by_settle_bar"] = D.groupby("settle").agg(turn_sum=("turn", "sum"), mean_abs_alloc=("alloc", lambda x: x.abs().mean()))
    # fc vs z among cases
    C = S[(S.fc >= 2) & S.hour.isin([0, 16])]
    out["cases_fc_bucket_vs_z"] = C.groupby(pd.cut(C.fc, [2, 5, 10, 15, 19.99, 21])).agg(n=("z", "size"), z=("z", "mean"), ex8=("f8", "mean"), ex24=("f24", "mean"))
    return out
