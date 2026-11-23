def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 8
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            hi20 = pd.Series(c).shift(1).rolling(20).max().values
            r1 = pd.Series(c).pct_change().values
            r5 = pd.Series(c).pct_change(5).values
            r20 = pd.Series(c).pct_change(20).values
            vol20 = pd.Series(r1).rolling(20).std().values
            vol60 = pd.Series(r1).rolling(60).std().values
            # breakout flag and failure
            bo = c > hi20
            dist20 = c / hi20 - 1
            fc = b["forecast"].astype(float).values
            for i in range(0, n - H, H):
                fwd = c[i + H] / c[i] - 1
                # failed breakout within last 5 bars: breakout bar k, close now below its old high
                fb_depth = np.nan
                for k in range(max(0, i - 5), i):
                    if bo[k] and not np.isnan(hi20[k]) and c[i] < hi20[k]:
                        fb_depth = c[i] / hi20[k] - 1
                rows.append(dict(coin=coin, w=w, year=ts[i].year, wd=ts[i].dayofweek,
                                 fwd=fwd, r1=r1[i], r5=r5[i], r20=r20[i], dist20=dist20[i],
                                 vr=vol20[i] / vol60[i] if vol60[i] else np.nan,
                                 vol20=vol20[i], fb=fb_depth, fc=fc[i]))
    d = pd.DataFrame(rows)
    drift = d.groupby("coin")["fwd"].mean()
    sd = d.groupby("coin")["fwd"].std()
    d["u"] = d["fwd"] - d["coin"].map(drift)
    d["z"] = d["u"] / d["coin"].map(sd)
    out = {}
    def grp(col, q=5):
        x = d.dropna(subset=[col]).copy()
        x["b"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        g = x.groupby("b")["u"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["zmean"] = x.groupby("b")["z"].mean()
        return g.drop(columns="std").round(4)
    for col in ["r1", "r5", "r20", "dist20", "vr", "vol20"]:
        out["quintile_" + col] = grp(col)
    fb = d["fb"].notna()
    a, bb = d.loc[fb, "u"], d.loc[~fb, "u"]
    out["failed_breakout_vs_rest"] = pd.DataFrame({"mean": [a.mean(), bb.mean()], "n": [len(a), len(bb)],
        "t_welch": [stats.ttest_ind(a, bb, equal_var=False).statistic, np.nan]}, index=["fb", "rest"]).round(4)
    # breakout still above (not failed) in last 5 bars
    g = d.groupby("wd")["u"].agg(["mean", "count", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["weekday"] = g.drop(columns="std").round(4)
    g = d.groupby("year")["u"].agg(["mean", "count"]); out["year"] = g.round(4)
    g = d.groupby("coin")["u"].agg(["mean", "count"]); g["drift"] = drift; out["coin"] = g.round(4)
    # book: largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w
            x["prev_coin"] = x["coin_return"].shift(1); x["next_coin"] = x["coin_return"].shift(-1)
            dd.append(x)
    D = pd.concat(dd).dropna(subset=["book_return"])
    act = D[D["book_return"].abs() > 1e-9]
    out["book_active_days"] = pd.Series({"n_active": len(act), "mean_book": act["book_return"].mean(),
        "mean_coin_on_active": act["coin_return"].mean(), "corr_book_coin": act["book_return"].corr(act["coin_return"]),
        "share_top10pct_gain_sum": act["book_return"].nlargest(max(1, len(act)//10)).sum() / act["book_return"].sum() if act["book_return"].sum() != 0 else np.nan}).round(5)
    top = act.nlargest(30, "book_return"); bot = act.nsmallest(30, "book_return")
    out["book_extremes"] = pd.DataFrame({"top30": [top["book_return"].mean(), top["coin_return"].mean(), top["prev_coin"].mean()],
                                         "bottom30": [bot["book_return"].mean(), bot["coin_return"].mean(), bot["prev_coin"].mean()]},
                                        index=["book", "coin", "coin_prev_day"]).round(4)
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T)
    T["af"] = T["entry_forecast"].abs()
    T["b"] = pd.qcut(T["af"].rank(method="first"), 4, labels=False)
    out["trades_by_entryforecast_q"] = T.groupby("b")["net_profit_loss_percent"].agg(["mean", "median", "count"]).round(3)
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    return out
