def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c, ws in data["days"].items():
        b = data["bars"][c]
        for w, df in ws.items():
            d = df.copy(); d["coin"] = c; d["win"] = w
            bb = b[w][["timestamp", "postRebalance_current_allocation", "forecast",
                       "debug_info.components.sma_cross.last_history_value"]].copy()
            bb.columns = ["timestamp", "pos", "fc", "spread"]
            bb["day"] = pd.to_datetime(bb["timestamp"]).dt.floor("D")
            bb = bb.groupby("day").last()
            d["day"] = pd.to_datetime(d["day"])
            if d["day"].dt.tz is None and bb.index.tz is not None:
                bb.index = bb.index.tz_localize(None)
            d = d.merge(bb[["pos", "fc", "spread"]], left_on="day", right_index=True, how="left")
            d["pos_prev"] = d["pos"].shift(1)
            d["fc_prev"] = d["fc"].shift(1)
            d["spread_prev"] = d["spread"].shift(1)
            # days since forecast turned positive
            on = (d["fc"] > 0).astype(int)
            grp = (on != on.shift()).cumsum()
            d["age"] = on.groupby(grp).cumcount().where(on == 1)
            d["age_prev"] = d["age"].shift(1)
            d["fwd20"] = d["close"].shift(-20) / d["close"] - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["book_return", "coin_return"])
    ann = np.sqrt(365)
    out["sharpe"] = pd.Series({
        "book": D["book_return"].mean() / D["book_return"].std() * ann,
        "coin": D["coin_return"].mean() / D["coin_return"].std() * ann,
        "book_sd": D["book_return"].std(), "coin_sd": D["coin_return"].std(),
        "mean_pos_when_in": D.loc[D["pos_prev"] > 0.01, "pos_prev"].mean()})
    I = D[D["pos_prev"] > 0.01].copy()
    I["per_unit"] = I["book_return"] / I["pos_prev"]
    I["posb"] = pd.cut(I["pos_prev"], [0, 0.5, 1.0, 1.5, 2.3])
    out["by_pos_size"] = I.groupby("posb", observed=True).agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"), book_sd=("book_return", "std"))
    I["ageb"] = pd.cut(I["age_prev"], [-1, 10, 30, 60, 120, 2000])
    out["by_signal_age"] = I.groupby("ageb", observed=True).agg(n=("book_return", "size"), coin=("coin_return", "mean"), coin_sd=("coin_return", "std"), fc=("fc_prev", "mean"))
    I["spb"] = pd.qcut(I["spread_prev"], 4)
    out["by_raw_spread"] = I.groupby("spb", observed=True).agg(n=("book_return", "size"), coin=("coin_return", "mean"), pos=("pos_prev", "mean"))
    # forward 20d coin return vs forecast bucket (non-overlapping-ish via every 20th)
    S = D.iloc[::20].dropna(subset=["fwd20", "fc"])
    S["fcb"] = pd.cut(S["fc"], [-0.01, 0.001, 5, 10, 15, 20.1])
    out["fwd20_by_fc"] = S.groupby("fcb", observed=True)["fwd20"].agg(["size", "mean", "median"])
    # contribution of worst days
    I["sign"] = np.where(I["book_return"] > 0, "up", "down")
    out["tail"] = pd.Series({
        "share_days_book_lt_-5%": (I["book_return"] < -0.05).mean(),
        "sum_book_lt_-5%": I.loc[I["book_return"] < -0.05, "book_return"].sum(),
        "sum_book_all_in": I["book_return"].sum(),
        "sum_book_gt_5%": I.loc[I["book_return"] > 0.05, "book_return"].sum()})
    # exit gap: coin return in 10 days after trade exits vs entries
    return out
