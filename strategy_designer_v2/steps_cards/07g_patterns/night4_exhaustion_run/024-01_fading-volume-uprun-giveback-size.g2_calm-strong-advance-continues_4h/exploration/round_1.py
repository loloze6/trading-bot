def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            past = c / c.shift(H) - 1
            mabs = past.abs().rolling(180, min_periods=90).mean()
            scaled = past / mabs
            vol = r1.rolling(180, min_periods=90).std()
            vfade = np.log(v.rolling(9).sum() / v.shift(9).rolling(9).sum())
            sgn = np.sign(r1)
            run = sgn.groupby((sgn != sgn.shift()).cumsum()).cumcount() + 1
            run = run * sgn
            past6 = c / c.shift(6) - 1
            fwd = c.shift(-H) / c - 1
            fwd6 = c.shift(-6) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, len(b), H)
            d = pd.DataFrame({"coin": coin, "w": w, "fc": b["forecast"].values[idx] if "forecast" in b else np.nan,
                              "scaled": scaled.values[idx], "vol": vol.values[idx], "vfade": vfade.values[idx],
                              "run": run.values[idx], "past6": past6.values[idx], "past": past.values[idx],
                              "fwd": fwd.values[idx], "fwd6": fwd6.values[idx],
                              "hour": ts.dt.hour.values[idx], "wd": ts.dt.weekday.values[idx],
                              "year": ts.dt.year.values[idx]})
            rows.append(d)
    g = pd.concat(rows).dropna(subset=["fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    def tab(key, q=5):
        x = g.dropna(subset=[key]).copy()
        x["b"] = x.groupby("coin")[key].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = x.groupby("b")["ex"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t[["mean", "count", "t"]].round(4)
    out = {}
    out["fc_bins"] = tab("fc", 3) if g["fc"].notna().any() else "na"
    out["scaled_q"] = tab("scaled")
    out["vfade_q"] = tab("vfade")
    out["past6_q"] = tab("past6")
    out["vol_q"] = tab("vol")
    # run length (signed) buckets
    g["runb"] = np.clip(g["run"], -5, 5)
    t = g.groupby("runb")["ex"].agg(["mean", "count", "std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["run_signed"] = t.round(4)
    # interaction: big up run with fading vs rising volume
    x = g.dropna(subset=["scaled", "vfade"]).copy()
    x["sq"] = x.groupby("coin")["scaled"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    x["vf"] = np.where(x["vfade"] < x.groupby("coin")["vfade"].transform("median"), "fade", "rise")
    out["scaled_x_vol"] = x.groupby(["sq", "vf"])["ex"].agg(["mean", "count"]).round(4)
    # by year and coin
    out["by_year"] = g.groupby("year")["ex"].agg(["mean", "count"]).round(4)
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dd.append(d)
    D = pd.concat(dd).dropna(subset=["book_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["book_by_coin"] = D.groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean")).round(5)
    out["book_by_wd"] = D.groupby("wd").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count")).round(5)
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    tr["dur_d"] = tr["duration_minutes"] / 1440
    tr["fb"] = pd.qcut(tr["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades_by_entry_fc"] = tr.groupby("fb").agg(n=("net_profit_loss_percent", "count"), net=("net_profit_loss_percent", "mean"),
                                                       fc=("entry_forecast", "mean"), dur=("dur_d", "mean")).round(3)
    return out
