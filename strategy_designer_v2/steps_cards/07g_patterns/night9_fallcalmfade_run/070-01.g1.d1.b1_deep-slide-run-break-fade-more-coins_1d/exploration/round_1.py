def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        # drift over all windows
        allr = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            allr.append(c[1:]/c[:-1]-1)
        drift = np.nanmean(np.concatenate(allr)) if allr else 0.0
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            o = df["open"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1)/c - 1
            nxt3 = c.shift(-3)/c - 1
            # down run length before this bar
            dn = (r < 0).astype(int)
            run = np.zeros(len(df), dtype=int)
            cnt = 0
            for i in range(len(df)):
                run[i] = cnt  # down closes ending at i-1
                if i < len(df):
                    cnt = cnt+1 if dn.iloc[i] == 1 else 0
            vol20 = r.rolling(20).std()
            ret20 = c/c.shift(20)-1
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                "wd": pd.to_datetime(df["timestamp"]).dt.weekday,
                "r": r, "nxt_u": nxt - drift, "nxt3_u": nxt3 - 3*drift,
                "run": run, "regime": df["regime"].astype(str),
                "fc": df["forecast"].astype(float),
                "vol20": vol20, "ret20": ret20,
                "z": r/vol20,
                "body": (c-o)/(df["high"].astype(float)-df["low"].astype(float)).replace(0,np.nan),
            })
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)

    def ct(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 5: return pd.Series({"n": len(s), "days": s["day"].nunique() if len(s) else 0, "mean": np.nan, "t": np.nan})
        dev = s[col] - s[col].mean()
        g = dev.groupby(s["day"]).sum()
        G = len(g)
        se = np.sqrt((g**2).sum()*G/(G-1))/len(s)
        return pd.Series({"n": len(s), "days": G, "mean": s[col].mean(), "t": s[col].mean()/se})

    out = {}
    A["brk"] = (A["r"] > 0) & (A["run"] >= 2)
    A["rg"] = A["regime"].map(lambda x: x if x in ("trending","unknown","chop") else "other")
    # 1 run breaks by regime, next-day unusual (raw, long sign)
    out["break_by_regime_nxt"] = A[A.brk].groupby("rg").apply(lambda s: ct(s,"nxt_u"))
    out["break_by_regime_nxt3"] = A[A.brk].groupby("rg").apply(lambda s: ct(s,"nxt3_u"))
    # 2 grading by run length inside each regime
    A["runb"] = pd.cut(A["run"], [1,2,3,4,30], labels=["2","3","4","5+"])
    out["break_run_regime_nxt"] = A[A.brk].groupby(["rg","runb"]).apply(lambda s: ct(s,"nxt_u"))
    # 3 all bars: next day after daily z-move, by regime
    A["zb"] = pd.qcut(A["z"], 5, labels=["q1","q2","q3","q4","q5"])
    out["z_quint_by_regime_nxt"] = A.groupby(["rg","zb"]).apply(lambda s: ct(s,"nxt_u"))
    out["z_quint_all_nxt3"] = A.groupby("zb").apply(lambda s: ct(s,"nxt3_u"))
    # 4 weekday
    out["weekday_nxt"] = A.groupby("wd").apply(lambda s: ct(s,"nxt_u"))
    # 5 vol level (in-window terciles per coin)
    A["volq"] = A.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["vol_by_nxt"] = A.groupby("volq").apply(lambda s: ct(s,"nxt_u"))
    # 6 regime share of bars
    out["regime_share"] = A["rg"].value_counts(normalize=True)
    # 7 book daily returns by largest gains/losses
    D = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            D.append(df.assign(coin=coin, win=w))
    D = pd.concat(D, ignore_index=True)
    book = D.groupby("day")["book_return"].mean().dropna()
    out["book_by_year"] = book.groupby(pd.to_datetime(book.index).year).agg(["count","mean","std"])
    # case returns by year
    cases = A[A.fc < 0]
    out["cases_by_year"] = cases.groupby(cases["day"].dt.year).apply(lambda s: ct(s.assign(sh=-s["nxt_u"]),"sh"))
    out["cases_by_coin"] = cases.groupby("coin").apply(lambda s: ct(s.assign(sh=-s["nxt_u"]),"sh"))
    return out
