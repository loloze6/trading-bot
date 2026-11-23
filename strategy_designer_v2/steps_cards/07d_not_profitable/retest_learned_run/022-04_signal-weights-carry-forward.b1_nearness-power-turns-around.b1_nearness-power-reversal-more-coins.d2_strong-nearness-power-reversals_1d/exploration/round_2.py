def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    COST = 0.0011  # per unit of allocation changed (half a round trip of 0.22%)
    # grid checks: signal vs trend-alone at several trend lookbacks
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].values; f = df["forecast"].values; n = len(c)
            cs = pd.Series(c)
            tr = {L: cs.pct_change(L).values for L in (10, 20, 60)}
            for i in range(0, n-5, 5):
                rows.append((coin, f[i], c[i+5]/c[i]-1, tr[10][i], tr[20][i], tr[60][i]))
    g = pd.DataFrame(rows, columns=["coin","f","r","t10","t20","t60"])
    g["u"] = g["r"] - g.groupby("coin")["r"].transform("mean")
    g = g[g.f != 0]
    s = np.sign(g.f)
    res = {}
    for L in ("t10","t20","t60"):
        x = g.dropna(subset=[L]); sx = np.sign(x.f); tx = np.sign(x[L])
        al = sx == tx
        a = (sx*x.u)[al]; m = (tx*x.u)
        res[L] = {"n_aligned": al.sum(), "sig&trend_unus%": 100*a.mean(),
                  "t_aligned": stats.ttest_1samp(a,0).statistic,
                  "trend_alone_unus%": 100*m.mean(), "t_trend_alone": stats.ttest_1samp(m,0).statistic,
                  "trend_when_sig_disagrees%": 100*m[~al].mean(),
                  "sig_against_trend_unus%": 100*(sx*x.u)[~al].mean()}
    out["trend_filter_check"] = pd.DataFrame(res).T
    # simulated daily books from the recorded allocation, with variants
    recs = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].values; al = df["postRebalance_current_allocation"].values.astype(float)
            r = np.r_[c[1:]/c[:-1]-1, 0.0]
            cs = pd.Series(c)
            t20 = np.sign(cs.pct_change(20).fillna(0).values)
            t60 = np.sign(cs.pct_change(60).fillna(0).values)
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            vars_ = {"orig": al, "long_only": np.where(al > 0, al, 0),
                     "trend20": np.where(np.sign(al) == t20, al, 0),
                     "trend60": np.where(np.sign(al) == t60, al, 0),
                     "hold": np.ones_like(al)}
            for k, a in vars_.items():
                da = np.abs(np.diff(np.r_[a[0] if k == "hold" else 0, a]))
                net = a*r - COST*da
                # returns over bar i+1 credited; shift so day aligned
                recs.append(pd.DataFrame({"k": k, "coin": coin, "w": w, "day": day, "ret": net,
                                          "inpos": (a != 0).astype(float)}))
    R = pd.concat(recs)
    D = R.groupby(["k","w","day"]).agg(ret=("ret","mean"), inpos=("inpos","mean")).reset_index()
    wo = sorted(D.w.unique(), key=lambda s: int(s[1:]))
    summ = {}
    for k, d in D.groupby("k"):
        d = d.copy(); d["wi"] = d.w.map({w: i for i, w in enumerate(wo)}); d = d.sort_values(["wi","day"])
        x = d.ret.values; v = np.cumprod(1+x); dd = (v/np.maximum.accumulate(v)-1).min()
        yr = v[-1]**(365/len(x)) - 1
        summ[k] = {"sharpe": x.mean()/x.std(ddof=1)*np.sqrt(365), "mean": x.mean(),
                   "mean_in_pos": x.mean()/d.inpos.mean(), "yearly": yr, "maxdd": dd, "calmar": yr/abs(dd),
                   "min_win_sharpe_leave_out": min(
                       (lambda y: y.mean()/y.std(ddof=1)*np.sqrt(365))(d[d.w != w].ret.values) for w in wo)}
    out["variant_books"] = pd.DataFrame(summ).T
    # orig book's worst windows: coin trend and side held
    o = R[R.k == "orig"]
    ww = []
    for w, d in o.groupby("w"):
        ww.append((w, d.ret.sum()/d.groupby("coin").ngroups))
    out["orig_window_sum"] = pd.Series(dict(ww)).sort_values().head(8)
    return out
