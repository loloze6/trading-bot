def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data['bars'].items():
        parts = []
        for w, b in wins.items():
            ts = pd.to_datetime(b['timestamp'], utc=True)
            s = pd.Series(b['close'].astype(float).values)
            df = pd.DataFrame({'coin': coin, 'w': w,
                               'hc': (ts + pd.Timedelta(hours=1)).dt.hour.values,
                               'year': ts.dt.year.values,
                               'day': (ts + pd.Timedelta(hours=1)).dt.floor('D').astype(str).values,
                               'pos': np.arange(len(s))})
            df['r1'] = s.pct_change().values
            df['r2'] = (s / s.shift(2) - 1).values
            df['r24'] = (s / s.shift(24) - 1).values
            df['f1'] = (s.shift(-1) / s - 1).values
            df['f2'] = (s.shift(-2) / s - 1).values
            df['f8'] = (s.shift(-8) / s - 1).values
            df['f24'] = (s.shift(-24) / s - 1).values
            parts.append(df)
        d = pd.concat(parts, ignore_index=True)
        sd = d['r1'].std()
        for c, k in [('f1', 1), ('f2', 2), ('f8', 8), ('f24', 24), ('r2', 2), ('r24', 24)]:
            d[c + 'n'] = d[c] / (sd * np.sqrt(k))
        for c in ['f1n', 'f2n', 'f8n', 'f24n']:
            d[c] = d[c] - d[c].mean()
        rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def st(x):
        x = x.dropna(); n = len(x)
        return pd.Series({'mean': x.mean(), 't': x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan, 'n': n})

    def clustered(sub, col):
        # mean across coins per day, then t over days
        g = sub.groupby(['w', 'day'])[col].mean()
        return st(g)

    out = {}
    # evening 21:00-23:00 bars: 2h return from close of bar ending 21:00
    E = D[D['hc'] == 21].copy()
    out['eve2h_clustered_by_day'] = clustered(E, 'f2n')
    out['eve2h_by_year'] = E.groupby('year')['f2n'].apply(st).unstack()
    out['eve2h_by_coin'] = E.groupby('coin')['f2n'].apply(st).unstack()
    O = D[D['hc'] != 21]
    O = O[O['pos'] % 2 == 0]
    out['other2h_clustered'] = clustered(O, 'f2n')
    # bar 14:00 negative
    F = D[D['hc'] == 14]
    out['bar14_clustered'] = clustered(F, 'f1n')
    out['bar14_by_year'] = F.groupby('year')['f1n'].apply(st).unstack()

    # settlement asymmetry: against-trend 2h move, trend-signed next 8h
    A = D[(D['r2'] * D['r24'] < 0) & D['hc'].isin([0, 8, 16])].copy()
    A['tr8'] = np.sign(A['r24']) * A['f8n']
    out['settle_by_hour_clustered'] = A.groupby('hc').apply(lambda x: clustered(x, 'tr8'))
    out['settle8_by_year'] = A[A['hc'] == 8].groupby('year')['tr8'].apply(st).unstack()
    out['settle16_by_year'] = A[A['hc'] == 16].groupby('year')['tr8'].apply(st).unstack()
    # graded? at 08: by |r2n| tercile, continuation of 2h move = -tr8
    A8 = A[A['hc'] == 8].dropna(subset=['r2n', 'tr8']).copy()
    A8['q'] = pd.qcut(A8['r2n'].abs(), 3, labels=False)
    A8['cont'] = np.sign(A8['r2']) * A8['f8n']
    out['settle8_cont_by_abs2h_tercile'] = A8.groupby('q')['cont'].apply(st).unstack()
    # all bars at 08 (no trend condition): continuation of 2h move
    B8 = D[D['hc'] == 8].dropna(subset=['r2n', 'f8n']).copy()
    B8['cont'] = np.sign(B8['r2']) * B8['f8n']
    B8['q'] = pd.qcut(B8['r2n'].abs(), 3, labels=False)
    out['all08_cont_by_abs2h_tercile'] = B8.groupby('q')['cont'].apply(st).unstack()
    # night window 0-8: trend-signed 8h after counter-trend move vs morning
    # rebound after falls: 24h grid, negative r24 only, by quintile of r24n
    G = D[(D['pos'] % 24 == 0)].dropna(subset=['r24n', 'f24n']).copy()
    Gn = G[G['r24'] < 0].copy()
    Gn['q'] = pd.qcut(Gn['r24n'], 5, labels=False)
    out['falls_next24_by_quintile'] = Gn.groupby('q')['f24n'].apply(st).unstack()
    out['falls_q0_clustered'] = clustered(Gn[Gn['q'] == 0], 'f24n')
    out['falls_q0_by_year'] = Gn[Gn['q'] == 0].groupby('year')['f24n'].apply(st).unstack()
    Gp = G[G['r24'] > 0].copy()
    Gp['q'] = pd.qcut(Gp['r24n'], 5, labels=False)
    out['rises_next24_by_quintile'] = Gp.groupby('q')['f24n'].apply(st).unstack()
    return out
