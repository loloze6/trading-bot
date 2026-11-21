def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 240
    allrows = []; caserows = []
    for coin, ws in bars.items():
        rr = []
        for w, df in ws.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            rr += list(c[idx + H] / c[idx] - 1)
        dr = np.mean(rr); us = np.std(rr)
        for w, df in ws.items():
            c = df["close"].values; f = df["forecast"].fillna(0).values; n = len(c)
            s = pd.Series(c)
            r24 = s.pct_change(24).values
            mabs = s.pct_change(24).abs().rolling(720, min_periods=200).mean().values
            r720 = s.pct_change(720).values
            for start in range(0, n - H, H):
                t = start
                allrows.append(dict(coin=coin, prior=r720[t], r24=r24[t], depth=-r24[t]/mabs[t] if mabs[t] > 0 else np.nan,
                                    s=(c[t+H]/c[t]-1-dr)/us, u=c[t+H]/c[t]-1-dr))
                end = min(start + H, n)
                hit = np.where(f[start:end] >= 2)[0]
                if len(hit) == 0: continue
                tc = start + hit[0]
                if tc + H >= n: continue
                caserows.append(dict(coin=coin, prior=r720[tc], depth=-r24[tc]/mabs[tc] if mabs[tc] > 0 else np.nan,
                                     s=(c[tc+H]/c[tc]-1-dr)/us, u=c[tc+H]/c[tc]-1-dr))
    a = pd.DataFrame(allrows); d = pd.DataFrame(caserows)
    def reg(x, v, y="s"):
        x = x[[v, y]].dropna(); r = stats.linregress(x[v], x[y])
        return pd.Series(dict(n=len(x), slope=r.slope, t=r.slope / r.stderr))
    out = {}
    out["slopes"] = pd.DataFrame({
        "all_grid_prior_pos": reg(a[a.prior > 0], "prior"),
        "all_grid_prior_pos_and_fall": reg(a[(a.prior > 0) & (a.r24 < 0)], "prior"),
        "all_grid_prior_pos_and_rise": reg(a[(a.prior > 0) & (a.r24 >= 0)], "prior"),
        "all_grid_prior_any": reg(a, "prior"),
        "cases_prior": reg(d, "prior"),
        "cases_logprior": reg(d.assign(lp=np.log1p(d.prior.clip(lower=0))), "lp"),
        "cases_depth": reg(d, "depth"),
        "cases_prior_depth_lt1": reg(d[d.depth < 1], "prior"),
        "cases_prior_depth_ge1": reg(d[d.depth >= 1], "prior"),
    }).T
    def tt(x):
        x = x.dropna(); return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x)))))
    a2 = a[a.prior > 0].copy()
    a2["pq"] = pd.qcut(a2.prior.rank(method="first"), 4, labels=False)
    out["all_grid_prior_pos_q_u"] = a2.groupby("pq")["u"].apply(tt).unstack()
    out["all_grid_prior_nonpos_u"] = tt(a[a.prior <= 0]["u"]).to_frame().T
    out["cases_u"] = tt(d["u"]).to_frame().T
    out["all_grid_prior_pos_fall_u"] = tt(a[(a.prior > 0) & (a.r24 < 0)]["u"]).to_frame().T
    out["all_grid_prior_pos_rise_u"] = tt(a[(a.prior > 0) & (a.r24 >= 0)]["u"]).to_frame().T
    return out
