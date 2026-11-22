def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    fc = 'forecast'
    raw = 'debug_info.components.relief_rally.last_history_value'
    rows = []
    drift = {}
    usual = {}
    for coin, ws in data["bars"].items():
        rets = {h: [] for h in (6, 12, 18, 36)}
        for w, b in ws.items():
            c = b['close'].values
            for h in rets:
                idx = np.arange(0, len(c) - h, h)
                rets[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: np.mean(v) for h, v in rets.items()}
        usual[coin] = {h: np.std(v) for h, v in rets.items()}
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            f = b[fc].fillna(0).values
            c = b['close'].values
            r = b[raw].values if raw in b else np.full(len(b), np.nan)
            ts = pd.to_datetime(b['timestamp'])
            ref = 0.0
            seen = set()
            for t in range(len(f)):
                if f[t] >= 0:
                    ref = 0.0
                    continue
                if f[t] <= ref - 2:
                    ref = f[t]
                    cell = t // H
                    if cell in seen:
                        continue
                    seen.add(cell)
                    row = dict(coin=coin, w=w, year=ts[t].year, f=f[t], raw=r[t])
                    for h in (6, 12, 18, 36):
                        if t + h < len(c):
                            row['u%d' % h] = -(c[t + h] / c[t] - 1 - drift[coin][h])
                    rows.append(row)
                else:
                    ref = max(ref, f[t])
    d = pd.DataFrame(rows)
    def summ(g):
        x = g['u18'].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out = {}
    out['overall'] = summ(d)
    out['abs_forecast_dist'] = d['f'].abs().describe()
    out['share_f_eq_-20'] = float((d['f'] <= -19.99).mean())
    d['rawq'] = pd.qcut(d['raw'].rank(method='first'), 4, labels=False)
    out['by_raw_quartile'] = d.groupby('rawq').apply(summ)
    d['fq'] = pd.qcut(d['f'].abs().rank(method='first'), 4, labels=False)
    out['by_absf_quartile'] = d.groupby('fq').apply(summ)
    out['by_coin'] = d.groupby('coin').apply(summ)
    out['by_year'] = d.groupby('year').apply(summ)
    hz = {}
    for h in (6, 12, 18, 36):
        x = d['u%d' % h].dropna()
        hz[h] = dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))))
    out['by_horizon_overlapping_cases'] = pd.DataFrame(hz).T
    out['raw_desc'] = d['raw'].describe()
    out['spearman_raw_u18'] = str(stats.spearmanr(d['raw'], d['u18'], nan_policy='omit'))
    out['drift18'] = pd.Series({k: v[18] for k, v in drift.items()})
    return out
