def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for coin in data["days"]:
        for w, d in data["days"][coin].items():
            b = data["bars"][coin][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            alloc = b.groupby("day")["postRebalance_current_allocation"].last()
            dd = d.copy()
            dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.set_index("day")
            dd["alloc_prev"] = alloc.reindex(dd.index).shift(1)
            c = dd["close"]
            for n in (60, 90):
                dd[f"ret{n}"] = c.shift(1) / c.shift(n + 1) - 1
            dd["above100"] = c.shift(1) / c.shift(1).rolling(100, min_periods=60).mean() - 1
            dd["coin"] = coin; dd["wn"] = int(w[1:])
            rows.append(dd.reset_index())
    D = pd.concat(rows).dropna(subset=["book_return", "alloc_prev"])
    D["side"] = np.sign(D["alloc_prev"]).map({1: "long", -1: "short", 0: "flat"})
    mu = D.groupby("coin")["coin_return"].mean()
    out["coin_mean_daily"] = mu
    D["gross"] = D["alloc_prev"] * D["coin_return"]
    D["market"] = D["alloc_prev"] * D["coin"].map(mu)
    g = D.groupby("side")
    out["side_gain"] = pd.DataFrame({"n": g.size(), "book": g["book_return"].mean(), "gross": g["gross"].mean(), "market": g["market"].mean(), "timing": g["gross"].mean() - g["market"].mean(), "t_book": g["book_return"].apply(lambda s: s.mean() / s.std() * np.sqrt(len(s)) if s.std() > 0 else np.nan)})
    for col in ("ret60", "ret90", "above100"):
        X = D.dropna(subset=[col]).copy()
        X["trend"] = np.where(X[col] > 0, "up", "down")
        out[f"by_{col}_side"] = X.groupby(["trend", "side"])["book_return"].agg(["size", "mean", "std"])
    # variants: actual, long-only, shorts flat when ret90>0
    def metrics(col):
        B = D.groupby(["wn", "day"])[col].mean().sort_index()
        eq = (1 + B).cumprod(); mdd = (eq / eq.cummax() - 1).min()
        ar = eq.iloc[-1] ** (365 / len(B)) - 1
        return {"sharpe": B.mean() / B.std() * np.sqrt(365), "ann": ar, "mdd": mdd, "calmar": ar / -mdd}
    D["v_actual"] = D["book_return"]
    D["v_longonly"] = np.where(D["side"] == "short", 0.0, D["book_return"])
    r90 = D["ret90"].fillna(0)
    D["v_noshort_up90"] = np.where((D["side"] == "short") & (r90 > 0), 0.0, D["book_return"])
    D["v_nolong_down90"] = np.where((D["side"] == "long") & (r90 < 0), 0.0, D["book_return"])
    D["v_trendonly90"] = np.where(((D["side"] == "short") & (r90 > 0)) | ((D["side"] == "long") & (r90 < 0)), 0.0, D["book_return"])
    out["variants"] = pd.DataFrame({k: metrics(k) for k in ["v_actual", "v_longonly", "v_noshort_up90", "v_nolong_down90", "v_trendonly90"]}).T
    S = D[D["side"] == "short"]
    out["short_by_year"] = S.groupby(pd.to_datetime(S["day"]).dt.year)["book_return"].agg(["size", "mean", "sum"])
    return out
