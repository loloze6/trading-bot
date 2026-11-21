def explore(data):
    import pandas as pd, numpy as np
    out = {}
    # ---- book daily returns: mean over coins per (window, day)
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    P = D.groupby(["wn", "day"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("coin", "count")).dropna().reset_index()
    P = P.sort_values(["wn", "day"]).reset_index(drop=True)
    eq = (1 + P["book"]).cumprod()
    dd = eq / eq.cummax() - 1
    P["dd"] = dd
    trough = dd.idxmin()
    peak = eq[:trough + 1].idxmax()
    out["deepest_fall"] = pd.Series({"depth": dd.min(), "days": trough - peak,
                                     "peak_window": P.loc[peak, "wn"], "trough_window": P.loc[trough, "wn"],
                                     "book_ret_in_fall": eq[trough] / eq[peak] - 1,
                                     "hold_ret_in_fall": (1 + P.loc[peak + 1:trough, "coin"]).prod() - 1})
    # per-window summary
    g = P.groupby("wn")
    out["by_window"] = pd.DataFrame({"book_mean_bps": g["book"].mean() * 1e4, "hold_mean_bps": g["coin"].mean() * 1e4,
                                     "book_chain": g["book"].apply(lambda x: (1 + x).prod() - 1),
                                     "hold_chain": g["coin"].apply(lambda x: (1 + x).prod() - 1),
                                     "min_dd": g["dd"].min(), "ncoins": g["n"].mean()})
    # top falls episodes (separate drawdowns)
    eps = []
    inn = False
    for i in range(len(P)):
        if dd[i] < 0 and not inn:
            inn = True; s = i - 1 if i > 0 else 0; m = i
        if inn:
            if dd[i] < dd[m]: m = i
            if dd[i] == 0:
                eps.append((dd[m], s, m)); inn = False
    if inn: eps.append((dd[m], s, m))
    eps = sorted(eps)[:6]
    out["top_falls"] = pd.DataFrame([{"depth": e[0], "days": e[2] - e[1], "w_start": P.loc[e[1], "wn"], "w_end": P.loc[e[2], "wn"],
                                      "hold_ret": (1 + P.loc[e[1] + 1:e[2], "coin"]).prod() - 1} for e in eps])
    # ---- bar-level decomposition
    B = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            x = pd.DataFrame({"close": b["close"].values, "pos": b["postRebalance_current_allocation"].values,
                              "fc": b["forecast"].values})
            x["ret"] = x["close"].shift(-1) / x["close"] - 1
            x["fee"] = (b["total_portfolio_value"].values - b["postRebalance_total_value"].values) / b["total_portfolio_value"].values
            r1 = x["close"].pct_change()
            x["vol30"] = r1.rolling(180).std()
            x["vol_rel"] = x["vol30"] / r1.rolling(180, min_periods=60).std().rolling(540, min_periods=180).mean()
            x["ret30"] = x["close"] / x["close"].shift(180) - 1
            x["ret7"] = x["close"] / x["close"].shift(42) - 1
            x["ret1d"] = x["close"] / x["close"].shift(6) - 1
            x["coin"] = c; x["w"] = w
            B.append(x)
    B = pd.concat(B).dropna(subset=["ret", "pos"])
    B["gross"] = B["pos"] * B["ret"]
    B["net"] = B["gross"] - B["fee"].fillna(0)
    B["side"] = np.where(B["pos"] > 0, "long", np.where(B["pos"] < 0, "short", "flat"))
    def summ(gb):
        return pd.DataFrame({"bars": gb.size(), "gross_bps": gb["gross"].mean() * 1e4, "fee_bps": gb["fee"].mean() * 1e4,
                             "net_bps": gb["net"].mean() * 1e4, "mean_abs_pos": gb["pos"].apply(lambda s: s.abs().mean()),
                             "net_sd_bps": gb["net"].std() * 1e4})
    out["by_side"] = summ(B.groupby("side"))
    B["volq"] = pd.qcut(B["vol_rel"], 5, labels=False)
    out["by_vol_rel_q"] = summ(B.groupby("volq"))
    B["t30"] = np.sign(B["ret30"])
    out["by_side_and_30d_trend"] = summ(B.groupby(["side", "t30"]))
    # alignment of 1-day move against position (late-stage reversal?)
    B["fc_q"] = pd.qcut(B["fc"], 5, labels=False, duplicates="drop")
    out["by_forecast_q"] = summ(B.groupby("fc_q"))
    # stretched: ret1d in direction of position, scaled
    B["d1_aligned"] = np.sign(B["pos"]) * B["ret1d"] / (B["vol30"] * np.sqrt(6))
    B["d1q"] = pd.qcut(B["d1_aligned"], 5, labels=False, duplicates="drop")
    out["by_1d_move_with_position_q"] = summ(B[B["side"] != "flat"].groupby("d1q"))
    return out
