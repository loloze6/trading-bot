def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # ---- daily book vs holding
    rows = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin"] = c; d["window"] = w
            rows.append(d[["coin","window","day","book_return","coin_return"]])
    D = pd.concat(rows).dropna()
    book = D.groupby(["window","day"]).agg(b=("book_return","mean"), h=("coin_return","mean")).reset_index()
    out["book"] = pd.Series({"mean": book.b.mean(), "sd": book.b.std(), "n_days": len(book),
                             "hold_mean": book.h.mean(), "sharpe": book.b.mean()/book.b.std()*np.sqrt(365),
                             "hold_sharpe": book.h.mean()/book.h.std()*np.sqrt(365)})
    out["book_by_window"] = book.groupby("window").agg(b=("b","sum"), h=("h","sum"), n=("b","size"))
    # ---- bar level: drift vs timing, features recomputed from prices
    br = []
    for c in bars:
        mu = pd.concat([b.close.pct_change().dropna() for b in bars[c].values()]).mean()
        for w, b in bars[c].items():
            r1 = b.close.pct_change()
            r = r1.shift(-1)
            pos = b.postRebalance_current_allocation.fillna(0)
            ts = pd.to_datetime(b.timestamp)
            ret20 = b.close/b.close.shift(20)-1
            sd20 = r1.rolling(20).std()
            vol30 = r1.rolling(30).std()
            br.append(pd.DataFrame({"coin": c, "window": w, "year": ts.dt.year.values, "pos": pos.values,
                                    "gain": (pos*r).values, "drift": (pos*mu).values, "r": r.values, "mu": mu,
                                    "fc": b.forecast.fillna(0).values,
                                    "ss": (ret20/(sd20*np.sqrt(20))).values, "ret20": ret20.values,
                                    "vol30": vol30.values, "unk": (b.regime=="unknown").values}))
    B = pd.concat(br, ignore_index=True)
    B = B[B.r.notna()]
    B["timing"] = B.gain - B.drift
    B["agit"] = B.groupby("coin").vol30.transform(lambda s: s > s.median())
    inpos = B[B.pos.abs() > 1e-9]
    out["decomp"] = pd.Series({"gain_sum": B.gain.sum(), "drift_sum": B.drift.sum(), "timing_sum": B.timing.sum(),
                               "timing_t_inpos": stats.ttest_1samp(inpos.timing, 0).statistic, "n_inpos": len(inpos),
                               "mean_pos_inpos": inpos.pos.mean()})
    out["by_coin"] = B.groupby("coin").agg(gain=("gain","sum"), drift=("drift","sum"), timing=("timing","sum"),
                                           posdays=("pos", lambda s: (s.abs()>1e-9).sum()))
    out["by_window"] = B.groupby("window").agg(gain=("gain","sum"), drift=("drift","sum"), timing=("timing","sum"),
                                               posdays=("pos", lambda s: (s.abs()>1e-9).sum()))
    out["by_agit_inpos"] = inpos.groupby("agit").agg(gain=("gain","sum"), timing=("timing","sum"),
                                                     mean_gain=("gain","mean"), n=("gain","size"))
    # in-profile: being in (f>0) vs not (f==0), daily excess r-mu
    P = B[B.unk].copy(); P["ex"] = P.r - P.mu
    out["inprof_daily_ex_by_f"] = P.groupby(P.fc > 0).agg(ex=("ex","mean"), n=("ex","size"),
                                   t=("ex", lambda s: s.mean()/s.std()*np.sqrt(len(s))))
    out["outprof_daily_ex"] = pd.Series({"ex": (B[~B.unk].r - B[~B.unk].mu).mean(), "n": (~B.unk).sum()})
    # ---- grid cases at several horizons, grading by recomputed swing-scaled rise
    res = []; qtabs = {}
    for h in [3, 7, 14, 28]:
        cases = []
        for c in bars:
            allr = []
            for w, b in bars[c].items():
                idx = np.arange(0, len(b)-h, h)
                allr.append(b.close.values[idx+h]/b.close.values[idx]-1)
            m = np.concatenate(allr).mean()
            for w, b in bars[c].items():
                idx = np.arange(0, len(b)-h, h)
                r1 = b.close.pct_change()
                ss = (b.close/b.close.shift(20)-1)/(r1.rolling(20).std()*np.sqrt(20))
                cases.append(pd.DataFrame({"ex": b.close.values[idx+h]/b.close.values[idx]-1-m,
                                           "ss": ss.values[idx], "f": b.forecast.fillna(0).values[idx],
                                           "unk": (b.regime.values[idx]=="unknown"),
                                           "agit": r1.rolling(30).std().values[idx]}))
        C = pd.concat(cases, ignore_index=True)
        Q = C[C.unk & C.ss.notna()]
        Qp = Q[Q.ss > 0]
        sl = stats.linregress(Qp.ss, Qp.ex)
        sla = stats.linregress(Q.ss, Q.ex)
        res.append({"h": h, "n_inprof": len(Q), "ex_inprof": Q.ex.mean(),
                    "t_inprof": Q.ex.mean()/Q.ex.std()*np.sqrt(len(Q)),
                    "n_ss>0": len(Qp), "ex_ss>0": Qp.ex.mean(), "ex_ss<=0": Q[Q.ss<=0].ex.mean(),
                    "slope_ss>0": sl.slope, "t_slope_ss>0": sl.slope/sl.stderr,
                    "slope_all": sla.slope, "t_slope_all": sla.slope/sla.stderr,
                    "ex_f>0": Q[Q.f>0].ex.mean(), "ex_f0": Q[Q.f<=0].ex.mean(),
                    "ex_outprof": C[~C.unk].ex.mean(), "n_outprof": (~C.unk).sum()})
        if h in (14,):
            Q = Q.copy(); Q["q"] = pd.qcut(Q.ss, 5, labels=False, duplicates="drop")
            qtabs[h] = Q.groupby("q").agg(ss=("ss","mean"), ex=("ex","mean"), n=("ex","size"),
                                          t=("ex", lambda s: s.mean()/s.std()*np.sqrt(len(s))))
    out["grading_by_h"] = pd.DataFrame(res)
    out["ss_quintile_h14_inprof"] = qtabs[14]
    # ---- trades
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for w, t in data["trades"][c].items() if len(t)])
    p = T.net_profit_loss_percent.sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(p), "sum": p.sum(), "top5": p.head(5).sum(),
                               "top10pct": p.head(max(1, len(p)//10)).sum(),
                               "win_share": (p > 0).mean(), "median": p.median(),
                               "mean_days": T.duration_minutes.mean()/1440})
    return out
