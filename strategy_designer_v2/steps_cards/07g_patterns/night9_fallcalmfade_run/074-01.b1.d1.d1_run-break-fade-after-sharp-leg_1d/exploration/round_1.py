def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            o = b["open"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            nxt3 = c.shift(-3) / c - 1
            down = (r < 0).astype(int)
            # run of down closes before this bar
            run = np.zeros(len(c)); cnt = 0
            for i in range(len(c)):
                run[i] = cnt if r.iloc[i] > 0 else np.nan
                if r.iloc[i] < 0: cnt += 1
                elif r.iloc[i] > 0: cnt = 0
            vol30 = r.rolling(30).std()
            ret5 = c / c.shift(5) - 1
            tr60 = c / c.shift(60) - 1
            rng = (h - l) / c
            clpos = (c - l) / (h - l).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "r": r, "nxt": nxt, "nxt3": nxt3, "run": run,
                               "z5": ret5 / vol30, "zr": r / vol30, "tr60": tr60, "vol30": vol30,
                               "rngz": rng / vol30, "clpos": clpos, "wd": ts.dt.weekday,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "fc": b["forecast"].astype(float)})
            df["rows"] = np.arange(len(df))
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    mu = D["nxt"].mean()
    D["un"] = D["nxt"] - mu
    D["trend"] = np.where(D["tr60"] < -0.10, "falling", np.where(D["tr60"] > 0.10, "rising", np.where(D["tr60"].notna(), "choppy", "na")))
    def tt(s):
        s = s.dropna(); n = len(s)
        return pd.Series({"n": n, "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    up = D[D["run"].notna()]
    up = up.assign(runb=up["run"].clip(upper=4))
    out["upday_next_by_trend_run"] = up.groupby(["trend", "runb"])["un"].apply(tt).unstack()
    # all days by trend & sign of today's move z
    D["zrb"] = pd.cut(D["zr"], [-99, -2, -1, 0, 1, 2, 99])
    out["next_by_trend_zr"] = D.groupby(["trend", "zrb"])["un"].apply(tt).unstack()
    D["z5b"] = pd.cut(D["z5"], [-99, -4, -2, 0, 2, 4, 99])
    out["next_by_trend_z5"] = D.groupby(["trend", "z5b"])["un"].apply(tt).unstack()
    D["clb"] = pd.cut(D["clpos"], [0, .2, .4, .6, .8, 1.0], include_lowest=True)
    out["next_by_trend_closepos"] = D.groupby(["trend", "clb"])["un"].apply(tt).unstack()
    out["next_by_weekday"] = D.groupby("wd")["un"].apply(tt).unstack()
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    DD = pd.concat(dd)
    out["book_by_window"] = DD.groupby("w")["book_return"].agg(["mean", "std", "count"])
    t = pd.concat([tr.assign(coin=c) for c, ws in data["trades"].items() for w, tr in ws.items()])
    out["trades_summary"] = t.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median", "min", "max"])
    return out
