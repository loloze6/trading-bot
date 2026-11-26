def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r = c.pct_change()
            sd20 = r.rolling(20, min_periods=20).std()
            b["z"] = r / sd20.shift(1)
            b["nxt"] = c.shift(-1) / c - 1
            b["nxt3"] = c.shift(-3) / c - 1
            b["ret5"] = c / c.shift(5) - 1
            b["ret20"] = c / c.shift(20) - 1
            b["ret60"] = c / c.shift(60) - 1
            b["ma50"] = c / c.rolling(50, min_periods=30).mean() - 1
            b["rng"] = (b["high"] - b["low"]) / c.shift(1) / sd20.shift(1)
            b["cl"] = (b["high"] - c) / (b["high"] - b["low"])
            b["sd20"] = sd20
            b["prevz"] = b["z"].shift(1)
            b["gapdown"] = b["open"] / c.shift(1) - 1
            b["coin"] = coin; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["pos"] = np.arange(len(b))
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    drift = B.groupby("coin")["nxt"].mean()
    B["ex"] = B["nxt"] - B["coin"].map(drift)
    cases = B[B["regime"] == "mean_reversion"].dropna(subset=["nxt"]).copy()
    cases["gain"] = cases["postRebalance_current_allocation"] * cases["nxt"]
    out["n_cases"] = len(cases)
    def summ(g):
        return pd.Series({"n": len(g), "mean_nxt": g["nxt"].mean(), "mean_ex": g["ex"].mean(),
                          "t_ex": stats.ttest_1samp(g["ex"], 0).statistic if len(g) > 2 else np.nan,
                          "hit": (g["nxt"] > 0).mean(), "mean_gain": g["gain"].mean(),
                          "mean_alloc": g["postRebalance_current_allocation"].mean(),
                          "nxt3": g["nxt3"].mean()})
    out["by_year"] = cases.groupby("year").apply(summ)
    out["by_coin"] = cases.groupby("coin").apply(summ)
    cases["ret20_q"] = pd.qcut(cases["ret20"], 4, labels=False)
    out["by_ret20_q"] = cases.groupby("ret20_q").apply(summ)
    cases["ret60_q"] = pd.qcut(cases["ret60"], 4, labels=False)
    out["by_ret60_q"] = cases.groupby("ret60_q").apply(summ)
    cases["ma50_pos"] = cases["ma50"] > 0
    out["by_above_ma50"] = cases.groupby("ma50_pos").apply(summ)
    cases["z_q"] = pd.qcut(cases["z"], 4, labels=False)
    out["by_z_q"] = cases.groupby("z_q").apply(summ)
    cases["cl_q"] = pd.qcut(cases["cl"], 4, labels=False, duplicates="drop")
    out["by_cl_q"] = cases.groupby("cl_q").apply(summ)
    cases["ret5_q"] = pd.qcut(cases["ret5"], 4, labels=False)
    out["by_ret5_q"] = cases.groupby("ret5_q").apply(summ)
    cases["prevdown"] = cases["prevz"] < -1
    out["by_prev_sharp_down"] = cases.groupby("prevdown").apply(summ)
    # condition alone on all bars: above ma50 among non-case bars vs others
    nc = B[B["regime"] != "mean_reversion"].dropna(subset=["nxt", "ma50"])
    out["noncase_ex_by_above_ma50"] = nc.groupby(nc["ma50"] > 0)["ex"].agg(["count", "mean"])
    # book daily
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dl.append(d)
    D = pd.concat(dl, ignore_index=True)
    D["wn"] = D["win"].str[1:].astype(int)
    book = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index().sort_values(["wn", "day"])
    v = (1 + book["book_return"]).cumprod()
    dd = v / v.cummax() - 1
    book["dd"] = dd.values
    out["max_dd"] = dd.min()
    # worst book days and the window of deepest dd
    i = dd.idxmin()
    peak = v.loc[:i].idxmax()
    out["deepest_fall_window_span"] = f"from {book.loc[peak,'wn']} to {book.loc[i,'wn']}, days {i-peak}"
    out["book_by_window"] = book.groupby("wn").agg(n=("book_return", "size"), book=("book_return", "sum"), hold=("coin_return", "sum"))
    # worst cases contribution
    cs = cases.sort_values("gain")
    out["worst10_gain_sum"] = cs["gain"].head(10).sum()
    out["all_gain_sum"] = cs["gain"].sum()
    out["worst10_profile"] = cs.head(10)[["coin", "year", "z", "cl", "ret20", "ret60", "nxt", "postRebalance_current_allocation"]].describe().round(3)
    return out
