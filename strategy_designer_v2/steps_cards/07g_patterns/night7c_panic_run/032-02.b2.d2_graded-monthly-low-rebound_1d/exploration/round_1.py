def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c, h, l, o = b["close"], b["high"], b["low"], b["open"]
            rng = (h - l) / c
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            d["r1"] = c.pct_change()
            for k in (1, 3, 5):
                d[f"f{k}"] = c.shift(-k) / c - 1
            d["ret30"] = c / c.shift(30) - 1
            d["low30"] = l.shift(1).rolling(30).min()
            d["mr30"] = rng.shift(0).rolling(30).mean()
            d["depth"] = (d["low30"] - c) / (d["mr30"] * c)
            d["rng"] = rng
            d["rngz"] = rng / rng.shift(1).rolling(30).mean()
            d["vol30"] = d["r1"].rolling(30).std()
            d["r1z"] = d["r1"] / d["vol30"].shift(1)
            d["clv"] = (c - l) / (h - l)
            d["fc"] = b["forecast"]
            d["pos"] = b["postRebalance_current_allocation"]
            d["pos_i"] = np.arange(len(b))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    mean1 = D.groupby("coin")["f1"].transform("mean")
    D["x1"] = D["f1"] - mean1

    def ct(s, days):
        s = pd.DataFrame({"v": s, "d": days}).dropna()
        if len(s) < 5: return (np.nan, np.nan, len(s), 0)
        m = s["v"].mean(); g = (s["v"] - m).groupby(s["d"]).sum(); n = len(s); Dn = len(g)
        se = np.sqrt((g**2).sum() * Dn / (Dn - 1)) / n
        return (m, m / se, n, Dn)

    def tab(mask, col="x1", by=None):
        out = {}
        sub = D[mask]
        if by is None:
            m, t, n, dn = ct(sub[col], sub["day"]); return pd.Series({"mean": m, "t": t, "n": n, "days": dn})
        for k, g in sub.groupby(by):
            m, t, n, dn = ct(g[col], g["day"]); out[k] = {"mean": m, "t": t, "n": n, "days": dn}
        return pd.DataFrame(out).T

    res = {}
    v = D.dropna(subset=["r1z", "x1"])
    D["r1z_q"] = pd.qcut(D["r1z"], 10, labels=False)
    res["next1x_by_todayret_decile_zscored"] = tab(D["r1z"].notna(), by="r1z_q")
    D["vol_q"] = D.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    res["next1x_by_vol30_quintile"] = tab(D["vol_q"].notna(), by="vol_q")
    big_down = D["r1z"] < -1.5
    res["next1x_after_bigdown_by_volq"] = tab(big_down, by="vol_q")
    D["wd"] = D["ts"].dt.weekday
    res["next1x_by_weekday"] = tab(D["x1"].notna(), by="wd")
    brk = (D["depth"] > 0) & (D["ret30"] < 0)
    for k in (1, 3, 5):
        D[f"x{k}"] = D[f"f{k}"] - D.groupby("coin")[f"f{k}"].transform("mean")
    res["break_vs_h"] = pd.DataFrame({k: tab(brk & (D["pos_i"] % k == 0), col=f"x{k}") for k in (1, 3, 5)}).T
    D["clv_q"] = pd.cut(D["clv"], [0, .2, .4, .6, .8, 1.0], include_lowest=True, labels=False)
    res["break_next1x_by_clv"] = tab(brk, by="clv_q")
    res["all_next1x_by_clv"] = tab(D["clv"].notna(), by="clv_q")
    D["rngz_q"] = pd.qcut(D["rngz"], 5, labels=False)
    res["all_next1x_by_rangeexp_q"] = tab(D["rngz"].notna(), by="rngz_q")
    res["break_by_coin"] = tab(brk, by="coin")
    res["break_by_window"] = tab(brk, by="win")
    D["fc_q"] = pd.qcut(D["fc"].where(D["fc"] > 0), 4, labels=False, duplicates="drop")
    res["forecast_quartile"] = tab(D["fc_q"].notna(), by="fc_q")
    # down-move day in decline but not break
    dec = D["ret30"] < 0
    res["decline_bigdown_nobreak"] = tab(dec & big_down & ~brk)
    res["decline_bigdown_break"] = tab(dec & big_down & brk)
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)], ignore_index=True)
    res["trades"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return res
