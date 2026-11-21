def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 18
    # coin drift per 18 bars
    rows = []
    for coin, wins in data["bars"].items():
        rets = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            rets.extend(list(c[idx + H] / c[idx] - 1))
        drift = np.mean(rets) if rets else np.nan
        sd = np.std(rets) if rets else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            f = b["forecast"].fillna(0).values
            # 180-bar (30 day) past return, 42-bar return, 12-bar range width
            past30 = pd.Series(c).pct_change(180).values
            past7 = pd.Series(c).pct_change(42).values
            hi = b["high"].rolling(12).max().shift(1)
            lo = b["low"].rolling(12).min().shift(1)
            width = ((hi - lo) / b["close"]).values
            wmed = pd.Series(width).rolling(180, min_periods=60).median().values
            ma = pd.Series(c).rolling(300, min_periods=150).mean().values
            # cases: first bar of nonzero forecast after flat, one per grid cell
            seen = set()
            prev = 0.0
            for t in range(n):
                if f[t] < 0 and prev >= 0:
                    cell = t // H
                    if cell not in seen and t + H < n:
                        seen.add(cell)
                        r = c[t + H] / c[t] - 1
                        rows.append(dict(coin=coin, win=w, wnum=int(w[1:]),
                                         unusual=-(r - drift), total=-r,
                                         strength=-(r - drift) / sd,
                                         past30=past30[t], past7=past7[t],
                                         narrow=width[t] / wmed[t] if wmed[t] == wmed[t] else np.nan,
                                         abovema=c[t] / ma[t] - 1 if ma[t] == ma[t] else np.nan,
                                         fc=f[t]))
                prev = f[t]
    df = pd.DataFrame(rows)
    out["n_cases"] = len(df)
    def summ(g):
        return pd.Series(dict(n=len(g), unusual=g.unusual.mean(), total=g.total.mean(),
                              t_total=g.total.mean() / (g.total.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan))
    out["by_past30_quint"] = df.dropna(subset=["past30"]).groupby(pd.qcut(df.past30.dropna(), 5)).apply(summ)
    out["by_abovema_quint"] = df.dropna(subset=["abovema"]).groupby(pd.qcut(df.abovema.dropna(), 5)).apply(summ)
    out["by_narrow_quint"] = df.dropna(subset=["narrow"]).groupby(pd.qcut(df.narrow.dropna(), 5)).apply(summ)
    out["by_past7_quint"] = df.groupby(pd.qcut(df.past7, 5)).apply(summ)
    out["by_window"] = df.groupby("wnum").apply(summ)
    out["by_coin"] = df.groupby("coin").apply(summ)
    # book daily per window
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d[["book_return", "coin_return"]].copy()
            dd["wnum"] = int(w[1:]); dd["coin"] = coin; dd["i"] = range(len(dd))
            dl.append(dd)
    D = pd.concat(dl)
    daily = D.groupby(["wnum", "i"])[["book_return", "coin_return"]].mean()
    out["book_by_window"] = daily.groupby(level=0).agg(["mean", "std", "count"])
    # trades
    tl = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                tt = t[["side", "profit_loss_percent", "net_profit_loss_percent", "duration_minutes"]].copy()
                tt["wnum"] = int(w[1:]); tl.append(tt)
    T = pd.concat(tl)
    out["trades"] = T.groupby("side").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"),
                                          net=("net_profit_loss_percent", "mean"),
                                          dur_h=("duration_minutes", lambda x: x.mean() / 60))
    # allocation size mean when short
    al = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            a = b["postRebalance_current_allocation"]
            al.append(dict(share_in=(a.abs() > 1e-6).mean(), mean_abs=a[a.abs() > 1e-6].abs().mean()))
    out["exposure"] = pd.DataFrame(al).mean()
    return out
