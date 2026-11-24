import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            lr = np.log(c).diff()
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            r5 = c / c.shift(5) - 1
            vol = lr.rolling(30).std()
            fwd = c.shift(-H) / c - 1
            n = len(c)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                rows.append(dict(coin=coin, w=w, day=ts[i].normalize(), year=ts[i].year,
                                 wd=ts[i].weekday(), r20=r20[i], r60=r60[i], r5=r5[i],
                                 vol=vol[i], fwd=fwd[i], fc=b["forecast"].iloc[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby("coin")["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    d = d.dropna(subset=["r20", "r60", "vol", "ex"])
    d["z20"] = d["r20"] / (d["vol"] * np.sqrt(20))
    d["z60"] = d["r60"] / (d["vol"] * np.sqrt(60))
    d["aligned"] = np.sign(d["r20"]) == np.sign(d["r60"])

    def ct(x, day):
        x = pd.Series(x.values); day = pd.Series(day.values)
        m = x.mean(); s = (x - m).groupby(day).sum()
        se = np.sqrt((s ** 2).sum()) / len(x)
        return pd.Series(dict(mean=m, t=m / se if se > 0 else np.nan, n=len(x), days=day.nunique()))

    out = {}
    d["dir20"] = np.sign(d["r20"]) * d["ex"]
    d["dir60"] = np.sign(d["r60"]) * d["ex"]
    out["aligned_vs_opposed_dir20"] = d.groupby("aligned").apply(lambda g: ct(g["dir20"], g["day"]))
    out["opposed_dir60"] = ct(d.loc[~d.aligned, "dir60"], d.loc[~d.aligned, "day"])
    d["q20"] = pd.qcut(d["z20"], 6, labels=False)
    out["z20_sextile_raw_ex"] = d.groupby("q20").apply(lambda g: pd.concat([ct(g["ex"], g["day"]), pd.Series({"z20": g["z20"].mean()})]))
    d["q60"] = pd.qcut(d["z60"], 6, labels=False)
    out["z60_sextile_raw_ex"] = d.groupby("q60").apply(lambda g: pd.concat([ct(g["ex"], g["day"]), pd.Series({"z60": g["z60"].mean()})]))
    a = d[d.aligned].copy()
    a["side"] = np.where(a["r20"] > 0, "up", "down")
    out["aligned_by_side"] = a.groupby("side").apply(lambda g: ct(g["dir20"], g["day"]))
    a["volq"] = a.groupby("coin")["vol"].transform(lambda v: pd.qcut(v.rank(method="first"), 3, labels=False))
    out["aligned_by_volterc"] = a.groupby("volq").apply(lambda g: ct(g["dir20"], g["day"]))
    out["aligned_by_year"] = a.groupby("year").apply(lambda g: ct(g["dir20"], g["day"]))
    d["r5dir"] = np.sign(d["r5"]) * np.sign(d["r20"])
    out["aligned_by_r5_agree"] = d[d.aligned].groupby(d.loc[d.aligned, "r5dir"]).apply(lambda g: ct(g["dir20"], g["day"]))
    d["q5"] = pd.qcut(d["r5"] / (d["vol"] * np.sqrt(5)), 6, labels=False)
    out["z5_sextile_raw_ex"] = d.groupby("q5").apply(lambda g: ct(g["ex"], g["day"]))
    # book: daily returns, biggest days
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; dd.append(t)
    dd = pd.concat(dd)
    bk = dd.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    bk["wd"] = pd.to_datetime(bk.index).weekday
    out["book_by_weekday"] = bk.groupby("wd")[["book_return", "coin_return"]].agg(["mean", "count"])
    q = bk["book_return"].quantile([0.02, 0.98])
    out["book_extremes_coin_ret"] = pd.DataFrame({
        "worst2pct": bk.loc[bk.book_return <= q.iloc[0], ["book_return", "coin_return"]].mean(),
        "best2pct": bk.loc[bk.book_return >= q.iloc[1], ["book_return", "coin_return"]].mean()})
    out["corr_book_coin_daily"] = float(bk["book_return"].corr(bk["coin_return"]))
    return out
