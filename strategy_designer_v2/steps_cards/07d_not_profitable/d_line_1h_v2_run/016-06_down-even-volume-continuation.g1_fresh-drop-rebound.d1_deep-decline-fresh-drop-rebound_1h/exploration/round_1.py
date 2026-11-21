def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]; trades = data["trades"]
    # book per window and per coin
    rows = []
    allbook = []
    for c in days:
        for w, d in days[c].items():
            b = d["book_return"].dropna(); h = d["coin_return"].dropna()
            rows.append((c, w, b.mean(), b.std(), h.mean(), len(b)))
            allbook.append(d.assign(coin=c, win=w))
    df = pd.DataFrame(rows, columns=["coin", "win", "bmean", "bstd", "hmean", "n"])
    ab = pd.concat(allbook)
    # equal-weight daily book: mean across coins per window-day
    eq = ab.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    pw = eq.groupby(level=0).agg(['mean', 'std', 'count'])
    pw.columns = ['_'.join(x) for x in pw.columns]
    pw["book_sharpe"] = pw["book_return_mean"] / pw["book_return_std"] * np.sqrt(365)
    pw["hold_sharpe"] = pw["coin_return_mean"] / pw["coin_return_std"] * np.sqrt(365)
    out["per_window"] = pw[["book_return_mean", "coin_return_mean", "book_sharpe", "hold_sharpe"]].round(5)
    pc = df.groupby("coin")[["bmean", "hmean"]].mean()
    out["per_coin_mean_daily"] = pc
    # exposure, market part vs timing, fees
    rows = []; gridrows = []
    for c in bars:
        allc = pd.concat([bars[c][w]["close"] for w in bars[c]])
        for w, b in bars[c].items():
            r1 = b["close"].shift(-1) / b["close"] - 1
            pos = b["postRebalance_current_allocation"].fillna(0)
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            rows.append((c, w, pos.mean(), (pos > 0).mean(), (pos * r1).sum(), fee.sum(), r1.mean()))
            cl = b["close"].values
            r72 = pd.Series(cl).pct_change(72).values
            r720 = pd.Series(cl).pct_change(720).values
            vol = pd.Series(cl).pct_change().rolling(72).std().values
            vol720 = pd.Series(cl).pct_change().rolling(720).std().values
            f = b["forecast"].values
            for i in range(0, len(cl) - 72, 72):
                gridrows.append((c, w, f[i], cl[i + 72] / cl[i] - 1, r72[i], r720[i], vol[i] / vol720[i] if vol720[i] else np.nan, pos.values[i]))
    ex = pd.DataFrame(rows, columns=["coin", "win", "pos_mean", "share_long", "gross", "fees", "r1mean"])
    out["exposure_fees_by_coin"] = ex.groupby("coin")[["pos_mean", "share_long", "gross", "fees"]].mean().round(4)
    g = pd.DataFrame(gridrows, columns=["coin", "win", "f", "fwd", "r72", "r720", "volratio", "pos"])
    g["exc"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    ga = g[g.f > 0].copy()
    ga["fq"] = pd.qcut(ga.f.rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["active_by_forecast_tercile"] = ga.groupby("fq")["exc"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    ga["trend30"] = pd.qcut(ga.r720.rank(method="first"), 3, labels=["down30", "mid30", "up30"])
    out["active_by_30d_trend"] = ga.groupby("trend30")["fwd"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["active_by_30d_trend_x_ftercile"] = ga.groupby(["trend30", "fq"])["fwd"].mean().unstack().round(4)
    ga["vr"] = pd.qcut(ga.volratio.rank(method="first"), 3, labels=["calm", "mid", "hot"])
    out["active_by_volratio"] = ga.groupby("vr")["fwd"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["inactive_vs_active_fwd"] = g.groupby(g.f > 0)["fwd"].agg(["mean", "count"])
    # drawdown of equal-weight chained book
    chain = (1 + eq["book_return"]).cumprod()
    dd = chain / chain.cummax() - 1
    out["max_dd"] = float(dd.min())
    out["yearly_ret"] = float(chain.iloc[-1] ** (365 / len(chain)) - 1)
    # trades
    t = pd.concat([trades[c][w].assign(coin=c, win=w) for c in trades for w in trades[c] if len(trades[c][w])])
    out["trades"] = pd.Series({"n": len(t), "mean_gross": t.profit_loss_percent.mean(), "mean_net": t.net_profit_loss_percent.mean(),
                               "win_rate": (t.net_profit_loss_percent > 0).mean(), "mean_days": t.duration_minutes.mean() / 1440})
    return out
