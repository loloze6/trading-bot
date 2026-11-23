def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    H = [6, 12, 24, 36, 48, 72]
    rows = []
    for coin in bars:
        # drift per horizon
        drift = {}; usual = {}
        for h in H:
            rs = []
            for w, b in bars[coin].items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs); drift[h] = rs.mean(); usual[h] = rs.std()
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            f = b["forecast"].fillna(0).values
            c = b["close"].values
            nz = np.where(f != 0)[0]
            seen = set()
            for i in nz:
                wk = (ts[i] + pd.Timedelta(hours=1)).isocalendar()[:2]
                if (wk) in seen: continue
                seen.add(wk)
                r = {"coin": coin, "w": w, "year": ts[i].year, "f": f[i], "side": np.sign(f[i]),
                     "alloc": b["postRebalance_current_allocation"].iloc[i]}
                # weekend return and 30-day return
                if i >= 48: r["wk48"] = c[i] / c[i-48] - 1
                if i >= 720: r["mo720"] = c[i] / c[i-720] - 1
                if i >= 168: r["wk_week"] = c[i-48]/c[i-168]-1
                for h in H:
                    if i + h < len(c):
                        tot = (c[i+h]/c[i]-1)*np.sign(f[i])
                        r[f"tot{h}"] = tot
                        r[f"unu{h}"] = tot - drift[h]*np.sign(f[i])
                # max adverse within 12
                if i + 12 < len(c):
                    r["mae12"] = (b["low"].values[i+1:i+13].min()/c[i]-1) if f[i]>0 else -(b["high"].values[i+1:i+13].max()/c[i]-1)
                rows.append(r)
    cs = pd.DataFrame(rows)
    out = {}
    def summ(g):
        d = {}
        for h in H:
            x = g[f"unu{h}"].dropna()
            d[f"u{h}"] = x.mean(); d[f"t{h}"] = x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        d["n"] = len(g); return pd.Series(d)
    out["by_horizon_all"] = summ(cs).to_frame().T
    out["by_side"] = cs.groupby("side").apply(summ)
    out["by_coin"] = cs.groupby("coin").apply(summ)
    out["by_year"] = cs.groupby("year").apply(summ)
    cs["fq"] = pd.qcut(cs["f"].abs(), 4, labels=False, duplicates="drop")
    out["by_absf_quartile"] = cs.groupby("fq").apply(summ)
    cs["moq"] = pd.qcut((cs["mo720"]*cs["side"]), 3, labels=False, duplicates="drop")
    out["by_trend_strength_tercile"] = cs.groupby("moq").apply(summ)
    out["mae12"] = cs["mae12"].describe().to_frame()
    out["alloc_abs"] = cs["alloc"].abs().describe().to_frame()
    # trades
    tl = []
    for coin in trades:
        for w, t in trades[coin].items():
            if len(t): tt = t.copy(); tt["coin"]=coin; tl.append(tt)
    T = pd.concat(tl)
    T["year"] = pd.to_datetime(T["entry_time"]).dt.year
    out["trades_by_side"] = T.groupby("side").agg(n=("net_profit_loss_percent","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), dur_h=("duration_minutes", lambda x: x.mean()/60))
    out["trades_by_year"] = T.groupby("year").agg(n=("net_profit_loss_percent","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"))
    # book daily, drawdown
    dl = []
    for coin in days:
        for w, d in days[coin].items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["w"]=w; dl.append(dd)
    D = pd.concat(dl)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"]).agg(br=("book_return","mean"), cr=("coin_return","mean")).dropna().reset_index().sort_values(["wn","day"])
    v = (1+B["br"]).cumprod().values
    peak = np.maximum.accumulate(v); ddn = v/peak-1
    B["dd"] = ddn; B["year"] = pd.to_datetime(B["day"]).dt.year
    out["book_by_year"] = B.groupby("year").agg(book_sum=("br","sum"), hold_sum=("cr","sum"), min_dd=("dd","min"), ndays=("br","size"))
    out["book_by_window"] = B.groupby("wn").agg(book_sum=("br","sum"), hold_sum=("cr","sum"), min_dd=("dd","min"))
    out["worst_days_book"] = B.nsmallest(10,"br")[["wn","br","cr"]].reset_index(drop=True)
    out["maxdd"] = float(ddn.min())
    return out
