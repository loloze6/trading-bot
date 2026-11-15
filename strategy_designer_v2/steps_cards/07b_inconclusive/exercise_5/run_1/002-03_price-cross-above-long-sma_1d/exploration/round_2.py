def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    mu = {}
    for c, ws in bars.items():
        mu[c] = pd.concat([df["close"].pct_change().dropna() for df in ws.values()]).mean()
    rows = []; blocks = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; n = len(df)
            fc = df["forecast"].values
            al = df["postRebalance_current_allocation"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            p20 = pd.Series(cl).pct_change(20).values
            p60 = pd.Series(cl).pct_change(60).values
            for t in range(0, n, 20):
                if t + 20 < n:
                    rows.append(dict(coin=c, win=w, year=yr[t], fc=fc[t], p20=p20[t], p60=p60[t],
                                     ex=cl[t+20]/cl[t]-1-20*mu[c]))
            # main measure blocks
            fwd = np.full(n, np.nan)
            fwd[:n-20] = cl[20:]/cl[:n-20]-1-20*mu[c]
            for s in range(0, n, 20):
                idx = np.arange(s, min(s+20, n))
                v = al[idx]*fwd[idx]
                ok = ~np.isnan(v)
                if ok.any():
                    blocks.append(dict(coin=c, year=yr[s], val=np.nansum(v), nz=(al[idx][ok] != 0).any(),
                                       p20=p20[s]))
    d = pd.DataFrame(rows); b = pd.DataFrame(blocks)
    def tt(x):
        x = pd.Series(x).dropna(); return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, median=x.median()))
    out["block_all"] = tt(b.val)
    out["block_by_coin"] = b.groupby("coin").val.apply(tt).unstack()
    out["block_leave_coin_out"] = pd.DataFrame({c: tt(b[b.coin != c].val) for c in b.coin.unique()}).T
    out["block_by_year"] = b.groupby("year").val.apply(tt).unstack()
    s = b.val.sort_values(ascending=False)
    out["block_drop_top5_t"] = tt(s.iloc[5:])
    out["block_winsor_1pct"] = tt(b.val.clip(b.val.quantile(0.01), b.val.quantile(0.99)))
    on = d[d.fc > 0].copy()
    on["p20q"] = pd.qcut(on.p20, 4, labels=["p1","p2","p3","p4"])
    out["on_by_past20_quartile"] = on.groupby("p20q").ex.apply(tt).unstack()
    on["p60q"] = pd.qcut(on.p60, 4, labels=["p1","p2","p3","p4"])
    out["on_by_past60_quartile"] = on.groupby("p60q").ex.apply(tt).unstack()
    a = on[on.p20 > 0].ex; bb = on[on.p20 <= 0].ex
    out["on_p20up_minus_down"] = pd.Series(dict(diff=a.mean()-bb.mean(), welch=stats.ttest_ind(a, bb, equal_var=False).statistic,
                                                 diff_winsor=a.clip(-0.5,0.5).mean()-bb.clip(-0.5,0.5).mean(),
                                                 welch_winsor=stats.ttest_ind(a.clip(-0.5,0.5), bb.clip(-0.5,0.5), equal_var=False).statistic))
    out["on_p20up_by_coin"] = on[on.p20 > 0].groupby("coin").ex.apply(tt).unstack()
    # all bars graded past20 (spearman)
    dd = d.dropna(subset=["p20"])
    out["all_spearman_p20_ex"] = pd.Series(stats.spearmanr(dd.p20, dd.ex)[:2], index=["rho","p"])
    out["on_spearman_p20_ex"] = pd.Series(stats.spearmanr(on.dropna(subset=["p20"]).p20, on.dropna(subset=["p20"]).ex)[:2], index=["rho","p"])
    out["on_spearman_fc_ex"] = pd.Series(stats.spearmanr(on.fc, on.ex)[:2], index=["rho","p"])
    return out
