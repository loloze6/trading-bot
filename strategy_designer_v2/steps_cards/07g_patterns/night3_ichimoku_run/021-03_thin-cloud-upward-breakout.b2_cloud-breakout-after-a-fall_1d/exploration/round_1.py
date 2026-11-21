def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 5, 10, 26]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c, hi, lo = d["close"].astype(float), d["high"].astype(float), d["low"].astype(float)
            n = len(d)
            f = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n)})
            lr = np.log(c).diff()
            f["vol20"] = lr.rolling(20).std()
            f["r1"] = c.pct_change(1)
            f["r5"] = c.pct_change(5)
            f["r26"] = c.pct_change(26)
            mid9 = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
            mid26 = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            mid52 = (hi.rolling(52).max() + lo.rolling(52).min()) / 2
            f["kijun_dist"] = (c / mid26 - 1) / (f["vol20"] * np.sqrt(26))
            f["tk"] = (mid9 / mid26 - 1) / (f["vol20"] * np.sqrt(26))
            rng26 = hi.rolling(26).max() - lo.rolling(26).min()
            f["pos26"] = (c - lo.rolling(26).min()) / rng26
            f["mid52_dist"] = (c / mid52 - 1) / (f["vol20"] * np.sqrt(52))
            spanA = ((mid9 + mid26) / 2).shift(26)
            spanB = mid52.shift(26)
            top = np.maximum(spanA, spanB); bot = np.minimum(spanA, spanB)
            f["cloud_dist"] = np.where(c > top, c / top - 1, np.where(c < bot, c / bot - 1, 0.0)) / (f["vol20"] * np.sqrt(26))
            f.loc[top.isna(), "cloud_dist"] = np.nan
            f["cloud_thick"] = (top - bot) / c / (f["vol20"] * np.sqrt(26))
            f["volz"] = f["vol20"] / lr.rolling(60, min_periods=40).std()
            f["wd"] = pd.to_datetime(d["timestamp"]).dt.weekday
            for h in H:
                f[f"fwd{h}"] = c.shift(-h) / c - 1
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    # per coin drift and usual move, non-overlapping grid
    out = {}
    feats = ["r1", "r5", "r26", "kijun_dist", "tk", "pos26", "mid52_dist", "cloud_dist", "cloud_thick", "vol20", "volz"]
    res = []
    for h in H:
        g = A[A["pos"] % h == 0].copy()
        st = g.groupby("coin")[f"fwd{h}"].agg(["mean", "std"])
        g["u"] = (g[f"fwd{h}"] - g["coin"].map(st["mean"])) / g["coin"].map(st["std"])
        for ft in feats:
            s = g[[ft, "u", "coin"]].dropna()
            if len(s) < 30: continue
            s["q"] = s.groupby("coin")[ft].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
            top = s[s.q == 2]["u"]; bot = s[s.q == 0]["u"]
            rho, p = stats.spearmanr(s[ft], s["u"])
            t = stats.ttest_ind(top, bot, equal_var=False).statistic
            # coins agreeing in sign
            sg = s.groupby("coin").apply(lambda x: np.sign(stats.spearmanr(x[ft], x["u"])[0]) if len(x) > 5 else 0).sum()
            res.append(dict(h=h, feat=ft, n=len(s), rho=round(rho, 3), top_minus_bot=round(top.mean() - bot.mean(), 3), t=round(t, 2), coin_sign_sum=sg))
    out["feature_grid"] = pd.DataFrame(res)
    # weekday daily returns
    g = A[A["pos"] % 1 == 0].dropna(subset=["fwd1"])
    st = g.groupby("coin")["fwd1"].agg(["mean", "std"])
    g = g.assign(u=(g["fwd1"] - g["coin"].map(st["mean"])) / g["coin"].map(st["std"]))
    wd = g.groupby("wd")["u"].agg(["mean", "count", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["weekday_next_day"] = wd.round(3)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    if tr:
        T = pd.concat(tr)
        out["trades"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"), days=("duration_minutes", lambda x: x.mean() / 1440)).round(3)
    out["bars_per_window"] = A.groupby(["coin"])["pos"].max().describe().round(1)
    return out
