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
            f = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "pos": np.arange(len(b)),
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "ret14": c / c.shift(14) - 1,
                "ret60": c / c.shift(60) - 1,
                "ret3": c / c.shift(3) - 1,
                "ret1": r1,
                "vr": v.rolling(14).mean() / v.rolling(30).mean() - 1,
                "vr3": v.rolling(3).mean() / v.rolling(30).mean() - 1,
                "vol30": r1.rolling(30).std(),
                "fwd": c.shift(-H) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
            })
            rows.append(f)
    df = pd.concat(rows, ignore_index=True)
    return df

def ct(x, day):
    d = pd.DataFrame({"x": x.values, "d": day.values}).dropna()
    n = len(d)
    if n < 5: return np.nan, n, 0
    m = d["x"].mean()
    s = (d["x"] - m).groupby(d["d"]).sum()
    se = np.sqrt((s**2).sum()) / n
    return m / se if se > 0 else np.nan, n, d["d"].nunique()

def table(g, col, q=5):
    g = g.dropna(subset=[col, "ex"]).copy()
    g["bin"] = pd.qcut(g[col], q, labels=False, duplicates="drop")
    out = []
    for k, s in g.groupby("bin"):
        t, n, nd = ct(s["ex"], s["day"])
        out.append({"bin": k, "lo": s[col].min(), "hi": s[col].max(), "mean_ex": s["ex"].mean(), "t": t, "n": n, "days": nd})
    return pd.DataFrame(out)

def explore(data):
    df = build(data)
    df["day"] = df["ts"].dt.floor("D")
    grid = df[(df["pos"] % H == 0) & df["fwd"].notna()].copy()
    drift = grid.groupby("coin")["fwd"].mean()
    grid["ex"] = grid["fwd"] - grid["coin"].map(drift)
    grid["vol_n_ex"] = grid["ex"]
    res = {}
    up = grid[grid["ret14"] > 0]; dn = grid[grid["ret14"] <= 0]
    res["fc_bins_active"] = table(grid[grid["fc"] > 0], "fc", 4)
    res["up_vr"] = table(up, "vr", 5)
    res["down_vr"] = table(dn, "vr", 5)
    res["all_ret14"] = table(grid, "ret14", 5)
    res["all_ret60"] = table(grid, "ret60", 5)
    res["all_vol30"] = table(grid, "vol30", 5)
    res["all_vr3"] = table(grid, "vr3", 5)
    # daily: next-day return after large daily moves, standardized
    d = df.dropna(subset=["ret1", "fwd1", "vol30"]).copy()
    d["z1"] = d["ret1"] / d["vol30"]
    d["ex"] = d["fwd1"] - d["coin"].map(d.groupby("coin")["fwd1"].mean())
    res["daily_z1"] = table(d, "z1", 5)
    d["wd"] = d["ts"].dt.weekday
    wd = []
    for k, s in d.groupby("wd"):
        t, n, nd = ct(s["ex"], s["day"]); wd.append({"wd": k, "mean": s["ex"].mean(), "t": t, "n": n})
    res["weekday_next"] = pd.DataFrame(wd)
    # book by year and pos
    days = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; days.append(x)
    D = pd.concat(days); D["day"] = pd.to_datetime(D["day"])
    bk = D.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    bk["yr"] = bk.index.year
    res["book_by_year"] = bk.groupby("yr").agg(book=("book_return", "mean"), hold=("coin_return", "mean"), n=("book_return", "size"))
    # before/after book's largest gains and losses
    bk = bk.sort_index()
    bk["prev"] = bk["coin_return"].shift(1); bk["next"] = bk["book_return"].shift(-1)
    q = bk["book_return"].quantile([0.05, 0.95])
    res["extremes"] = pd.DataFrame({
        "worst5%": bk[bk["book_return"] <= q[0.05]][["book_return", "coin_return", "prev", "next"]].mean(),
        "best5%": bk[bk["book_return"] >= q[0.95]][["book_return", "coin_return", "prev", "next"]].mean()})
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; tr.append(x)
    T = pd.concat(tr)
    T["days"] = T["duration_minutes"] / 1440
    T["dbin"] = pd.qcut(T["days"], 4, duplicates="drop")
    res["trades_by_duration"] = T.groupby("dbin", observed=True)["net_profit_loss_percent"].agg(["mean", "median", "count"])
    res["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count"])
    return res
