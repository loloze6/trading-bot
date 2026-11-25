def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            cl = b["close"].astype(float)
            r = cl.pct_change()
            fwd = cl.shift(-1)/cl - 1
            pos = b["postRebalance_current_allocation"].astype(float)
            vol20 = r.rolling(20).std()
            df = pd.DataFrame({
                "coin": c, "w": w, "pos": pos, "fwd": fwd, "r": r,
                "fc": b["forecast"].astype(float),
                "agit": (b["regime"] == "unknown"),
                "t20": cl/cl.shift(20)-1, "t60": cl/cl.shift(60)-1,
                "r3": cl.shift(1)/cl.shift(4)-1,
                "z": r/vol20, "vol20": vol20,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A.groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    A["gain"] = A["pos"]*A["fwd"]
    S = A[A["fc"] > 0].dropna(subset=["fwd"])
    out = {}
    def summ(g):
        return pd.Series({"n": len(g), "mean_fwd": g["fwd"].mean(), "mean_ex": g["ex"].mean(),
                          "t_ex": g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "mean_gain": g["gain"].mean(), "mean_pos": g["pos"].mean()})
    S = S.copy()
    S["fcq"] = pd.qcut(S["fc"], 5, labels=False, duplicates="drop")
    out["by_forecast_q"] = S.groupby("fcq").apply(summ)
    S["t20b"] = pd.cut(S["t20"], [-9, -0.2, -0.05, 0.05, 0.2, 9])
    out["by_trend20"] = S.groupby("t20b").apply(summ)
    S["t60b"] = pd.cut(S["t60"], [-9, -0.1, 0.1, 9])
    out["by_trend60"] = S.groupby("t60b").apply(summ)
    S["r3b"] = pd.cut(S["r3"], [-9, -0.1, -0.03, 0.03, 9])
    out["by_prior3d"] = S.groupby("r3b").apply(summ)
    S["volq"] = pd.qcut(S["vol20"], 4, labels=False)
    out["by_vol20_q"] = S.groupby("volq").apply(summ)
    out["by_coin"] = S.groupby("coin").apply(summ)
    out["by_year"] = S.groupby("yr").apply(summ)
    out["by_window"] = S.groupby("w").apply(summ)
    # condition-alone comparisons: agitated, down day, but forecast 0 (shouldn't happen) / all agitated bars by t20
    Ag = A[A["agit"]].dropna(subset=["fwd"]).copy()
    Ag["sig"] = Ag["fc"] > 0
    Ag["t20b"] = pd.cut(Ag["t20"], [-9, -0.2, -0.05, 0.05, 0.2, 9])
    out["agit_t20_sig_vs_nosig"] = Ag.groupby(["t20b", "sig"]).apply(lambda g: pd.Series({"n": len(g), "mean_ex": g["ex"].mean()}))
    # book daily
    D = []
    for c in days:
        for w, d in days[c].items():
            d = d[["day", "book_return"]].copy(); d["w"] = w; d["coin"] = c
            D.append(d)
    D = pd.concat(D)
    bd = D.groupby(["w", "day"])["book_return"].mean().reset_index()
    bd["wn"] = bd["w"].str[1:].astype(int)
    bd = bd.sort_values(["wn", "day"]).dropna()
    v = (1+bd["book_return"]).cumprod().values
    peak = np.maximum.accumulate(v); dd = v/peak - 1
    bd["dd"] = dd
    i = int(np.argmin(dd)); pk = int(np.argmax(v[:i+1]))
    out["deepest_dd"] = pd.Series({"dd": dd[i], "days_peak_to_trough": i-pk,
                                   "peak_window": bd.iloc[pk]["w"], "trough_window": bd.iloc[i]["w"]})
    out["dd_by_window_min"] = bd.groupby("w")["dd"].min()
    out["window_book_ret"] = bd.groupby("w")["book_return"].agg(lambda x: (1+x).prod()-1)
    # what was held in the deepest fall
    seg = bd.iloc[pk:i+1][["w", "day"]]
    key = set(zip(seg["w"], seg["day"]))
    Dd = D[[ (a, b) in key for a, b in zip(D["w"], D["day"]) ]]
    out["dd_by_coin_sumret"] = Dd.groupby("coin")["book_return"].sum()
    return out
