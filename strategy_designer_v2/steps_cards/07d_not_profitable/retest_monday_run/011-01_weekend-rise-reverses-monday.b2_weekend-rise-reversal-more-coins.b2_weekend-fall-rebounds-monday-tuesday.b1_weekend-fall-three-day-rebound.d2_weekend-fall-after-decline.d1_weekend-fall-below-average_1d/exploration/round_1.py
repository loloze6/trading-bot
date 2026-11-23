def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # ---- book daily series
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(b=("book_return", "mean"), h=("coin_return", "mean")).dropna().reset_index().sort_values(["wn", "day"])
    B["v"] = (1 + B["b"]).cumprod(); B["peak"] = B["v"].cummax(); B["dd"] = B["v"] / B["peak"] - 1
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["book_by_window"] = B.groupby("wn").agg(n=("b", "size"), book_mean=("b", "mean"), hold_mean=("h", "mean"), book_sum=("b", "sum"), hold_sum=("h", "sum"), min_dd=("dd", "min"))
    out["book_by_year"] = B.groupby("year").agg(n=("b", "size"), book_sum=("b", "sum"), hold_sum=("h", "sum"), book_sd=("b", "std"))
    out["max_dd"] = float(B["dd"].min())
    # ---- cases: Sunday bars with forecast>0
    cs = []
    allgrid = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values
            n = len(b)
            r3 = np.full(n, np.nan); r3[:n-3] = cl[3:] / cl[:-3] - 1
            r1 = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
            s = pd.Series(cl)
            sma50 = s.rolling(50, min_periods=50).mean()
            sma200 = s.rolling(200, min_periods=100).mean()
            prior7 = s / s.shift(7) - 1
            prior30 = s / s.shift(30) - 1
            vol30 = pd.Series(r1).rolling(30).std()
            volr = b["volume"] / b["volume"].rolling(30).mean()
            f = pd.DataFrame({"coin": c, "w": w, "wd": ts.dt.weekday, "year": ts.dt.year, "r3": r3, "r1": r1,
                              "dist50": cl / sma50 - 1, "dist200": cl / sma200 - 1, "p7": prior7, "p30": prior30,
                              "vol30": vol30, "volr": volr, "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"]})
            f["pos"] = np.arange(n)
            allgrid.append(f)
    A = pd.concat(allgrid, ignore_index=True)
    # drift per coin: non-overlapping 3-bar grid
    g = A[A["pos"] % 3 == 0]
    drift = g.groupby("coin")["r3"].mean()
    A["ex3"] = A["r3"] - A["coin"].map(drift)
    C = A[(A["wd"] == 6) & (A["fc"] > 0)].dropna(subset=["r3"]).copy()
    out["n_cases"] = len(C)
    def summ(x):
        return pd.Series({"n": len(x), "r3": x["r3"].mean(), "ex3": x["ex3"].mean(), "t_ex": stats.ttest_1samp(x["ex3"], 0).statistic if len(x) > 2 else np.nan, "win": (x["r3"] > 0).mean()})
    C["fcq"] = pd.qcut(C["fc"], 4, labels=False)
    out["by_forecast_q"] = C.groupby("fcq").apply(summ)
    C["d200"] = np.where(C["dist200"].isna(), "na", np.where(C["dist200"] < 0, "below200", "above200"))
    out["by_sma200"] = C.groupby("d200").apply(summ)
    C["p30q"] = pd.qcut(C["p30"], 4, labels=False)
    out["by_prior30_q"] = C.groupby("p30q").apply(summ)
    C["volq"] = pd.qcut(C["vol30"], 4, labels=False)
    out["by_vol30_q"] = C.groupby("volq").apply(summ)
    C["vrq"] = pd.qcut(C["volr"], 4, labels=False)
    out["by_sunday_volratio_q"] = C.groupby("vrq").apply(summ)
    out["by_year"] = C.groupby("year").apply(summ)
    # condition-alone: weekday bars (not Sunday) with r1<0 and dist50<0, vs Sunday cases
    O = A[(A["wd"] != 6) & (A["r1"] < 0) & (A["dist50"] < 0)].dropna(subset=["r3"])
    O = O[O["pos"] % 3 == 0]
    out["other_day_fall_below50"] = summ(O)
    S_above = A[(A["wd"] == 6) & (A["r1"] < 0) & (A["dist50"] >= 0)].dropna(subset=["r3"])
    out["sunday_fall_above50"] = summ(S_above)
    # drawdown period: which window, and holdings
    i = B["dd"].idxmin(); trough = B.loc[i]
    peak_i = B.loc[:i, "v"].idxmax()
    out["dd_peak_trough_windows"] = f"peak w{int(B.loc[peak_i,'wn'])} trough w{int(trough['wn'])} days {int(B.index.get_loc(i)-B.index.get_loc(peak_i))}"
    return out
