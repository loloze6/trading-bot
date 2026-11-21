def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []; days_all = []
    for c, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            pos = b["postRebalance_current_allocation"].fillna(0)
            r1 = b["close"].shift(-1) / b["close"] - 1
            lr = np.log(b["close"]).diff()
            vol30 = lr.rolling(30).std()
            vz = (vol30 - vol30.rolling(120, min_periods=60).mean()) / vol30.rolling(120, min_periods=60).std()
            ret28 = b["close"] / b["close"].shift(28) - 1
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]).fillna(0) / b["total_portfolio_value"]
            df = pd.DataFrame({"coin": c, "win": w, "pos": pos, "g": pos * r1, "r1": r1, "vz": vz,
                               "ret28": ret28, "fee": fee, "fc": b["forecast"], "year": pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
        for w, d in data["days"][c].items():
            dd = d[["day", "book_return", "coin_return"]].copy(); dd["coin"] = c; dd["win"] = w
            days_all.append(dd)
    B = pd.concat(rows).dropna(subset=["r1"])
    D = pd.concat(days_all)
    cm = D.groupby("coin")["coin_return"].mean()
    B["mkt"] = B["pos"] * B["coin"].map(cm)
    B["tim"] = B["g"] - B["mkt"]
    out["per_coin"] = B.groupby("coin").agg(mean_gain=("g", "mean"), mkt=("mkt", "mean"), timing=("tim", "mean"),
                                            fee=("fee", "mean"), long_share=("pos", lambda x: (x > 0).mean()),
                                            mean_abs_pos=("pos", lambda x: x.abs().mean()))
    B["side"] = np.sign(B["pos"])
    out["by_side"] = B.groupby("side").agg(n=("g", "size"), gain=("g", "mean"), timing=("tim", "mean"), r1=("r1", "mean"))
    B["vzq"] = pd.qcut(B["vz"], 5, labels=False)
    out["by_volz_side"] = B.groupby(["vzq", "side"])["g"].agg(["size", "mean"]).unstack()
    B["tq"] = pd.qcut(B["ret28"], 5, labels=False)
    out["by_ret28_side"] = B.groupby(["tq", "side"])["g"].agg(["size", "mean"]).unstack()
    B["fq"] = pd.qcut(B["fc"].abs().rank(method="first"), 5, labels=False)
    out["by_fcabs"] = B.groupby("fq").agg(gain=("g", "mean"), timing=("tim", "mean"), fee=("fee", "mean"), absfc=("fc", lambda x: x.abs().mean()))
    out["by_year"] = B.groupby("year").agg(gain=("g", "mean"), timing=("tim", "mean"), fee=("fee", "mean"), long=("pos", lambda x: (x > 0).mean()))
    # book daily
    bk = D.dropna(subset=["book_return"]).groupby(["win", "day"]).agg(b=("book_return", "mean"), h=("coin_return", "mean")).reset_index()
    bk["wn"] = bk["win"].str[1:].astype(int); bk = bk.sort_values(["wn", "day"])
    eq = (1 + bk["b"]).cumprod(); dd = eq / eq.cummax() - 1
    bk["dd"] = dd.values
    out["book_overall"] = pd.Series({"mean": bk["b"].mean(), "sd": bk["b"].std(), "maxdd": dd.min(), "days": len(bk),
                                     "hold_mean": bk["h"].mean()})
    out["by_window"] = bk.groupby("wn").agg(book=("b", "sum"), hold=("h", "sum"), worst_dd=("dd", "min"), n=("b", "size"))
    # deepest fall: trough and its peak
    t = dd.values.argmin(); pk = eq.values[:t + 1].argmax()
    seg = bk.iloc[pk:t + 1]
    out["deepest_fall"] = pd.Series({"days": len(seg), "book_sum": seg["b"].sum(), "hold_sum": seg["h"].sum(),
                                     "windows": ",".join(seg["win"].unique())})
    return out
