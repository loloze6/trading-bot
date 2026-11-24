import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 14
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            ma50 = c.rolling(50).mean()
            dist = c / ma50 - 1
            r30 = c / c.shift(30) - 1
            r14 = c / c.shift(14) - 1
            swell = v.rolling(14).mean() / v.rolling(30).mean() - 1
            lr = np.log(c).diff()
            vol30 = lr.rolling(30).std()
            fwd = c.shift(-H) / c - 1
            idx = np.arange(0, len(b), H)
            for i in idx:
                if np.isnan(fwd.iloc[i]): continue
                rows.append(dict(coin=coin, w=w, ts=b["timestamp"].iloc[i], fwd=fwd.iloc[i],
                                 dist=dist.iloc[i], r30=r30.iloc[i], r14=r14.iloc[i], swell=swell.iloc[i],
                                 vol30=vol30.iloc[i], fc=b["forecast"].iloc[i], reg=b["regime"].iloc[i],
                                 year=pd.Timestamp(b["timestamp"].iloc[i]).year))
            r1 = c.pct_change(); nxt = r1.shift(-1)
            z = r1 / r1.rolling(30).std().shift(1)
            daily.append(pd.DataFrame(dict(coin=coin, ts=b["timestamp"], r=r1, nxt=nxt, z=z,
                       wd=pd.to_datetime(b["timestamp"]).dt.weekday, dist=dist)))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["day"] = pd.to_datetime(g["ts"]).dt.floor("D")
    d = pd.concat(daily).dropna(subset=["r", "nxt"])
    d["exn"] = d["nxt"] - d.groupby("coin")["nxt"].transform("mean")
    d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")

    def ct(x, days):
        x = np.asarray(x, float); n = len(x)
        if n < 5: return np.nan
        m = x.mean(); S = pd.Series(x - m).groupby(np.asarray(days)).sum()
        return m * n / np.sqrt((S ** 2).sum())

    def bins(df, col, val="ex", q=5):
        df = df.dropna(subset=[col, val]).copy()
        df["b"] = df.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        out = df.groupby("b").apply(lambda s: pd.Series(dict(n=len(s), mean=s[val].mean(),
                    t=ct(s[val], s["day"]), xmean=s[col].mean())))
        hi, lo = df[df.b == q-1], df[df.b == 0]
        out.loc["hi-lo t", "t"] = stats.ttest_ind(hi[val], lo[val], equal_var=False).statistic
        return out

    res = {}
    res["regime"] = g.groupby("reg").apply(lambda s: pd.Series(dict(n=len(s), mean=s.ex.mean(), t=ct(s.ex, s.day))))
    tr = g[g.reg == "trending"]
    res["trend_fc_bins"] = tr.assign(fb=pd.cut(tr.fc, [-0.1, 0, 0.5, 1, 1.5, 21])).groupby("fb").apply(
        lambda s: pd.Series(dict(n=len(s), mean=s.ex.mean(), t=ct(s.ex, s.day))))
    res["dist_q_all"] = bins(g, "dist")
    res["r30_q_all"] = bins(g, "r30")
    res["r30_q_below"] = bins(g[g.dist < 0], "r30")
    res["r30_q_above"] = bins(g[g.dist > 0], "r30")
    res["swell_q_all"] = bins(g, "swell")
    res["swell_q_below"] = bins(g[g.dist < 0], "swell")
    res["vol30_q_all"] = bins(g, "vol30")
    res["vol30_q_above"] = bins(g[g.dist > 0], "vol30")
    res["year_trend_pos"] = tr[tr.fc > 0].groupby("year").apply(lambda s: pd.Series(dict(n=len(s), mean=s.ex.mean(), t=ct(s.ex, s.day))))
    res["daily_z_bins"] = bins(d.dropna(subset=["z"]), "z", val="exn", q=10)
    res["weekday_next"] = d.groupby((d.wd + 1) % 7).apply(lambda s: pd.Series(dict(n=len(s), mean=s.exn.mean(), t=ct(s.exn, s.day))))
    # book weekday
    bd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            bd.append(x.assign(coin=coin))
    bd = pd.concat(bd).dropna(subset=["book_return"])
    bk = bd.groupby("day")[["book_return", "coin_return"]].mean()
    bk["wd"] = pd.to_datetime(bk.index).weekday
    res["book_weekday"] = bk.groupby("wd").agg(n=("book_return", "size"), mean=("book_return", "mean"), coin=("coin_return", "mean"))
    # trades
    tl = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tl.append(t.assign(coin=coin))
    tl = pd.concat(tl)
    tl["days"] = tl.duration_minutes / 1440
    tl["db"] = pd.cut(tl.days, [0, 14, 15, 30, 60, 1000])
    res["trades_by_dur"] = tl.groupby("db").agg(n=("net_profit_loss_percent", "size"), mean=("net_profit_loss_percent", "mean"), med=("net_profit_loss_percent", "median"))
    return res
