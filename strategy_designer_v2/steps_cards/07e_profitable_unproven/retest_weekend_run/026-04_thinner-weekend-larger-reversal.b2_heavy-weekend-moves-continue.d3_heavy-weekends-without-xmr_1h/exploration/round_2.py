import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars, trades = data["bars"], data["trades"]
    out = {}
    drift, usual = {}, {}
    for c in bars:
        for h in (48,):
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            ts = pd.to_datetime(b["timestamp"]); cl = b["close"].values; vol = b["volume"].values
            n = len(cl)
            for kind, wd in (("weekend", 6), ("midweek", 2)):
                sel = np.where((ts.dt.weekday.values == wd) & (ts.dt.hour.values == 23))[0]
                for i in sel:
                    if i < 168 or i + 48 >= n: continue
                    m48 = cl[i] / cl[i-48] - 1
                    vr = vol[i-47:i+1].mean() / max(vol[i-167:i-47].mean(), 1e-12)
                    sg = np.sign(m48)
                    recs.append({"coin": c, "kind": kind, "vr": vr, "z": abs(m48)/usual[(c,48)],
                                 "sign": sg, "u48": sg*(cl[i+48]/cl[i]-1-drift[(c,48)]),
                                 "s48": usual[(c,48)]})
    R = pd.DataFrame(recs)
    R["str"] = R["u48"] / R["s48"]
    def tt(x): return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/x.std()*np.sqrt(len(x))})
    for kind in ("weekend", "midweek"):
        K = R[R.kind == kind].copy()
        K["vq"] = pd.qcut(K["vr"], 5, labels=[f"v{i}" for i in range(1, 6)])
        out[f"{kind}_strength_by_vq5"] = K.groupby("vq")["str"].apply(tt).unstack()
        K["lvr"] = np.log(K["vr"])
        X = np.column_stack([np.ones(len(K)), K["lvr"], K["z"]])
        beta, *_ = np.linalg.lstsq(X, K["str"].values, rcond=None)
        res = K["str"].values - X @ beta
        cov = np.linalg.inv(X.T @ X) * res.var(ddof=3)
        out[f"{kind}_ols_str_on_logvr_z"] = pd.DataFrame({"beta": beta, "t": beta/np.sqrt(np.diag(cov))},
                                                         index=["const", "log_vr", "z"])
    H = R[(R.kind == "weekend") & (R.vr > 1)].copy()
    H["zq"] = pd.qcut(H["z"], 3, labels=["small", "mid", "large"])
    H["vq"] = pd.qcut(H["vr"], 3, labels=["v_low", "v_mid", "v_high"])
    out["heavy_weekend_by_zq"] = H.groupby("zq")["str"].apply(tt).unstack()
    out["heavy_weekend_by_vq"] = H.groupby("vq")["str"].apply(tt).unstack()
    H["side"] = np.where(H.sign > 0, "up", "down")
    out["heavy_weekend_side_vq"] = H.groupby(["side", "vq"])["str"].apply(tt).unstack()
    # trades: top 10
    T = []
    for c in trades:
        for w, t in trades[c].items():
            if len(t):
                t = t.copy(); t["coin"] = c; t["win"] = w; T.append(t)
    T = pd.concat(T)
    top = T.sort_values("net_profit_loss_percent", ascending=False).head(10)
    out["top10_by_coin_side"] = top.groupby(["coin", "side"])["net_profit_loss_percent"].agg(["count", "sum"])
    out["top10_by_year"] = top.groupby(pd.to_datetime(top["entry_time"]).dt.year)["net_profit_loss_percent"].agg(["count", "sum"])
    out["top10_duration_hours"] = (top["duration_minutes"] / 60).describe()
    out["all_duration_hours"] = (T["duration_minutes"] / 60).describe()
    out["by_side_all"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "sum", "median"])
    return out
