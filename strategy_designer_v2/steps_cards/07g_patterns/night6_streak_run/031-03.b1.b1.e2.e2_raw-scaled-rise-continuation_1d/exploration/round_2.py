import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    H = 5
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(allr); usual = np.std(allr, ddof=1)
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"]; r1 = c.pct_change()
            vol = r1.rolling(60, min_periods=20).std()
            vsr = (c / c.shift(10) - 1) / (vol * np.sqrt(10))
            v = d["volume"]
            volu = v / v.rolling(20, min_periods=10).mean()
            volu5 = v.rolling(5).mean() / v.rolling(60, min_periods=20).mean()
            clpos = (c - d["low"]) / (d["high"] - d["low"]).replace(0, np.nan)
            fwd = c.shift(-H) / c - 1
            sel = d.index[::H]
            out = pd.DataFrame({
                "coin": coin,
                "day": pd.to_datetime(d.loc[sel, "timestamp"]).dt.floor("D").values,
                "vsr": vsr[sel].values, "volu": volu[sel].values, "volu5": volu5[sel].values,
                "clpos": clpos[sel].values, "fwd": fwd[sel].values,
                "alloc": d.loc[sel, "postRebalance_current_allocation"].values})
            out["unus"] = out["fwd"] - drift
            out["str"] = out["unus"] / usual
            rows.append(out)
    A = pd.concat(rows).dropna(subset=["fwd", "vsr", "volu"])

    def ct(sub, col="unus"):
        sub = sub.dropna(subset=[col])
        if len(sub) < 10: return pd.Series({"n": len(sub), "mean": np.nan, "t": np.nan, "days": 0})
        dev = sub[col] - sub[col].mean()
        s = dev.groupby(sub["day"]).sum(); D = len(s)
        se = np.sqrt((s**2).sum() * D / (D - 1)) / len(sub)
        return pd.Series({"n": len(sub), "mean": sub[col].mean(), "t": sub[col].mean() / se,
                          "days": D, "strength": sub["str"].mean()})

    def slope(sub, x, y="str"):
        sub = sub.dropna(subset=[x, y]).copy()
        X = sub[x] - sub[x].mean(); b = (X * sub[y]).sum() / (X**2).sum()
        e = sub[y] - sub[y].mean() - b * X
        s = (X * e).groupby(sub["day"]).sum(); D = len(s)
        se = np.sqrt((s**2).sum() * D / (D - 1)) / (X**2).sum()
        return pd.Series({"n": len(sub), "days": D, "slope": b, "t": b / se})

    res = {}
    A["lvolu"] = np.log(A["volu"]); A["lvolu5"] = np.log(A["volu5"])
    up = A[A["vsr"] >= 1]; dn = A[A["vsr"] <= -1]
    res["slope_str_on_logvolume_surge"] = pd.DataFrame({
        "all": slope(A, "lvolu"), "vsr>=1": slope(up, "lvolu"), "vsr<=-1": slope(dn, "lvolu"),
        "vsr_-1_to_1": slope(A[A["vsr"].abs() < 1], "lvolu")}).T
    res["slope_str_on_log5dvolume"] = pd.DataFrame({
        "all": slope(A, "lvolu5"), "vsr>=1": slope(up, "lvolu5"), "vsr<=-1": slope(dn, "lvolu5")}).T
    A["vsr_x_lv"] = A["vsr"] * A["lvolu"]
    res["slope_str_on_vsr_x_logvolu"] = pd.DataFrame({"all": slope(A, "vsr_x_lv"),
                                                      "vsr": slope(A, "vsr")}).T
    res["vsr>=1_by_volu_tercile"] = up.groupby(pd.qcut(up["volu"], 3)).apply(ct)
    res["vsr_-1to1_by_volu_quint"] = A[A["vsr"].abs() < 1].groupby(
        pd.qcut(A[A["vsr"].abs() < 1]["volu"], 5)).apply(ct)
    res["vsr>=1_by_closepos"] = up.groupby(pd.qcut(up["clpos"], 3)).apply(ct)
    # trades
    T = []
    for coin, wins in trades.items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    T = pd.concat(T)
    T["dur_d"] = T["duration_minutes"] / 1440
    res["trades_summary"] = pd.Series({"n": len(T), "mean_net": T["net_profit_loss_percent"].mean(),
        "median_net": T["net_profit_loss_percent"].median(), "win_share": (T["net_profit_loss_percent"] > 0).mean(),
        "mean_dur_days": T["dur_d"].mean(),
        "top10pct_share_of_sum": T["net_profit_loss_percent"].nlargest(max(1, len(T)//10)).sum() / T["net_profit_loss_percent"].sum()})
    res["trades_by_entry_forecast"] = T.groupby(pd.qcut(T["entry_forecast"], 3, duplicates="drop"))["net_profit_loss_percent"].agg(["count", "mean", "median"])
    res["trades_by_duration"] = T.groupby(pd.cut(T["dur_d"], [0, 5.5, 10, 20, 999]))["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return res
