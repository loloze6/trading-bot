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
            sma50 = cl.rolling(50).mean()
            sma20 = cl.rolling(20).mean()
            b["slope50"] = sma50 / sma50.shift(10) - 1
            b["slope20"] = sma20 / sma20.shift(5) - 1
            b["r60"] = cl.pct_change(60)
            b["a50"] = (cl > sma50).astype(float).where(sma50.notna())
            for k in ["slope50", "slope20", "r60", "a50"]:
                b[k + "_p"] = b[k].shift(1)
            d = data["days"][c][w][["day", "book_return", "coin_return"]].copy()
            d["day"] = pd.to_datetime(d["day"]).dt.floor("D")
            if d["day"].dt.tz is not None and b["day"].dt.tz is None:
                b["day"] = b["day"].dt.tz_localize("UTC")
            if b["day"].dt.tz is not None and d["day"].dt.tz is None:
                d["day"] = d["day"].dt.tz_localize("UTC")
            m = d.merge(b[["day", "slope50_p", "slope20_p", "r60_p", "a50_p"]], on="day", how="left")
            m["coin"] = c; m["wi"] = int(w[1:])
            rows.append(m)
    M = pd.concat(rows).dropna(subset=["book_return"])

    def stats(br_col):
        Bk = M.groupby(["wi", "day"])[br_col].mean().reset_index().sort_values(["wi", "day"])
        r = Bk[br_col].values
        eq = np.cumprod(1 + r)
        dd = eq / np.maximum.accumulate(eq) - 1
        ann = eq[-1] ** (365 / len(r)) - 1
        early = Bk["wi"] <= 10
        return pd.Series({"sharpe": r.mean() / r.std() * np.sqrt(365), "mean": r.mean(),
                          "maxdd": dd.min(), "calmar": ann / -dd.min(),
                          "early_mean": r[early.values].mean(), "late_mean": r[~early.values].mean()})
    conds = {
        "base": pd.Series(True, index=M.index),
        "slope50>0": M["slope50_p"] > 0,
        "slope50>0.0145": M["slope50_p"] > 0.0145,
        "r60>0": M["r60_p"] > 0,
        "above50": M["a50_p"] == 1,
        "slope20>0": M["slope20_p"] > 0,
    }
    res = {}
    for k, cnd in conds.items():
        col = "br_" + k
        M[col] = M["book_return"].where(cnd.fillna(False), 0.0)
        res[k] = stats(col)
    out["counterfactual"] = pd.DataFrame(res).T.round(4)

    T = []
    for c in coins:
        for w in wins:
            t = data["trades"][c][w].copy(); t["coin"] = c; t["wi"] = int(w[1:])
            b = data["bars"][c][w].copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            cl = b["close"]; sma50 = cl.rolling(50).mean()
            b["slope50"] = sma50 / sma50.shift(10) - 1
            b["dist20"] = cl / cl.rolling(20).mean() - 1
            b["r20"] = cl.pct_change(20)
            t["et"] = pd.to_datetime(t["entry_time"])
            if t["et"].dt.tz is not None and b["ts"].dt.tz is None: b["ts"] = b["ts"].dt.tz_localize("UTC")
            if b["ts"].dt.tz is not None and t["et"].dt.tz is None: t["et"] = t["et"].dt.tz_localize("UTC")
            t = pd.merge_asof(t.sort_values("et"), b[["ts", "slope50", "dist20", "r20"]].sort_values("ts"),
                              left_on="et", right_on="ts", direction="backward")
            T.append(t)
    T = pd.concat(T)
    T["short"] = (T["duration_minutes"] / 1440 <= 3).astype(int)
    out["trades_by_entry_slope50"] = T.groupby(pd.qcut(T["slope50"], 5, duplicates="drop")).agg(
        net=("net_profit_loss_percent", "mean"), med=("net_profit_loss_percent", "median"),
        n=("net_profit_loss_percent", "size"), share_short=("short", "mean")).round(3)
    out["trades_by_entry_dist20"] = T.groupby(pd.qcut(T["dist20"], 5, duplicates="drop")).agg(
        net=("net_profit_loss_percent", "mean"), med=("net_profit_loss_percent", "median"),
        n=("net_profit_loss_percent", "size"), share_short=("short", "mean")).round(3)
    return out
