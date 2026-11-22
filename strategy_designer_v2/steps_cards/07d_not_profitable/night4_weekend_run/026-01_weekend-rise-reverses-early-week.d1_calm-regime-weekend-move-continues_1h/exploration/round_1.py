def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # per-case analysis on Monday-00 active bars
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values
            n = len(b)
            act = np.where((b["regime"].values == "trending") & (b["forecast"].abs().values >= 2))[0]
            for i in act:
                if i + 48 >= n or i - 48 < 0:
                    continue
                f = b["forecast"].iloc[i]
                r48 = c[i+48]/c[i]-1
                r24 = c[i+24]/c[i]-1
                wk = c[i]/c[i-48]-1
                # prior 7-day return before weekend
                pre = c[i-48]/c[i-48-120]-1 if i-168 >= 0 else np.nan
                alloc = b["postRebalance_current_allocation"].iloc[i]
                rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, f=f, r48=r48, r24=r24,
                                 wk=wk, pre=pre, alloc=alloc, sret=np.sign(f)*r48, sret24=np.sign(f)*r24,
                                 sret_d2=np.sign(f)*(c[i+48]/c[i+24]-1)))
    d = pd.DataFrame(rows)
    d["absf"] = d["f"].abs()
    d["fbin"] = pd.cut(d["absf"], [2, 5, 10, 15, 20.01], right=False)
    def agg(g):
        return pd.Series(dict(n=len(g), mean_sret=g.sret.mean(), t=g.sret.mean()/(g.sret.std()/np.sqrt(len(g))),
                              day1=g.sret24.mean(), day2=g.sret_d2.mean(), mean_absalloc=g.alloc.abs().mean(),
                              mean_abswk=g.wk.abs().mean()))
    out["by_forecast_size"] = d.groupby("fbin", observed=True).apply(agg)
    out["by_coin"] = d.groupby("coin").apply(agg)
    out["by_year"] = d.groupby("year").apply(agg)
    out["by_side"] = d.groupby(np.sign(d["f"])).apply(agg)
    d["wkq"] = pd.qcut(d["wk"].abs(), 5, labels=False)
    out["by_abs_weekend_move_quintile"] = d.groupby("wkq").apply(agg)
    d["prealign"] = np.sign(d["pre"]) == np.sign(d["wk"])
    out["by_prior5d_same_dir"] = d.dropna(subset=["pre"]).groupby("prealign").apply(agg)
    # book: exposure and daily returns
    dd = []
    for coin, ws in data["days"].items():
        for w, x in ws.items():
            b = data["bars"][coin][w]
            ts = pd.to_datetime(b["timestamp"])
            inpos = (b["postRebalance_current_allocation"].abs() > 0).groupby(ts.dt.floor("D")).max()
            x = x.copy()
            x["day"] = pd.to_datetime(x["day"])
            x["inpos"] = x["day"].map(inpos).fillna(False).values
            x["coin"] = coin; x["win"] = w
            dd.append(x)
    D = pd.concat(dd)
    out["share_days_in_position"] = float(D["inpos"].mean())
    out["book_ret_in_vs_out"] = D.groupby("inpos")[["book_return", "coin_return"]].agg(["mean", "std", "count"])
    out["mean_abs_alloc_when_in"] = float(np.nanmean([data["bars"][c][w]["postRebalance_current_allocation"].abs().replace(0, np.nan).mean() for c in data["bars"] for w in data["bars"][c]]))
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()])
    out["trades"] = pd.Series(dict(n=len(T), gross=T.profit_loss_percent.mean(), net=T.net_profit_loss_percent.mean(),
                                   win=(T.net_profit_loss_percent > 0).mean(), dur_h=T.duration_minutes.mean()/60))
    # per window book mean
    out["book_by_window_mean"] = D.groupby("win")["book_return"].mean().describe()
    return out
