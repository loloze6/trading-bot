def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = 5
    rows = []
    stat = {}
    for c in bars:
        allr = []
        for w, b in bars[c].items():
            cl = b["close"].values
            for i in range(0, len(cl) - H, H):
                allr.append(cl[i + H] / cl[i] - 1)
        allr = np.array(allr)
        drift, sd = allr.mean(), allr.std(ddof=1)
        stat[c] = (drift, sd)
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r30 = cl / cl.shift(30) - 1
            r60 = cl / cl.shift(60) - 1
            r10 = cl / cl.shift(10) - 1
            vol = cl.pct_change().rolling(20).std()
            hi = b["high"].rolling(30).max(); lo = b["low"].rolling(30).min()
            rngw = (hi - lo) / cl
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for i in range(0, len(b) - H, H):
                f = b["forecast"].iloc[i]
                if f < 0:
                    fwd = cl.iloc[i + H] / cl.iloc[i] - 1
                    rows.append(dict(coin=c, w=w, yr=yr.iloc[i], f=f, fwd=fwd,
                                     tot=-fwd, unus=-(fwd - drift), st=-(fwd - drift) / sd,
                                     r30=r30.iloc[i], r60=r60.iloc[i], r10=r10.iloc[i],
                                     vol=vol.iloc[i], rngw=rngw.iloc[i], drift=drift))
    d = pd.DataFrame(rows)
    def summ(g):
        return pd.Series(dict(n=len(g), tot=g.tot.mean(), unus=g.unus.mean(), st=g.st.mean(),
                              t_tot=g.tot.mean() / (g.tot.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan))
    out = {}
    out["all"] = summ(d).to_frame().T
    d["fq"] = pd.qcut(d.f, 4, labels=["strongest", "q2", "q3", "weakest"])
    out["by_forecast"] = d.groupby("fq").apply(summ)
    for col in ["r30", "r60", "r10", "vol", "rngw"]:
        dd = d.dropna(subset=[col]).copy()
        dd["q"] = pd.qcut(dd[col], 4, labels=["q1low", "q2", "q3", "q4high"])
        out["by_" + col] = dd.groupby("q").apply(summ)
    out["by_year"] = d.groupby("yr").apply(summ)
    out["by_coin"] = d.groupby("coin").apply(summ)
    # book
    bk = []
    for c in days:
        for w, x in days[c].items():
            x = x.copy(); x["coin"] = c; x["w"] = w; bk.append(x)
    bk = pd.concat(bk)
    bk["yr"] = pd.to_datetime(bk["day"]).dt.year
    daily = bk.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna()
    out["book_by_window"] = daily.groupby(level=0).agg(n=("br", "size"), br=("br", "mean"), cr=("cr", "mean"))
    # exposure and market part
    expo = []
    for c in bars:
        mcr = pd.concat([days[c][w]["coin_return"] for w in days[c]]).mean()
        for w, b in bars[c].items():
            a = b["postRebalance_current_allocation"]
            expo.append(dict(coin=c, short_share=(a < 0).mean(), mean_alloc=a.mean(), mkt=a.mean() * mcr))
    e = pd.DataFrame(expo)
    out["exposure"] = pd.Series(dict(short_share=e.short_share.mean(), mean_alloc=e.mean_alloc.mean(),
                                     mkt_part=e.mkt.mean(), book_mean=daily.br.mean()))
    tr = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            tr.append(t)
    t = pd.concat(tr)
    out["trades"] = pd.Series(dict(n=len(t), gross=t.profit_loss_percent.mean(), net=t.net_profit_loss_percent.mean(),
                                   win=(t.net_profit_loss_percent > 0).mean(), dur_days=t.duration_minutes.mean() / 1440))
    return out
