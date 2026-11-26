import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            d = pd.DataFrame({"ts": pd.to_datetime(b["timestamp"])})
            d["coin"] = coin; d["w"] = w
            d["r1"] = c.pct_change()
            rr = (h - l) / c
            d["mrr"] = rr.rolling(30, min_periods=20).mean()
            d["sc"] = d["r1"] / d["mrr"]
            d["rng_sc"] = rr / d["mrr"]
            d["clv"] = ((c - l) / (h - l)).where(h > l)
            d["f1"] = c.shift(-1) / c - 1
            d["f3"] = c.shift(-3) / c - 1
            d["r60"] = c / c.shift(60) - 1
            d["r5"] = c / c.shift(5) - 1
            dn = (d["r1"] < 0).astype(int)
            d["streak"] = dn.groupby((dn != dn.shift()).cumsum()).cumsum() * dn
            d["pos"] = np.arange(len(d))
            d["alloc"] = b["postRebalance_current_allocation"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["r1"].mean()
    D["x1"] = D["f1"] - D["coin"].map(mu)
    D["x3"] = D["f3"] - 3 * D["coin"].map(mu)
    D["day"] = D["ts"].dt.floor("D")
    D["wd"] = D["ts"].dt.dayofweek
    D["vol_hi"] = D.groupby("coin")["mrr"].transform(lambda s: s > s.median())
    D["trend"] = pd.cut(D["r60"], [-np.inf, -0.1, 0.1, np.inf], labels=["fall", "chop", "rise"])

    def summ(df, col="x1", by=None):
        out = {}
        for k, g in df.groupby(by, observed=True):
            g = g.dropna(subset=[col])
            if len(g) < 20:
                continue
            m = g[col].mean()
            s = (g[col] - m).groupby(g["day"]).sum()
            se = np.sqrt((s ** 2).sum()) / len(g)
            out[k] = {"n": len(g), "days": g["day"].nunique(), "mean%": 100 * m, "t_day": m / se if se > 0 else np.nan}
        return pd.DataFrame(out).T

    res = {}
    A = D.dropna(subset=["sc", "x1"]).copy()
    A["scq"] = pd.qcut(A["sc"], 10, labels=False)
    res["all_days_by_scaled_ret_decile"] = summ(A, by="scq")
    Dn = A[A["r1"] < 0].copy()
    Dn["fq"] = pd.qcut(-Dn["sc"], 5, labels=False)
    Dn["clvq"] = pd.qcut(Dn["clv"], 5, labels=False, duplicates="drop")
    res["down_fallq_x_clvq_mean%"] = Dn.groupby(["fq", "clvq"])["x1"].mean().unstack() * 100
    res["down_by_clvq"] = summ(Dn, by="clvq")
    top = Dn[Dn["fq"] == 4]
    res["topfall_by_trend"] = summ(top, by="trend")
    res["topfall_by_volhi"] = summ(top, by="vol_hi")
    res["down_by_streak"] = summ(Dn.assign(st=Dn["streak"].clip(upper=4)), by="st")
    res["all_by_weekday"] = summ(A, by="wd")
    res["topfall_by_weekday"] = summ(top, by="wd")
    res["topfall_x3_grid"] = summ(top[top["pos"] % 3 == 0], col="x3", by="fq")
    Dn["r5q"] = pd.qcut(Dn["r5"], 5, labels=False)
    res["down_by_5d_ret_q"] = summ(Dn, by="r5q")
    A["rngq"] = pd.qcut(A["rng_sc"], 5, labels=False)
    res["all_by_range_scaled_q_and_sign"] = A.groupby(["rngq", A["r1"] < 0])["x1"].mean().unstack() * 100
    res["by_coin_topfall"] = summ(top, by="coin")
    # book
    bd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; bd.append(t)
    B = pd.concat(bd, ignore_index=True)
    B["day"] = pd.to_datetime(B["day"])
    bk = B.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    bk["wd"] = bk.index.dayofweek
    res["book_by_weekday_mean%"] = bk.groupby("wd")[["book_return", "coin_return"]].mean() * 100
    q = bk["book_return"].quantile([0.02, 0.98])
    res["book_extreme_days_coin_ret%"] = pd.DataFrame({
        "worst2%": bk[bk["book_return"] <= q.iloc[0]]["coin_return"].describe() * 100,
        "best2%": bk[bk["book_return"] >= q.iloc[1]]["coin_return"].describe() * 100})
    res["book_by_year_mean%"] = bk.groupby(bk.index.year)[["book_return", "coin_return"]].mean() * 100
    return res
