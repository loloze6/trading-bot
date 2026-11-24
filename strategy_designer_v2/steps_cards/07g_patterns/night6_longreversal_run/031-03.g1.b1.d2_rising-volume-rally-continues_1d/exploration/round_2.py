import pandas as pd, numpy as np
from scipy import stats

H = 14

def build(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "pos": np.arange(len(b)),
                "ret14": c / c.shift(14) - 1,
                "vr": v.rolling(14).mean() / v.rolling(30).mean() - 1,
                "vr7": v.rolling(7).mean() / v.rolling(30).mean() - 1,
                "vr60": v.rolling(14).mean() / v.rolling(60).mean() - 1,
                "vol30": r1.rolling(30).std(),
                "fwd": c.shift(-H) / c - 1,
                "fwd7": c.shift(-7) / c - 1,
            }))
    return pd.concat(rows, ignore_index=True)

def ct(x, day):
    d = pd.DataFrame({"x": x.values, "d": day.values}).dropna()
    n = len(d)
    if n < 5: return np.nan, n, 0
    m = d["x"].mean()
    s = (d["x"] - m).groupby(d["d"]).sum()
    se = np.sqrt((s**2).sum()) / n
    return m / se if se > 0 else np.nan, n, d["d"].nunique()

def table(g, col, q=5, ex="ex"):
    g = g.dropna(subset=[col, ex]).copy()
    g["bin"] = pd.qcut(g[col], q, labels=False, duplicates="drop")
    out = []
    for k, s in g.groupby("bin"):
        t, n, nd = ct(s[ex], s["day"])
        out.append({"bin": k, "lo": s[col].min(), "hi": s[col].max(), "mean_ex": s[ex].mean(), "mean_tot": s["fwd"].mean() if ex=="ex" else np.nan, "t": t, "n": n, "days": nd})
    return pd.DataFrame(out)

def slope_t(g, col, ex="ex"):
    g = g.dropna(subset=[col, ex]).copy()
    z = (g[col].rank(pct=True) - 0.5)
    prod = z * (g[ex] - g[ex].mean()) / (z**2).mean()
    t, n, nd = ct(prod, g["day"])
    return pd.Series({"slope_per_rank": prod.mean(), "t": t, "n": n, "days": nd})

def explore(data):
    df = build(data)
    df["day"] = df["ts"].dt.floor("D"); df["yr"] = df["ts"].dt.year
    grid = df[(df["pos"] % H == 0) & df["fwd"].notna()].copy()
    grid["ex"] = grid["fwd"] - grid["coin"].map(grid.groupby("coin")["fwd"].mean())
    res = {}
    res["all_vr"] = table(grid, "vr", 5)
    res["slopes"] = pd.DataFrame({
        "vr_all": slope_t(grid, "vr"), "vr_up": slope_t(grid[grid.ret14 > 0], "vr"),
        "vr_down": slope_t(grid[grid.ret14 <= 0], "vr"),
        "vr7_all": slope_t(grid, "vr7"), "vr60_all": slope_t(grid, "vr60"),
        "vol30_all": slope_t(grid, "vol30")})
    # vr low quintile by year
    q20 = grid["vr"].quantile(0.2)
    g = grid.dropna(subset=["vr"])
    out = []
    for y, s in g.groupby("yr"):
        lo = s[s.vr <= q20]; hi = s[s.vr > q20]
        t, n, nd = ct(lo["ex"], lo["day"])
        out.append({"yr": y, "low_vr_ex": lo["ex"].mean(), "t": t, "n": n, "rest_ex": hi["ex"].mean()})
    res["low_vr_by_year"] = pd.DataFrame(out)
    # per coin sign of low quintile
    pc = g.assign(low=g.vr <= q20).groupby(["coin", "low"])["ex"].mean().unstack()
    res["coins_low_minus_rest_neg_share"] = float(((pc[True] - pc[False]) < 0).mean())
    res["coins_n"] = float(len(pc))
    # vr controlling vol30: within vol30 terciles
    g2 = g.dropna(subset=["vol30"]).copy()
    g2["vt"] = pd.qcut(g2["vol30"], 3, labels=False)
    res["vr_slope_within_vol_tercile"] = pd.DataFrame({k: slope_t(s, "vr") for k, s in g2.groupby("vt")})
    res["corr_vr_vol30"] = float(g2[["vr", "vol30"]].corr(method="spearman").iloc[0, 1])
    # 7-day horizon grid
    g7 = df[(df["pos"] % 7 == 0) & df["fwd7"].notna()].copy()
    g7["ex7"] = g7["fwd7"] - g7["coin"].map(g7.groupby("coin")["fwd7"].mean())
    res["vr_7d_horizon"] = slope_t(g7, "vr", "ex7")
    res["coin_usual_move14_mean_sd"] = float(grid.groupby("coin")["fwd"].std().mean())
    return res
