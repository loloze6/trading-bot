def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["ret1"]
            b["fee"] = (b["postRebalance_total_value"] - b["total_portfolio_value"]) / b["total_portfolio_value"]
            b["r28"] = b["close"] / b["close"].shift(28) - 1
            b["lr"] = np.log(b["close"]).diff()
            b["vol30"] = b["lr"].rolling(30).std()
            b["vol30_rel"] = b["vol30"] / b["lr"].expanding(30).std()
            b["dd90"] = b["close"] / b["close"].rolling(90, min_periods=20).max() - 1
            b["coin"] = coin; b["w"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby("coin")["ret1"].mean()
    B["mkt"] = B["pos"] * B["coin"].map(mu)
    B["side"] = np.sign(B["pos"]).map({1: "long", -1: "short", 0: "flat"})
    out["by_side"] = B.groupby("side").agg(n=("gain", "size"), mean_gain=("gain", "mean"),
                                         sum_gain=("gain", "sum"), mean_pos=("pos", "mean"),
                                         fee_sum=("fee", "sum"))
    out["by_coin"] = B.groupby("coin").agg(mean_gain=("gain", "mean"), mkt=("mkt", "mean"),
                                         fee=("fee", "mean"), mean_abs_pos=("pos", lambda x: x.abs().mean()),
                                         long_share=("pos", lambda x: (x > 0).mean()))
    out["by_year_side"] = B.groupby(["year", "side"])["gain"].sum().unstack()
    # forecast bins vs next 1d gain
    B["fq"] = pd.qcut(B["forecast"], 10, labels=False, duplicates="drop")
    out["by_forecast_decile"] = B.groupby("fq").agg(fc=("forecast", "mean"), pos=("pos", "mean"),
                                                  ret1=("ret1", "mean"), gain=("gain", "mean"))
    B["vq"] = B.groupby("coin")["vol30_rel"].transform(lambda x: pd.qcut(x, 4, labels=False, duplicates="drop"))
    out["by_volq_side"] = B.groupby(["vq", "side"]).agg(n=("gain", "size"), gain=("gain", "mean"),
                                                     ret1=("ret1", "mean")).unstack()
    # book daily
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    D["wn"] = D["w"].str[1:].astype(int)
    bk = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index()
    bk = bk.sort_values(["wn", "day"])
    eq = (1 + bk["book_return"]).cumprod()
    dd = eq / eq.cummax() - 1
    bk["dd"] = dd.values
    out["book_stats"] = pd.Series({"mean": bk["book_return"].mean(), "hold_mean": bk["coin_return"].mean(),
                                   "maxdd": dd.min(), "ndays": len(bk),
                                   "years": len(bk) / 365, "chain": eq.iloc[-1]})
    out["by_window"] = bk.groupby("wn").agg(book=("book_return", "sum"), hold=("coin_return", "sum"),
                                          worst_dd=("dd", "min"))
    # deepest fall: find trough, peak
    ti = dd.idxmin(); pi = eq.loc[:ti].idxmax()
    seg = bk.loc[pi:ti]
    out["deepest_fall"] = pd.Series({"days": len(seg), "windows": str(sorted(seg["wn"].unique())),
                                     "book_sum": seg["book_return"].sum(), "hold_sum": seg["coin_return"].sum()})
    return out
