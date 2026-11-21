def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    # 1) daily returns by weekday (each bar's next-day return, non-overlapping by construction)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            ts = pd.to_datetime(df["timestamp"])
            for i in range(len(c) - 1):
                rows.append(dict(coin=coin, wnum=int(w[1:]), yr=ts.iloc[i].year,
                                 wd=(ts.iloc[i] + pd.Timedelta(days=1)).weekday(),
                                 r=c[i+1]/c[i]-1))
    d = pd.DataFrame(rows)
    d["ex"] = d["r"] - d.groupby("coin")["r"].transform("mean")
    def tt(s):
        return s.mean()/s.std()*np.sqrt(len(s)) if len(s) > 2 else np.nan
    out["next-day excess return pct by weekday of the day earned"] = d.groupby("wd")["ex"].agg(
        n="count", mean_pct=lambda s: s.mean()*100, t=tt)
    out["t by weekday x coin"] = d.groupby(["coin","wd"])["ex"].apply(tt).unstack()
    d["half"] = np.where(d["wnum"] <= 12, "w1-w12", "w13-w24")
    out["mean pct by weekday x half"] = d.groupby(["half","wd"])["ex"].mean().unstack()*100
    out["t by weekday x half"] = d.groupby(["half","wd"])["ex"].apply(tt).unstack()
    # weekend vs weekday: days 5,6 (Sat, Sun) minus Mon-Fri, Welch
    we = d[d.wd >= 5]["ex"]; wk = d[d.wd < 5]["ex"]
    out["weekend minus weekdays (pct, welch t)"] = pd.Series(dict(
        diff_pct=(we.mean()-wk.mean())*100, t=stats.ttest_ind(we, wk, equal_var=False).statistic,
        n_we=len(we), n_wk=len(wk)))
    out["t by weekday x year"] = d.groupby(["yr","wd"])["ex"].apply(tt).unstack()

    # 2) 5-day grid: volume surprise and nearness, size in percent, by window halves
    g = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            n = len(c)
            vol = df["volume"].astype(float)
            volz = np.log(vol / vol.rolling(60, min_periods=20).mean())
            hi = df["high"].astype(float).rolling(30, min_periods=10).max()
            lo = df["low"].astype(float).rolling(30, min_periods=10).min()
            near = (c - lo) / (hi - lo)
            r1 = c.pct_change()
            for i in range(0, n - 5, 5):
                g.append(dict(coin=coin, wnum=int(w[1:]), fwd=c[i+5]/c[i]-1,
                              volz=volz.iloc[i], near=near.iloc[i], r1=r1.iloc[i]))
    g = pd.DataFrame(g).replace([np.inf, -np.inf], np.nan)
    g["exr"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["half"] = np.where(g["wnum"] <= 12, "w1-w12", "w13-w24")
    res = {}
    for k in ["volz", "near"]:
        s = g.dropna(subset=[k])
        q = s.groupby("coin")[k].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        res[k + " Q5-Q1 pct"] = (s[q == 4]["exr"].mean() - s[q == 0]["exr"].mean())*100
        res[k + " Q5-Q1 t"] = stats.ttest_ind(s[q == 4]["exr"], s[q == 0]["exr"], equal_var=False).statistic
        for h in ["w1-w12", "w13-w24"]:
            sh = s[s.half == h]
            x = sh.groupby("coin")[k].transform(lambda v: (v - v.mean())/v.std())
            r = stats.linregress(x, sh["exr"])
            res[f"{k} slope t {h}"] = r.slope/r.stderr
    out["volz and near: spread and halves"] = pd.Series(res)
    # volume surprise interacting with day sign: signed continuation
    s = g.dropna(subset=["volz", "r1"]).copy()
    s["sx"] = np.sign(s["r1"]) * s["exr"]
    q = s.groupby("coin")["volz"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["signed 5d continuation of last day pct by volume-surprise quintile"] = s.groupby(q)["sx"].agg(
        n="count", mean_pct=lambda v: v.mean()*100, t=tt)

    # 3) book: days around largest book losses/gains
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df[["book_return", "coin_return"]].copy()
            x["coin"] = coin; x["w"] = w
            dd.append(x.reset_index(drop=True))
    dd = pd.concat(dd)
    bk = dd.groupby(["w", dd.groupby(["w", "coin"]).cumcount()])[["book_return", "coin_return"]].mean().dropna()
    lo_q = bk["book_return"].quantile(0.02); hi_q = bk["book_return"].quantile(0.98)
    out["book worst/best 2% days: mean coin return pct"] = pd.Series(dict(
        worst_book_pct=bk[bk.book_return <= lo_q]["book_return"].mean()*100,
        worst_coin_pct=bk[bk.book_return <= lo_q]["coin_return"].mean()*100,
        best_book_pct=bk[bk.book_return >= hi_q]["book_return"].mean()*100,
        best_coin_pct=bk[bk.book_return >= hi_q]["coin_return"].mean()*100,
        corr_book_coin=bk["book_return"].corr(bk["coin_return"])))
    return out
