import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; o = b["open"]
            r1 = c.pct_change()
            rng = (b["high"] - b["low"]) / c.shift(1)
            rr = rng / rng.rolling(20).mean()
            sd20 = r1.rolling(20).std()
            f5 = (c.shift(1) / c.shift(6) - 1) / (sd20 * np.sqrt(5))
            r60 = c / c.shift(60) - 1
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            pos = (b["high"] > b["low"]) * 0 + (c - b["low"]) / (b["high"] - b["low"])
            df = pd.DataFrame({"coin": coin, "win": w, "day": b["timestamp"].astype(str).str[:10],
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "r1": r1, "z1": r1 / sd20, "rr": rr, "f5": f5, "r60": r60,
                               "clpos": pos, "sd": sd20, "nxt": nxt, "nxt2": nxt2,
                               "regime": b["regime"], "alloc": b["postRebalance_current_allocation"],
                               "fc": b["forecast"]})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["nxt"].mean()
    D["u"] = D["nxt"] - D["coin"].map(drift)
    D["uz"] = D["u"] / D["sd"]
    D["trend"] = np.where(D["r60"] < -0.10, "falling", np.where(D["r60"] > 0.10, "rising", "choppy"))
    D.loc[D["r60"].isna(), "trend"] = np.nan

    def ct(sub, col="u"):
        s = sub.dropna(subset=[col])
        if len(s) < 5: return pd.Series({"n": len(s), "mean": np.nan, "t": np.nan, "days": 0})
        m = s[col].mean()
        g = s.groupby("day")[col].apply(lambda x: (x - m).sum())
        se = np.sqrt((g ** 2).sum()) / len(s)
        return pd.Series({"n": len(s), "days": len(g), "mean": m, "t": m / se if se > 0 else np.nan})

    out = {}
    E = D.dropna(subset=["trend", "rr", "r1", "u"])
    up = E[E.r1 > 0]
    # up days by trend x width
    up = up.assign(wide=pd.qcut(up.rr, 3, labels=["narrow", "mid", "wide"]))
    out["up_days_trend_x_width_nextday"] = up.groupby(["trend", "wide"]).apply(ct).round(4)
    # falling up-wide days by prior 5d fall tercile
    fw = up[(up.trend == "falling") & (up.rr > 1)].dropna(subset=["f5"])
    fw = fw.assign(f5q=pd.qcut(fw.f5, 4, labels=False))
    out["falling_wide_up_by_f5_quartile"] = fw.groupby("f5q").apply(ct).round(4)
    fw2 = fw.assign(z1q=pd.qcut(fw.z1, 4, labels=False))
    out["falling_wide_up_by_upday_size_quartile"] = fw2.groupby("z1q").apply(ct).round(4)
    fw3 = fw.assign(cpq=pd.qcut(fw.clpos, 3, labels=False))
    out["falling_wide_up_by_closepos_tercile"] = fw3.groupby("cpq").apply(ct).round(4)
    # all days: next day by own-day z1 quintile per trend
    E2 = E.assign(zq=E.groupby("trend")["z1"].transform(lambda x: pd.qcut(x, 5, labels=False)))
    out["all_days_trend_x_z1quintile_next_uz"] = E2.groupby(["trend", "zq"]).apply(lambda s: ct(s, "uz")).round(3)
    # falling, down days, by width
    dn = E[(E.r1 < 0)]
    dn = dn.assign(wide=pd.qcut(dn.rr, 3, labels=["narrow", "mid", "wide"]))
    out["down_days_trend_x_width_next"] = dn.groupby(["trend", "wide"]).apply(ct).round(4)
    # weekday in falling
    out["falling_weekday_next"] = E[E.trend == "falling"].groupby("wd").apply(ct).round(4)
    # the book's active bars: next day by forecast size halves and by window
    A = D[D.alloc < 0].dropna(subset=["u"])
    A = A.assign(sh=-A.u, big=(A.fc.abs() > A.fc.abs().median()))
    out["book_active_short_gain_by_size_half"] = A.groupby("big").apply(lambda s: ct(s, "sh")).round(4)
    out["book_active_by_window"] = A.groupby("win").apply(lambda s: ct(s, "sh")).round(4)
    out["book_active_by_coin"] = A.groupby("coin").apply(lambda s: ct(s, "sh")).round(4)
    # 2-day in falling wide up days
    fw4 = fw.dropna(subset=["nxt2"]).assign(u2=lambda s: s.nxt2 - 2 * s.coin.map(drift))
    out["falling_wide_up_2day"] = ct(fw4, "u2").round(4)
    return out
