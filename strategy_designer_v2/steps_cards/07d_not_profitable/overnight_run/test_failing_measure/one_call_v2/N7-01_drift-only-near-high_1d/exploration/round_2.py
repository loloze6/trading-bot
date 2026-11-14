import numpy as np, pandas as pd

def explore(data):
    out = {}
    coins = list(data["days"].keys())
    wins = list(data["days"][coins[0]].keys())
    rows = []
    for c in coins:
        for w in wins:
            b = data["bars"][c][w].copy()
            cl = b["close"]
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["r60"] = cl.pct_change(60)
            b["r30"] = cl.pct_change(30)
            sma50 = cl.rolling(50).mean()
            b["above50"] = (cl > sma50).astype(float).where(sma50.notna())
            b["slope50"] = (sma50 / sma50.shift(10) - 1)
            lr = np.log(cl).diff()
            b["vol20"] = lr.rolling(20).std()
            b["alloc_prev"] = b["postRebalance_current_allocation"].shift(1)
            b["r30_prev"] = b["r30"].shift(1); b["r60_prev"] = b["r60"].shift(1)
            b["above50_prev"] = b["above50"].shift(1); b["slope50_prev"] = b["slope50"].shift(1)
            b["vol_prev"] = b["vol20"].shift(1)
            d = data["days"][c][w][["day", "book_return", "coin_return"]].copy()
            d["day"] = pd.to_datetime(d["day"]).dt.floor("D")
            if d["day"].dt.tz is not None and b["day"].dt.tz is None:
                b["day"] = b["day"].dt.tz_localize("UTC")
            if b["day"].dt.tz is not None and d["day"].dt.tz is None:
                d["day"] = d["day"].dt.tz_localize("UTC")
            m = d.merge(b[["day", "alloc_prev", "r30_prev", "r60_prev", "above50_prev", "slope50_prev", "vol_prev"]], on="day", how="left")
            m["coin"] = c; m["wi"] = int(w[1:])
            rows.append(m)
    M = pd.concat(rows).dropna(subset=["book_return"])
    # book daily return
    Bk = M.groupby(["wi", "day"])["book_return"].mean().reset_index().sort_values(["wi", "day"])
    eq = (1 + Bk["book_return"]).cumprod().values
    dd = eq / np.maximum.accumulate(eq) - 1
    Bk["indd"] = (np.arange(len(dd)) <= 1161).astype(int)
    out["book_sharpe_part"] = Bk.groupby("indd")["book_return"].agg(["mean", "std", "count"]).round(5)
    act = M[M["alloc_prev"] > 0].copy()
    out["active_days_count"] = int(len(act))
    def tab(col, q=None, bins=None):
        g = act.groupby(pd.qcut(act[col], q, duplicates="drop") if q else act[col])
        r = g["book_return"].agg(["mean", "std", "count", "sum"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        r["coin_mean"] = g["coin_return"].mean()
        return r.round(4)
    out["by_r60"] = tab("r60_prev", 5)
    out["by_r30"] = tab("r30_prev", 5)
    out["by_above50"] = tab("above50_prev")
    out["by_slope50"] = tab("slope50_prev", 5)
    out["by_vol"] = tab("vol_prev", 5)
    # combined: slope50 sign
    act["slope_pos"] = (act["slope50_prev"] > 0).astype(float).where(act["slope50_prev"].notna())
    out["by_slope_sign_x_inDD"] = act.assign(early=(act["wi"] <= 10).astype(int)).groupby(["early", "slope_pos"])["book_return"].agg(["mean", "std", "count", "sum"]).round(4)
    # trades: fees
    T = []
    for c in coins:
        for w in wins:
            t = data["trades"][c][w].copy(); t["wi"] = int(w[1:]); T.append(t)
    T = pd.concat(T)
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trades_summary"] = pd.Series({"n": len(T), "gross_mean": T["profit_loss_percent"].mean(), "net_mean": T["net_profit_loss_percent"].mean(),
                                       "win_net": (T["net_profit_loss_percent"] > 0).mean(), "dur_median": T["dur_d"].median(),
                                       "share_dur_le2": (T["dur_d"] <= 2).mean()}).round(4)
    T["early"] = (T["wi"] <= 10).astype(int)
    out["trades_by_duration"] = T.groupby(pd.cut(T["dur_d"], [0, 1, 3, 7, 15, 40, 500]))["net_profit_loss_percent"].agg(["mean", "count", "sum"]).round(3)
    return out
