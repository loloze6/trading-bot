def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            pos = b["postRebalance_current_allocation"].fillna(0)
            nxt = c.shift(-1) / c - 1
            gain = pos * nxt
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            ret30 = c / c.shift(30) - 1
            ret90 = c / c.shift(90) - 1
            ma100 = c / c.rolling(100, min_periods=60).mean() - 1
            vol20 = c.pct_change().rolling(20).std()
            age = -b["debug_info.components.below_age.last_history_value"]
            fwd14 = c.shift(-14) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "pos": pos, "nxt": nxt, "gain": gain, "fee": fee,
                               "ret30": ret30, "ret90": ret90, "ma100": ma100, "vol20": vol20,
                               "age": age, "fc": b["forecast"], "fwd14": fwd14,
                               "year": pd.to_datetime(b["timestamp"]).dt.year, "i": np.arange(len(b))})
            rows.append(df)
    d = pd.concat(rows)
    out["coins_windows"] = d.groupby("coin")["w"].nunique()
    coinmean = d.groupby("coin")["nxt"].mean()
    d["cm"] = d["coin"].map(coinmean)
    d["mkt"] = d["pos"] * d["cm"]
    d["timing"] = d["gain"] - d["mkt"]
    on = d[d["pos"] > 0]
    out["share_long"] = float((d["pos"] > 0).mean())
    out["decomp_per_bar"] = pd.Series({"gain": d["gain"].mean(), "mkt": d["mkt"].mean(),
                                       "timing": d["timing"].mean(), "fee": d["fee"].mean()})
    out["long_bars_by_coin"] = on.groupby("coin").agg(n=("gain", "size"), gain=("gain", "mean"),
                                                     nxt=("nxt", "mean"), cm=("cm", "mean"))
    out["long_by_year"] = on.groupby("year").agg(n=("gain", "size"), gain=("gain", "mean"), nxt=("nxt", "mean"))
    # long bars by prior trend
    on = on.copy()
    on["tr90"] = pd.qcut(on["ret90"], 3, labels=["low", "mid", "high"])
    on["ma"] = np.where(on["ma100"] > 0, "above_ma100", "below_ma100")
    on["agebin"] = pd.cut(on["age"], [0, 5, 10, 20, 40, 61])
    on["vb"] = pd.qcut(on["vol20"], 3, labels=["lowvol", "mid", "highvol"])
    for k in ["tr90", "ma", "agebin", "vb"]:
        g = on.groupby(k).agg(n=("nxt", "size"), nxt=("nxt", "mean"), gain=("gain", "mean"),
                              t=("nxt", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
        out["long_by_" + k] = g
    # 14-day grid fwd by ma side, all bars with age>0
    g = d[(d["i"] % 14 == 0) & (d["age"] > 0)].copy()
    g["ex"] = g["fwd14"] - g["coin"].map(d[d["i"] % 14 == 0].groupby("coin")["fwd14"].mean())
    g["ma"] = np.where(g["ma100"] > 0, "above", "below")
    res = {}
    for k, s in g.groupby("ma"):
        s = s.dropna(subset=["ex", "age"])
        sl = stats.linregress(s["age"], s["ex"])
        res[k] = {"n": len(s), "mean_ex": s["ex"].mean(), "slope": sl.slope, "t": sl.slope / sl.stderr}
    out["grid_age_by_ma100"] = pd.DataFrame(res)
    return out
