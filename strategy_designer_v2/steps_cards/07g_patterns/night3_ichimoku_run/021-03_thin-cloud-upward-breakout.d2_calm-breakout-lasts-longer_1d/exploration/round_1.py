def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    # --- cross-bar cases: 40-bar fwd return, by vol, past return, distance features
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(cl)
            lr = np.log(cl)
            r1 = np.r_[np.nan, np.diff(lr)]
            for i in np.where(b["regime"].values == "trending")[0]:
                f40 = cl[i+40]/cl[i]-1 if i+40 < n else np.nan
                f20 = cl[i+20]/cl[i]-1 if i+20 < n else np.nan
                f10 = cl[i+10]/cl[i]-1 if i+10 < n else np.nan
                p20 = cl[i]/cl[i-20]-1 if i >= 20 else np.nan
                p5 = cl[i]/cl[i-5]-1 if i >= 5 else np.nan
                v20 = np.nanstd(r1[max(1,i-19):i+1]) if i >= 5 else np.nan
                d1 = r1[i]
                hi = b["high"].values; lo = b["low"].values
                rng = (hi[i]-lo[i])/cl[i]
                rows.append(dict(coin=c, win=w, i=i, f40=f40, f20=f20, f10=f10, p20=p20, p5=p5,
                                 v20=v20, d1=d1, rng=rng, fc=b["forecast"].values[i],
                                 year=pd.Timestamp(b["timestamp"].values[i]).year))
    X = pd.DataFrame(rows)
    out["n_cross"] = len(X)
    out["cross_by_year"] = X.groupby("year").agg(n=("f40","count"), f40=("f40","mean"), f20=("f20","mean"), f10=("f10","mean"))
    out["cross_by_coin"] = X.groupby("coin").agg(n=("f40","count"), f40=("f40","mean"), f20=("f20","mean"))
    def terc(col):
        d = X.dropna(subset=[col,"f40"]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
        g = d.groupby("q").agg(n=("f40","count"), f40=("f40","mean"), f20=("f20","mean"), f10=("f10","mean"), x=(col,"mean"))
        return g
    for col in ["v20","p20","p5","d1","rng"]:
        out["cross_terc_"+col] = terc(col)
    sp = {}
    for col in ["v20","p20","p5","d1","rng","fc"]:
        d = X.dropna(subset=[col,"f40"])
        r, p = stats.spearmanr(d[col], d["f40"]); sp[col] = f"rho={r:.3f} p={p:.3f} n={len(d)}"
    out["cross_spearman_f40"] = pd.Series(sp)
    # --- all bars: past-N vs future-N, non-overlapping grid
    res = []
    for N in [10, 20, 40]:
        pp, ff = [], []
        for c in bars:
            for w, b in bars[c].items():
                cl = b["close"].values
                for i in range(N, len(cl)-N, N):
                    pp.append(cl[i]/cl[i-N]-1); ff.append(cl[i+N]/cl[i]-1)
        pp, ff = np.array(pp), np.array(ff)
        r, p = stats.spearmanr(pp, ff)
        hi = ff[pp > np.quantile(pp, 2/3)]; lo = ff[pp < np.quantile(pp, 1/3)]
        t = stats.ttest_ind(hi, lo, equal_var=False)
        res.append(dict(N=N, n=len(pp), rho=r, p=p, top=hi.mean(), bot=lo.mean(), t=t.statistic))
    out["mom_all_bars"] = pd.DataFrame(res)
    # vol level vs fwd 20
    pp, ff = [], []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"].values; r1 = np.r_[np.nan, np.diff(np.log(cl))]
            for i in range(20, len(cl)-20, 20):
                pp.append(np.nanstd(r1[i-19:i+1])); ff.append(cl[i+20]/cl[i]-1)
    pp, ff = np.array(pp), np.array(ff)
    q = pd.qcut(pp, 3, labels=False)
    out["vol_terc_fwd20"] = pd.DataFrame({"q":q,"f":ff}).groupby("q")["f"].agg(["count","mean","std"])
    # --- daily: weekday
    D = pd.concat([d.assign(coin=c) for c in days for d in days[c].values()])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["weekday_coin_ret"] = D.groupby("wd")["coin_return"].agg(["count","mean"])
    out["weekday_book_ret"] = D.groupby("wd")["book_return"].agg(["count","mean"])
    # large daily moves -> next day
    D = D.sort_values(["coin","day"])
    D["nxt"] = D.groupby("coin")["coin_return"].shift(-1)
    D["z"] = D.groupby("coin")["coin_return"].transform(lambda s: (s - s.mean())/s.std())
    D["zb"] = pd.cut(D["z"], [-99,-2,-1,1,2,99])
    out["nextday_after_move"] = D.groupby("zb")["nxt"].agg(["count","mean"])
    # --- trades
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values() if len(t)])
    T["year"] = pd.to_datetime(T["entry_time"]).dt.year
    out["trades_by_year"] = T.groupby("year")["net_profit_loss_percent"].agg(["count","mean","median","min"])
    T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 3, labels=False)
    out["trades_by_fc_terc"] = T.groupby("fq").agg(n=("net_profit_loss_percent","count"), pnl=("net_profit_loss_percent","mean"), fc=("entry_forecast","mean"), dur=("duration_minutes","mean"))
    return out
