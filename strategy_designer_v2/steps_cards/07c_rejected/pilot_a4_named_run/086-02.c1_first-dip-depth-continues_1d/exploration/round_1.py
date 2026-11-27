def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    for coin, ws in bars.items():
        r5 = []
        for w, df in ws.items():
            c = df["close"].values
            for i in range(0, len(c) - 5, 5):
                r5.append(c[i+5]/c[i]-1)
        drift[coin] = np.mean(r5); usual[coin] = np.std(r5)
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            ret = pd.Series(c).pct_change()
            vol30 = ret.rolling(30, min_periods=15).std()
            # up run count before each bar
            up = (ret > 0).astype(int).values
            run = np.zeros(len(c), int)
            for i in range(1, len(c)):
                run[i] = run[i-1] + 1 if up[i] else 0
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(1, len(c)):
                if ret.iloc[i] < 0 and run[i-1] >= 2:
                    rec = dict(coin=coin, w=w, year=yr[i], pos=i, run=run[i-1],
                               z=ret.iloc[i]/vol30.iloc[i] if vol30.iloc[i] > 0 else np.nan,
                               regime=df["regime"].iloc[i],
                               runret=c[i-1]/c[i-1-run[i-1]]-1 if i-1-run[i-1] >= 0 else np.nan,
                               fc=df["forecast"].iloc[i])
                    for h in [1, 2, 3, 5, 10]:
                        rec[f"s{h}"] = -(c[i+h]/c[i]-1) if i+h < len(c) else np.nan
                    rec["u5"] = rec["s5"] + drift[coin] if not np.isnan(rec["s5"]) else np.nan
                    rows.append(rec)
    d = pd.DataFrame(rows)
    d["inprof"] = d["regime"].isin(["mean_reversion", "unknown"])
    d["grp"] = np.where(d["regime"] == "mean_reversion", "profile", np.where(d["regime"] == "chop", "outside", d["regime"]))
    def summ(g):
        out = {"n": len(g)}
        for h in [1, 2, 3, 5, 10]:
            x = g[f"s{h}"].dropna()
            out[f"mean_s{h}"] = x.mean()
            out[f"t_s{h}"] = x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan
        x = g["u5"].dropna(); out["mean_u5"] = x.mean()
        out["t_u5"] = x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(out)
    res = {}
    res["by_group"] = d.groupby("grp").apply(summ)
    p = d[d.grp == "profile"].copy()
    res["profile_by_coin"] = p.groupby("coin").apply(summ)
    res["profile_by_year"] = p.groupby("year").apply(summ)
    res["profile_by_window"] = p.groupby("w").apply(summ)
    p["runb"] = pd.cut(p["run"], [1, 2, 3, 5, 30])
    res["profile_by_run"] = p.groupby("runb").apply(summ)
    p["zq"] = pd.qcut(p["z"], 3, labels=["deep", "mid", "shallow"])
    res["profile_by_depth"] = p.groupby("zq").apply(summ)
    p["rrq"] = pd.qcut(p["runret"], 3, labels=["small", "mid", "big"])
    res["profile_by_runret"] = p.groupby("rrq").apply(summ)
    o = d[d.grp == "outside"].copy()
    o["zq"] = pd.qcut(o["z"], 3, labels=["deep", "mid", "shallow"])
    res["outside_by_depth"] = o.groupby("zq").apply(summ)
    res["corr_profile"] = pd.Series({"z_vs_u5": p[["z", "u5"]].corr().iloc[0, 1],
                                     "run_vs_u5": p[["run", "u5"]].corr().iloc[0, 1],
                                     "runret_vs_u5": p[["runret", "u5"]].corr().iloc[0, 1]})
    res["drift_usual"] = pd.DataFrame({"drift5": drift, "usual5": usual})
    return res
