import numpy as np, pandas as pd

def _ct(dev, days):
    d = pd.DataFrame({"v": dev.values, "d": days.values}).dropna()
    N = len(d)
    if N < 5: return (np.nan, np.nan, N, 0)
    m = d.v.mean()
    g = d.groupby("d").v.agg(["sum", "count"])
    G = len(g)
    r = g["sum"] - m * g["count"]
    se = np.sqrt(G / (G - 1) * (r ** 2).sum()) / N if G > 1 else np.nan
    return (m, m / se if se else np.nan, N, G)

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        parts = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            up = (r1 > 0).astype(int); dn = (r1 < 0).astype(int)
            us = up.groupby((up != up.shift()).cumsum()).cumsum() * up
            ds = dn.groupby((dn != dn.shift()).cumsum()).cumsum() * dn
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "streak": us - ds,
                "ret30": c / c.shift(30) - 1,
                "ret5": c / c.shift(5) - 1,
                "ret1": r1,
                "vol20": np.log(c).diff().rolling(20).std(),
                "fwd5": c.shift(-5) / c - 1,
                "alloc": b["postRebalance_current_allocation"],
                "fc": b["forecast"],
            })
            df["vol20rel"] = df["vol20"] / np.log(c).diff().rolling(90, min_periods=60).std()
            df["pos"] = np.arange(len(df))
            df = df[df.pos % 5 == 0]
            parts.append(df)
        cd = pd.concat(parts)
        drift = cd["fwd5"].mean(); usual = cd["fwd5"].std()
        cd["dev"] = cd["fwd5"] - drift
        cd["str"] = cd["dev"] / usual
        rows.append(cd)
    A = pd.concat(rows).dropna(subset=["fwd5"])
    A["wd"] = A["day"].dt.weekday

    def tab(key):
        out = []
        for k, g in A.groupby(key):
            m, t, n, G = _ct(g["dev"], g["day"])
            out.append({"grp": str(k), "mean_dev": round(m, 4), "t": round(t, 2), "n": n, "days": G,
                        "strength": round(g["str"].mean(), 3)})
        return pd.DataFrame(out)

    A["streak_b"] = A["streak"].clip(-5, 5)
    A["r30s"] = np.sign(A["ret30"])
    A["streak_x_r30"] = A["streak_b"].astype(str) + "|" + A["r30s"].astype(str)
    # per-coin quintiles
    for col in ["ret30", "ret5", "ret1", "vol20rel"]:
        A[col + "_q"] = A.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    A["ret5_q_x_r30"] = A["ret5_q"].astype(str) + "|" + A["r30s"].astype(str)
    A["vol_x_r30"] = A["vol20rel_q"].astype(str) + "|" + A["r30s"].astype(str)
    res = {
        "streak": tab("streak_b"),
        "streak_x_r30sign": tab("streak_x_r30"),
        "ret30_quint": tab("ret30_q"),
        "ret5_quint": tab("ret5_q"),
        "ret1_quint": tab("ret1_q"),
        "volrel_quint": tab("vol20rel_q"),
        "ret5q_x_r30": tab("ret5_q_x_r30"),
        "volq_x_r30": tab("vol_x_r30"),
        "weekday": tab("wd"),
    }
    # book: daily pooled
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d.copy(); x["coin"] = coin; x["win"] = w; dl.append(x)
    D = pd.concat(dl)
    bk = D.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    bk["yr"] = pd.to_datetime(bk.index).year
    res["book_by_year"] = bk.groupby("yr").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"),
                                               n=("book_return", "size"), book_std=("book_return", "std"))
    return res
