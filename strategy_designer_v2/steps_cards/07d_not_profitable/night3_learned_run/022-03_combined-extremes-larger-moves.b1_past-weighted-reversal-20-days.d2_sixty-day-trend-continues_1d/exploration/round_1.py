def explore(data):
    import numpy as np, pandas as pd
    out = {}
    days = data["days"]; bars = data["bars"]
    # pooled per coin/window daily stats
    rows = []
    for c in days:
        for w, d in days[c].items():
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            last = b.groupby("day").last()
            dd = d.copy()
            dd["day"] = pd.to_datetime(dd["day"])
            dd = dd.set_index("day")
            dd["pos"] = last["postRebalance_current_allocation"].shift(1).reindex(dd.index)
            dd["fc"] = last["forecast"].shift(1).reindex(dd.index)
            dd["coin"] = c; dd["win"] = w
            dd["year"] = dd.index.year
            # 60-day return known at prior close
            cl = dd["close"]
            dd["r60"] = (cl / cl.shift(60) - 1).shift(1)
            dd["r20"] = (cl / cl.shift(20) - 1).shift(1)
            dd["vol20"] = dd["coin_return"].rolling(20).std().shift(1)
            rows.append(dd.reset_index())
    D = pd.concat(rows)
    D = D.dropna(subset=["book_return", "coin_return"])
    drift = D.groupby("coin")["coin_return"].mean()
    D["drift"] = D["coin"].map(drift)
    D["side"] = np.sign(D["pos"]).map({1: "long", -1: "short", 0: "flat"})
    D["market"] = D["pos"] * D["drift"]
    D["gross"] = D["pos"] * D["coin_return"]
    D["timing"] = D["gross"] - D["market"]
    D["fee"] = D["gross"] - D["book_return"]
    g = D.groupby("side").agg(n=("book_return", "size"), book=("book_return", "mean"),
                              gross=("gross", "mean"), market=("market", "mean"),
                              timing=("timing", "mean"), fee=("fee", "mean"),
                              abspos=("pos", lambda x: x.abs().mean()))
    out["by_side_coin_days"] = g
    # daily book (mean across coins per day) by window
    B = D.groupby(["win", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean"),
                                       long_share=("pos", lambda x: (x > 0).mean()),
                                       netpos=("pos", "mean")).reset_index()
    wn = B.groupby("win").agg(n=("book", "size"), book=("book", "mean"), hold=("hold", "mean"),
                              netpos=("netpos", "mean"), long_share=("long_share", "mean"))
    wn["corr"] = B.groupby("win").apply(lambda x: x["book"].corr(x["hold"]))
    wn["sum_book"] = B.groupby("win")["book"].sum()
    wn["sum_hold"] = B.groupby("win")["hold"].sum()
    out["by_window"] = wn
    # deepest falls: chain in window order
    B["wnum"] = B["win"].str[1:].astype(int)
    B = B.sort_values(["wnum", "day"])
    eq = (1 + B["book"]).cumprod().values
    peak = np.maximum.accumulate(eq); ddn = eq / peak - 1
    i = ddn.argmin(); j = eq[:i + 1].argmax()
    seg = B.iloc[j:i + 1]
    out["deepest_fall"] = pd.Series({"depth": ddn[i], "days": i - j, "start_win": seg["wnum"].iloc[0],
                                     "end_win": seg["wnum"].iloc[-1], "book_sum": seg["book"].sum(),
                                     "hold_sum": seg["hold"].sum(), "netpos": seg["netpos"].mean(),
                                     "long_share": seg["long_share"].mean()})
    # book gain by short side per window
    sw = D[D.side == "short"].groupby("win").agg(n=("gross", "size"), gross=("gross", "mean"), coin=("coin_return", "mean"))
    out["short_by_window"] = sw
    # by year side
    out["by_year_side"] = D.groupby(["year", "side"])["gross"].agg(["size", "mean"]).unstack()
    # gross by r60 quintile x side, with vol20 interaction
    D["q60"] = D.groupby("coin")["r60"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["by_r60_quint"] = D.groupby("q60").agg(n=("coin_return", "size"), next_coin=("coin_return", "mean"),
                                                gross=("gross", "mean"), pos=("pos", "mean"))
    D["vq"] = D.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["gross_by_vol_side"] = D.groupby(["vq", "side"])["gross"].agg(["size", "mean"]).unstack()
    # same sign r20 and r60 (aligned) vs not
    D["align"] = np.sign(D["r20"]) == np.sign(D["r60"])
    out["gross_by_align_side"] = D.groupby(["align", "side"])["gross"].agg(["size", "mean"]).unstack()
    out["by_coin"] = D.groupby("coin").agg(book=("book_return", "mean"), hold=("coin_return", "mean"),
                                           long_share=("pos", lambda x: (x > 0).mean()))
    out["totals"] = pd.Series({"book_daily_mean": B["book"].mean(), "hold_daily_mean": B["hold"].mean(),
                               "book_sd": B["book"].std(), "hold_sd": B["hold"].std()})
    return out
