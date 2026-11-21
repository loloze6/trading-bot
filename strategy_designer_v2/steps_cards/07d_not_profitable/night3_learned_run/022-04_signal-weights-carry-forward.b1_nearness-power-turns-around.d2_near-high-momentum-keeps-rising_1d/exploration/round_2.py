def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; grid = []
    for coin, wins in data["bars"].items():
        allr = []; r5all = []
        for w, b in wins.items():
            c = b["close"].values.astype(float)
            allr.append(pd.Series(c).pct_change().dropna().values)
            if len(c) > 5:
                idx = np.arange(0, len(c) - 5, 5)
                r5all.append(c[idx + 5] / c[idx] - 1)
        mu1 = np.concatenate(allr).mean(); r5c = np.concatenate(r5all); mu5 = r5c.mean(); sd5 = r5c.std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            nxt = c.shift(-1) / c - 1
            a = b["postRebalance_current_allocation"].astype(float)
            ret20 = c / c.shift(20) - 1
            ret60 = c / c.shift(60) - 1
            vol20 = c.pct_change().rolling(20).std()
            r5 = c.shift(-5) / c - 1 - mu5
            nh = b["debug_info.components.near_high.post_pipeline_value"] if "debug_info.components.near_high.post_pipeline_value" in b else pd.Series(np.nan, index=b.index)
            r20c = b["debug_info.components.ret20.post_pipeline_value"] if "debug_info.components.ret20.post_pipeline_value" in b else pd.Series(np.nan, index=b.index)
            df = pd.DataFrame({"coin": coin, "w": w, "a": a, "nxt": nxt, "mu1": mu1,
                               "f": b["forecast"].astype(float),
                               "fee": (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"],
                               "vol20": vol20, "ret20": ret20, "ret60": ret60,
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
            pos = np.arange(len(b)) % 5 == 0
            g = pd.DataFrame({"coin": coin, "f": b["forecast"].astype(float), "r5x": r5, "sd5": sd5,
                              "nh": pd.to_numeric(nh, errors="coerce"), "r20c": pd.to_numeric(r20c, errors="coerce"),
                              "vol20": vol20, "ret20": ret20, "ret60": ret60})[pos]
            grid.append(g)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["nxt", "a"])
    D["gain"] = D["a"] * D["nxt"]; D["mkt"] = D["a"] * D["mu1"]
    D["side"] = np.where(D["a"] > 0, "long", np.where(D["a"] < 0, "short", "flat"))
    try:
        s = D.groupby("side").agg(n=("gain", "size"), mean_gain=("gain", "mean"), mkt=("mkt", "mean"),
                                  mean_alloc=("a", "mean"), mean_nxt=("nxt", "mean"), fee=("fee", "mean"))
        s["share_of_total_gain"] = D.groupby("side")["gain"].sum() / D["gain"].sum()
        out["by_side"] = s
    except Exception as e: out["by_side"] = str(e)
    out["totals"] = pd.Series({"fee_per_bar": D["fee"].mean(), "gain_per_bar": D["gain"].mean(),
                               "mkt_per_bar": D["mkt"].mean(), "mean_abs_alloc": D["a"].abs().mean(),
                               "coin_mean_daily": D["nxt"].mean()})
    out["by_coin"] = D.groupby("coin").agg(gain=("gain", "mean"), mkt=("mkt", "mean"), fee=("fee", "mean"),
                                           long_share=("a", lambda x: (x > 0).mean()), coin=("nxt", "mean"))
    out["by_year"] = D.groupby("year").agg(gain=("gain", "mean"), mkt=("mkt", "mean"), coin=("nxt", "mean"),
                                           long_share=("a", lambda x: (x > 0).mean()), absA=("a", lambda x: x.abs().mean()))
    G = pd.concat(grid, ignore_index=True).dropna(subset=["r5x", "f"])
    try:
        G["fq"] = pd.qcut(G["f"].rank(method="first"), 5, labels=False)
        out["grid_by_forecast_quintile"] = G.groupby("fq").agg(n=("r5x", "size"), f=("f", "mean"), r5x=("r5x", "mean"),
                                                               t=("r5x", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    except Exception as e: out["grid_by_forecast_quintile"] = str(e)
    try:
        res = {}
        for col in ["nh", "r20c", "ret20", "ret60", "f"]:
            gg = G.dropna(subset=[col])
            sl = stats.linregress(gg[col].values, gg["r5x"].values)
            res[col] = (sl.slope, sl.slope / sl.stderr, len(gg))
        out["component_slopes"] = pd.DataFrame(res, index=["slope", "t", "n"]).T
    except Exception as e: out["component_slopes"] = str(e)
    try:
        G2 = G.dropna(subset=["vol20"]).copy()
        G2["vq"] = G2.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
        G2["dir"] = np.sign(G2["f"]) * G2["r5x"]
        rr = []
        for q, gq in G2.groupby("vq"):
            sl = stats.linregress(gq["f"].values, gq["r5x"].values)
            rr.append({"vq": q, "n": len(gq), "dir_move": gq["dir"].mean(),
                       "long_r5x": gq.loc[gq.f > 0, "r5x"].mean(), "short_r5x": gq.loc[gq.f < 0, "r5x"].mean(),
                       "slope_t": sl.slope / sl.stderr})
        out["grid_by_vol_tercile"] = pd.DataFrame(rr)
        D2 = D.dropna(subset=["vol20"]).copy()
        D2["vq"] = D2.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
        out["book_by_vol_side"] = D2.groupby(["vq", "side"])["gain"].agg(["size", "mean"])
    except Exception as e: out["vol"] = str(e)
    try:
        G3 = G.dropna(subset=["ret60"]).copy()
        G3["tq"] = G3.groupby("coin")["ret60"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
        rr = []
        for q, gq in G3.groupby("tq"):
            sl = stats.linregress(gq["f"].values, gq["r5x"].values)
            rr.append({"ret60_tercile": q, "n": len(gq), "mean_r5x": gq["r5x"].mean(),
                       "long_r5x": gq.loc[gq.f > 0, "r5x"].mean(), "short_r5x": gq.loc[gq.f < 0, "r5x"].mean(),
                       "short_share": (gq.f < 0).mean(), "slope_t": sl.slope / sl.stderr})
        out["grid_by_ret60_tercile"] = pd.DataFrame(rr)
    except Exception as e: out["ret60"] = str(e)
    try:
        dd = []
        for coin, wins in data["days"].items():
            for w, d in wins.items():
                dd.append(pd.DataFrame({"w": w, "day": d["day"].values, "br": d["book_return"].values, "cr": d["coin_return"].values}))
        DD = pd.concat(dd, ignore_index=True).dropna()
        P = DD.groupby(["w", "day"])[["br", "cr"]].mean().reset_index()
        P["wn"] = P["w"].str[1:].astype(int); P = P.sort_values(["wn", "day"]).reset_index(drop=True)
        eq = (1 + P["br"]).cumprod(); P["dd"] = (eq / eq.cummax() - 1).values
        heq = (1 + P["cr"]).cumprod(); P["hdd"] = (heq / heq.cummax() - 1).values
        out["deepest_fall_book_hold"] = pd.Series({"book": P["dd"].min(), "hold": P["hdd"].min(),
                                                   "book_mean": P["br"].mean(), "hold_mean": P["cr"].mean(),
                                                   "book_sharpe": P["br"].mean()/P["br"].std()*np.sqrt(365),
                                                   "hold_sharpe": P["cr"].mean()/P["cr"].std()*np.sqrt(365)})
        out["per_window"] = P.groupby("wn").agg(book=("br", "mean"), coin=("cr", "mean"), minDD=("dd", "min")).round(5)
        # per-window windows where book down and coin up / down
        pw = P.groupby("wn").agg(b=("br", "sum"), c=("cr", "sum"))
        out["window_quadrants"] = pd.crosstab(pw["b"] > 0, pw["c"] > 0)
    except Exception as e: out["days"] = str(e)
    return out
