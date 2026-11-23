def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # ---- book daily returns
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w; dd["wi"] = int(w[1:])
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["wi", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wi", "day"])
    B = B.dropna()
    v = (1 + B.book_return).cumprod(); dd_ = v / v.cummax() - 1
    B["dd"] = dd_.values; B["year"] = pd.to_datetime(B.day).dt.year
    out["book_by_year"] = B.groupby("year").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"),
                                                 book_sd=("book_return", "std"), min_dd=("dd", "min"), n=("book_return", "size"))
    out["book_by_window"] = B.groupby("wi").agg(book_sum=("book_return", "sum"), coin_sum=("coin_return", "sum"), min_dd=("dd", "min"))
    out["deepest_dd"] = float(dd_.min())
    # ---- per bar features
    F = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            rng = (b.high - b.low).replace(0, np.nan)
            b["cl"] = (b.high - b.close) / rng
            b["vr"] = b.volume / b.volume.shift(1).rolling(20).mean()
            b["r1"] = b.close.shift(-1) / b.close - 1
            b["ret20"] = b.close / b.close.shift(20) - 1
            b["ret60"] = b.close / b.close.shift(60) - 1
            b["above50"] = (b.close > b.close.rolling(50).mean()).astype(float)
            b.loc[b.close.rolling(50).count() < 50, "above50"] = np.nan
            b["dayret"] = b.close / b.close.shift(1) - 1
            b["vol20"] = b.dayret.rolling(20).std()
            b["alloc"] = b.postRebalance_current_allocation
            b["gain"] = b.alloc * b.r1
            b["coin"] = c; b["wi"] = int(w[1:])
            F.append(b[["coin", "wi", "cl", "vr", "r1", "ret20", "ret60", "above50", "dayret", "vol20", "alloc", "gain", "forecast"]])
    F = pd.concat(F)
    mu = F.groupby("coin").r1.mean()
    F["ex"] = F.r1 - F.coin.map(mu)
    F = F.dropna(subset=["r1"])
    out["alloc_desc"] = F.alloc.describe()
    out["forecast_desc"] = F.forecast.describe()
    F["fq"] = pd.qcut(F.forecast.rank(method="first"), 5, labels=False)
    out["by_forecast_q"] = F.groupby("fq").agg(fc=("forecast", "mean"), alloc=("alloc", "mean"), r1=("r1", "mean"), ex=("ex", "mean"), gain=("gain", "mean"), n=("r1", "size"))
    # trend states
    G = F.dropna(subset=["ret20"]).copy()
    G["r20q"] = pd.qcut(G.ret20, 5, labels=False)
    G["sig"] = (G.forecast > G.forecast.median()).astype(int)
    out["trend_x_signal"] = G.groupby(["r20q", "sig"]).agg(r1=("r1", "mean"), ex=("ex", "mean"), gain=("gain", "mean"), alloc=("alloc", "mean"), n=("r1", "size"))
    H = F.dropna(subset=["above50"])
    H["sig"] = (H.forecast > H.forecast.median()).astype(int)
    out["ma50_x_signal"] = H.groupby(["above50", "sig"]).agg(r1=("r1", "mean"), ex=("ex", "mean"), gain=("gain", "mean"), sdgain=("gain", "std"), alloc=("alloc", "mean"), n=("r1", "size"))
    # slope within states
    res = {}
    for s, g in H.groupby("above50"):
        sl = stats.linregress(g.forecast, g.ex); res[f"above50={s}"] = [sl.slope, sl.slope / sl.stderr, len(g)]
    out["slope_by_ma50"] = pd.DataFrame(res, index=["slope", "t", "n"]).T
    # volatility state
    V = F.dropna(subset=["vol20"]).copy()
    V["vq"] = pd.qcut(V.vol20, 4, labels=False)
    V["sig"] = (V.forecast > V.forecast.median()).astype(int)
    out["vol_x_signal"] = V.groupby(["vq", "sig"]).agg(ex=("ex", "mean"), gain=("gain", "mean"), sdgain=("gain", "std"), alloc=("alloc", "mean"), n=("r1", "size"))
    # in drawdown years: share of book gain from low forecast days
    F["lowfc"] = (F.forecast < 2).astype(int)
    out["lowfc_share"] = F.groupby("lowfc").agg(share=("r1", "size"), alloc=("alloc", "mean"), gain=("gain", "mean"), ex=("ex", "mean"))
    return out
