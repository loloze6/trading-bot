def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            allr.append(c[1:]/c[:-1]-1)
        cat = np.concatenate(allr)
        drift = np.nanmean(cat)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); o = df["open"].astype(float)
            h = df["high"].astype(float); l = df["low"].astype(float)
            r = c.pct_change()
            run = np.zeros(len(df), dtype=int); cnt = 0
            for i in range(len(df)):
                run[i] = cnt
                cnt = cnt+1 if (r.iloc[i] < 0) else 0
            vol20 = r.rolling(20).std()
            runret = pd.Series(np.nan, index=df.index)
            for i in range(len(df)):
                if run[i] >= 1 and i-run[i]-1 >= 0:
                    runret.iloc[i] = c.iloc[i-1]/c.iloc[i-run[i]-1]-1
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                "r": r, "n1": c.shift(-1)/c-1-drift, "n3": c.shift(-3)/c-1-3*drift,
                "run": run, "rg": df["regime"].astype(str),
                "ret20": c/c.shift(20)-1, "ret60": c/c.shift(60)-1,
                "z": r/vol20, "runz": runret/(vol20*np.sqrt(np.maximum(run,1))),
                "runret_v": runret/vol20,
                "cl": (c-l)/(h-l).replace(0,np.nan),
            })
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    def ct(s, col):
        s = s.dropna(subset=[col])
        if len(s) < 8: return pd.Series({"n": len(s), "days": np.nan, "mean": np.nan, "t": np.nan})
        dev = s[col]-s[col].mean(); g = dev.groupby(s["day"]).sum(); G = len(g)
        se = np.sqrt((g**2).sum()*G/(G-1))/len(s)
        return pd.Series({"n": len(s), "days": G, "mean": s[col].mean(), "t": s[col].mean()/se})
    out = {}
    B = A[(A.r > 0) & (A.run >= 2)].copy()
    out["all_breaks_n1"] = ct(B, "n1"); out["all_breaks_n3"] = ct(B, "n3")
    nb = A[~((A.r > 0) & (A.run >= 2))]
    out["nonbreak_n1"] = ct(nb, "n1")
    B["tr60"] = pd.cut(B["ret60"], [-9, -0.10, 0.10, 9], labels=["falling","choppy","rising"])
    out["break_by_trend60_n1"] = B.groupby("tr60").apply(lambda s: ct(s,"n1"))
    out["break_by_trend60_n3"] = B.groupby("tr60").apply(lambda s: ct(s,"n3"))
    B["r20b"] = pd.qcut(B["ret20"], 4, labels=["q1","q2","q3","q4"])
    out["break_by_ret20q_n1"] = B.groupby("r20b").apply(lambda s: ct(s,"n1"))
    B["rvb"] = pd.qcut(B["runret_v"], 4, labels=["deep","q2","q3","shallow"])
    out["break_by_runfall_n1"] = B.groupby("rvb").apply(lambda s: ct(s,"n1"))
    out["break_by_runfall_n3"] = B.groupby("rvb").apply(lambda s: ct(s,"n3"))
    B["zb"] = pd.qcut(B["z"], 3, labels=["small_up","mid_up","big_up"])
    out["break_by_upsize_n1"] = B.groupby("zb").apply(lambda s: ct(s,"n1"))
    B["clb"] = pd.cut(B["cl"], [-0.01,0.5,0.8,1.01], labels=["low","mid","high"])
    out["break_by_closeloc_n1"] = B.groupby("clb").apply(lambda s: ct(s,"n1"))
    out["break_by_year_n1"] = B.groupby(B["day"].dt.year).apply(lambda s: ct(s,"n1"))
    out["break_by_coin_n1"] = B.groupby("coin").apply(lambda s: ct(s,"n1"))
    # slope n1 on runret_v and z
    s = B.dropna(subset=["n1","runret_v","z"])
    X = np.column_stack([np.ones(len(s)), s["runret_v"], s["z"]])
    beta, *_ = np.linalg.lstsq(X, s["n1"].values, rcond=None)
    res = s["n1"].values - X@beta
    cov = np.linalg.inv(X.T@X)*(res@res)/(len(s)-3)
    out["ols_n1_on_runfall_upz"] = pd.Series({"b_runfall": beta[1], "t_runfall": beta[1]/np.sqrt(cov[1,1]), "b_upz": beta[2], "t_upz": beta[2]/np.sqrt(cov[2,2]), "n": len(s)})
    return out
