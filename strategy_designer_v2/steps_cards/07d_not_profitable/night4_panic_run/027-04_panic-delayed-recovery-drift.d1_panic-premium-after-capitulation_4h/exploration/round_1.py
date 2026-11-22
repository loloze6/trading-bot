def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars, trades, days = data["bars"], data["trades"], data["days"]
    H = 78
    out = {}
    # normal drift per coin
    drift, usual = {}, {}
    for c in bars:
        rs = []
        for w, b in bars[c].items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - H, H)
            rs += list(cl[idx + H] / cl[idx] - 1)
        drift[c] = np.mean(rs); usual[c] = np.std(rs)
    # entries: forecast goes from 0 to >0
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; hi = b["high"].values; lo = b["low"].values
            f = b["forecast"].fillna(0).values
            ent = np.where((f > 0) & (np.r_[0, f[:-1]] <= 0))[0]
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for i in ent:
                if i + H >= len(cl): continue
                r = cl[i + H] / cl[i] - 1
                rows.append(dict(coin=c, win=w, year=yr[i], f=f[i],
                    fwd=r, unusual=r - drift[c],
                    lag6=cl[i] / cl[i-6] - 1 if i >= 6 else np.nan,
                    stretch=cl[i-6] / cl[i-12] - 1 if i >= 12 else np.nan,
                    prior90=cl[i-12] / cl[i-552] - 1 if i >= 552 else np.nan,
                    prior30=cl[i-12] / cl[i-192] - 1 if i >= 192 else np.nan,
                    fwd_from_stretch_end=cl[i + H - 6] / cl[i - 6] - 1 - drift[c] if i >= 6 else np.nan,
                    fwd6d=cl[min(i+36,len(cl)-1)] / cl[i] - 1,
                    fwd_late=cl[i+H]/cl[i+36]-1,
                    alloc=b["postRebalance_current_allocation"].values[i]))
    e = pd.DataFrame(rows)
    def summ(g):
        return pd.Series(dict(n=len(g), mean_unusual=g.unusual.mean(),
            t=g.unusual.mean() / (g.unusual.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
            mean_fwd=g.fwd.mean(), hit=(g.fwd > 0).mean()))
    out["entries_all"] = summ(e).to_frame().T
    out["by_f_quint"] = e.groupby(pd.qcut(e.f.rank(method="first"), 4, labels=False)).apply(summ)
    out["by_prior90_quart"] = e.dropna(subset=["prior90"]).groupby(pd.qcut(e.prior90.dropna(), 4)).apply(summ)
    out["by_prior30_quart"] = e.dropna(subset=["prior30"]).groupby(pd.qcut(e.prior30.dropna(), 4)).apply(summ)
    out["by_lag6_quart"] = e.dropna(subset=["lag6"]).groupby(pd.qcut(e.lag6.dropna(), 4)).apply(summ)
    out["by_stretch_quart"] = e.dropna(subset=["stretch"]).groupby(pd.qcut(e.stretch.dropna(), 4)).apply(summ)
    out["by_coin"] = e.groupby("coin").apply(summ)
    out["by_year"] = e.groupby("year").apply(summ)
    out["timing"] = pd.Series(dict(from_stretch_end_unusual=e.fwd_from_stretch_end.mean(),
        lag6_mean=e.lag6.mean(), fwd6d=e.fwd6d.mean(), fwd_late=e.fwd_late.mean(), alloc=e.alloc.mean()))
    # book daily returns per window, chained; drawdowns
    dd_rows = []; chain = []
    wins = sorted(set(w for c in days for w in days[c]), key=lambda x: int(x[1:]))
    for w in wins:
        br = pd.concat([days[c][w].set_index("day")["book_return"] for c in days if w in days[c]], axis=1).mean(axis=1).dropna()
        cr = pd.concat([days[c][w].set_index("day")["coin_return"] for c in days if w in days[c]], axis=1).mean(axis=1).dropna()
        ex = pd.concat([bars[c][w].assign(d=pd.to_datetime(bars[c][w].timestamp).dt.floor("D")).groupby("d")["postRebalance_current_allocation"].mean() for c in bars if w in bars[c]], axis=1).mean(axis=1)
        v = (1 + br).cumprod(); dd = v / v.cummax() - 1
        dd_rows.append(dict(win=w, book=(1+br).prod()-1, hold=(1+cr).prod()-1, maxdd=dd.min(),
            exposure=ex.abs().mean(), sharpe=br.mean()/br.std()*np.sqrt(365) if br.std()>0 else np.nan,
            hold_sharpe=cr.mean()/cr.std()*np.sqrt(365)))
        chain.append(br)
    out["by_window"] = pd.DataFrame(dd_rows).set_index("win")
    ch = pd.concat(chain, ignore_index=True); v = (1+ch).cumprod(); dd = v/v.cummax()-1
    out["chain"] = pd.Series(dict(yearly=(v.iloc[-1])**(365/len(ch))-1, maxdd=dd.min(), days=len(ch)))
    # trades
    tr = pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c] if len(trades[c][w])])
    out["trades"] = pd.Series(dict(n=len(tr), mean_net=tr.net_profit_loss_percent.mean(), mean_gross=tr.profit_loss_percent.mean(),
        hit=(tr.net_profit_loss_percent>0).mean(), dur_days=tr.duration_minutes.mean()/1440,
        worst=tr.net_profit_loss_percent.min(), p10=tr.net_profit_loss_percent.quantile(.1)))
    return out
