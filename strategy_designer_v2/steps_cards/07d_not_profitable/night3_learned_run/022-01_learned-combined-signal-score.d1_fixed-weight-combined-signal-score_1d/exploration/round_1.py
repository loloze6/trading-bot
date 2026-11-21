def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # book daily returns per coin/window, then mean across coins per day
    drows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["win"] = w
            drows.append(dd)
    D = pd.concat(drows)
    wnum = lambda s: int(s[1:])
    D["wn"] = D["win"].map(wnum)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().dropna().sort_index()
    # per window summary
    pw = B.groupby(level=0).agg(book_mean=("book_return", "mean"), hold_mean=("coin_return", "mean"),
                                book_sd=("book_return", "std"), n=("book_return", "size"))
    chain = (1 + B["book_return"]).cumprod()
    dd_ = chain / chain.cummax() - 1
    pw["min_dd_in_chain"] = dd_.groupby(level=0).min()
    out["per_window"] = pw.round(5)
    out["overall"] = pd.Series({"book_mean": B.book_return.mean(), "hold_mean": B.coin_return.mean(),
                                "deepest_fall": dd_.min(), "years": len(B) / 365,
                                "chain_end": chain.iloc[-1]})
    # per coin
    pc = D.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std"])
    out["per_coin"] = pc.round(5)
    # bar-level: position gain, market vs timing, long vs short, forecast bins
    rows = []
    for c in bars:
        cm = []
        for w, b in bars[c].items():
            r = b["close"].shift(-1) / b["close"] - 1
            cm.append(r)
        mu = pd.concat(cm).mean()
        for w, b in bars[c].items():
            r = b["close"].shift(-1) / b["close"] - 1
            r5 = b["close"].shift(-5) / b["close"] - 1
            x = b["postRebalance_current_allocation"]
            f = b["forecast"]
            comp = {k: b.get(f"debug_info.components.{k}.post_pipeline_value") for k in ["mom28", "rev1", "high90", "vol30"]}
            df = pd.DataFrame({"coin": c, "wn": wnum(w), "r": r, "r5": r5, "x": x, "f": f, "mu": mu,
                               "vol": r.rolling(30).std(), "ret28": b["close"] / b["close"].shift(28) - 1,
                               "pos": np.arange(len(b))})
            for k, v in comp.items():
                df[k] = v.values if v is not None else np.nan
            df["cost"] = (b["postRebalance_current_allocation"] - b["previous_allocation"]).abs()
            df["pv"] = b["total_portfolio_value"]; df["pvp"] = b["postRebalance_total_value"]
            rows.append(df)
    X = pd.concat(rows, ignore_index=True)
    X["gain"] = X.x * X.r
    X["mkt"] = X.x * X.mu
    X["timing"] = X.gain - X.mkt
    X["fee"] = (X.pv - X.pvp) / X.pv
    out["gain_split_per_bar"] = pd.Series({"gain": X.gain.mean(), "market": X.mkt.mean(), "timing": X.timing.mean(),
                                           "fee": X.fee.mean(), "mean_abs_alloc": X.x.abs().mean(),
                                           "share_long": (X.x > 0).mean(), "share_short": (X.x < 0).mean(),
                                           "mean_alloc": X.x.mean()})
    X["side"] = np.sign(X.x)
    out["by_side"] = X.groupby("side").agg(n=("gain", "size"), gain=("gain", "mean"), r=("r", "mean"),
                                           absx=("x", lambda s: s.abs().mean())).round(5)
    # forecast bins vs 5d returns on grid
    G = X[(X.pos % 5 == 0)].dropna(subset=["r5", "f"]).copy()
    G["mu5"] = G.groupby("coin").r5.transform("mean")
    G["ex5"] = G.r5 - G.mu5
    G["fbin"] = pd.cut(G.f, [-21, -10, -5, -2, 0.001, 2, 5, 10, 21])
    out["forecast_bins_5d"] = G.groupby("fbin", observed=True).agg(n=("ex5", "size"), ex5=("ex5", "mean"),
                                                                   r5=("r5", "mean")).round(4)
    # each component alone: t of comp*ex5
    ct = {}
    for k in ["mom28", "rev1", "high90", "vol30"]:
        s = (G[k] * G.ex5).dropna()
        ct[k] = pd.Series({"mean": s.mean(), "t": s.mean() / s.std() * np.sqrt(len(s)), "n": len(s),
                           "corr": G[[k, "ex5"]].dropna().corr().iloc[0, 1]})
    out["components_alone"] = pd.DataFrame(ct).T.round(4)
    out["component_corr"] = G[["mom28", "rev1", "high90", "vol30"]].corr().round(2)
    # regime: by 28d return tercile and vol tercile, position gain
    X["vol_t"] = X.groupby("coin").vol.transform(lambda s: pd.qcut(s, 3, labels=["lo", "mid", "hi"]))
    X["mom_t"] = X.groupby("coin").ret28.transform(lambda s: pd.qcut(s, 3, labels=["dn", "mid", "up"]))
    out["gain_by_state"] = X.groupby(["mom_t", "vol_t"], observed=True).agg(
        n=("gain", "size"), gain_bps=("gain", lambda s: s.mean() * 1e4), x=("x", "mean"),
        r_bps=("r", lambda s: s.mean() * 1e4)).round(2)
    # worst days of the book: what held
    worst = B.book_return.nsmallest(40)
    out["worst40_days_mean"] = pd.Series({"book": worst.mean(), "coin": B.loc[worst.index, "coin_return"].mean()})
    return out
