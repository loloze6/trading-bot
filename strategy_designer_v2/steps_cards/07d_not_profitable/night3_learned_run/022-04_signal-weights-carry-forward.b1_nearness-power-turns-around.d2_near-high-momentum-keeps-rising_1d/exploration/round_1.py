def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; grid = []
    for coin, wins in data["bars"].items():
        # coin drift over all windows (daily) and 5-bar
        allr = []; r5all = []
        for w, b in wins.items():
            c = b["close"].values
            allr.append(pd.Series(c).pct_change().dropna().values)
            idx = np.arange(0, len(c) - 5, 5)
            r5all.append(c[idx + 5] / c[idx] - 1)
        mu1 = np.concatenate(allr).mean(); mu5 = np.concatenate(r5all).mean()
        sd5 = np.concatenate(r5all).std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            nxt = c.shift(-1) / c - 1
            a = b["postRebalance_current_allocation"]
            ret20 = c / c.shift(20) - 1
            vol20 = c.pct_change().rolling(20).std()
            nh = b.get("debug_info.components.near_high.post_pipeline_value")
            r20c = b.get("debug_info.components.ret20.post_pipeline_value")
            df = pd.DataFrame({"coin": coin, "w": w, "a": a, "nxt": nxt, "mu1": mu1,
                               "f": b["forecast"], "fee": b["postRebalance_total_value"] - b["total_portfolio_value"],
                               "pv": b["total_portfolio_value"], "vol20": vol20, "ret20": ret20,
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
            idx = np.arange(0, len(c) - 5, 5)
            g = pd.DataFrame({"coin": coin, "f": b["forecast"].values[idx],
                              "r5x": (c.values[idx + 5] / c.values[idx] - 1) - mu5,
                              "sd5": sd5,
                              "nh": nh.values[idx] if nh is not None else np.nan,
                              "r20c": r20c.values[idx] if r20c is not None else np.nan,
                              "vol20": vol20.values[idx], "ret20": ret20.values[idx]})
            grid.append(g)
    D = pd.concat(rows).dropna(subset=["nxt", "a"])
    D["gain"] = D["a"] * D["nxt"]; D["mkt"] = D["a"] * D["mu1"]
    D["side"] = np.where(D["a"] > 0, "long", np.where(D["a"] < 0, "short", "flat"))
    s = D.groupby("side").agg(n=("gain", "size"), mean_gain=("gain", "mean"), mkt=("mkt", "mean"),
                              mean_alloc=("a", "mean"), mean_nxt=("nxt", "mean"))
    s["share_of_total_gain"] = D.groupby("side")["gain"].sum() / D["gain"].sum()
    out["by_side"] = s
    out["fee_share"] = pd.Series({"fees_over_pv_mean_per_bar": (-(D["fee"]) / D["pv"]).mean(),
                                  "gain_mean_per_bar": D["gain"].mean(), "mkt_mean": D["mkt"].mean()})
    out["by_coin"] = D.groupby("coin").agg(gain=("gain", "mean"), mkt=("mkt", "mean"), long_share=("a", lambda x: (x > 0).mean()))
    out["by_year"] = D.groupby("year").agg(gain=("gain", "mean"), mkt=("mkt", "mean"), coin=("nxt", "mean"), long_share=("a", lambda x: (x > 0).mean()))
    G = pd.concat(grid).dropna(subset=["r5x", "f"])
    G["fq"] = pd.qcut(G["f"], 5, labels=False, duplicates="drop")
    out["grid_by_forecast_quintile"] = G.groupby("fq").agg(n=("r5x", "size"), f=("f", "mean"), r5x=("r5x", "mean"),
                                                           t=("r5x", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    # components separately
    res = {}
    for col in ["nh", "r20c", "ret20"]:
        gg = G.dropna(subset=[col])
        sl = stats.linregress(gg[col], gg["r5x"])
        res[col] = (sl.slope, sl.slope / sl.stderr, len(gg))
    out["component_slopes(slope,t,n)"] = pd.DataFrame(res, index=["slope", "t", "n"]).T
    # vol state
    G2 = G.dropna(subset=["vol20"]).copy()
    G2["vq"] = G2.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=False))
    G2["dir"] = np.sign(G2["f"]) * G2["r5x"]
    out["grid_by_vol_tercile"] = G2.groupby("vq").agg(n=("dir", "size"), dir_move=("dir", "mean"),
                                                      t=("dir", lambda x: x.mean() / x.std() * np.sqrt(len(x))),
                                                      slope_t=("r5x", lambda x: stats.linregress(G2.loc[x.index, "f"], x).slope / stats.linregress(G2.loc[x.index, "f"], x).stderr))
    D2 = D.dropna(subset=["vol20"]).copy()
    D2["vq"] = D2.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["book_gain_by_vol_tercile_side"] = D2.groupby(["vq", "side"])["gain"].agg(["size", "mean"])
    # book daily chain and deepest falls
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(pd.DataFrame({"w": w, "day": d["day"], "br": d["book_return"], "cr": d["coin_return"]}))
    DD = pd.concat(dd).dropna()
    P = DD.groupby(["w", "day"])[["br", "cr"]].mean().reset_index()
    P["wn"] = P["w"].str[1:].astype(int); P = P.sort_values(["wn", "day"])
    eq = (1 + P["br"]).cumprod(); dd_ = eq / eq.cummax() - 1
    P["dd"] = dd_.values
    out["deepest_fall"] = float(dd_.min())
    out["per_window"] = P.groupby("wn").agg(book=("br", "mean"), coin=("cr", "mean"), minDD=("dd", "min")).round(5)
    return out
