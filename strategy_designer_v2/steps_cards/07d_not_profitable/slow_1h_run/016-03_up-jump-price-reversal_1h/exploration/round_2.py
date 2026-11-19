def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    recs = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            c = b["close"].reset_index(drop=True)
            r1 = c.pct_change()
            past = c / c.shift(72) - 1
            top3 = r1.clip(lower=0).rolling(72).apply(lambda x: np.sort(x)[-3:].sum(), raw=True)
            share = (top3 / past).where(past > 0).clip(upper=1)
            vol72 = r1.rolling(72).std()
            past7d = c / c.shift(168) - 1
            fwd = c.shift(-72) / c - 1
            idx = np.arange(0, len(c), 72)
            df = pd.DataFrame({"coin": coin, "w": w, "past": past.iloc[idx].values,
                               "share": share.iloc[idx].values, "fwd": fwd.iloc[idx].values,
                               "vol": vol72.iloc[idx].values, "past7d": past7d.iloc[idx].values,
                               "fc": b["forecast"].iloc[idx].values})
            recs.append(df)
    G = pd.concat(recs)
    mu = G.groupby("coin")["fwd"].mean()
    G["ex"] = G["fwd"] - G["coin"].map(mu)
    T = G[(G["past"] > 0)].dropna(subset=["share", "fwd"]).copy()
    T["sq"] = pd.qcut(T["share"], 5, labels=False)
    out["fwd_by_share_quintile"] = T.groupby("sq").agg(share=("share", "mean"), fwd=("fwd", "mean"),
                                                       ex=("ex", "mean"), n=("fwd", "size"),
                                                       fc=("fc", "mean"))
    T["pq"] = pd.qcut(T["past"], 3, labels=False)
    out["fwd_by_rise_tercile_x_share_hi_lo"] = T.assign(hi=T["share"] > T["share"].median()).groupby(["pq", "hi"])["fwd"].agg(["mean", "count"])
    T["vq"] = T.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["fwd_by_vol_tercile_x_share_hi_lo"] = T.assign(hi=T["share"] > T["share"].median()).groupby(["vq", "hi"])["fwd"].agg(["mean", "count"])
    T["l7"] = np.sign(T["past7d"])
    out["fwd_by_7d_sign_x_share_hi_lo"] = T.assign(hi=T["share"] > T["share"].median()).groupby(["l7", "hi"])["fwd"].agg(["mean", "count"])
    N = G[(G["past"] <= 0)].dropna(subset=["fwd"])
    out["fwd_after_fall_mean_n"] = pd.Series({"mean": N["fwd"].mean(), "n": len(N)})
    out["fwd_after_rise_mean_t_n"] = pd.Series({"mean": T["fwd"].mean(), "t": stats.ttest_1samp(T["fwd"], 0).statistic, "n": len(T)})
    # daily book: fees vs gross
    dd = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["gross"] = b["postRebalance_current_allocation"] * (b["close"].shift(-1) / b["close"] - 1)
            dd.append(b.groupby("day")[["fee", "gross"]].sum().mean())
    out["daily_fee_vs_gross"] = pd.concat(dd, axis=1).mean(axis=1)
    out["share_desc"] = T["share"].describe()
    return out
