def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    col = 'debug_info.components.fail_exc.last_history_value'
    H = [1, 3, 5, 10]
    drift = {}; usual = {}
    for c, ws in data['bars'].items():
        for h in H:
            rs = []
            for w, b in ws.items():
                cl = b['close'].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    rows = []; brk = []
    for c, ws in data['bars'].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b['close'].values; n = len(cl)
            raw = b[col].fillna(0).values if col in b else np.zeros(n)
            year = pd.to_datetime(b['timestamp']).dt.year.values
            s = pd.Series(cl)
            vol20 = s.pct_change().rolling(20).std().values
            prevhigh = s.shift(1).rolling(20).max().values
            depth = cl / prevhigh - 1
            for h in H:
                seen = set(); seen2 = set()
                for t in range(n - h):
                    g = t // h
                    r = cl[t + h] / cl[t] - 1
                    if raw[t] > 0 and g not in seen:
                        seen.add(g)
                        rows.append(dict(coin=c, h=h, year=year[t], exc=raw[t], excv=raw[t] / 100 / vol20[t] if vol20[t] > 0 else np.nan,
                                         depth=depth[t], r=r, unus=r - drift[(c, h)]))
                    if np.isfinite(prevhigh[t]) and cl[t] > prevhigh[t] and g not in seen2:
                        seen2.add(g)
                        brk.append(dict(coin=c, h=h, year=year[t], ext=(cl[t] / prevhigh[t] - 1) * 100,
                                        extv=(cl[t] / prevhigh[t] - 1) / vol20[t] if vol20[t] > 0 else np.nan,
                                        r=r, unus=r - drift[(c, h)]))
    d = pd.DataFrame(rows); bk = pd.DataFrame(brk)
    def sl(x, y):
        m = np.isfinite(x) & np.isfinite(y)
        if m.sum() < 10: return pd.Series({'slope': np.nan, 't': np.nan, 'n': m.sum()})
        s = stats.linregress(x[m], y[m])
        rho, p = stats.spearmanr(x[m], y[m])
        return pd.Series({'slope': s.slope, 't': s.slope / s.stderr, 'spearman': rho, 'p_sp': p, 'n': m.sum()})
    out = {}
    out['fail_spearman_by_h'] = d.groupby('h').apply(lambda g: sl(g.exc.values, g.r.values))
    def wins(g):
        x = g.exc.clip(upper=g.exc.quantile(0.95)).values
        y = g.r.clip(g.r.quantile(0.01), g.r.quantile(0.99)).values
        return sl(x, y)
    out['fail_winsorized_by_h'] = d.groupby('h').apply(wins)
    out['fail_excvol_by_h'] = d.groupby('h').apply(lambda g: sl(g.excv.values, g.r.values))
    out['fail_depth_by_h'] = d.groupby('h').apply(lambda g: sl(g.depth.values, g.r.values))
    d5 = d[d.h == 5]
    out['fail_h5_slope_by_coin'] = d5.groupby('coin').apply(lambda g: sl(g.exc.values, g.r.values))
    out['fail_h5_slope_by_year'] = d5.groupby('year').apply(lambda g: sl(g.exc.values, g.r.values))
    def summ(g):
        return pd.Series({'n': len(g), 'mean_unus_long': g.unus.mean(),
                          't': g.unus.mean() / (g.unus.std() / np.sqrt(len(g))), 'mean_raw': g.r.mean()})
    out['breakout_all_by_h'] = bk.groupby('h').apply(summ)
    out['breakout_ext_slope_by_h'] = bk.groupby('h').apply(lambda g: sl(g.extv.values, g.r.values))
    b5 = bk[bk.h == 5].copy()
    b5['q'] = pd.qcut(b5.extv, 5, labels=False, duplicates='drop')
    out['breakout_h5_by_extv_q'] = b5.groupby('q').apply(summ)
    out['breakout_h5_slope_by_coin'] = b5.groupby('coin').apply(lambda g: sl(g.extv.values, g.r.values))
    return out
