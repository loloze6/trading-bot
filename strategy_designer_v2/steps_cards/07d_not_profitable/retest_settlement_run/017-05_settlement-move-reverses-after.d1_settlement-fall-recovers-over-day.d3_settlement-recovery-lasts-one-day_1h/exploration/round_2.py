def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    def q(x, k):
        return pd.qcut(x.rank(method="first"), k, labels=False)
    rows = []; allrows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values.astype(float)
            n = len(df)
            reg = (df["regime"] == "mean_reversion").values
            fc = df["debug_info.components.fall2h.post_pipeline_value"].values.astype(float)
            s = pd.Series(cl)
            tr30 = (s / s.shift(720) - 1).values
            tr7 = (s / s.shift(168) - 1).values
            lr = np.log(s).diff()
            vol = lr.rolling(168).std().values
            volL = lr.rolling(1440).std().values
            cell = np.arange(n) // 24
            seen = set()
            ts = pd.to_datetime(df["timestamp"])
            for i in np.where(reg)[0]:
                if cell[i] in seen: continue
                seen.add(cell[i])
                r = {h: (cl[i+h]/cl[i]-1 if i+h < n else np.nan) for h in (6, 12, 24, 48)}
                rows.append(dict(coin=c, w=w, f=fc[i], r6=r[6], r12=r[12], r24=r[24], r48=r[48],
                                 tr30=tr30[i], tr7=tr7[i],
                                 vr=(vol[i]/volL[i]) if (volL[i] == volL[i] and volL[i] > 0) else np.nan,
                                 hour=(ts.iloc[i].hour+1) % 24))
            for i in np.arange(0, n-24, 24):
                allrows.append(dict(coin=c, r24=cl[i+24]/cl[i]-1, tr30=tr30[i], tr7=tr7[i]))
    cs = pd.DataFrame(rows); al = pd.DataFrame(allrows)
    drift = al.groupby("coin")["r24"].mean(); sd = al.groupby("coin")["r24"].std()
    cs["d"] = cs.coin.map(drift); cs["sd"] = cs.coin.map(sd)
    cs["u24"] = cs.r24 - cs.d
    cs["u2d"] = (1+cs.r48)/(1+cs.r24) - 1 - cs.d
    def agg(g):
        g = g.dropna(subset=["u24"])
        m = len(g)
        return pd.Series(dict(n=m, f=g.f.mean(), tot24=g.r24.mean(), u24=g.u24.mean(),
                              t24=g.u24.mean()/(g.u24.std()/np.sqrt(m)) if m > 2 else np.nan,
                              strength=(g.u24/g.sd).mean(), r6=g.r6.mean(), r12=g.r12.mean(),
                              u2d=g.u2d.mean()))
    out = {}
    pos_ = cs[cs.f > 0].copy()
    pos_["q"] = q(pos_.f, 5)
    out["by_forecast_quintile"] = pos_.groupby("q").apply(agg)
    out["forecast_zero"] = agg(cs[~(cs.f > 0)]).to_frame().T
    cs["sig"] = cs.f > 0
    cs["trend30"] = np.sign(cs.tr30); cs["trend7"] = np.sign(cs.tr7)
    out["by_trend30_sig"] = cs.groupby(["trend30", "sig"]).apply(agg)
    out["by_trend7_sig"] = cs.groupby(["trend7", "sig"]).apply(agg)
    cs["volq"] = q(cs.vr.fillna(cs.vr.median()), 3)
    out["by_volratio_sig"] = cs.groupby(["volq", "sig"]).apply(agg)
    out["by_hour_sig"] = cs.groupby(["hour", "sig"]).apply(agg)
    out["by_coin_sig"] = cs[cs.sig].groupby("coin").apply(agg)
    top = pos_[pos_.q >= 3]
    out["top2q_by_trend30"] = top.groupby(np.sign(top.tr30)).apply(agg)
    # book daily
    dl = []
    for c in days:
        for w, d in days[c].items():
            dd = d.copy(); dd["coin"] = c; dd["w"] = w; dl.append(dd)
    D = pd.concat(dl)
    D["wn"] = D.w.str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(b=("book_return", "mean"), h=("coin_return", "mean")).dropna().sort_index()
    out["book_vs_hold"] = pd.DataFrame({"mean": [B.b.mean(), B.h.mean()], "std": [B.b.std(), B.h.std()],
        "sharpe": [B.b.mean()/B.b.std()*np.sqrt(365), B.h.mean()/B.h.std()*np.sqrt(365)]}, index=["book", "hold"])
    out["corr_book_hold"] = float(B.b.corr(B.h))
    out["beta_book_on_hold"] = float(np.polyfit(B.h, B.b, 1)[0])
    B["hq"] = q(B.h, 5)
    out["book_by_hold_quintile"] = B.groupby("hq")[["b", "h"]].mean()
    v = (1+B.b).cumprod().values; hv = (1+B.h).cumprod().values
    peak = np.maximum.accumulate(v); dd = v/peak-1
    j = int(np.argmin(dd)); i0 = int(np.argmax(v[:j+1]))
    out["deepest_fall"] = pd.DataFrame({"book_fall": [dd[j]], "days": [j-i0],
        "hold_over_same": [hv[j]/hv[i0]-1], "window_start": [B.index[i0][0]], "window_end": [B.index[j][0]]})
    # 5 worst 30-day stretches of book vs hold
    out["by_window_book_hold"] = B.groupby(level=0)[["b", "h"]].sum().describe().T
    # trades
    tl = []
    for c in trades:
        for w, t in trades[c].items():
            if len(t): tt = t.copy(); tt["coin"] = c; tl.append(tt)
    T = pd.concat(tl)
    T["dur_h"] = T.duration_minutes/60
    T["fq"] = q(T.entry_forecast.astype(float), 5)
    out["trades_by_entry_forecast"] = T.groupby("fq").agg(n=("dur_h", "size"), f=("entry_forecast", "mean"),
        dur_h=("dur_h", "mean"), pl=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    out["trade_side_counts"] = T.side.value_counts()
    return out
