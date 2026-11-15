def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    h = 10
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            sma50 = pd.Series(c).rolling(50).mean().values
            for i in range(0, len(df) - h, h):
                p20 = c[i]/c[i-20]-1 if i >= 20 else np.nan
                p10 = c[i]/c[i-10]-1 if i >= 10 else np.nan
                d50 = c[i]/sma50[i]-1 if not np.isnan(sma50[i]) else np.nan
                rows.append((coin, w, ts.iloc[i].year, f[i], c[i+h]/c[i]-1, p20, p10, d50))
    s = pd.DataFrame(rows, columns=["coin","w","year","f","r","p20","p10","d50"])
    s["ex"] = s["r"] - s.groupby("coin")["r"].transform("mean")
    out = {}
    def reg(g, x):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 10 or g[x].std() == 0: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        sl = stats.linregress(g[x], g["ex"])
        return pd.Series(dict(n=len(g), slope=sl.slope, t=sl.slope/sl.stderr))
    on = s[s.f>0]; off = s[s.f==0]
    res = []
    for x in ["p20","p10","d50"]:
        a = reg(on, x); b = reg(off, x); c_ = reg(s, x)
        res.append(dict(x=x, on_n=a.n, on_slope=a.slope, on_t=a.t, off_n=b.n, off_slope=b.slope, off_t=b.t, all_t=c_.t))
    out["momentum_slopes"] = pd.DataFrame(res)
    out["on_p20_by_coin"] = on.groupby("coin").apply(lambda g: reg(g, "p20"))
    out["on_p20_by_year"] = on.groupby("year").apply(lambda g: reg(g, "p20"))
    on = on.copy()
    on["q"] = pd.qcut(on["p20"], 4, labels=False)
    top = on[on.q == 3]["ex"]; bot = on[on.q == 0]["ex"]
    out["on_top_minus_bottom"] = pd.Series(dict(diff=top.mean()-bot.mean(), t=stats.ttest_ind(top, bot, equal_var=False).statistic, n_top=len(top), n_bot=len(bot), top_pos=(top>0).mean(), bot_pos=(bot>0).mean()))
    on["dq"] = pd.qcut(on["d50"], 4)
    out["on_by_d50"] = on.groupby("dq")["ex"].agg(["count","mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    return out
