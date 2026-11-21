def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    H = 26
    rows = []
    drift = {}
    usual = {}
    for c in bars:
        fr = []
        for w, b in bars[c].items():
            cl = b["close"].values
            for i in range(0, len(cl) - H, H):
                fr.append(cl[i + H] / cl[i] - 1)
        drift[c] = np.mean(fr) if fr else np.nan
        usual[c] = np.std(fr) if fr else np.nan
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(b)
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for i in range(0, n - H, H):
                f = b["forecast"].iloc[i]
                r = cl[i + H] / cl[i] - 1
                # past 26d return, 30d vol
                p26 = cl[i] / cl[i - 26] - 1 if i >= 26 else np.nan
                lr = np.diff(np.log(cl[max(0, i - 30):i + 1]))
                v30 = np.std(lr) if len(lr) >= 20 else np.nan
                rows.append(dict(coin=c, win=w, year=yr[i], f=f, r=r, ex=r - drift[c], p26=p26, v30=v30,
                                 slope=b.get("debug_info.components.slope_size.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                                 volraw=b.get("debug_info.components.vol30.last_history_value", pd.Series([np.nan]*n)).iloc[i]))
    df = pd.DataFrame(rows)
    act = df[df.f < 0].copy()
    out = {}
    out["cases active/all"] = f"{len(act)}/{len(df)}; mean fwd r active {act.r.mean():.4f} t {stats.ttest_1samp(act.r,0).statistic:.2f}; inactive {df[df.f>=0].r.mean():.4f}"
    out["active by year"] = act.groupby("year").agg(n=("r", "size"), r=("r", "mean"), ex=("ex", "mean"))
    out["inactive by year"] = df[df.f >= 0].groupby("year").agg(n=("r", "size"), r=("r", "mean"))
    act["fq"] = pd.qcut(act.f, 4, labels=False, duplicates="drop")
    out["by forecast quartile (0=most short)"] = act.groupby("fq").agg(n=("r", "size"), f=("f", "mean"), r=("r", "mean"), ex=("ex", "mean"))
    a2 = act.dropna(subset=["p26"]).copy()
    a2["pq"] = pd.qcut(a2.p26, 4, labels=False, duplicates="drop")
    out["by past26 return quartile"] = a2.groupby("pq").agg(n=("r", "size"), p26=("p26", "mean"), r=("r", "mean"), ex=("ex", "mean"))
    a3 = act.dropna(subset=["v30"]).copy()
    a3["vq"] = pd.qcut(a3.v30, 4, labels=False, duplicates="drop")
    out["by vol30 quartile"] = a3.groupby("vq").agg(n=("r", "size"), v=("v30", "mean"), r=("r", "mean"), ex=("ex", "mean"))
    a4 = act.dropna(subset=["slope"]).copy()
    a4["sq"] = pd.qcut(a4.slope, 4, labels=False, duplicates="drop")
    out["by raw slope quartile (0=steepest fall)"] = a4.groupby("sq").agg(n=("r", "size"), s=("slope", "mean"), r=("r", "mean"), ex=("ex", "mean"))
    out["by coin"] = act.groupby("coin").agg(n=("r", "size"), r=("r", "mean"), drift=("ex", lambda x: 0)).drop(columns="drift").join(pd.Series(drift, name="drift"))
    # book daily
    bd = []
    for c in days:
        for w, d in days[c].items():
            b = bars[c][w].reset_index(drop=True)
            pos = b["postRebalance_current_allocation"].values
            cr = b["close"].pct_change().shift(-1).values
            bd.append(dict(coin=c, win=w, book=d.book_return.mean(), coin_r=d.coin_return.mean(), n=d.book_return.notna().sum(),
                           posmean=np.nanmean(pos), gross=np.nansum(pos[:-1] * cr[:-1]), mkt=np.nansum(pos[:-1]) * 0))
    bdf = pd.DataFrame(bd)
    allday = pd.concat([d for c in days for d in days[c].values()])
    out["book mean daily / coin mean daily"] = f"{allday.book_return.mean():.6f} / {allday.coin_return.mean():.6f}; mean pos {np.nanmean(np.concatenate([bars[c][w]['postRebalance_current_allocation'].values for c in bars for w in bars[c]])):.3f}"
    tr = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values() if len(t)])
    out["trades"] = tr.groupby("side").agg(n=("net_profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"), dur_days=("duration_minutes", lambda x: x.mean() / 1440))
    out["trade worst/best decile mean net"] = f"{tr.net_profit_loss_percent.quantile(0.1):.2f} / {tr.net_profit_loss_percent.quantile(0.9):.2f}; share winners {(tr.net_profit_loss_percent>0).mean():.2f}"
    return out
