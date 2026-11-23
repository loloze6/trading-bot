def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        drift = {}
        for H in (24, 48, 72):
            g = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - H, H)
                g.append(c[idx + H] / c[idx] - 1)
            drift[H] = np.concatenate(g).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"]
            r1 = c.pct_change()
            vol = r1.rolling(24).std()
            z = r1 / vol
            vlong = r1.rolling(24 * 30).std()
            df = pd.DataFrame({"coin": coin, "w": w, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                               "year": ts.dt.year, "z": z, "vrel": vol / vlong})
            for H in (24, 48, 72):
                df["x%d" % H] = c.shift(-H) / c - 1 - drift[H]
            # 24h move from bar t+24 to t+48 (the day after the tested day)
            df["x24_48"] = c.shift(-48) / c.shift(-24) - 1 - drift[24]
            rows.append(df)
    d = pd.concat(rows)
    d = d[np.isfinite(d.z)].dropna(subset=["z", "x24"])
    d["s"] = -np.sign(d.z)
    out = {}
    h0 = d[d.hour == 0].copy()
    h0["zq"] = pd.cut(h0.z.abs(), [0, 0.5, 1, 1.5, 2, 3, 100])
    def sm(g, col):
        v = (g.s * g[col]).dropna()
        return pd.Series({"n": len(v), "mean_%": 100 * v.mean(), "t": v.mean() / (v.std() / np.sqrt(len(v)))})
    out["hour0_by_absz_24h"] = h0.groupby("zq").apply(lambda g: sm(g, "x24")).round(3)
    out["hour0_by_absz_48h"] = h0.groupby("zq").apply(lambda g: sm(g, "x48")).round(3)
    out["hour0_by_absz_72h"] = h0.groupby("zq").apply(lambda g: sm(g, "x72")).round(3)
    out["hour0_by_absz_day2"] = h0.groupby("zq").apply(lambda g: sm(g, "x24_48")).round(3)
    big = h0[h0.z.abs() >= 1].copy()
    big["wkend"] = np.where(big.wd >= 5, "satsun", "monfri")
    out["hour0_big_weekend"] = big.groupby("wkend").apply(lambda g: sm(g, "x24")).round(3)
    a = (big.s * big.x24)[big.wkend == "satsun"]; bb = (big.s * big.x24)[big.wkend == "monfri"]
    out["weekend_minus_week_welch_t"] = float(stats.ttest_ind(a, bb, equal_var=False).statistic)
    big = big.dropna(subset=["vrel"])
    big["vq"] = pd.qcut(big.vrel, 3, labels=["lowvol", "mid", "highvol"])
    out["hour0_big_vol_x_weekend"] = big.groupby(["vq", "wkend"]).apply(lambda g: sm(g, "x24")).round(3)
    a = (big.s * big.x24)[big.vq == "highvol"]; bb = (big.s * big.x24)[big.vq == "lowvol"]
    out["hour0_highvol_minus_lowvol_welch_t"] = float(stats.ttest_ind(a, bb, equal_var=False).statistic)
    # all hours, high relative vol, graded by |z| at 24h
    al = d.dropna(subset=["vrel"]).copy()
    al = al[al.hour != 0]
    al["vq"] = pd.qcut(al.vrel, 3, labels=["lowvol", "mid", "highvol"])
    al["zq"] = pd.cut(al.z.abs(), [0, 1, 2, 3, 100])
    out["otherhours_vol_by_absz_24h"] = al.groupby(["vq", "zq"]).apply(lambda g: sm(g, "x24")).round(3)
    # book daily returns: by year, and worst-day context
    br = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["day", "book_return", "coin_return"]].copy(); x["w"] = w; br.append(x)
    br = pd.concat(br)
    br["day"] = pd.to_datetime(br["day"])
    bk = br.groupby(["w", "day"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean")).dropna().reset_index()
    bk["year"] = bk.day.dt.year
    out["book_by_year"] = bk.groupby("year").apply(lambda g: pd.Series({
        "days": len(g), "mean_%": 100 * g.book.mean(), "sharpe": g.book.mean() / g.book.std() * np.sqrt(365),
        "corr_coin": g.book.corr(g.coin)})).round(3)
    bk["cq"] = pd.qcut(bk.coin.abs(), 5, labels=["q1small", "q2", "q3", "q4", "q5large"])
    out["book_by_abs_coin_day"] = bk.groupby("cq").book.agg(["count", "mean", "std"]).mul([1, 100, 100]).round(3)
    return out
