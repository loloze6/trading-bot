def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # ---- book daily (mean over coins), holding daily
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    P = D.groupby(["window", "day"])[["book_return", "coin_return"]].mean().reset_index()
    P["wn"] = P["window"].str[1:].astype(int)
    P = P.sort_values(["wn", "day"]).dropna()
    def sh(x): return x.mean() / x.std() * np.sqrt(365)
    out["book_vs_hold"] = pd.DataFrame({"mean": [P.book_return.mean(), P.coin_return.mean()],
                                        "sharpe": [sh(P.book_return), sh(P.coin_return)]}, index=["book", "hold"])
    eq = (1 + P.book_return).cumprod().values
    dd = eq / np.maximum.accumulate(eq) - 1
    i = dd.argmin(); j = eq[:i + 1].argmax()
    out["deepest_fall"] = f"{dd[i]:.3f} from {P.window.iloc[j]} to {P.window.iloc[i]}, {i-j} days"
    pw = P.groupby("wn").agg(book=("book_return", "sum"), hold=("coin_return", "sum"))
    out["per_window_sum"] = pw.round(3)
    # ---- bar level
    B = []
    for c in bars:
        for w, b in bars[c].items():
            x = b[["close", "high", "low", "forecast", "postRebalance_current_allocation"]].copy().reset_index(drop=True)
            r = x.close.pct_change()
            x["nxt"] = r.shift(-1)
            x["gain"] = x.postRebalance_current_allocation * x.nxt
            lr = np.log(x.close).diff()
            x["vol20"] = lr.rolling(20).std(); x["vol180"] = lr.rolling(180).std()
            x["ret180"] = x.close / x.close.shift(180) - 1   # 30-day
            x["ret42"] = x.close / x.close.shift(42) - 1
            x["fwd72"] = x.close.shift(-72) / x.close - 1
            x["pos_in_grid"] = np.arange(len(x)) % 72 == 0
            x["coin"] = c; x["window"] = w
            B.append(x)
    B = pd.concat(B, ignore_index=True)
    mdr = B.groupby("coin").nxt.mean()
    B["mkt"] = B.postRebalance_current_allocation * B.coin.map(mdr)
    B["side"] = np.sign(B.postRebalance_current_allocation)
    g = B.dropna(subset=["gain"]).groupby("side").agg(n=("gain", "size"), gain_sum=("gain", "sum"),
                                                     mkt_sum=("mkt", "sum"), mean_alloc=("postRebalance_current_allocation", "mean"))
    out["by_side"] = g
    B["trend30"] = np.sign(B.ret180)
    B["agree"] = np.where(B.side == B.trend30, "with30d", "against30d")
    out["side_x_trend30"] = B.dropna(subset=["gain", "ret180"]).groupby(["side", "agree"]).gain.agg(["size", "sum", "mean"])
    out["by_coin"] = B.dropna(subset=["gain"]).groupby("coin").agg(gain=("gain", "sum"), mkt=("mkt", "sum"))
    # ---- grid: forward returns by situation
    G = B[B.pos_in_grid].dropna(subset=["fwd72", "forecast"]).copy()
    drift = G.groupby("coin").fwd72.mean()
    G["ex"] = G.fwd72 - G.coin.map(drift)
    G["dirmove"] = np.sign(G.forecast) * G.fwd72
    G["direx"] = np.sign(G.forecast) * G.ex
    G["fs"] = np.sign(G.forecast)
    out["grid_by_sign"] = G.groupby("fs").agg(n=("ex", "size"), total=("dirmove", "mean"), unusual=("direx", "mean"))
    G["fq"] = pd.qcut(G.forecast.abs(), 4, labels=False)
    out["grid_by_absfc_q"] = G.groupby(["fs", "fq"]).dirmove.agg(["size", "mean"])
    G["vr"] = G.vol20 / G.vol180
    G["vq"] = pd.qcut(G.vr, 3, labels=["quiet", "mid", "loud"])
    def tt(s): return pd.Series({"n": len(s), "mean": s.mean(), "t": stats.ttest_1samp(s, 0).statistic})
    out["grid_by_volratio"] = G.dropna(subset=["vr"]).groupby("vq").dirmove.apply(tt).unstack()
    G["ag"] = np.where(np.sign(G.forecast) == np.sign(G.ret180), "with30d", "against30d")
    out["grid_by_trend30"] = G.dropna(subset=["ret180"]).groupby(["fs", "ag"]).dirmove.apply(tt).unstack()
    # ---- falls: worst 30 book days vs coin
    P2 = P.copy()
    worst = P2.nsmallest(30, "book_return")
    out["worst30_days"] = pd.Series({"book_mean": worst.book_return.mean(), "coin_mean": worst.coin_return.mean(),
                                     "share_coin_up": (worst.coin_return > 0).mean()})
    out["mean_abs_alloc"] = B.postRebalance_current_allocation.abs().mean()
    return out
