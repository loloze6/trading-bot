def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # ---- daily book
    rows = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin"] = c; d["window"] = w
            rows.append(d[["coin","window","day","book_return","coin_return"]])
    D = pd.concat(rows).dropna()
    book = D.groupby(["window","day"]).agg(b=("book_return","mean"), h=("coin_return","mean")).reset_index()
    out["book_mean_sd_n"] = pd.Series({"mean": book.b.mean(), "sd": book.b.std(), "n": len(book),
                                      "hold_mean": book.h.mean(),
                                      "sharpe": book.b.mean()/book.b.std()*np.sqrt(365)})
    # ---- bar-level decomposition: drift vs timing
    br = []
    for c in bars:
        mus = []
        for w, b in bars[c].items():
            r = b.close.pct_change(); mus.append(r.dropna())
        mu = pd.concat(mus).mean()
        for w, b in bars[c].items():
            b = b.copy()
            r = b.close.pct_change().shift(-1)
            pos = b.postRebalance_current_allocation.fillna(0)
            ts = pd.to_datetime(b.timestamp)
            fc = b.forecast.fillna(0)
            ret60 = b.close/b.close.shift(60)-1
            vol30 = b.close.pct_change().rolling(30).std()
            br.append(pd.DataFrame({"coin": c, "window": w, "year": ts.dt.year, "pos": pos,
                                    "gain": pos*r, "drift": pos*mu, "r": r, "mu": mu, "fc": fc,
                                    "vol30": vol30, "regime": b.regime}))
    B = pd.concat(br).dropna(subset=["r"])
    B["timing"] = B.gain - B.drift
    # agitation vs coin's pooled median of vol30 (approximate)
    B["agit"] = B.groupby("coin").vol30.transform(lambda s: s > s.median())
    inpos = B[B.pos.abs() > 1e-9]
    out["decomp_sum"] = pd.Series({"gain_sum": B.gain.sum(), "drift_sum": B.drift.sum(), "timing_sum": B.timing.sum(),
                                   "timing_t": stats.ttest_1samp(inpos.timing, 0).statistic, "n_inpos": len(inpos)})
    out["by_coin"] = B.groupby("coin").agg(gain=("gain","sum"), drift=("drift","sum"), timing=("timing","sum"),
                                           posdays=("pos", lambda s: (s.abs()>1e-9).sum()))
    out["by_window"] = B.groupby("window").agg(gain=("gain","sum"), drift=("drift","sum"), timing=("timing","sum"),
                                               hold=("r","sum"), posdays=("pos", lambda s: (s.abs()>1e-9).sum()))
    out["by_year"] = B.groupby("year").agg(gain=("gain","sum"), drift=("drift","sum"), timing=("timing","sum"))
    out["by_agit_inpos"] = inpos.groupby("agit").agg(gain=("gain","sum"), timing=("timing","sum"),
                                                     mean_gain=("gain","mean"), n=("gain","size"))
    out["by_regime"] = B.groupby("regime").agg(gain=("gain","sum"), n=("gain","size"), posn=("pos", lambda s: (s.abs()>1e-9).sum()))
    # ---- forecast grading at several horizons on non-overlapping grid
    res = []
    for h in [3, 7, 14, 30]:
        cases = []
        for c in bars:
            allr = []
            for w, b in bars[c].items():
                idx = np.arange(0, len(b)-h, h)
                allr.append(b.close.values[idx+h]/b.close.values[idx]-1)
            m = np.concatenate(allr).mean() if allr else np.nan
            for w, b in bars[c].items():
                idx = np.arange(0, len(b)-h, h)
                fr = b.close.values[idx+h]/b.close.values[idx]-1
                raw = b.get("debug_info.components.swing_rise.last_history_value")
                f = b.forecast.values[idx]
                cases.append(pd.DataFrame({"f": f, "ex": fr-m, "raw": raw.values[idx] if raw is not None else np.nan,
                                           "unk": (b.regime.values[idx]=="unknown")}))
        C = pd.concat(cases)
        P = C[(C.f > 0)]
        sl = stats.linregress(P.f, P.ex) if len(P) > 5 else None
        Q = C[C.unk & C.raw.notna()]
        sl2 = stats.linregress(Q.raw, Q.ex) if len(Q) > 5 else None
        res.append({"h": h, "n_f>0": len(P), "mean_ex_f>0": P.ex.mean(), "t_mean": stats.ttest_1samp(P.ex,0).statistic,
                    "slope_fc": sl.slope if sl else np.nan, "t_slope_fc": sl.slope/sl.stderr if sl else np.nan,
                    "n_inprof_raw": len(Q), "slope_raw": sl2.slope if sl2 else np.nan,
                    "t_slope_raw": sl2.slope/sl2.stderr if sl2 else np.nan,
                    "mean_ex_inprof_f0": C[C.unk & (C.f<=0)].ex.mean(), "n_inprof_f0": (C.unk & (C.f<=0)).sum()})
    out["grading_by_h"] = pd.DataFrame(res)
    # forecast quintiles at h=14 in-profile
    h=14; cases=[]
    for c in bars:
        allr=[]
        for w,b in bars[c].items():
            idx=np.arange(0,len(b)-h,h); allr.append(b.close.values[idx+h]/b.close.values[idx]-1)
        m=np.concatenate(allr).mean()
        for w,b in bars[c].items():
            idx=np.arange(0,len(b)-h,h)
            raw=b["debug_info.components.swing_rise.last_history_value"].values[idx]
            cases.append(pd.DataFrame({"raw":raw,"ex":b.close.values[idx+h]/b.close.values[idx]-1-m,
                                       "unk":b.regime.values[idx]=="unknown"}))
    C=pd.concat(cases); Q=C[C.unk & C.raw.notna()].copy()
    Q["q"]=pd.qcut(Q.raw,5,labels=False)
    out["raw_quintile_h14"]=Q.groupby("q").agg(raw=("raw","mean"),ex=("ex","mean"),n=("ex","size"),
                                               t=("ex",lambda s: s.mean()/s.std()*np.sqrt(len(s))))
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for w,t in data["trades"][c].items() if len(t)])
    p = T.net_profit_loss_percent.sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(p), "sum": p.sum(), "top5": p.head(5).sum(), "top10pct": p.head(max(1,len(p)//10)).sum(),
                               "win_share": (p>0).mean(), "median": p.median()})
    return out
