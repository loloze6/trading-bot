import numpy as np, pandas as pd

def explore(data):
    out = {}
    cases = []
    tr = []
    for c, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 84, 84)
            allr += list(cl[idx + 84] / cl[idx] - 1)
        drift = float(np.mean(allr)) if len(allr) else 0.0
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values.astype(float); hi = b["high"].values.astype(float); lo = b["low"].values.astype(float)
            n = len(cl)
            if n < 200:
                continue
            S = pd.Series
            width = (S(hi).rolling(6).max() - S(lo).rolling(6).min()).values
            mbr = S(hi - lo).rolling(180, min_periods=60).mean().values
            ratio = width / mbr
            r6 = S(cl).pct_change(6).values
            usual6 = S(cl).pct_change(6).abs().rolling(180, min_periods=60).mean().values
            depth = -r6 / usual6
            r180 = S(cl).pct_change(180).values
            r42 = S(cl).pct_change(42).values
            fwd = np.full(n, np.nan); fwd[:n - 84] = cl[84:] / cl[:n - 84] - 1
            cell = np.arange(n) // 84
            ok = (ratio >= 4) & (r6 < 0) & np.isfinite(fwd) & np.isfinite(ratio)
            if ok.any():
                df = pd.DataFrame({"cell": cell[ok], "ratio": ratio[ok], "depth": depth[ok], "r180": r180[ok],
                                   "r42": r42[ok], "fwd": fwd[ok]})
                df = df.groupby("cell", as_index=False).first()
                df["un"] = df["fwd"] - drift
                df["wn"] = int(w[1:])
                cases.append(df)
            t = data["trades"][c][w]
            if len(t):
                ts = pd.to_datetime(b["timestamp"]).values
                pos = np.clip(np.searchsorted(ts, pd.to_datetime(t["entry_time"]).values), 0, n - 1)
                tt = pd.DataFrame({"pl": t["net_profit_loss_percent"].values, "ratio": ratio[pos], "depth": depth[pos],
                                   "r180": r180[pos], "r42": r42[pos], "wn": int(w[1:])})
                tr.append(tt)
    C = pd.concat(cases, ignore_index=True)
    def agg(g):
        m = g["un"].mean(); s = g["un"].std(); k = len(g)
        return pd.Series({"n": k, "mean_un": m, "t": m / (s / np.sqrt(k)) if k > 2 and s > 0 else np.nan})
    C["rb"] = pd.cut(C["ratio"], [4, 5.5, 7.5, 10, 1e9], right=False).astype(str)
    C["tb"] = np.where(C["r180"] > 0, "r30d_up", "r30d_down")
    out["cases_ratio_x_trend30"] = C.groupby(["rb", "tb"]).apply(agg)
    C["db"] = pd.qcut(C["depth"], 4, duplicates="drop").astype(str)
    out["cases_by_depth"] = C.groupby("db").apply(agg)
    C["r42b"] = pd.qcut(C["r42"], 4, duplicates="drop").astype(str)
    out["cases_by_7d_ret"] = C.groupby("r42b").apply(agg)
    C["deep"] = C["wn"].between(12, 18)
    out["cases_deepwindows"] = C.groupby(["deep", "tb"]).apply(agg)
    T = pd.concat(tr, ignore_index=True)
    T["deep"] = T["wn"].between(12, 18)
    T["up30"] = T["r180"] > 0
    out["trades_deep_x_up30"] = T.groupby(["deep", "up30"])["pl"].agg(["count", "mean", "median", "min"])
    T["r42b"] = pd.qcut(T["r42"], 4, duplicates="drop").astype(str)
    out["trades_by_7d_ret"] = T.groupby("r42b")["pl"].agg(["count", "mean"])
    T["rb"] = pd.qcut(T["ratio"], 4, duplicates="drop").astype(str)
    out["trades_by_ratio"] = T.groupby("rb")["pl"].agg(["count", "mean"])
    return out
