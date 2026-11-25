def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c, h, l = b["close"], b["high"], b["low"]
            rng = (h - l) / c
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            d["r1"] = c.pct_change()
            d["f1"] = c.shift(-1) / c - 1
            d["f3"] = c.shift(-3) / c - 1
            d["vol30"] = d["r1"].rolling(30).std()
            d["r1z"] = d["r1"] / d["vol30"].shift(1)
            d["clv"] = (c - l) / (h - l)
            d["mr30"] = rng.rolling(30).mean()
            d["mr365r"] = d["mr30"] / rng.rolling(365, min_periods=91).mean()
            d["ret30"] = c / c.shift(30) - 1
            d["dep_raw"] = b.get("debug_info.components.depth.post_pipeline_value")
            d["rw_raw"] = b.get("debug_info.components.range_width.post_pipeline_value")
            d["fc"] = b["forecast"]
            d["pos_i"] = np.arange(len(b))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D"); D["year"] = D["ts"].dt.year
    D["x1"] = D["f1"] - D.groupby("coin")["f1"].transform("mean")
    D["x3"] = D["f3"] - D.groupby("coin")["f3"].transform("mean")
    D["volr"] = D.groupby("coin")["vol30"].rank(pct=True)

    def ct(v, days):
        s = pd.DataFrame({"v": v, "d": days}).dropna()
        if len(s) < 5: return (np.nan, np.nan, len(s), 0)
        m = s["v"].mean(); g = (s["v"] - m).groupby(s["d"]).sum(); n = len(s); Dn = len(g)
        se = np.sqrt((g**2).sum() * Dn / (Dn - 1)) / n
        return (m, m / se, n, Dn)
    def tab(mask, col="x1", by=None):
        sub = D[mask]
        if by is None:
            m, t, n, dn = ct(sub[col], sub["day"]); return pd.Series({"mean": m, "t": t, "n": n, "days": dn})
        return pd.DataFrame({k: dict(zip(["mean","t","n","days"], ct(g[col], g["day"]))) for k, g in sub.groupby(by)}).T

    res = {}
    # signal: -r1z * vol rank (graded down-move in high vol), position-weighted next-day excess
    D["sig"] = -D["r1z"] * D["volr"]
    D["sig_x1"] = np.sign(D["sig"]) * D["x1"]
    D["sig_q"] = pd.qcut(D["sig"], 10, labels=False)
    res["x1_by_sig_decile"] = tab(D["sig"].notna(), by="sig_q")
    bd = D["r1z"] < -1.5
    D["hv"] = (D["volr"] > 0.6).astype(int)
    res["bigdown_highvol_by_year"] = tab(bd & (D["hv"] == 1), by="year")
    res["bigdown_highvol_by_coin"] = tab(bd & (D["hv"] == 1), by="coin")
    res["bigdown_highvol_x3_grid"] = tab(bd & (D["hv"] == 1) & (D["pos_i"] % 3 == 0), col="x3")
    # graded r1z within high vol
    D["r1z_q5"] = pd.qcut(D["r1z"], 5, labels=False)
    res["x1_by_r1z_q_highvol"] = tab(D["hv"] == 1, by="r1z_q5")
    res["x1_by_r1z_q_lowvol"] = tab(D["hv"] == 0, by="r1z_q5")
    # close location: low-minus-high spread by year / coin
    D["clv_s"] = np.where(D["clv"] < 0.2, 1, np.where(D["clv"] > 0.8, -1, np.nan))
    D["clv_x1"] = D["clv_s"] * D["x1"]
    res["clv_extreme_signed_by_year"] = tab(D["clv_s"].notna(), col="clv_x1", by="year")
    res["clv_extreme_signed_by_coin"] = tab(D["clv_s"].notna(), col="clv_x1", by="coin")
    res["clv_extreme_signed_by_vol"] = tab(D["clv_s"].notna(), col="clv_x1", by="hv")
    res["clv_low_x3_grid"] = tab((D["clv"] < 0.2) & (D["pos_i"] % 3 == 0), col="x3")
    # forecast parts on active bars
    act = D["fc"] > 0
    D["dep_q"] = pd.qcut(D["dep_raw"].where(act), 3, labels=False, duplicates="drop")
    D["rw_q"] = pd.qcut(D["rw_raw"].where(act), 3, labels=False, duplicates="drop")
    res["active_by_depth_tercile"] = tab(D["dep_q"].notna(), by="dep_q")
    res["active_by_rangewidth_tercile"] = tab(D["rw_q"].notna(), by="rw_q")
    # range ratio graded on all decline days with down day
    dec_dn = (D["ret30"] < 0) & (D["r1"] < 0)
    D["mr_q"] = pd.qcut(D["mr365r"].where(dec_dn), 5, labels=False, duplicates="drop")
    res["decline_downday_by_rangeratio_q"] = tab(D["mr_q"].notna(), by="mr_q")
    return res
