def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    tr = pd.concat([t.assign(coin=c, w=w) for c, ws in data["trades"].items() for w, t in ws.items()])
    tr["dur_d"] = tr.duration_minutes / 1440.0
    out["trades by side"] = tr.groupby("side").agg(n=("dur_d", "size"), dur=("dur_d", "mean"),
        pl=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        win=("profit_loss_percent", lambda x: (x > 0).mean()))
    out["trades by duration"] = tr.groupby(pd.cut(tr.dur_d, [-0.1, 1, 4, 5.5, 10, 30, 1000])).agg(
        n=("dur_d", "size"), pl=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    out["trades by entry_regime"] = tr.groupby("entry_regime").agg(n=("dur_d", "size"),
        pl=("profit_loss_percent", "mean"), dur=("dur_d", "mean"))
    out["trades pl quantiles"] = tr.profit_loss_percent.quantile([0.05, 0.25, 0.5, 0.75, 0.95])
    # bars: position holding stats
    H = 5
    drift = {}; usual = {}
    for coin, ws in bars.items():
        allr = []
        for w, df in ws.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                allr.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(allr); usual[coin] = np.std(allr)
    rows = []; posrows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]; r1 = c.pct_change()
            z = r1 / r1.rolling(20).std().shift(1)
            r90 = c / c.shift(90) - 1
            ret30 = c / c.shift(30) - 1
            n = len(df)
            alloc = df["postRebalance_current_allocation"].fillna(0)
            g = alloc * (c.shift(-1) / c - 1)
            posrows.append(pd.DataFrame(dict(coin=coin, w=w, alloc=alloc, g=g,
                                             mr=(df.regime == "mean_reversion"))))
            for i in range(0, n - H, 1):
                zi = z.iat[i]
                if not (pd.notna(zi) and zi >= 2 and pd.notna(r90.iat[i]) and r90.iat[i] < 0):
                    continue
                f1 = c.iat[i + 1] / c.iat[i] - 1
                f5 = c.iat[i + H] / c.iat[i] - 1
                f2_5 = c.iat[i + H] / c.iat[i + 1] - 1
                rows.append(dict(coin=coin, w=w, cell=i // H, z=zi, r90=r90.iat[i], r30=ret30.iat[i],
                                 f1=f1, f5=f5, f25=f2_5, s5=(f5 - drift[coin]) / usual[coin],
                                 ex5=f5 - drift[coin], mr=df.regime.iat[i] == "mean_reversion"))
    d = pd.DataFrame(rows).drop_duplicates(["coin", "w", "cell"])
    def summ(g):
        return pd.Series(dict(n=len(g), f1=g.f1.mean(), f25=g.f25.mean(), ex5=g.ex5.mean(),
            t_ex5=g.ex5.mean() / (g.ex5.std() / np.sqrt(len(g))), s5=g.s5.mean()))
    out["falling bounces overall"] = summ(d).to_frame().T
    lr = stats.linregress(d.z.clip(upper=8), d.s5)
    out["s5 on z slope"] = pd.Series(dict(slope=lr.slope, t=lr.slope / lr.stderr, n=len(d)))
    lr2 = stats.linregress(d.r90, d.s5)
    out["s5 on r90 slope"] = pd.Series(dict(slope=lr2.slope, t=lr2.slope / lr2.stderr))
    d2 = d.dropna(subset=["r30"])
    lr3 = stats.linregress(d2.r30, d2.s5)
    out["s5 on r30 slope"] = pd.Series(dict(slope=lr3.slope, t=lr3.slope / lr3.stderr))
    out["by r30 quintile"] = d2.groupby(pd.qcut(d2.r30, 5)).apply(summ)
    out["by z quartile"] = d.groupby(pd.qcut(d.z, 4)).apply(summ)
    P = pd.concat(posrows)
    out["position"] = pd.Series(dict(share_short=(P.alloc < 0).mean(), share_long=(P.alloc > 0).mean(),
        mean_abs_alloc_when_in=P.alloc[P.alloc != 0].abs().mean(),
        gain_in_mr_bars=P.g[P.mr].sum(), gain_other_bars=P.g[~P.mr].sum(),
        n_short_bars_not_mr=((P.alloc < 0) & ~P.mr).sum(), n_short_bars_mr=((P.alloc < 0) & P.mr).sum()))
    # book by window
    D = pd.concat([df.assign(coin=c, w=w) for c, ws in data["days"].items() for w, df in ws.items()])
    bw = D.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    out["book by window (mean daily x1e4)"] = (bw * 1e4).round(2)
    return out
