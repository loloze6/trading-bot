def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    drows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            nxt = c.shift(-1) / c - 1
            a = b["postRebalance_current_allocation"].fillna(0)
            pa = b["previous_allocation"].fillna(0)
            hi = b["high"].rolling(30).max(); lo = b["low"].rolling(30).min()
            nmr = (c - c.shift(30)).abs() / (hi - lo)
            r30 = c / c.shift(30) - 1
            vol = c.pct_change().rolling(30).std()
            r5 = c / c.shift(5) - 1
            df = pd.DataFrame({"coin": coin, "win": w, "year": pd.to_datetime(b["timestamp"]).dt.year,
                               "alloc": a, "turn": (a - pa).abs(), "nxt": nxt, "fc": b["forecast"],
                               "nmr": nmr, "r30": r30, "vol": vol, "r5": r5, "regime": b["regime"]})
            df["gain"] = df["alloc"] * df["nxt"]
            df["cost"] = df["turn"] * 0.0011
            rows.append(df)
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; drows.append(d)
    B = pd.concat(rows, ignore_index=True)
    act = B[B["alloc"] != 0].copy()
    act["side"] = np.sign(act["alloc"])
    act["dirret"] = act["side"] * act["nxt"]
    out["totals"] = pd.Series({"bars": len(B), "active": len(act), "gross_gain_sum": B["gain"].sum(),
                               "cost_sum": B["cost"].sum(), "mean_abs_alloc_active": act["alloc"].abs().mean(),
                               "turnover_per_bar": B["turn"].mean()})
    out["by_side"] = act.groupby("side").agg(n=("gain", "size"), gain_mean=("gain", "mean"),
                                             dirret=("dirret", "mean"), cost=("cost", "mean"))
    act["nmr_bin"] = pd.qcut(act["nmr"], 4, duplicates="drop")
    out["by_nmr"] = act.groupby("nmr_bin").agg(n=("gain", "size"), gain=("gain", "mean"), dirret=("dirret", "mean"), cost=("cost", "mean"))
    act["fc_bin"] = pd.qcut(act["fc"].abs(), 4, duplicates="drop")
    out["by_absfc"] = act.groupby("fc_bin").agg(n=("gain", "size"), gain=("gain", "mean"), dirret=("dirret", "mean"), cost=("cost", "mean"))
    act["vol_bin"] = pd.qcut(act["vol"], 4, duplicates="drop")
    out["by_vol"] = act.groupby("vol_bin").agg(n=("gain", "size"), gain=("gain", "mean"), dirret=("dirret", "mean"), cost=("cost", "mean"))
    act["r5s"] = act["side"] * act["r5"]
    act["r5_bin"] = pd.qcut(act["r5s"], 5, duplicates="drop")
    out["by_recent5d_in_dir"] = act.groupby("r5_bin").agg(n=("gain", "size"), gain=("gain", "mean"), dirret=("dirret", "mean"))
    out["by_year"] = act.groupby("year").agg(n=("gain", "size"), gain=("gain", "mean"), dirret=("dirret", "mean"), longshare=("side", lambda s: (s > 0).mean()))
    D = pd.concat(drows, ignore_index=True)
    bk = D.groupby(["win", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index()
    bk["wn"] = bk["win"].str[1:].astype(int)
    bk = bk.sort_values(["wn", "day"]).dropna(subset=["br"])
    eq = (1 + bk["br"]).cumprod(); dd = eq / eq.cummax() - 1
    bk["dd"] = dd.values
    out["book"] = pd.Series({"mean": bk["br"].mean(), "sd": bk["br"].std(), "maxdd": dd.min(), "days": len(bk)})
    out["by_window"] = bk.groupby("wn").agg(days=("br", "size"), book=("br", "mean"), coin=("cr", "mean"), mindd=("dd", "min"),
                                           bookcum=("br", lambda s: (1 + s).prod() - 1), coincum=("cr", lambda s: (1 + s).prod() - 1))
    return out
