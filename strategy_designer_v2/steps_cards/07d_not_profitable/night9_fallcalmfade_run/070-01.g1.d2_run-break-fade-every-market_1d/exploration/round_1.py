def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    allrows = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].astype(float)
            allr.append((c.shift(-1)/c-1).dropna())
        drift = pd.concat(allr).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r = c/c.shift(1)-1
            nxt = c.shift(-1)/c-1
            dn = (r < 0).astype(int)
            run = np.zeros(len(df)); cnt = 0
            for i in range(len(df)):
                # run of down days ending at i-1
                run[i] = cnt
                cnt = cnt+1 if r.iloc[i] < 0 else 0
            runfall = np.full(len(df), np.nan)
            for i in range(len(df)):
                k = int(run[i])
                if k > 0 and i-k-1 >= 0:
                    runfall[i] = c.iloc[i-1]/c.iloc[i-k-1]-1
            t60 = c/c.shift(60)-1
            t20 = c/c.shift(20)-1
            v30 = r.rolling(30).std()
            vall = r.expanding(30).std()
            ag = v30/vall
            yr = pd.to_datetime(df["timestamp"]).dt.year
            alloc = df["postRebalance_current_allocation"].astype(float)
            d = pd.DataFrame({"coin": coin, "w": w, "year": yr, "fc": df["forecast"].astype(float),
                              "run": run, "up": r, "upret": r, "runfall": runfall,
                              "t60": t60, "t20": t20, "ag": ag, "u": -(nxt-drift), "tot": -nxt,
                              "alloc": alloc, "gain": alloc*nxt, "isup": r > 0})
            d = d[nxt.notna()]
            allrows.append(d)
    A = pd.concat(allrows, ignore_index=True)
    A["case"] = (A["fc"] <= -2) & A["isup"]
    C = A[A["case"]].copy()
    def summ(g):
        return pd.Series({"n": len(g), "mean_u": g["u"].mean(), "t": g["u"].mean()/(g["u"].std()/np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "mean_tot": g["tot"].mean(), "book_gain_sum": g["gain"].sum()})
    out = {}
    out["cases_by_year"] = C.groupby("year").apply(summ)
    out["cases_by_window"] = C.groupby("w").apply(summ)
    out["cases_by_coin"] = C.groupby("coin").apply(summ)
    C["trend"] = pd.cut(C["t60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    C["agb"] = np.where(C["ag"] > 1, "agit", "calm")
    out["cases_by_trend_ag"] = C.dropna(subset=["t60"]).groupby(["trend", "agb"]).apply(summ)
    C["t20b"] = pd.qcut(C["t20"], 4)
    out["cases_by_t20q"] = C.dropna(subset=["t20"]).groupby("t20b").apply(summ)
    C["upq"] = pd.qcut(C["upret"], 4)
    out["cases_by_upday_q"] = C.groupby("upq").apply(summ)
    C["rfq"] = pd.qcut(C["runfall"], 4)
    out["cases_by_runfall_q"] = C.dropna(subset=["runfall"]).groupby("rfq").apply(summ)
    C["runb"] = C["run"].clip(upper=5)
    out["cases_by_run"] = C.groupby("runb").apply(summ)
    # non-case bars by trend (condition alone)
    N = A[~A["case"]].copy()
    N["trend"] = pd.cut(N["t60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    N["t20b"] = pd.cut(N["t20"], [-9, -0.1, 0, 0.1, 99])
    out["noncase_by_trend"] = N.dropna(subset=["t60"]).groupby("trend").apply(summ)
    out["noncase_by_t20"] = N.dropna(subset=["t20"]).groupby("t20b").apply(summ)
    out["coverage_t60_cases"] = float(C["t60"].notna().mean())
    # book daily
    dl = []
    for coin, wins in days.items():
        for w, df in wins.items():
            x = df[["day", "book_return", "coin_return"]].copy(); x["w"] = w; dl.append(x)
    D = pd.concat(dl)
    B = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    B["wn"] = B["w"].str[1:].astype(int)
    B = B.sort_values(["wn", "day"]).dropna()
    B["year"] = pd.to_datetime(B["day"]).dt.year
    v = (1+B["book_return"]).cumprod(); dd = v/v.cummax()-1
    B["dd"] = dd.values
    out["book_by_year"] = B.groupby("year").agg(mean_book=("book_return", "mean"), sd_book=("book_return", "std"),
                                                mean_coin=("coin_return", "mean"), mindd=("dd", "min"), n=("day", "count"))
    out["book_by_window"] = B.groupby("w").agg(sum_book=("book_return", "sum"), mean_coin=("coin_return", "mean"), mindd=("dd", "min"))
    out["deepest_dd"] = float(dd.min())
    # gain by coin-day trend during held days
    H = A[A["alloc"] != 0].copy()
    H["trend"] = pd.cut(H["t60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    out["held_gain_by_trend"] = H.dropna(subset=["t60"]).groupby("trend")["gain"].agg(["count", "mean", "sum"])
    H["t20b"] = pd.cut(H["t20"], [-9, -0.1, 0, 0.1, 99])
    out["held_gain_by_t20"] = H.dropna(subset=["t20"]).groupby("t20b")["gain"].agg(["count", "mean", "sum"])
    return out
