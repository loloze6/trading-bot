def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = 18
    # coin mean 18-bar return (drift) per coin, non-overlapping
    rows = []
    book_d = []; mkt_d = []
    for coin, wins in bars.items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(allr); sd = np.std(allr)
        # daily mean coin return for market part
        dret = pd.concat([d["coin_return"] for d in days[coin].values()]).mean()
        for w, b in wins.items():
            c = b["close"].values
            n = len(c)
            # trailing 30-day (180 bar) return, run length
            up = (np.diff(c, prepend=np.nan) > 0)
            runlen = np.zeros(n); r = 0
            for i in range(n):
                r = r + 1 if up[i] else 0; runlen[i] = r
            tr180 = pd.Series(c).pct_change(180).values
            tr42 = pd.Series(c).pct_change(42).values
            fc = b["forecast"].values
            rg = b.get("debug_info.components.run_gain.last_history_value", pd.Series(np.nan, index=b.index)).values
            vf = b.get("debug_info.components.vol_fade.last_history_value", pd.Series(np.nan, index=b.index)).values
            for g in range(0, n - H, H):
                seg = fc[g:g+H]
                cand = np.where(seg <= -2)[0]
                if len(cand) == 0: continue
                i = g + cand[0]
                if i + H >= n: continue
                ret = c[i+H] / c[i] - 1
                rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 fc=fc[i], rg=rg[i], vf=vf[i], runlen=runlen[i],
                                 tr180=tr180[i], tr42=tr42[i],
                                 unusual=-(ret - drift), total=-ret, strength=-(ret-drift)/sd))
            d = days[coin][w]
            alloc_day = b.set_index(pd.to_datetime(b["timestamp"]))["postRebalance_current_allocation"].resample("1D").mean()
            book_d.append(d["book_return"].dropna().values)
    df = pd.DataFrame(rows)
    def summ(g):
        return pd.Series(dict(n=len(g), unusual=g.unusual.mean(), t=g.unusual.mean()/(g.unusual.std()/np.sqrt(len(g))), total=g.total.mean(), strength=g.strength.mean()))
    out = {}
    out["all"] = summ(df)
    df["fcq"] = pd.qcut(df.fc.rank(method="first"), 5, labels=False)
    out["by_forecast_q (0=most neg)"] = df.groupby("fcq").apply(summ)
    df["rlq"] = pd.qcut(df.runlen.rank(method="first"), 5, labels=False)
    out["by_runlen_q"] = df.groupby("rlq").apply(summ)
    out["runlen_mean_by_q"] = df.groupby("rlq").runlen.mean()
    df["trq"] = pd.qcut(df.tr180.rank(method="first"), 5, labels=False)
    out["by_trailing30d_ret_q"] = df.dropna(subset=["tr180"]).groupby("trq").apply(summ)
    df["t7q"] = pd.qcut(df.tr42.rank(method="first"), 5, labels=False)
    out["by_trailing7d_ret_q"] = df.dropna(subset=["tr42"]).groupby("t7q").apply(summ)
    df["vfq"] = pd.qcut(df.vf.rank(method="first"), 5, labels=False)
    out["by_volfade_q"] = df.groupby("vfq").apply(summ)
    out["by_year"] = df.groupby("year").apply(summ)
    # book: daily
    bk = np.concatenate(book_d)
    out["book_daily"] = pd.Series(dict(mean=bk.mean(), sd=bk.std(), sharpe=bk.mean()/bk.std()*np.sqrt(365)))
    # allocation share short, mean allocation
    al = pd.concat([b["postRebalance_current_allocation"] for wins in bars.values() for b in wins.values()])
    out["alloc"] = pd.Series(dict(mean=al.mean(), share_short=(al<0).mean(), mean_when_short=al[al<0].mean()))
    tr = pd.concat([t for wins in data["trades"].values() for t in wins.values()])
    out["trades"] = pd.Series(dict(n=len(tr), gross=tr.profit_loss_percent.mean(), net=tr.net_profit_loss_percent.mean(), win=(tr.profit_loss_percent>0).mean(), dur_h=tr.duration_minutes.mean()/60))
    return out
