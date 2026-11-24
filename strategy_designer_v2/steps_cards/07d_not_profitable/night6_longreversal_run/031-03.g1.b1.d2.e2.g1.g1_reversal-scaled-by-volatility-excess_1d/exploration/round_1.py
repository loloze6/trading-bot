def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    coin = list(data["bars"].keys())[0]
    W = list(data["bars"][coin].keys())
    rows = []
    for w in W:
        b = data["bars"][coin][w].copy().reset_index(drop=True)
        b["w"] = w
        b["ret1"] = b["close"].shift(-1)/b["close"] - 1
        r = b["close"].pct_change()
        b["vol30"] = r.rolling(30, min_periods=20).std()
        b["volratio"] = b["vol30"]/b["vol30"].rolling(180, min_periods=45).mean()
        b["mom60"] = b["close"]/b["close"].shift(60) - 1
        b["mom20"] = b["close"]/b["close"].shift(20) - 1
        b["bret"] = b["postRebalance_total_value"].shift(-1)/b["postRebalance_total_value"] - 1
        b["alloc"] = b["postRebalance_current_allocation"]
        b["gross"] = b["alloc"]*b["ret1"]
        b["turn"] = (b["postRebalance_current_allocation"]-b["previous_allocation"]).abs()
        b["pos"] = np.arange(len(b))
        rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    mu = B["ret1"].mean()
    out = {}
    out["basic"] = pd.Series({"bars": len(B), "mean_coin_ret": mu, "mean_bret": B["bret"].mean(),
        "mean_gross": B["gross"].mean(), "fee_drag": B["gross"].mean()-B["bret"].mean(),
        "mean_turn": B["turn"].mean(), "mean_absalloc": B["alloc"].abs().mean(),
        "share_long": (B["alloc"]>0).mean()})
    # chain
    v = (1+B["bret"].fillna(0)).cumprod()
    dd = v/v.cummax()-1
    B["dd"] = dd.values
    peak_idx = None
    # deepest fall episode
    trough = dd.idxmin()
    peak = v.loc[:trough].idxmax()
    ep = B.loc[peak:trough]
    out["deepest"] = pd.Series({"depth": dd.min(), "bars": len(ep), "windows": ep["w"].nunique(),
        "coin_change_sum": ep["ret1"].sum(), "mean_alloc": ep["alloc"].mean(),
        "share_long": (ep["alloc"]>0).mean(), "mean_volratio": ep["volratio"].mean(),
        "gross_long": ep.loc[ep.alloc>0,"gross"].sum(), "gross_short": ep.loc[ep.alloc<0,"gross"].sum(),
        "fees": (ep["gross"]-ep["bret"]).sum(), "mean_mom60": ep["mom60"].mean()})
    # by window
    g = B.groupby("w")
    out["by_window"] = pd.DataFrame({"bret_sum": g["bret"].sum(), "coin_sum": g["ret1"].sum(),
        "gross_long": B[B.alloc>0].groupby("w")["gross"].sum(),
        "gross_short": B[B.alloc<0].groupby("w")["gross"].sum(), "volratio": g["volratio"].mean(),
        "mindd": g["dd"].min()}).round(4)
    def tab(key, q=5):
        c = pd.qcut(B[key], q, duplicates="drop")
        gg = B.groupby(c, observed=True)
        return pd.DataFrame({"n": gg.size(), "gross_mean": gg["gross"].mean(), "bret_mean": gg["bret"].mean(),
            "t_gross": gg["gross"].apply(lambda x: x.mean()/(x.std()/np.sqrt(x.count()))),
            "std_bret": gg["bret"].std(), "turn": gg["turn"].mean()})
    out["by_volratio"] = tab("volratio")
    out["by_mom60"] = tab("mom60")
    out["by_forecast"] = tab("forecast")
    out["by_side"] = B.groupby(np.sign(B["alloc"]))[["gross","bret","ret1"]].agg(["mean","count"])
    # signed mom60 vs side: long against downtrend etc.
    B["side_vs_trend"] = np.sign(B["alloc"])*np.sign(B["mom60"])
    out["side_vs_trend"] = B.groupby("side_vs_trend")[["gross","bret"]].agg(["mean","count","std"])
    # strength by |forecast| x volratio
    B["absf"] = B["forecast"].abs()
    B["fq"] = pd.qcut(B["absf"], 3, labels=["lo","mid","hi"])
    B["vq"] = pd.qcut(B["volratio"], 3, labels=["lo","mid","hi"])
    out["gross_absf_x_vol"] = B.pivot_table(index="fq", columns="vq", values="gross", aggfunc="mean", observed=True)
    out["bret_absf_x_vol"] = B.pivot_table(index="fq", columns="vq", values="bret", aggfunc="mean", observed=True)
    # worst 5% days of book: features
    q = B["bret"].quantile(0.05)
    worst = B[B["bret"]<=q]
    out["worst_days"] = pd.Series({"n": len(worst), "mean_absalloc": worst.alloc.abs().mean(),
        "all_absalloc": B.alloc.abs().mean(), "volratio": worst.volratio.mean(), "all_volratio": B.volratio.mean(),
        "share_long": (worst.alloc>0).mean(), "mean_absret1": worst.ret1.abs().mean(),
        "absf": worst.absf.mean(), "all_absf": B.absf.mean()})
    out["by_year"] = B.groupby(B["timestamp"].astype(str).str[:4])[["bret","gross","ret1"]].sum().round(3)
    return out
