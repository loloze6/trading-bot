def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 96
    rows = []
    allz = []
    drift = {}
    for coin, wins in data["bars"].items():
        # normal drift over 96 bars
        rs = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            rs += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(rs)
        for w, b in wins.items():
            c = b["close"].astype(float).values
            n = len(c)
            s = pd.Series(c)
            r24 = s / s.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=300).mean()
            z = (r24 / mabs).values
            r30 = (s / s.shift(720) - 1).values
            f = b["forecast"].fillna(0).values
            fprev = np.r_[0, f[:-1]]
            for g0 in range(0, n - H, H):
                seg = range(g0, g0 + H)
                # strategy case: forecast short and getting more negative by >=2
                for t in seg:
                    if f[t] <= -2 and f[t] - fprev[t] <= -2 * 0 - 0.0 and f[t] < fprev[t]:
                        if t + 192 < n:
                            rows.append(dict(coin=coin, win=int(w[1:]), kind="case", f=f[t], z=z[t], r30=r30[t],
                                r24=-(c[t+24]/c[t]-1), r48=-(c[t+48]/c[t]-1), r96=-(c[t+96]/c[t]-1),
                                r192=-(c[t+192]/c[t]-1), r0=-(r24.values[t]), hour=t))
                        break
                # price-based plunge regardless of regime
                for t in seg:
                    if np.isfinite(z[t]) and z[t] <= -1.5 and t + 192 < n:
                        allz.append(dict(coin=coin, win=int(w[1:]), z=z[t], r30=r30[t],
                            up48=c[t+48]/c[t]-1, up96=c[t+96]/c[t]-1, up192=c[t+192]/c[t]-1))
                        break
    df = pd.DataFrame(rows)
    df["drift"] = df.coin.map(drift)
    df["u96"] = df.r96 + df.drift
    def summ(g):
        return pd.Series({"n": len(g), "tot24": g.r24.mean(), "tot48": g.r48.mean(), "tot96": g.r96.mean(),
                          "tot192": g.r192.mean(), "unus96": g.u96.mean(),
                          "t96": g.r96.mean() / (g.r96.std() / np.sqrt(len(g)))})
    out["cases_all"] = summ(df)
    out["cases_by_coin"] = df.groupby("coin").apply(summ)
    df["fbin"] = pd.cut(df.f, [-20.01, -15, -8, -4, -1.9])
    out["cases_by_forecast"] = df.groupby("fbin").apply(summ)
    d2 = df.dropna(subset=["r30"]).copy()
    d2["r30q"] = pd.qcut(d2.r30, 5)
    out["cases_by_r30_quintile"] = d2.groupby("r30q").apply(summ)
    out["cases_by_window_tot96"] = df.groupby("win").r96.agg(["count", "mean"]).T
    az = pd.DataFrame(allz)
    az["state"] = np.where(az.r30 < 0, "r30<0", "r30>=0")
    az["zbin"] = pd.cut(az.z, [-99, -3, -2, -1.5])
    out["plunges_price_returns_up"] = az.groupby(["state", "zbin"])[["up48", "up96", "up192"]].agg(["count", "mean"]).round(4)
    # book
    br = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d[["book_return", "coin_return"]].dropna()
            br.append(dict(coin=coin, win=w, book=x.book_return.mean(), coin_r=x.coin_return.mean(), n=len(x)))
    bdf = pd.DataFrame(br)
    out["book_by_coin"] = bdf.groupby("coin")[["book", "coin_r"]].mean()
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                tt = t.copy(); tt["coin"] = coin; tr.append(tt)
    T = pd.concat(tr)
    out["trades_by_coin"] = T.groupby("coin").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda x: x.mean() / 60),
        win=("net_profit_loss_percent", lambda x: (x > 0).mean()))
    T["durbin"] = pd.cut(T.duration_minutes / 60, [0, 24, 96, 97, 200, 1e6])
    out["trades_by_duration"] = T.groupby("durbin").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"))
    return out
