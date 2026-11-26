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
            lo20 = c.shift(1).rolling(20).min()
            depth = (c / hi20 - 1) / sd20
            above = (c / hi20 - 1) / sd20
            tr60 = (c / c.shift(60) - 1) * 100
            fwd = c.shift(-H) / c - 1
            rngpos = (c - lo20) / (hi20 - lo20)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "day": ts.dt.floor("D"), "depth": depth, "tr60": tr60,
                               "fwd": fwd, "rngpos": rngpos, "wd": ts.dt.weekday, "pos": np.arange(len(b))})
            df = df[df["pos"] % H == 0]
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["fwd", "depth"])
    drift = d.groupby("coin")["fwd"].mean()
    usual = d.groupby("coin")["fwd"].std()
    d["ex"] = d["fwd"] - d["coin"].map(drift)
    d["z"] = d["ex"] / d["coin"].map(usual)
    d["half"] = np.where(d["w"].str[1:].astype(int) <= 12, "w7-12", "w13-18")
    d["trend"] = pd.cut(d["tr60"], [-1e9, -10, 10, 1e9], labels=["fall", "chop", "rise"])
    d["dq"] = pd.cut(d["depth"], [-100, -3, -1.5, -0.5, 0.01, 1, 100])

    def ct(g):
        s = g.groupby("day")["ex"].sum()
        cnt = g.groupby("day")["ex"].size()
        D = len(s)
        if D < 3:
            return np.nan
        m = g["ex"].mean(); n = len(g)
        dev = (g["ex"] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / n
        return m / se
    def agg(g):
        x = g["ex"]
        return pd.Series({"n": len(x), "days": g["day"].nunique(), "mean_ex%": 100 * x.mean(),
                          "median_ex%": 100 * x.median(), "t_day": ct(g), "strength": g["z"].mean(),
                          "hit_up": (x > 0).mean()})
    out = {}
    out["depth_clustered"] = d.groupby("dq").apply(agg)
    out["depth_by_half"] = d.groupby(["half", "dq"]).apply(agg)
    out["depth_by_trend_coarse"] = d.dropna(subset=["trend"]).assign(
        side=lambda x: pd.cut(x["depth"], [-100, -1.5, 0.01, 100], labels=["deep", "mid", "at/above"])
    ).groupby(["trend", "side"]).apply(agg)
    out["weekday_clustered"] = d.groupby("wd").apply(agg)
    out["weekday_by_half"] = d.groupby(["half", "wd"]).apply(agg)[["n", "mean_ex%", "t_day"]]
    # graded slope: regression of z on depth (clipped), day-clustered via day means
    dc = d.copy(); dc["dcl"] = dc["depth"].clip(-6, 4)
    sl = {}
    for nm, g in [("all", dc)] + [(h, x) for h, x in dc.groupby("half")] + [(str(t), x) for t, x in dc.dropna(subset=["trend"]).groupby("trend")]:
        sp = stats.spearmanr(g["dcl"], g["z"])
        X = g["dcl"] - g["dcl"].mean()
        b = (X * g["z"]).sum() / (X ** 2).sum()
        res = g["z"] - g["z"].mean() - b * X
        sc = (X * res).groupby(g["day"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (X ** 2).sum()
        sl[nm] = pd.Series({"n": len(g), "spearman": sp[0], "slope_z_per_swing": b, "t_day": b / se})
    out["slope_depth"] = pd.DataFrame(sl).T
    # per coin slope sign
    pc = {}
    for coin, g in dc.groupby("coin"):
        if len(g) > 30:
            pc[coin] = stats.spearmanr(g["dcl"], g["z"])[0]
    out["per_coin_spearman"] = pd.Series(pc)
    # book around largest gain/loss days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, w=w))
    D = pd.concat(dd)
    book = D.groupby(["w", "day"])["book_return"].mean().dropna()
    q = book.quantile([0.01, 0.05, 0.5, 0.95, 0.99])
    out["book_quantiles_%"] = q * 100
    out["book_top10_share_of_sum"] = float(book.nlargest(10).sum() / book.sum()) if book.sum() != 0 else np.nan
    out["book_bottom10_sum_%"] = float(book.nsmallest(10).sum() * 100)
    out["book_top10_sum_%"] = float(book.nlargest(10).sum() * 100)
    return out
