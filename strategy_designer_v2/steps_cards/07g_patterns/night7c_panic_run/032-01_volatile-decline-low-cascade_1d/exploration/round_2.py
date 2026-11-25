import numpy as np, pandas as pd
from scipy import stats

def day_t(df, col, key="day"):
    s = df.groupby(key)[col].sum()
    cnt = df.groupby(key)[col].size()
    m = df[col].mean()
    # day-clustered t: sum of deviations per day
    dev = (df[col] - m).groupby(df[key]).sum()
    se = np.sqrt((dev ** 2).sum()) / len(df)
    return m, m / se if se > 0 else np.nan, df[key].nunique(), len(df)

def explore(data):
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "year": ts.dt.year, "day": ts.dt.floor("D"),
                "fwd": c.shift(-H) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "r1": c / c.shift(1) - 1,
                "r30": c / c.shift(30) - 1,
                "dhigh": c / hi.shift(1).rolling(30).max() - 1,
                "dhigh_in": c / hi.rolling(30).max() - 1,
                "vol20": c.pct_change().rolling(20).std(),
            })
            df["pos"] = np.arange(len(df))
            rows.append(df)
    A = pd.concat(rows)
    g = A[A["pos"] % H == 0].dropna(subset=["fwd"]).copy()
    drift = g.groupby("coin")["fwd"].mean()
    g["unu"] = g["fwd"] - g["coin"].map(drift)
    res = {}
    # dhigh deciles, pooled per-coin ranks, day-clustered t
    d = g.dropna(subset=["dhigh"]).copy()
    d["b"] = d.groupby("coin")["dhigh"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    out = {}
    for k, x in d.groupby("b"):
        m, t, nd, n = day_t(x, "unu")
        out[k] = {"n": n, "days": nd, "mean_unu": m, "t_day": t, "dhigh": x["dhigh"].mean()}
    res["dhigh_deciles"] = pd.DataFrame(out).T.round(4)
    # top quintile vs rest by window and coin
    d["top"] = d["b"] >= 8
    bw = d.groupby(["win", "top"])["unu"].mean().unstack()
    bw["diff"] = bw[True] - bw[False]
    res["dhigh_top_by_window"] = bw.round(4)
    bc = d.groupby(["coin", "top"])["unu"].mean().unstack()
    bc["diff"] = bc[True] - bc[False]
    res["dhigh_top_by_coin"] = bc.round(4)
    # graded: within dhigh > -5%, rank correlation
    sub = d[d["dhigh"] > -0.05]
    res["spearman_dhigh_gt-5"] = str(stats.spearmanr(sub["dhigh"], sub["unu"]))
    res["spearman_dhigh_all"] = str(stats.spearmanr(d["dhigh"], d["unu"]))
    # next-day after daily move, all bars (1-day horizon non-overlapping), day-clustered
    a = A.dropna(subset=["fwd1", "r1", "vol20"]).copy()
    a["dr"] = a.groupby("coin")["fwd1"].transform("mean")
    a["unu1"] = a["fwd1"] - a["dr"]
    a["z"] = a["r1"] / a["vol20"]
    a["zb"] = pd.cut(a["z"], [-99, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 99])
    o = {}
    for k, x in a.groupby("zb", observed=True):
        m, t, nd, n = day_t(x, "unu1")
        o[str(k)] = {"n": n, "days": nd, "mean": m, "t_day": t}
    res["nextday_by_z"] = pd.DataFrame(o).T.round(5)
    big = a[a["z"] < -1.5]
    res["bigdrop_nextday_by_window"] = big.groupby("win")["unu1"].agg(["size", "mean"]).round(4)
    res["bigdrop_nextday_by_coin"] = big.groupby("coin")["unu1"].agg(["size", "mean"]).round(4)
    # 5-day after big drop (grid)
    g2 = g.dropna(subset=["r1", "vol20"]).copy()
    g2["z"] = g2["r1"] / g2["vol20"]
    g2["zb"] = pd.cut(g2["z"], [-99, -1.5, -0.5, 0.5, 1.5, 99])
    o = {}
    for k, x in g2.groupby("zb", observed=True):
        m, t, nd, n = day_t(x, "unu")
        o[str(k)] = {"n": n, "days": nd, "mean": m, "t_day": t}
    res["5d_after_1d_move"] = pd.DataFrame(o).T.round(4)
    # weekday day-clustered
    a["wd"] = pd.to_datetime(a["day"]).dt.weekday
    o = {}
    for k, x in a.groupby("wd"):
        m, t, nd, n = day_t(x, "unu1")
        o[k] = {"n": n, "days": nd, "mean": m, "t_day": t}
    res["weekday_next_day_clustered"] = pd.DataFrame(o).T.round(5)
    return res
