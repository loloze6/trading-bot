def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            r = c.pct_change()
            s30 = r.rolling(30, min_periods=15).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fa": (b["regime"] != "chop").astype(int),
                "r": r, "rz": r / s30,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "r3z": (c / c.shift(3) - 1) / s30,
                "r2z": (c / c.shift(2) - 1) / s30,
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
            })
            dn = (r < 0).astype(int)
            df["dns_prev"] = (dn.groupby((dn != dn.shift()).cumsum()).cumsum() * dn).shift(1)
            up = (r > 0).astype(int)
            df["ups"] = up.groupby((up != up.shift()).cumsum()).cumsum() * up
            df["idx"] = np.arange(len(df))
            df["half"] = np.where(df["win"].str[1:].astype(int) <= 12, "early", "late")
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    dr = {k: d[k].mean() for k in ["f1", "f2", "f3"]}
    for k in dr: d["u" + k[1]] = d[k] - dr[k]
    def summ(g, col="u1"):
        g = g.dropna(subset=[col])
        n = len(g)
        if n < 3: return pd.Series({"n": n, "mean%": np.nan, "t_day": np.nan, "days": np.nan})
        m = g[col].mean()
        dev = (g[col] - m).groupby(g["day"]).sum()
        nd = len(dev)
        se = np.sqrt((dev ** 2).sum() * nd / (nd - 1)) / n
        return pd.Series({"n": n, "mean%": 100 * m, "t_day": m / se, "days": nd})
    out = {}
    fa = d[d["fa"] == 1].copy()
    upd = fa[fa["r"] > 0].copy()
    upd["q"] = pd.qcut(upd["rz"], 4, labels=False, duplicates="drop")
    out["fa_up_by_rz_q4"] = upd.groupby("q").apply(summ)
    out["fa_up_by_rz_q4_half"] = upd.groupby(["half", "q"]).apply(summ)
    upd["pd"] = upd["dns_prev"].clip(0, 3)
    out["fa_up_by_prev_downstreak"] = upd.groupby("pd").apply(summ)
    upd["cq"] = pd.qcut(upd["clv"], 3, labels=False, duplicates="drop")
    out["fa_up_by_clv_t3"] = upd.groupby("cq").apply(summ)
    out["fa_up_by_coin"] = upd.groupby("coin").apply(summ)
    out["fa_up_by_half"] = upd.groupby("half").apply(summ)
    # 2-day and 3-day give-back after multi-day rises, non-overlapping grids
    for hz, col, zc in [(2, "u2", "r2z"), (3, "u3", "r3z")]:
        g = fa[(fa["idx"] % hz == 0) & (fa[zc] > 0)].copy()
        g["q"] = pd.qcut(g[zc], 3, labels=False, duplicates="drop")
        out[f"fa_{hz}d_after_rise_by_{zc}_t3"] = g.groupby("q").apply(lambda x: summ(x, col))
        out[f"fa_{hz}d_after_rise_half"] = g.groupby("half").apply(lambda x: summ(x, col))
    # outside FA, up days by rz
    nf = d[(d["fa"] == 0) & (d["r"] > 0)].copy()
    nf["q"] = pd.qcut(nf["rz"], 4, labels=False, duplicates="drop")
    out["nonfa_up_by_rz_q4"] = nf.groupby("q").apply(summ)
    return out
