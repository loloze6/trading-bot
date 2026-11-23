def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []; other = []; trows = []; drows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            ts = pd.to_datetime(b["timestamp"])
            r1 = pd.Series(c).pct_change()
            vol = r1.rolling(720, min_periods=720).std().values
            r24 = pd.Series(c).pct_change(24).values
            mabs = pd.Series(np.abs(r24)).rolling(720, min_periods=200).mean().values
            n = len(c)
            f48 = np.full(n, np.nan); f24 = np.full(n, np.nan)
            f48[:n-48] = c[48:] / c[:n-48] - 1
            f24[:n-24] = c[24:] / c[:n-24] - 1
            fc = b["forecast"].fillna(0).values
            wd = ts.dt.weekday.values; hr = ts.dt.hour.values
            for i in range(n):
                if hr[i] == 23 and not np.isnan(f48[i]) and not np.isnan(mabs[i]):
                    sc = r24[i] / mabs[i]
                    d = dict(coin=coin, w=w, year=ts[i].year, wd=wd[i], sc=sc, vol=vol[i],
                             f48=f48[i], f24=f24[i], fc=fc[i], alloc=b["postRebalance_current_allocation"].iloc[i])
                    if wd[i] == 6:
                        rows.append(d)
                    else:
                        other.append(d)
        for w, t in data["trades"][coin].items():
            if len(t):
                tt = t.copy(); tt["coin"] = coin; tt["w"] = w; trows.append(tt)
        for w, d in data["days"][coin].items():
            dd = d.copy(); dd["coin"] = coin; dd["w"] = w; drows.append(dd)
    S = pd.DataFrame(rows); O = pd.DataFrame(other)
    for D in (S, O):
        D["rev48"] = -np.sign(D["sc"]) * D["f48"] * 100
        D["rev24"] = -np.sign(D["sc"]) * D["f24"] * 100
        D["absc"] = D["sc"].abs()
        D["scq"] = D.groupby("coin")["absc"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
        D["volq"] = D.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    def agg(g):
        return pd.Series({"n": len(g), "rev48": g.rev48.mean(), "t48": g.rev48.mean()/(g.rev48.std()/np.sqrt(len(g))),
                          "rev24": g.rev24.mean(), "t24": g.rev24.mean()/(g.rev24.std()/np.sqrt(len(g)))})
    out = {}
    out["sunday_by_size_quint"] = S.groupby("scq").apply(agg)
    out["other_days_by_size_quint"] = O.groupby("scq").apply(agg)
    out["sunday_by_volq"] = S.groupby("volq").apply(agg)
    out["other_by_volq"] = O.groupby("volq").apply(agg)
    S["side"] = np.where(S.sc > 0, "short_after_rise", "long_after_fall")
    out["sunday_by_side"] = S.groupby("side").apply(agg)
    out["sunday_by_side_sizeq"] = S.groupby(["side", "scq"]).apply(agg)[["n","rev48","t48"]]
    out["sunday_by_volq_sizeq"] = S.groupby(["volq", "scq"]).apply(agg)[["n","rev48","t48"]]
    out["sunday_by_year"] = S.groupby("year").apply(agg)
    out["sunday_by_coin"] = S.groupby("coin").apply(agg)
    S["absalloc"] = S["alloc"].abs()
    out["alloc_by_sizeq"] = S.groupby("scq")["absalloc"].mean()
    out["alloc_by_volq"] = S.groupby("volq")["absalloc"].mean()
    T = pd.concat(trows)
    T["dur_h"] = T.duration_minutes / 60
    out["trades"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"),
                                        net=("net_profit_loss_percent", "mean"), dur=("dur_h", "mean"), comm=("total_commission", "mean"))
    out["trade_dur_dist"] = T["dur_h"].describe()
    Dd = pd.concat(drows)
    Dd["year"] = pd.to_datetime(Dd["day"]).dt.year
    bk = Dd.groupby(["w", "day"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean")).reset_index()
    bk["year"] = pd.to_datetime(bk["day"]).dt.year
    out["book_by_year"] = bk.groupby("year").agg(book_mean=("book", "mean"), book_sd=("book", "std"), coin_mean=("coin", "mean"))
    return out
