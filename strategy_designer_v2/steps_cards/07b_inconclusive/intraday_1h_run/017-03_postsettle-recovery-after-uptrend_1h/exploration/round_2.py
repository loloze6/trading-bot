import numpy as np, pandas as pd
from scipy import stats

def _t(x, y):
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if len(x) < 30:
        return np.nan, len(x)
    r = stats.linregress(x, y)
    return r.slope / r.stderr, len(x)

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 2, 2)
            rs.append(c[idx + 2] / c[idx] - 1)
        m2 = np.nanmean(np.concatenate(rs))
        for w, df in wins.items():
            d = pd.DataFrame({"ts": pd.to_datetime(df["timestamp"], utc=True), "close": df["close"].values})
            d["hour"] = d["ts"].dt.hour
            d["year"] = d["ts"].dt.year
            d["wd"] = d["ts"].dt.weekday
            d["rise"] = d["close"] / d["close"].shift(72) - 1
            d["ex2"] = d["close"].shift(-2) / d["close"] - 1 - m2
            d["coin"] = coin
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A = A[A["rise"] > 0]
    out = {}
    for hr in [15, 20, 23]:
        g = A[A["hour"] == hr]
        t = []
        for k, gg in g.groupby("year"):
            tt, n = _t(gg["rise"].values, gg["ex2"].values)
            t.append({"year": k, "n": n, "t_rise": tt, "mean_bp": gg["ex2"].mean() * 1e4})
        out[f"h{hr}_by_year"] = pd.DataFrame(t)
    g = A[A["hour"] == 15]
    t = []
    for k, gg in g.groupby("coin"):
        tt, n = _t(gg["rise"].values, gg["ex2"].values)
        t.append({"coin": k, "n": n, "t_rise": tt, "mean_bp": gg["ex2"].mean() * 1e4})
    out["h15_by_coin"] = pd.DataFrame(t)
    t = []
    for k, gg in g.groupby(g["wd"] >= 5):
        tt, n = _t(gg["rise"].values, gg["ex2"].values)
        t.append({"weekend": k, "n": n, "t_rise": tt, "mean_bp": gg["ex2"].mean() * 1e4})
    out["h15_weekend"] = pd.DataFrame(t)
    sett = A[A["hour"].isin([23, 7, 15])]
    non = A[~A["hour"].isin([23, 7, 15, 0, 8, 16])]
    out["settle_vs_other"] = pd.DataFrame([
        {"grp": "settle", "t_rise": _t(sett["rise"].values, sett["ex2"].values)[0], "mean_bp": sett["ex2"].mean() * 1e4, "n": len(sett)},
        {"grp": "other", "t_rise": _t(non["rise"].values, non["ex2"].values)[0], "mean_bp": non["ex2"].mean() * 1e4, "n": len(non)}])
    return out
