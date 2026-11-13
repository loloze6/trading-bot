import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            f10 = c.shift(-10) / c - 1
            f1 = c.shift(-1) / c - 1
            vol20 = r1.rolling(20).std()
            r5 = c / c.shift(5) - 1
            d = pd.DataFrame({
                "coin": coin, "w": w,
                "fc": b["forecast"].astype(float),
                "dist": b["debug_info.components.below_ma.last_history_value"].astype(float),
                "r1": r1, "r5": r5, "f1": f1, "f10": f10, "vol20": vol20,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "up_share": (x > 0).mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["dist_raw_describe"] = A["dist"].describe()
    A["distq"] = pd.qcut(A["dist"], 10, duplicates="drop")
    out["f10_by_dist_decile"] = A.groupby("distq").apply(lambda g: summ(g, "f10"))
    A["fcb"] = pd.cut(A["fc"], [-21, -10, -5, -2, -0.0001, 0.0001], labels=["<-10", "-10..-5", "-5..-2", "-2..0", "0"])
    out["f10_by_forecast"] = A.groupby("fcb").apply(lambda g: summ(g, "f10"))
    A["r1q"] = A.groupby("coin")["r1"].transform(lambda x: pd.qcut(x, 10, labels=False, duplicates="drop"))
    out["f1_by_r1_decile"] = A.groupby("r1q").apply(lambda g: summ(g, "f1"))
    out["f10_by_r1_decile"] = A.groupby("r1q").apply(lambda g: summ(g, "f10"))
    A["r5q"] = A.groupby("coin")["r5"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    A["below"] = A["dist"] < 0
    out["f10_by_r5q_and_below"] = A.groupby(["below", "r5q"]).apply(lambda g: summ(g, "f10"))
    A["volq"] = A.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["f10_by_vol_and_below"] = A.groupby(["below", "volq"]).apply(lambda g: summ(g, "f10"))
    out["f1_by_weekday"] = A.groupby("wd").apply(lambda g: summ(g, "f1"))
    out["f10_below_by_coin"] = A[A.below].groupby("coin").apply(lambda g: summ(g, "f10"))
    out["f10_below_by_year"] = A[A.below].groupby("yr").apply(lambda g: summ(g, "f10"))
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    tr["dur_d"] = tr["duration_minutes"] / 1440
    tr["durb"] = pd.cut(tr["dur_d"], [0, 1.5, 3, 7, 20, 1000])
    out["trades_by_duration"] = tr.groupby("durb")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades_side"] = tr.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median", "sum"])
    out["trade_comm_mean"] = float(tr["total_commission"].mean())
    return out
