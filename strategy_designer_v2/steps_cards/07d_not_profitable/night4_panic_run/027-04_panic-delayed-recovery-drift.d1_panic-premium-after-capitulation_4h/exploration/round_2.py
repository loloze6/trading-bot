def explore(data):
    import numpy as np, pandas as pd
    bars, days = data["bars"], data["days"]
    H = 78
    out = {}
    drift = {}
    for c in bars:
        rs = []
        for w, b in bars[c].items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - H, H)
            rs += list(cl[idx + H] / cl[idx] - 1)
        drift[c] = np.mean(rs)
    rows = []; barrows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; lo = b["low"].values; hi = b["high"].values
            f = b["forecast"].fillna(0).values
            al = b["postRebalance_current_allocation"].fillna(0).values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            n = len(cl)
            # bar-level: position, prior 90d return, next-bar return
            p90 = np.full(n, np.nan); p90[540:] = cl[540:] / cl[:-540] - 1
            r1 = np.r_[cl[1:] / cl[:-1] - 1, np.nan]
            p7 = np.full(n, np.nan); p7[42:] = cl[42:] / cl[:-42] - 1
            barrows.append(pd.DataFrame(dict(coin=c, win=w, year=yr, al=al, p90=p90, p7=p7, gain=al * r1, f=f)))
            ent = np.where((f > 0) & (np.r_[0, f[:-1]] <= 0))[0]
            for i in ent:
                if i + H >= n or i < 552: continue
                r = cl[i + H] / cl[i] - 1
                # rebound from 30d low at entry
                lo30 = lo[max(0, i - 180):i + 1].min()
                rows.append(dict(coin=c, win=w, year=yr[i], f=f[i], unusual=r - drift[c],
                                 prior90=cl[i - 12] / cl[i - 552] - 1,
                                 reb=cl[i] / lo30 - 1, p7=cl[i] / cl[i - 42] - 1,
                                 mae=lo[i:i + H + 1].min() / cl[i] - 1))
    e = pd.DataFrame(rows)
    B = pd.concat(barrows, ignore_index=True)
    def summ(g):
        return pd.Series(dict(n=len(g), mean_unusual=g.unusual.mean(),
                              t=g.unusual.mean() / (g.unusual.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                              hit=(g.unusual > 0).mean(), mae=g.mae.mean()))
    deep = e[e.prior90 <= -0.396]
    rest = e[e.prior90 > -0.396]
    out["deep_by_year"] = deep.groupby("year").apply(summ)
    out["deep_by_coin"] = deep.groupby("coin").apply(summ)
    out["prior90_deciles"] = e.groupby(pd.qcut(e.prior90, 8)).apply(summ)
    out["rest_by_reb"] = rest.groupby(pd.qcut(rest.reb, 4)).apply(summ)
    out["deep_by_reb"] = deep.groupby(pd.qcut(deep.reb, 3)).apply(summ)
    out["all_by_p7"] = e.groupby(pd.qcut(e.p7, 4)).apply(summ)
    # bar-level: where the book's gain comes from by prior 90d return of the bar
    Bv = B.dropna(subset=["gain"])
    Bv["p90q"] = pd.cut(Bv.p90, [-1, -0.4, -0.2, 0, 0.5, 100])
    out["bars_by_p90"] = Bv.groupby("p90q").agg(bars=("gain", "size"), mean_alloc=("al", "mean"),
                                                 gain_sum=("gain", "sum"), gain_mean=("gain", "mean"))
    # long bars with forecast 0 (held after signal ended) vs forecast>0
    Bl = Bv[Bv.al > 0.01]
    out["long_bars_by_forecast_on"] = Bl.groupby(Bl.f > 0).agg(bars=("gain", "size"), gain_sum=("gain", "sum"), gain_mean=("gain", "mean"))
    out["long_bars_by_p7"] = Bl.groupby(pd.qcut(Bl.p7, 4)).agg(bars=("gain", "size"), gain_sum=("gain", "sum"), gain_mean=("gain", "mean"))
    # worst windows: exposure by p90 bucket
    ww = Bv[Bv.win.isin(["w2", "w7", "w9", "w14"])]
    out["worst_windows_p90"] = ww.groupby(["win", "p90q"]).agg(bars=("gain", "size"), mean_alloc=("al", "mean"), gain_sum=("gain", "sum"))
    return out
