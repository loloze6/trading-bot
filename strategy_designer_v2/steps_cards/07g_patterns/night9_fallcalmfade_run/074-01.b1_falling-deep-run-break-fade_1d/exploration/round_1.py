def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            sd30 = r.rolling(30, min_periods=20).std()
            tr60 = (c / c.shift(60) - 1) * 100
            down = (r < 0).astype(int)
            # run length of down closes ending at t-1
            run = np.zeros(len(b), dtype=int)
            cnt = 0
            for i in range(len(b)):
                run[i] = cnt if (r.iloc[i] > 0) else 0
                if r.iloc[i] < 0: cnt += 1
                elif r.iloc[i] > 0: cnt = 0
            # run loss
            logc = np.log(c)
            runloss = pd.Series([ (logc.iloc[i-1]-logc.iloc[i-1-run[i]]) if run[i]>0 and i-1-run[i]>=0 else np.nan for i in range(len(b))])
            df = pd.DataFrame({"coin": coin, "win": w, "ts": b["timestamp"], "r": r, "nxt": nxt,
                               "sd30": sd30, "tr60": tr60, "run": run,
                               "depth": -runloss / sd30, "bounce_z": r / sd30,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "fc": b["forecast"].astype(float)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["ts"] = pd.to_datetime(d["ts"])
    d["wd"] = d["ts"].dt.weekday
    d["day"] = d["ts"].dt.floor("D")
    drift = d.groupby("coin")["nxt"].transform("mean")
    d["adj"] = d["nxt"] - drift
    medsd = d.groupby("coin")["sd30"].transform("median")
    d["agit"] = np.where(d["sd30"] > medsd, "agit", "calm")
    d["trend"] = pd.cut(d["tr60"], [-1e9, -10, 10, 1e9], labels=["falling", "choppy", "rising"])
    d = d.dropna(subset=["adj"])
    def summ(g):
        x = g["adj"]
        if len(x) < 5: return pd.Series({"n": len(x), "mean%": np.nan, "t": np.nan})
        # day-clustered t
        s = g.groupby("day")["adj"].sum()
        nd = len(s)
        m = x.mean()
        dev = (g["adj"] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev**2).sum()) / len(x)
        return pd.Series({"n": len(x), "days": nd, "mean%": 100*m, "t": m/se})
    bnc = d[d["run"] >= 1].dropna(subset=["trend"])
    out = {}
    out["bounce_by_trend"] = bnc.groupby("trend").apply(summ)
    bnc2 = bnc.copy()
    bnc2["runb"] = pd.cut(bnc2["run"], [0, 1, 2, 3, 100], labels=["1", "2", "3", "4+"])
    out["bounce_trend_run"] = bnc2.groupby(["trend", "runb"]).apply(summ)
    bnc2["depthq"] = bnc2.groupby("trend")["depth"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["bounce_trend_depthq"] = bnc2.groupby(["trend", "depthq"]).apply(summ)
    bnc2["bzq"] = bnc2.groupby("trend")["bounce_z"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["bounce_trend_bouncesizeq"] = bnc2.groupby(["trend", "bzq"]).apply(summ)
    out["bounce_trend_agit"] = bnc.groupby(["trend", "agit"]).apply(summ)
    # all days: next day after up/down days by trend and size
    dd = d.dropna(subset=["trend", "sd30"]).copy()
    dd["zq"] = pd.cut(dd["r"] / dd["sd30"], [-99, -2, -1, 0, 1, 2, 99])
    out["all_trend_zbin"] = dd.groupby(["trend", "zq"]).apply(summ)
    out["weekday_all"] = dd.groupby("wd").apply(summ)
    out["weekday_falling"] = dd[dd["trend"] == "falling"].groupby("wd").apply(summ)
    return out
