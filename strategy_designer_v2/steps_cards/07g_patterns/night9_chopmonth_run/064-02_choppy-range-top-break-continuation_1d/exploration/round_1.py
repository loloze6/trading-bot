def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            tr60 = c / c.shift(60) - 1
            hi30 = c.shift(1).rolling(30, min_periods=20).max()
            lo30 = c.shift(1).rolling(30, min_periods=20).min()
            dhi = (c - hi30) / hi30 / sd30
            dlo = (c - lo30) / lo30 / sd30
            z1 = r1 / sd30
            r5past = c / c.shift(5) - 1
            z5 = r5past / (sd30 * np.sqrt(5))
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            vol = b["volume"].astype(float)
            vz = vol / vol.rolling(30, min_periods=20).mean()
            sd365 = r1.rolling(30, min_periods=20).std()
            agit = sd30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "year": pd.to_datetime(b["timestamp"]).dt.year,
                               "z1": z1, "z5": z5, "dhi": dhi, "dlo": dlo, "tr60": tr60, "fwd": fwd, "fwd1": fwd1,
                               "clv": clv, "vz": vz, "agit": agit, "sd": sd30,
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % H == 0].groupby("coin")["fwd"].mean()
    A["ufwd"] = A["fwd"] - A["coin"].map(drift)
    A["trend"] = np.where(A.tr60 > 0.10, "rising", np.where(A.tr60 < -0.10, "falling", "choppy"))
    A.loc[A.tr60.isna(), "trend"] = np.nan
    A["ag"] = np.where(A.agit > 0.5, "agit", "calm"); A.loc[A.agit.isna(), "ag"] = np.nan
    G = A[(A.pos % H == 0)].dropna(subset=["ufwd", "z1", "trend"])
    out = {}
    def tab(g, col):
        def f(x):
            u = x["ufwd"]; return pd.Series({"n": len(u), "mean": u.mean(), "t": u.mean() / (u.std() / np.sqrt(len(u))) if len(u) > 2 else np.nan})
        return g.groupby(col).apply(f)
    G["z1b"] = pd.cut(G.z1, [-99, -2, -1, 1, 2, 99])
    out["z1 bins by trend"] = tab(G, ["trend", "z1b"])
    G["z5b"] = pd.cut(G.z5, [-99, -1.5, -0.5, 0.5, 1.5, 99])
    out["z5 bins by trend"] = tab(G, ["trend", "z5b"])
    G["dhib"] = pd.cut(G.dhi, [-99, -3, -1, 0, 1, 99])
    out["dhi bins by trend"] = tab(G, ["trend", "dhib"])
    G["dlob"] = pd.cut(G.dlo, [-99, 0, 1, 3, 99])
    out["dlo bins by trend"] = tab(G, ["trend", "dlob"])
    G["clvb"] = pd.cut(G.clv, [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
    out["clv bins by trend x ag"] = tab(G.dropna(subset=["ag"]), ["trend", "ag", "clvb"])
    out["weekday"] = tab(G, "wd")
    G["vzb"] = pd.cut(G.vz, [0, .7, 1, 1.5, 2.5, 99])
    out["volume ratio by trend"] = tab(G, ["trend", "vzb"])
    out["trend x ag"] = tab(G.dropna(subset=["ag"]), ["trend", "ag"])
    return out
