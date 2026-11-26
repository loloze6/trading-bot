import pandas as pd, numpy as np

def explore(data):
    def build(H):
        per = []
        for coin, wins in data["bars"].items():
            gg = []
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                o, h, l, c = b["open"], b["high"], b["low"], b["close"]
                rng = h - l
                rr = rng / rng.rolling(20, min_periods=20).mean()
                r1 = c / c.shift(1) - 1
                r20 = c / c.shift(20) - 1
                vol20 = r1.rolling(20).std()
                atr = (rng / c).rolling(20).mean()
                fwd = c.shift(-H) / c - 1
                idx = np.arange(0, len(b), H)
                idx = idx[idx + H < len(b)]
                gg.append(pd.DataFrame({"coin": coin,
                    "day": b["timestamp"].iloc[idx].astype(str).str[:10].values,
                    "rr": rr.iloc[idx].values, "r1": r1.iloc[idx].values, "r20": r20.iloc[idx].values,
                    "r1v": (r1 / vol20).iloc[idx].values, "r20v": (r20 / (vol20 * np.sqrt(20))).iloc[idx].values,
                    "fwd": fwd.iloc[idx].values}))
            g = pd.concat(gg)
            g["un"] = g["fwd"] - g["fwd"].mean()
            g["str"] = g["un"] / g["fwd"].std()
            per.append(g)
        return pd.concat(per, ignore_index=True).dropna(subset=["rr", "r20", "r1v", "r20v"])

    def summ(df, key):
        out = []
        for k, s in df.groupby(key, observed=True):
            d = s.groupby("day")["un"].sum(); n = len(s); nd = len(d)
            t = (d.sum() / n) / (np.sqrt(nd) * d.std(ddof=1) / n) if nd > 2 else np.nan
            out.append({"grp": str(k), "n": n, "days": nd, "mean_un": round(s["un"].mean(), 5),
                        "strength": round(s["str"].mean(), 4), "t": round(t, 2)})
        return pd.DataFrame(out)

    res = {}
    G = build(3)
    up = G[G["r20"] > 0].copy()
    up["rr_q"] = pd.qcut(up["rr"], 5)
    res["r20pos_by_rr_q"] = summ(up, "rr_q")
    dn = G[G["r20"] <= 0].copy()
    dn["rr_q"] = pd.qcut(dn["rr"], 5)
    res["r20neg_by_rr_q"] = summ(dn, "rr_q")
    # all days, vol-scaled 20d trend quintile
    G["r20v_q"] = pd.qcut(G["r20v"], 5)
    res["all_by_r20v_q"] = summ(G, "r20v_q")
    # wide days, vol-scaled 20d trend
    wd = G[G["rr"] >= 1.5].copy()
    wd["r20v_q"] = pd.qcut(wd["r20v"], 5)
    res["wide_by_r20v_q"] = summ(wd, "r20v_q")
    # wide & up-trend, by sign of the day's move
    wu = wd[wd["r20"] > 0].copy()
    wu["r1_sign"] = np.sign(wu["r1"])
    res["wide_r20pos_by_r1sign"] = summ(wu, "r1_sign")
    # interaction: rr * r20v product among r20>0
    up["prod_q"] = pd.qcut(up["rr"] * up["r20v"], 5)
    res["r20pos_by_rr_x_r20v_q"] = summ(up, "prod_q")
    # horizons for wide & r20 > 0.134
    hz = []
    for H in [1, 2, 5, 10]:
        g = build(H)
        s = g[(g["rr"] >= 1.5) & (g["r20"] > 0.134)]
        d = s.groupby("day")["un"].sum(); n = len(s); nd = len(d)
        hz.append({"H": H, "n": n, "days": nd, "mean_un": round(s["un"].mean(), 5),
                   "strength": round(s["str"].mean(), 4),
                   "t": round((d.sum() / n) / (np.sqrt(nd) * d.std(ddof=1) / n), 2)})
    res["wide_strongup_by_horizon"] = pd.DataFrame(hz)
    # book: trades by duration and entry forecast
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["fq"] = pd.qcut(T["entry_forecast"], 4, duplicates="drop")
    res["trades_by_entry_fc"] = T.groupby("fq", observed=True)["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    T["dq"] = pd.cut(T["dur_d"], [0, 3.5, 6, 10, 20, 1000])
    res["trades_by_duration"] = T.groupby("dq", observed=True)["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    res["trades_win_share"] = round((T["net_profit_loss_percent"] > 0).mean(), 3)
    res["trades_top5pct_share_of_sum"] = round(T["net_profit_loss_percent"].nlargest(int(len(T) * 0.05)).sum() / T["net_profit_loss_percent"].sum(), 3)
    return res
