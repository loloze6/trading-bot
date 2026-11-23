import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    H = [12, 24, 48, 72, 96]
    # coin drift per horizon, non-overlapping grid per window
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            v = df["volume"].values
            f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            nz = np.where(f != 0)[0]
            for i in nz:
                r = {"coin": coin, "win": int(w[1:]), "year": ts.iloc[i].year,
                     "f": f[i], "side": np.sign(f[i])}
                for h in H:
                    if i + h < len(c):
                        r[f"u{h}"] = np.sign(f[i]) * (c[i + h] / c[i] - 1 - drift[(coin, h)])
                if i >= 168:
                    r["vr"] = v[i-47:i+1].mean() / v[i-167:i-47].mean()
                    r["wk"] = c[i] / c[i-48] - 1
                if i >= 720:
                    r["mkt30"] = c[i] / c[i-720] - 1
                r["wm"] = df["debug_info.components.weekend_move.post_pipeline_value"].iloc[i]
                r["tr"] = df["debug_info.components.trend30d.post_pipeline_value"].iloc[i]
                rows.append(r)
    d = pd.DataFrame(rows)

    def summ(g, col="u48"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "hit": (x > 0).mean()})
    out = {}
    out["by_horizon"] = pd.DataFrame({f"h{h}": summ(d, f"u{h}") for h in H}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_side"] = d.groupby("side").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["absf"] = d["f"].abs()
    d["fq"] = pd.qcut(d["absf"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["by_forecast_q"] = d.groupby("fq").apply(summ)
    d["vrq"] = pd.qcut(d["vr"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["by_volratio_t"] = d.groupby("vrq").apply(summ)
    d["wkq"] = pd.qcut((d["wk"].abs()).rank(method="first"), 3, labels=["small", "mid", "large"])
    out["by_abs_weekend_move_t"] = d.groupby("wkq").apply(summ)
    d["trq"] = pd.qcut(d["tr"].abs().rank(method="first"), 3, labels=["weak", "mid", "strong"])
    out["by_abs_trend_t"] = d.groupby("trq").apply(summ)
    out["by_side_h"] = d.groupby("side").apply(lambda g: pd.Series({f"t{h}": summ(g, f"u{h}")["t"] for h in H} | {f"m{h}": summ(g, f"u{h}")["mean"] for h in H}))
    out["corr_absf_u48"] = float(stats.spearmanr(d["absf"], d["u48"], nan_policy="omit")[0])
    out["median_u48"] = float(d["u48"].median())
    out["trim_mean_u48_5pct"] = float(stats.trim_mean(d["u48"].dropna(), 0.05))
    return out
