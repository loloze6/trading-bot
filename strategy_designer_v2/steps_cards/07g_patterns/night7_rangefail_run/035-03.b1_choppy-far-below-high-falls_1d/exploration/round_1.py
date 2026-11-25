import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            hi20 = c.shift(1).rolling(20).max()
            depth = (c / hi20 - 1) / sd20
            tr60 = (c / c.shift(60) - 1) * 100
            r5past = c / c.shift(5) - 1
            r1z = r1 / sd20
            vol_rel = sd20 / r1.rolling(60).std()
            fwd = c.shift(-H) / c - 1
            # range position over 20 days
            lo20 = c.shift(1).rolling(20).min()
            rngpos = (c - lo20) / (hi20 - lo20)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "depth": depth, "tr60": tr60, "r5past": r5past,
                               "r1z": r1z, "vol_rel": vol_rel, "fwd": fwd, "rngpos": rngpos,
                               "wd": ts.dt.weekday, "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                               "pos": np.arange(len(b))})
            df = df[df["pos"] % H == 0]
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["fwd", "depth"])
    drift = d.groupby("coin")["fwd"].mean()
    usual = d.groupby("coin")["fwd"].std()
    d["ex"] = d["fwd"] - d["coin"].map(drift)
    d["z"] = d["ex"] / d["coin"].map(usual)
    d["trend"] = pd.cut(d["tr60"], [-1e9, -10, 10, 1e9], labels=["fall", "chop", "rise"])
    d["dq"] = pd.cut(d["depth"], [-100, -4, -3, -2, -1, -0.3, 0.01, 100])
    def agg(g):
        x = g["ex"]
        return pd.Series({"n": len(x), "mean_ex%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "strength": g["z"].mean()})
    out = {}
    out["by_depth_all"] = d.groupby("dq").apply(agg)
    out["by_depth_trend"] = d.dropna(subset=["trend"]).groupby(["trend", "dq"]).apply(agg)
    d["r1q"] = pd.qcut(d["r1z"], 5)
    out["by_last_day_z"] = d.groupby("r1q").apply(agg)
    d["p5q"] = pd.qcut(d["r5past"], 5)
    out["by_past5"] = d.groupby("p5q").apply(agg)
    d["vq"] = pd.qcut(d["vol_rel"], 4)
    out["by_volrel"] = d.groupby("vq").apply(agg)
    out["by_weekday"] = d.groupby("wd").apply(agg)
    d["rp"] = pd.cut(d["rngpos"], [-1, 0, 0.2, 0.5, 0.8, 1, 10])
    out["by_rangepos"] = d.groupby("rp").apply(agg)
    # spearman correlations
    cc = {}
    for nm in ["depth", "r1z", "r5past", "vol_rel", "rngpos"]:
        s = d[[nm, "z"]].dropna()
        rho, p = stats.spearmanr(s[nm], s["z"])
        cc[nm] = rho
    out["spearman_vs_z"] = pd.Series(cc)
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, w=w))
    D = pd.concat(dd)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    book = D.groupby(["w", "day"])["book_return"].mean().dropna()
    out["book_by_window_%"] = book.groupby(level=0).agg(["count", "mean", "sum"]) * [1, 100, 100]
    return out
