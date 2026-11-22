def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; trades = data["trades"]
    out = {}
    tr = []
    for c in trades:
        for w, t in trades[c].items():
            t = t.copy(); t["coin"] = c; t["w"] = w; tr.append(t)
    t = pd.concat(tr)
    t["dur"] = t.duration_minutes / 1440
    t["yr"] = pd.to_datetime(t.entry_time).dt.year
    def s(g):
        return pd.Series(dict(n=len(g), gross=g.profit_loss_percent.mean(), med=g.profit_loss_percent.median(),
                              net=g.net_profit_loss_percent.mean(), win=(g.net_profit_loss_percent > 0).mean(),
                              comm=g.total_commission.mean()))
    out["by_side"] = t.groupby("side").apply(s)
    t["durb"] = pd.cut(t.dur, [-0.1, 1.5, 4.5, 5.5, 10.5, 20.5, 1000], labels=["<=1", "2-4", "5", "6-10", "11-20", ">20"])
    out["by_duration"] = t.groupby("durb").apply(s)
    out["by_entry_regime"] = t.groupby("entry_regime").apply(s)
    t["efq"] = pd.qcut(t.entry_forecast.rank(method="first"), 4, labels=["most_neg", "q2", "q3", "least_neg"])
    out["by_entry_forecast"] = t.groupby("efq").apply(s)
    out["gross_quantiles"] = t.profit_loss_percent.quantile([0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
    # position gain per bar by state
    rows = []
    for c in bars:
        mcr = []
        for w, b in bars[c].items():
            mcr.append(b["close"].pct_change())
        m = pd.concat(mcr).mean()
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; a = b["postRebalance_current_allocation"].fillna(0)
            nxt = cl.shift(-1) / cl - 1
            hi = b["high"].rolling(30).max(); lo = b["low"].rolling(30).min()
            rngw = (hi - lo) / cl
            f = b["forecast"].fillna(0)
            # bars since forecast last nonzero
            act = (f != 0)
            grp = act.cumsum()
            since = act.groupby(grp).cumcount().where(~act, 0)
            rows.append(pd.DataFrame(dict(coin=c, a=a, g=a * nxt, mk=a * m, f=f, rngw=rngw, since=since,
                                          short=a < 0, fc=b["regime"])))
    d = pd.concat(rows).dropna(subset=["g"])
    sh = d[d.short]
    out["short_bars"] = pd.Series(dict(n=len(sh), share_with_forecast0=(sh.f == 0).mean(),
                                       gain_fc_neg=sh[sh.f < 0].g.mean(), gain_fc0=sh[sh.f == 0].g.mean(),
                                       mk_fc_neg=sh[sh.f < 0].mk.mean(), mk_fc0=sh[sh.f == 0].mk.mean(),
                                       mean_abs_alloc=sh.a.abs().mean()))
    sh = sh.copy()
    sh["sinceb"] = pd.cut(sh.since, [-1, 0, 2, 5, 10, 1000], labels=["fc<0", "1-2", "3-5", "6-10", ">10"])
    out["short_gain_by_bars_since_signal"] = sh.groupby("sinceb").agg(n=("g", "size"), gain=("g", "mean"), mkt=("mk", "mean"))
    s2 = sh.dropna(subset=["rngw"]).copy()
    s2["rq"] = pd.qcut(s2.rngw, 4, labels=["narrow", "q2", "q3", "wide"])
    out["short_gain_by_range_width"] = s2.groupby("rq").agg(n=("g", "size"), gain=("g", "mean"), mkt=("mk", "mean"),
                                                         alloc=("a", "mean"))
    out["by_year_trades"] = t.groupby("yr").apply(s)
    return out
