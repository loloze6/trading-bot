def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    rows = []; allrows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            n = len(df)
            reg = (df["regime"] == "mean_reversion").values
            fc = df["debug_info.components.fall2h.post_pipeline_value"].values
            raw = df["debug_info.components.fall2h.last_history_value"].values
            s = pd.Series(cl)
            tr30 = (s / s.shift(720) - 1).values
            tr7 = (s / s.shift(168) - 1).values
            lr = np.log(s).diff()
            vol = lr.rolling(168).std().values
            volL = lr.rolling(1440).std().values
            pos = np.arange(n)
            cell = pos // 24
            seen = set()
            for i in np.where(reg)[0]:
                if cell[i] in seen: continue
                seen.add(cell[i])
                r = {}
                for h in (6, 12, 24, 48, 72):
                    r[h] = cl[i+h]/cl[i]-1 if i+h < n else np.nan
                rows.append(dict(coin=c, w=w, f=fc[i], raw=raw[i], r6=r[6], r12=r[12], r24=r[24],
                                 r48=r[48], r72=r[72], tr30=tr30[i], tr7=tr7[i],
                                 vr=vol[i]/volL[i] if volL[i] else np.nan,
                                 hour=(df["timestamp"].iloc[i].hour+1) % 24))
            # all non-overlapping 24 grid for drift and usual move
            idx = np.arange(0, n-24, 24)
            for i in idx:
                allrows.append(dict(coin=c, r24=cl[i+24]/cl[i]-1, tr30=tr30[i], tr7=tr7[i]))
    cs = pd.DataFrame(rows); al = pd.DataFrame(allrows)
    drift = al.groupby("coin")["r24"].mean(); sd = al.groupby("coin")["r24"].std()
    cs["d"] = cs["coin"].map(drift); cs["sd"] = cs["coin"].map(sd)
    for h in ("r24",):
        cs["u24"] = cs["r24"] - cs["d"]
    cs["u48"] = (cs["r48"]) - 2*cs["d"]
    cs["u2d"] = (1+cs["r48"])/(1+cs["r24"]) - 1 - cs["d"]
    pos_ = cs[cs.f > 0].copy()
    pos_["q"] = pd.qcut(pos_["f"], 5, labels=False)
    def agg(g):
        return pd.Series(dict(n=len(g), f=g.f.mean(), tot24=g.r24.mean(), u24=g.u24.mean(),
                              t24=g.u24.mean()/(g.u24.std()/np.sqrt(len(g))),
                              strength=(g.u24/g.sd).mean(), r6=g.r6.mean(), r12=g.r12.mean(),
                              u2d=g.u2d.mean(), tot48=g.r48.mean()))
    out = {}
    out["by_forecast_quintile"] = pos_.groupby("q").apply(agg)
    out["forecast_zero_cases"] = agg(cs[cs.f <= 0]).to_frame().T
    cs["trend30"] = np.sign(cs.tr30); cs["trend7"] = np.sign(cs.tr7)
    cs["sig"] = cs.f > 0
    out["by_trend30_sig"] = cs.groupby(["trend30", "sig"]).apply(agg)
    out["by_trend7_sig"] = cs.groupby(["trend7", "sig"]).apply(agg)
    cs["volq"] = pd.qcut(cs.vr, 3, labels=False)
    out["by_volratio_sig"] = cs.groupby(["volq", "sig"]).apply(agg)
    out["by_hour_sig"] = cs.groupby(["hour", "sig"]).apply(agg)
    out["by_coin_sig"] = cs[cs.sig].groupby("coin").apply(agg)
    top = pos_[pos_.q == 4]
    out["top_quintile_trend30"] = top.groupby(np.sign(top.tr30)).apply(agg)
    # book daily: mean across coins per (window, day)
    dl = []
    for c in days:
        for w, d in days[c].items():
            dd = d.copy(); dd["coin"] = c; dd["w"] = w; dl.append(dd)
    D = pd.concat(dl)
    B = D.groupby(["w", "day"]).agg(b=("book_return", "mean"), h=("coin_return", "mean")).dropna()
    out["book_vs_hold_daily"] = pd.DataFrame({"mean": [B.b.mean(), B.h.mean()], "std": [B.b.std(), B.h.std()],
        "sharpe": [B.b.mean()/B.b.std()*np.sqrt(365), B.h.mean()/B.h.std()*np.sqrt(365)]}, index=["book", "hold"])
    out["corr_book_hold"] = float(B.b.corr(B.h))
    B["hq"] = pd.qcut(B.h, 5, labels=False)
    out["book_by_hold_quintile"] = B.groupby("hq")[["b", "h"]].mean()
    return out
