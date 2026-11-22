def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    fc = 'forecast'
    rows = []
    drift = {}
    for coin, ws in data["bars"].items():
        rets = []
        for w, b in ws.items():
            c = b['close'].values
            idx = np.arange(0, len(c) - H, H)
            rets += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(rets)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            f = b[fc].fillna(0).values
            c = b['close'].values
            v = b['volume'].values
            ts = pd.to_datetime(b['timestamp'])
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            mad = pd.Series(np.abs(r1)).rolling(180, min_periods=45).mean().values
            sma = pd.Series(c).rolling(180, min_periods=45).mean().values
            ret180 = pd.Series(c).pct_change(180).values  # 30-day return
            ret540 = pd.Series(c).pct_change(540).values  # 90-day return
            ref = 0.0
            seen = set()
            for t in range(len(f)):
                if f[t] >= 0:
                    ref = 0.0
                    continue
                if f[t] <= ref - 2:
                    ref = f[t]
                    cell = t // H
                    if cell in seen or t + H >= len(c):
                        continue
                    seen.add(cell)
                    # streak
                    k = t
                    while k > 0 and c[k] > c[k - 1]:
                        k -= 1
                    nst = t - k
                    gain = c[t] / c[k] - 1 if nst > 0 else 0.0
                    gain_u = gain / mad[t] if mad[t] and not np.isnan(mad[t]) else np.nan
                    depth = max(0.0, 1 - c[t] / sma[t]) if not np.isnan(sma[t]) else np.nan
                    vfade = np.nan
                    if nst >= 2:
                        vfade = np.mean(v[t - nst // 2 + 1:t + 1]) / np.mean(v[k + 1:k + 1 + max(1, nst // 2)]) - 1 if np.mean(v[k + 1:k + 1 + max(1, nst // 2)]) > 0 else np.nan
                    rows.append(dict(coin=coin, year=ts[t].year, f=f[t], nst=nst, gain_u=gain_u,
                                     depth=depth, ret180=ret180[t], ret540=ret540[t], vfade=vfade,
                                     u18=-(c[t + H] / c[t] - 1 - drift[coin])))
                else:
                    ref = max(ref, f[t])
    d = pd.DataFrame(rows)
    def summ(g):
        x = g['u18'].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out = {}
    for col in ['gain_u', 'depth', 'nst', 'ret180', 'ret540', 'vfade']:
        dd = d.dropna(subset=[col])
        q = pd.qcut(dd[col].rank(method='first'), 4, labels=False)
        out['by_' + col + '_q'] = dd.groupby(q).apply(summ).join(dd.groupby(q)[col].median().rename('median'))
        out['spearman_' + col] = str(stats.spearmanr(dd[col], dd['u18']))
    dd = d.dropna(subset=['ret540'])
    out['by_90d_trend_sign'] = dd.groupby(dd['ret540'] < 0).apply(summ)
    dd2 = dd[dd['ret540'] < 0]
    q = pd.qcut(dd2['depth'].rank(method='first'), 3, labels=False)
    out['in_90d_down_by_depth_tercile'] = dd2.groupby(q).apply(summ)
    out['by_year_90d_down'] = dd2.groupby('year').apply(summ)
    out['by_year_90d_up'] = dd[dd['ret540'] >= 0].groupby('year').apply(summ)
    return out
