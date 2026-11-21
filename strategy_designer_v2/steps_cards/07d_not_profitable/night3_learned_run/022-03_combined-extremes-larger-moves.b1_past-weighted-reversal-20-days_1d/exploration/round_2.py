def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    def tt(x):
        x = pd.Series(x).dropna()
        return x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 and x.std() > 0 else np.nan
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = pd.Series(b["close"].values)
            a = b["postRebalance_current_allocation"].values
            r1 = c.pct_change().values
            nxt = c.pct_change().shift(-1).values
            raw = b["debug_info.components.rev_weighted.last_history_value"].values if "debug_info.components.rev_weighted.last_history_value" in b else np.full(len(c), np.nan)
            ma100 = c.rolling(100).mean().values
            r60 = (c / c.shift(60) - 1).values
            vol20 = np.log(c).diff().rolling(20).std().values
            vol120 = np.log(c).diff().rolling(120).std().values
            mode = np.where(np.sign(raw) == np.sign(-r1), "reversal", np.where(np.sign(raw) == np.sign(r1), "momentum", "none"))
            rows.append(pd.DataFrame(dict(coin=coin, w=w, a=a, g=a * nxt, nxt=nxt,
                trend=np.where(c.values > ma100, "above_ma100", "below_ma100"),
                r60=r60, vr=vol20 / vol120, mode=mode, side=np.sign(a))))
    df = pd.concat(rows, ignore_index=True)
    df = df[np.isfinite(df.g)]
    mu = df.groupby("coin").nxt.mean()
    df["mkt"] = df.a * df.coin.map(mu)
    df["timing"] = df.g - df.mkt
    out = {}
    out["by_side"] = df.groupby("side").agg(n=("g", "size"), mean_gain=("g", "mean"), mkt=("mkt", "mean"), timing=("timing", "mean"), meanabs_a=("a", lambda x: x.abs().mean()))
    out["side_by_trend"] = df.groupby(["side", "trend"]).agg(n=("g", "size"), mean_gain=("g", "mean"), coin_next=("nxt", "mean"))
    df["r60q"] = pd.qcut(df.r60, 5, labels=False)
    out["side_by_r60_quintile"] = df.groupby(["side", "r60q"]).agg(n=("g", "size"), mean_gain=("g", "mean"), coin_next=("nxt", "mean"), r60=("r60", "mean"))
    df["vrq"] = pd.qcut(df.vr, 4, labels=False)
    out["side_by_volratio_q"] = df.groupby(["side", "vrq"]).agg(n=("g", "size"), mean_gain=("g", "mean"), vr=("vr", "mean"))
    out["side_by_mode"] = df.groupby(["side", "mode"]).agg(n=("g", "size"), mean_gain=("g", "mean"))
    out["short_by_year_window_top_losses"] = df[df.side < 0].groupby("w").g.sum().sort_values().head(8)
    # 20-day non-overlapping: r60 quintile vs coin's next 20d excess
    rows2 = []
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 20, 20)
            rs += list(c[idx + 20] / c[idx] - 1)
        d = np.mean(rs)
        for w, b in wins.items():
            c = pd.Series(b["close"].values); f = b["forecast"].values
            r60 = (c / c.shift(60) - 1).values
            ma = (c > c.rolling(100).mean()).values
            for i in range(0, len(c) - 20, 20):
                rows2.append(dict(f=f[i], ex=c.values[i + 20] / c.values[i] - 1 - d, r60=r60[i], up=ma[i]))
    d2 = pd.DataFrame(rows2).dropna()
    d2["side"] = np.sign(d2.f)
    d2["sx"] = d2.side * d2.ex
    out["grid_side_by_trend"] = d2[d2.side != 0].groupby(["side", "up"]).sx.agg(["count", "mean", tt])
    d2["r60q"] = pd.qcut(d2.r60, 5, labels=False)
    out["grid_ex_by_r60q"] = d2.groupby("r60q").agg(n=("ex", "size"), ex=("ex", "mean"), r60=("r60", "mean"))
    out["grid_ex_by_r60q_t"] = d2.groupby("r60q").ex.apply(tt)
    # book drawdown: daily mean book return
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            dd.append(t.assign(coin=coin, w=w))
    D = pd.concat(dd)
    daily = D.groupby(["w", "day"]).book_return.mean()
    out["book_daily_by_window"] = daily.groupby(level=0).agg(["count", "mean", "std"])
    return out
