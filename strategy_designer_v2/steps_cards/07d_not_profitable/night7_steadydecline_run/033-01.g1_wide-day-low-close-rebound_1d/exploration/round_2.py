def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["r2"] = b["close"].shift(-2) / b["close"] - 1
            dr = b["close"].pct_change()
            b["dayret"] = dr
            b["sd30"] = dr.rolling(30).std()
            b["tr30"] = b["close"] / b["close"].shift(30) - 1
            rng = b["high"] - b["low"]
            b["widemult"] = rng / rng.rolling(20).mean()
            b["cl"] = (b["high"] + b["low"] - 2 * b["close"]) / rng.replace(0, np.nan)
            b["daykey"] = pd.to_datetime(b["timestamp"]).dt.floor("D").astype("int64")
            b["coin"] = c; b["w"] = w
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["r1"].mean()
    d["x1"] = d["r1"] - d["coin"].map(mu)
    d["sg"] = np.sign(d["forecast"])
    d["sx"] = d["sg"] * d["x1"]
    d["sr"] = d["sg"] * d["r1"]
    d["sx2"] = d["sg"] * (d["r2"] - 2 * d["coin"].map(mu))
    med = d.groupby("coin")["sd30"].transform("median")
    d["agit"] = np.where(d["sd30"].isna(), "na", np.where(d["sd30"] > med, "agitated", "calm"))
    out = {}

    def ct(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 5: return (np.nan, np.nan, len(s), 0)
        m = s[col].mean()
        dev = (s[col] - m).groupby(s["daykey"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / len(s)
        return (m, m / se, len(s), G)

    af = d["forecast"].abs()
    res = []
    for q in [0.6, 0.8, 0.9, 0.95]:
        th = af.quantile(q)
        for side in [1, -1, 0]:
            sub = d[(af >= th) & ((d["sg"] == side) if side != 0 else True)]
            m, t, n, G = ct(sub, "sr")
            m2, t2, _, _ = ct(sub, "sx2")
            res.append({"q": q, "th": th, "side": side, "total_1d": m, "t": t, "n": n, "days": G,
                        "net_1d": m - 0.0019, "sx_2d": m2, "share_coin_days": n / len(d)})
    out["threshold_books"] = pd.DataFrame(res)

    strong = af >= af.quantile(0.8)
    d["strong"] = strong
    res = []
    for a in ["agitated", "calm"]:
        for side in [1, -1]:
            m, t, n, G = ct(d[strong & (d["agit"] == a) & (d["sg"] == side)], "sx")
            # condition alone: same side bets on non-strong bars in that state
            m0, t0, n0, _ = ct(d[~strong & (d["agit"] == a) & (d["sg"] == side)], "sx")
            mx, tx, nx, _ = ct(d[d["agit"] == a], "x1")
            res.append({"agit": a, "side": side, "strong_sx": m, "t": t, "n": n,
                        "weak_sx": m0, "t_weak": t0, "n_weak": n0, "state_x1_all": mx, "t_state": tx})
    out["agitation_check"] = pd.DataFrame(res)

    d["tr"] = np.where(d["tr30"].isna(), "na", np.where(d["tr30"] > 0.05, "up30", np.where(d["tr30"] < -0.05, "down30", "flat30")))
    res = []
    for tr in ["up30", "flat30", "down30"]:
        for side in [1, -1]:
            m, t, n, G = ct(d[strong & (d["tr"] == tr) & (d["sg"] == side)], "sx")
            mx, tx, nx, _ = ct(d[(d["tr"] == tr)], "x1")
            res.append({"tr": tr, "side": side, "strong_sx": m, "t": t, "n": n, "state_x1_all": mx, "t_state": tx})
    out["trend30_check"] = pd.DataFrame(res)

    # wide day check: long side, wide quartile, close near low; and wide alone
    d["wq"] = pd.qcut(d["widemult"], 4, labels=False)
    res = []
    for wq in range(4):
        for loc, lo, hi in [("low_half", 0, 1.01), ("high_half", -1.01, 0)]:
            sub = d[(d["wq"] == wq) & (d["cl"] > lo) & (d["cl"] <= hi)]
            m, t, n, G = ct(sub, "x1")
            sub2 = sub.copy(); sub2["dn"] = sub2["dayret"] < 0
            m_dn, t_dn, n_dn, _ = ct(sub2[sub2["dn"]], "x1")
            m_up, t_up, n_up, _ = ct(sub2[~sub2["dn"]], "x1")
            res.append({"wq": wq, "loc": loc, "x1": m, "t": t, "n": n,
                        "x1_downday": m_dn, "t_dn": t_dn, "n_dn": n_dn, "x1_upday": m_up, "t_up": t_up, "n_up": n_up})
    out["wide_loc_dayret"] = pd.DataFrame(res)

    # book falls: chained daily book by window order
    dd_ = pd.concat([x.assign(coin=c, w=w) for c, ws in data["days"].items() for w, x in ws.items()])
    dd_["wn"] = dd_["w"].str[1:].astype(int)
    bk = dd_.groupby(["wn", "day"])["book_return"].mean().dropna().reset_index()
    v = (1 + bk["book_return"]).cumprod()
    dd = v / v.cummax() - 1
    out["book_deepest_fall"] = float(dd.min())
    i_end = int(dd.idxmin()); i_start = int(v[:i_end + 1].idxmax())
    out["fall_len_days"] = i_end - i_start
    out["fall_window"] = "w" + str(int(bk.loc[i_end, "wn"]))
    out["book_sd_daily"] = float(bk["book_return"].std())
    return out
