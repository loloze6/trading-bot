def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["days"].keys())
    wins = sorted(set(w for c in coins for w in data["days"][c].keys()), key=lambda s: int(s[1:]))
    chain = []
    for w in wins:
        frames = []
        for c in coins:
            if w in data["days"][c]:
                d = data["days"][c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c
                frames.append(d)
        if not frames:
            continue
        df = pd.concat(frames)
        g = df.groupby("day").agg(book=("book_return", "mean"), hold=("coin_return", "mean")).reset_index()
        g["window"] = w
        chain.append(g.dropna())
    ch = pd.concat(chain, ignore_index=True)
    ch["val"] = (1 + ch["book"]).cumprod()
    ch["peak"] = ch["val"].cummax()
    ch["dd"] = ch["val"] / ch["peak"] - 1
    out["max_dd"] = float(ch["dd"].min())
    yrs = len(ch) / 365
    out["yearly_return"] = float(ch["val"].iloc[-1] ** (1 / yrs) - 1)
    hv = (1 + ch["hold"]).cumprod()
    out["hold_max_dd"] = float((hv / hv.cummax() - 1).min())
    out["hold_yearly"] = float(hv.iloc[-1] ** (1 / yrs) - 1)
    ww = ch.groupby("window").agg(book_ret=("book", lambda x: (1 + x).prod() - 1),
                                  hold_ret=("hold", lambda x: (1 + x).prod() - 1),
                                  min_dd=("dd", "min"), days=("book", "size"))
    ww = ww.reindex([w for w in wins if w in ww.index])
    out["by_window"] = ww.round(4)
    # drawdown episodes (peak to trough)
    eps = []
    inn = False
    for i in range(len(ch)):
        if ch["dd"].iloc[i] < 0 and not inn:
            inn = True; s = i
        if inn and ch["dd"].iloc[i] == 0:
            seg = ch.iloc[s:i]
            j = seg["dd"].idxmin()
            eps.append(dict(start_win=ch["window"].iloc[s], trough_win=ch["window"].loc[j],
                            depth=seg["dd"].min(), days_to_trough=j - s + 1, len_days=i - s,
                            hold_ret_to_trough=(1 + ch["hold"].iloc[s:j + 1]).prod() - 1))
            inn = False
    if inn:
        seg = ch.iloc[s:]
        j = seg["dd"].idxmin()
        eps.append(dict(start_win=ch["window"].iloc[s], trough_win=ch["window"].loc[j],
                        depth=seg["dd"].min(), days_to_trough=j - s + 1, len_days=len(ch) - s,
                        hold_ret_to_trough=(1 + ch["hold"].iloc[s:j + 1]).prod() - 1))
    e = pd.DataFrame(eps).sort_values("depth").head(8)
    out["worst_dd_episodes"] = e.round(4)
    # correlation of book daily with hold daily, and down-day beta
    out["corr_book_hold"] = float(ch["book"].corr(ch["hold"]))
    dn = ch["hold"] < ch["hold"].quantile(0.1)
    out["book_mean_on_worst10pct_hold_days"] = float(ch.loc[dn, "book"].mean())
    out["hold_mean_on_worst10pct_hold_days"] = float(ch.loc[dn, "hold"].mean())
    # cases
    rows = []
    for c in coins:
        allr = []
        for w, b in data["bars"][c].items():
            cl = b["close"].values
            for i in range(0, len(cl) - 84, 84):
                allr.append(cl[i + 84] / cl[i] - 1)
        drift = np.mean(allr)
        for w, b in data["bars"][c].items():
            cl = b["close"].values.astype(float)
            f = b["forecast"].fillna(0).values
            al = b["postRebalance_current_allocation"].fillna(0).values
            n = len(cl)
            s = pd.Series(cl)
            r180 = s.pct_change(180).values
            r42 = s.pct_change(42).values
            lr = np.log(s).diff()
            vol42 = lr.rolling(42).std().values
            vol360 = lr.rolling(360).std().values
            ma180 = s.rolling(180).mean().values
            for start in range(0, n, 84):
                end = min(start + 84, n)
                idx = np.where(f[start:end] >= 2)[0]
                if len(idx) == 0:
                    continue
                i = start + idx[0]
                if i + 84 >= n:
                    continue
                r = cl[i + 84] / cl[i] - 1
                mn = cl[i:i + 85].min() / cl[i] - 1
                rows.append(dict(coin=c, window=w, f=f[i], alloc=al[i], r=r, u=r - drift, mn=mn,
                                 r30=r180[i], r7=r42[i], vr=vol42[i] / vol360[i] if vol360[i] > 0 else np.nan,
                                 below_ma=cl[i] / ma180[i] - 1))
    cs = pd.DataFrame(rows)
    out["n_cases"] = len(cs)
    def summ(g):
        n = len(g)
        return pd.Series(dict(n=n, mean_r=g["r"].mean(), mean_u=g["u"].mean(),
                              t=g["u"].mean() / (g["u"].std() / np.sqrt(n)) if n > 2 else np.nan,
                              mean_worst=g["mn"].mean(), share_worst_lt_m20=(g["mn"] < -0.2).mean(),
                              mean_alloc=g["alloc"].mean()))
    for col, nm in [("r30", "prior30d"), ("r7", "prior7d"), ("vr", "vol7d_over_vol60d"), ("below_ma", "price_vs_30d_mean"), ("f", "forecast")]:
        d = cs.dropna(subset=[col]).copy()
        d["q"] = pd.qcut(d[col].rank(method="first"), 5, labels=False)
        out["by_" + nm + "_quintile"] = d.groupby("q").apply(summ).join(d.groupby("q")[col].mean().rename(nm + "_mean")).round(4)
    out["by_coin"] = cs.groupby("coin").apply(summ).round(4)
    # exposure
    al = np.concatenate([b["postRebalance_current_allocation"].fillna(0).values for c in coins for b in data["bars"][c].values()])
    out["share_bars_long"] = float((al > 0.01).mean())
    out["mean_alloc_when_long"] = float(al[al > 0.01].mean())
    # trades
    tr = pd.concat([t.assign(coin=c) for c in coins for t in data["trades"][c].values() if len(t)], ignore_index=True)
    out["n_trades"] = len(tr)
    out["trade_pnl_stats"] = tr["net_profit_loss_percent"].describe().round(3)
    out["trade_duration_days"] = (tr["duration_minutes"] / 1440).describe().round(2)
    return out
