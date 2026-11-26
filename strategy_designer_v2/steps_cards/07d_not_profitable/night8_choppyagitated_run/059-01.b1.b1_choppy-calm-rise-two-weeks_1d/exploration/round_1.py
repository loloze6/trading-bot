def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    H = 14
    # coin drift over 14 bars, non-overlapping grid, all windows
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(b)
            r1 = pd.Series(cl).pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            ret7 = pd.Series(cl).pct_change(7)
            ret60 = pd.Series(cl).pct_change(60)
            sr = ret7 / (vol30 * np.sqrt(7))
            for i in range(0, n - H, H):
                rows.append(dict(coin=c, win=w, fwd=cl[i+H]/cl[i]-1, fc=b["forecast"].iloc[i],
                                 reg=b["regime"].iloc[i], sr=sr.iloc[i], r7=ret7.iloc[i],
                                 r60=ret60.iloc[i], vol=vol30.iloc[i],
                                 alloc=b["postRebalance_current_allocation"].iloc[i]))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - g["drift"]
    g["inprof"] = g["reg"] == "unknown"
    def summ(d):
        return pd.Series(dict(n=len(d), mean_fwd=d["fwd"].mean(), mean_ex=d["ex"].mean(),
                              t_ex=d["ex"].mean()/(d["ex"].std()/np.sqrt(len(d))) if len(d)>2 else np.nan,
                              hit=(d["fwd"]>0).mean()))
    g["srq"] = pd.cut(g["sr"], [-np.inf, -1, -0.5, 0, 0.5, 1, 1.5, np.inf])
    out["grid by scaled rise, in profile"] = g[g.inprof].groupby("srq").apply(summ)
    out["grid by scaled rise, out of profile"] = g[~g.inprof].groupby("srq").apply(summ)
    gp = g[g.inprof & (g.fc > 0)].copy()
    gp["fcq"] = pd.cut(gp["fc"], [0, 5, 10, 15, 20.1])
    out["in profile fc>0 by forecast"] = gp.groupby("fcq").apply(summ)
    out["in profile fc==0"] = summ(g[g.inprof & (g.fc <= 0)])
    out["in profile fc>0 by window"] = gp.groupby("win").apply(summ)
    out["in profile fc>0 by coin"] = gp.groupby("coin").apply(summ)
    # book daily: per window
    dd = []
    for c in days:
        for w, d in days[c].items():
            dd.append(d.assign(coin=c, win=w))
    D = pd.concat(dd)
    bk = D.groupby(["win", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index()
    def wsum(x):
        return pd.Series(dict(days=len(x), book_mean=x.br.mean(), book_sharpe=x.br.mean()/x.br.std()*np.sqrt(365),
                              hold_sharpe=x.cr.mean()/x.cr.std()*np.sqrt(365),
                              book_maxdd=((1+x.br.fillna(0)).cumprod()/(1+x.br.fillna(0)).cumprod().cummax()-1).min()))
    out["book by window"] = bk.groupby("win").apply(wsum)
    # trades
    T = []
    for c in trades:
        for w, t in trades[c].items():
            if len(t): T.append(t.assign(coin=c, win=w))
    T = pd.concat(T)
    T["dur_d"] = T["duration_minutes"]/1440
    T["fq"] = pd.cut(T["entry_forecast"], [0, 5, 10, 15, 20.1])
    out["trades by entry forecast"] = T.groupby("fq").agg(n=("net_profit_loss_percent", "size"),
        mean_net=("net_profit_loss_percent", "mean"), med_net=("net_profit_loss_percent", "median"),
        hit=("net_profit_loss_percent", lambda x: (x>0).mean()), dur=("dur_d", "mean"))
    T["durq"] = pd.cut(T["dur_d"], [0, 7, 14, 15, 30, 1000])
    out["trades by duration"] = T.groupby("durq").agg(n=("net_profit_loss_percent", "size"),
        mean_net=("net_profit_loss_percent", "mean"), hit=("net_profit_loss_percent", lambda x: (x>0).mean()))
    out["trades total"] = pd.Series(dict(n=len(T), mean_net=T.net_profit_loss_percent.mean(),
        worst=T.net_profit_loss_percent.min(), q10=T.net_profit_loss_percent.quantile(0.1),
        q90=T.net_profit_loss_percent.quantile(0.9)))
    return out
