def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # ---- book daily returns (mean across coins per window/day) ----
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
    B = B.dropna(subset=["book_return"])
    v = (1 + B["book_return"]).cumprod()
    dd_ = v / v.cummax() - 1
    B["dd"] = dd_.values
    B["v"] = v.values
    out["max_dd"] = float(dd_.min())
    # per window: book sum, coin sum, worst dd inside chain
    B["wd"] = pd.to_datetime(B["day"]).dt.dayofweek
    out["book_by_window"] = B.groupby("wn").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"),
                                                 min_dd=("dd", "min"), n=("book_return", "size")).round(5)
    out["book_by_weekday"] = B.groupby("wd")["book_return"].agg(["mean", "std", "count"])
    # ---- Friday cases ----
    cs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            b["ts"] = pd.to_datetime(b["timestamp"])
            r = b["close"].pct_change()
            b["ret_next"] = b["close"].shift(-1) / b["close"] - 1
            b["vol20"] = r.rolling(20).std()
            b["r14"] = b["close"] / b["close"].shift(14) - 1
            b["r60"] = b["close"] / b["close"].shift(60) - 1
            b["r3"] = b["close"] / b["close"].shift(3) - 1
            b["r1"] = r
            b["low365"] = b["close"].rolling(365, min_periods=200).min()
            b["dist_low"] = b["close"] / b["low365"] - 1
            b["ma50"] = b["close"] / b["close"].rolling(50).mean() - 1
            b["fc"] = b["debug_info.components.run14.post_pipeline_value"]
            b["alloc"] = b["postRebalance_current_allocation"]
            b["coin"] = c; b["wn"] = int(w[1:])
            b["dow"] = b["ts"].dt.dayofweek
            b["sat_day"] = (b["ts"] + pd.Timedelta(days=1)).dt.date
            cs.append(b[["coin", "wn", "dow", "ts", "sat_day", "ret_next", "vol20", "r14", "r60", "r3", "r1", "dist_low", "ma50", "fc", "alloc", "forecast"]])
    A = pd.concat(cs)
    F = A[(A["dow"] == 4) & A["fc"].notna() & A["ret_next"].notna()].copy()
    F["pnl"] = F["alloc"] * F["ret_next"]
    F["side"] = np.sign(F["fc"])
    F["sret"] = F["side"] * F["ret_next"]
    out["n_fri"] = len(F)
    def summ(g):
        return pd.Series({"n": len(g), "sret_mean": g["sret"].mean(), "t": g["sret"].mean() / (g["sret"].std() / np.sqrt(len(g))),
                          "pnl_mean": g["pnl"].mean(), "pnl_min_q05": g["pnl"].quantile(0.05)})
    out["by_side"] = F.groupby("side").apply(summ).round(5)
    F["fq"] = pd.qcut(F["fc"], 6, labels=False)
    out["by_fc_sextile"] = F.groupby("fq").apply(summ).round(5)
    F["vq"] = F.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["by_vol_tercile"] = F.groupby(["vq", "side"]).apply(summ).round(5)
    F["tq"] = np.sign(F["r60"])
    out["by_r60sign_side"] = F.groupby(["tq", "side"]).apply(summ).round(5)
    F["agree"] = np.sign(F["r60"]) == F["side"]
    out["by_agree60"] = F.groupby("agree").apply(summ).round(5)
    F["year"] = F["ts"].dt.year
    out["by_year_side"] = F.groupby(["year", "side"])["pnl"].agg(["mean", "count"]).round(5).unstack()
    # worst drawdown period: find days in the deepest dd stretch
    trough = int(np.argmin(dd_.values))
    peak = int(np.argmax(v.values[:trough + 1]))
    seg = B.iloc[peak:trough + 1]
    out["deepest_dd_windows"] = seg.groupby("wn")["book_return"].agg(["sum", "count"]).round(4)
    segset = set(zip(seg["wn"], seg["day"].astype(str)))
    F["satstr"] = F["sat_day"].astype(str)
    F["in_dd"] = [(w, s) in segset for w, s in zip(F["wn"], F["satstr"])]
    out["cases_in_dd"] = F.groupby(["in_dd", "side"]).apply(summ).round(5)
    out["dd_case_context"] = F.groupby("in_dd")[["vol20", "r60", "fc", "dist_low", "ma50"]].mean().round(4)
    # worst 15 Saturdays for book: context
    S = F.groupby("satstr").agg(pnl=("pnl", "mean"), fc=("fc", "mean"), longsh=("side", "mean"), vol=("vol20", "mean"), r60=("r60", "mean"))
    w = S.nsmallest(25, "pnl")
    out["worst25_sat_ctx"] = w[["pnl", "fc", "longsh", "vol", "r60"]].describe().round(4)
    out["all_sat_ctx"] = S[["pnl", "fc", "longsh", "vol", "r60"]].describe().round(4)
    return out
