import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    cases = []
    tr = []
    for c, ws in data["bars"].items():
        # drift per coin
        allr = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 84, 84)
            allr += list(cl[idx + 84] / cl[idx] - 1)
        drift = np.mean(allr) if allr else 0
        for w, b in ws.items():
            cl = b["close"].values; hi = b["high"].values; lo = b["low"].values
            n = len(cl)
            s = pd.Series
            width = s(hi).rolling(6).max() - s(lo).rolling(6).min()
            mbr = s(hi - lo).rolling(180, min_periods=60).mean()
            ratio = (width / mbr).values
            r6 = s(cl).pct_change(6).values
            usual6 = s(cl).pct_change(6).abs().rolling(180, min_periods=60).mean().values
            depth = -r6 / usual6
            r180 = s(cl).pct_change(180).values
            r42 = s(cl).pct_change(42).values
            raw = b["debug_info.components.panic.last_history_value"].values if "debug_info.components.panic.last_history_value" in b else np.full(n, np.nan)
            fwd = np.full(n, np.nan)
            fwd[:n - 84] = cl[84:] / cl[:n - 84] - 1
            fwd12 = np.full(n, np.nan); fwd12[:n - 12] = cl[12:] / cl[:n - 12] - 1
            cell = np.arange(n) // 84
            ok = (ratio >= 4) & (r6 < 0) & ~np.isnan(fwd)
            df = pd.DataFrame({"cell": cell, "ratio": ratio, "depth": depth, "r180": r180, "r42": r42,
                               "raw": raw, "fwd": fwd, "fwd12": fwd12})[ok]
            df = df.groupby("cell").first()
            df["un"] = df.fwd - drift
            df["coin"] = c; df["wn"] = int(w[1:])
            cases.append(df)
            t = data["trades"][c][w]
            if len(t):
                t = t.copy()
                ts = pd.to_datetime(b["timestamp"]).values
                pos = np.clip(np.searchsorted(ts, pd.to_datetime(t["entry_time"]).values), 0, n - 1)
                t["ratio"] = ratio[pos]; t["depth"] = depth[pos]; t["r180"] = r180[pos]; t["r42"] = r42[pos]
                t["fwd12"] = fwd12[pos]; t["wn"] = int(w[1:]); t["coin"] = c
                tr.append(t)
    C = pd.concat(cases)
    def agg(g):
        return pd.Series({"n": len(g), "mean_un": g.un.mean(), "t": g.un.mean() / (g.un.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    C["rb"] = pd.cut(C.ratio, [4, 5.5, 7.5, 10, 1e9], right=False)
    C["tb"] = np.where(C.r180 > 0, "r30d_up", np.where(C.r180 <= 0, "r30d_down", "nan"))
    out["cases_ratio_x_trend30"] = C.groupby(["rb", "tb"], observed=True).apply(agg)
    C["db"] = pd.qcut(C.depth, 4, duplicates="drop")
    out["cases_depth_ratio>=4"] = C.groupby("db", observed=True).apply(agg)
    C["r42b"] = pd.qcut(C.r42, 4, duplicates="drop")
    out["cases_by_7d_ret"] = C.groupby("r42b", observed=True).apply(agg)
    T = pd.concat(tr)
    T["deep"] = T.wn.between(12, 18)
    out["trades_deepfall_vs_rest"] = T.groupby("deep").net_profit_loss_percent.agg(["count", "mean", "median", "min"])
    T["f12b"] = pd.qcut(T.fwd12, 4, duplicates="drop")
    out["trades_by_next2d"] = T.groupby("f12b", observed=True).net_profit_loss_percent.agg(["count", "mean"])
    T["r42b"] = pd.qcut(T.r42, 4, duplicates="drop")
    out["trades_by_7d_ret"] = T.groupby("r42b", observed=True).net_profit_loss_percent.agg(["count", "mean"])
    T["rb"] = pd.qcut(T.ratio, 4, duplicates="drop")
    out["trades_by_ratio"] = T.groupby("rb", observed=True).net_profit_loss_percent.agg(["count", "mean"])
    out["deep_trades_by_r180sign"] = T[T.deep].assign(up=T.r180 > 0).groupby("up").net_profit_loss_percent.agg(["count", "mean"])
    return out
