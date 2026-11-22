def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    # book exposure and daily returns
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            a = b["postRebalance_current_allocation"].fillna(0)
            rows.append(dict(coin=c, bars=len(b), inpos=(a.abs() > 1e-6).mean(), meanalloc_in=a[a.abs() > 1e-6].mean() if (a.abs() > 1e-6).any() else np.nan))
    ex = pd.DataFrame(rows)
    out["exposure_by_coin"] = ex.groupby("coin")[["inpos", "meanalloc_in"]].mean()
    # trades
    tr = []
    for c in trades:
        for w, t in trades[c].items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = c; t["window"] = w; tr.append(t)
    T = pd.concat(tr)
    out["trades_summary"] = pd.DataFrame({
        "n": [len(T)], "mean_pl": [T.profit_loss_percent.mean()], "mean_net": [T.net_profit_loss_percent.mean()],
        "median_net": [T.net_profit_loss_percent.median()], "win": [(T.net_profit_loss_percent > 0).mean()],
        "mean_dur_h": [T.duration_minutes.mean() / 60], "worst": [T.net_profit_loss_percent.min()]})
    out["trades_by_coin"] = T.groupby("coin").net_profit_loss_percent.agg(["count", "mean", "min", "max"])
    # recompute panic situation with weaker thresholds; non-overlapping 18-bar grid
    H = 18; recs = []; allr = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"].values; n = len(cl)
            s = pd.Series(cl)
            r6 = s / s.shift(6) - 1
            mabs = r6.abs().rolling(180, min_periods=30).mean()
            z = r6 / mabs
            rg = (b["high"] - b["low"]) / b["close"]
            rg = rg.reset_index(drop=True)
            ratio = rg.rolling(6).mean() / rg.rolling(180, min_periods=30).mean()
            r42 = s / s.shift(42) - 1  # 7-day prior trend
            for i in range(0, n - H, H):
                allr.append((c, s[i + H] / s[i] - 1))
            # cases: per grid cell first bar meeting weak condition
            for g0 in range(0, n - H, H):
                for i in range(g0, min(g0 + H, n - H)):
                    if z[i] <= -1.0 and ratio[i] >= 1.5:
                        recs.append(dict(coin=c, w=w, z=z[i], ratio=ratio[i], r42=r42[i], ret=s[i + H] / s[i] - 1))
                        break
    A = pd.DataFrame(allr, columns=["coin", "r"])
    mu = A.groupby("coin").r.mean(); sd = A.groupby("coin").r.std()
    R = pd.DataFrame(recs)
    R["ex"] = R.ret - R.coin.map(mu)
    R["zb"] = pd.cut(R.z, [-99, -3, -2, -1.5, -1])
    R["rb"] = pd.cut(R.ratio, [1.5, 2, 3, 4, 99])
    g = lambda x: pd.Series({"n": len(x), "mean_ex": x.ex.mean(), "t": x.ex.mean() / (x.ex.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["by_fall_depth"] = R.groupby("zb").apply(g)
    out["by_range_ratio"] = R.groupby("rb").apply(g)
    out["fall_x_range"] = R.groupby(["zb", "rb"]).apply(g)
    R["trend"] = pd.cut(R.r42, [-9, -0.15, -0.05, 0.05, 9])
    out["by_prior7d"] = R.groupby("trend").apply(g)
    # book falls: deepest drawdown per coin chain
    dd = []
    for c in days:
        for w, d in days[c].items():
            br = d.book_return.dropna(); cr = d.coin_return.dropna()
            dd.append(dict(coin=c, w=w, book=(1 + br).prod() - 1, coin_ret=(1 + cr).prod() - 1, worstday=br.min()))
    D = pd.DataFrame(dd)
    out["window_book_vs_coin"] = D.groupby("w")[["book", "coin_ret", "worstday"]].mean()
    return out
