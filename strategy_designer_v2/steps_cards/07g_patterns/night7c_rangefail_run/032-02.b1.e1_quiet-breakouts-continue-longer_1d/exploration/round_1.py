def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data['bars']
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            d = df.copy().reset_index(drop=True)
            cl = d['close'].astype(float)
            d['coin'] = c; d['win'] = w; d['pos'] = np.arange(len(d))
            d['r1'] = cl.pct_change()
            for h in (1, 3, 5, 10, 20):
                d[f'f{h}'] = cl.shift(-h) / cl - 1
            ch = (cl - cl.shift(60)).abs(); vv = cl.diff().abs().rolling(60).sum()
            d['er'] = (ch / vv).rolling(5).mean()
            d['bdist'] = cl / cl.shift(1).rolling(60).max() - 1
            d['ldist'] = cl / cl.shift(1).rolling(60).min() - 1
            d['rv20'] = d['r1'].rolling(20).std()
            d['r1z'] = d['r1'] / d['rv20'].shift(1)
            ts = d['timestamp']
            tt = pd.to_datetime(ts, unit='ms') if np.issubdtype(ts.dtype, np.number) else pd.to_datetime(ts)
            d['wd'] = tt.dt.weekday; d['year'] = tt.dt.year
            d['sig'] = d['regime'] == 'trending'
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    for h in (1, 3, 5, 10, 20):
        g = A[A.pos % h == 0]
        dr = g.groupby('coin')[f'f{h}'].mean()
        A[f'u{h}'] = A[f'f{h}'] - A.coin.map(dr)

    def st(x):
        x = x.dropna(); n = len(x)
        if n < 2: return pd.Series({'n': n, 'mean': np.nan, 't': np.nan})
        m = x.mean(); s = x.std(ddof=1)
        return pd.Series({'n': n, 'mean': m, 't': m / (s / np.sqrt(n)) if s > 0 else np.nan})
    def grp(df, col, key):
        return df.groupby(key)[col].apply(st).unstack()
    def first_per_cell(mask, h=10):
        S = A[mask].copy(); S['cell'] = S.pos // h
        return S.groupby(['coin', 'win', 'cell']).head(1)

    out = {}
    E = first_per_cell(A.sig)
    E = E.dropna(subset=['u10'])
    out['signal_horizons'] = pd.DataFrame({f'u{h}': st(E[f'u{h}']) for h in (1, 3, 5, 10, 20)}).T
    E['r1_terc'] = pd.qcut(E['r1'], 3, labels=['low', 'mid', 'high'])
    out['sig_by_daygain'] = grp(E, 'u10', 'r1_terc')
    E['fc_terc'] = pd.qcut(E['forecast'].rank(method='first'), 3, labels=['low', 'mid', 'high'])
    out['sig_by_forecast'] = grp(E, 'u10', 'fc_terc')
    Eb = E.dropna(subset=['bdist'])
    if len(Eb) > 15:
        Eb = Eb.copy(); Eb['bd_terc'] = pd.qcut(Eb['bdist'].rank(method='first'), 3, labels=['small', 'mid', 'large'])
        out['sig_by_breakdist'] = grp(Eb, 'u10', 'bd_terc')
    Ee = E.dropna(subset=['er'])
    if len(Ee) > 15:
        Ee = Ee.copy(); Ee['er_terc'] = pd.qcut(Ee['er'].rank(method='first'), 3, labels=['low', 'mid', 'high'])
        out['sig_by_er'] = grp(Ee, 'u10', 'er_terc')
    out['sig_by_coin'] = grp(E, 'u10', 'coin')
    out['sig_by_year'] = grp(E, 'u10', 'year')

    # all upside breakouts graded by efficiency ratio
    U = first_per_cell((A.bdist > 0) & A.er.notna()).dropna(subset=['u10']).copy()
    U['er_q'] = pd.qcut(U['er'].rank(method='first'), 4, labels=['q1', 'q2', 'q3', 'q4'])
    out['upbreak_by_er'] = grp(U, 'u10', 'er_q')
    out['upbreak_by_er_u20'] = grp(U.dropna(subset=['u20']), 'u20', 'er_q')
    D = first_per_cell((A.ldist < 0) & A.er.notna()).dropna(subset=['u10']).copy()
    D['er_q'] = pd.qcut(D['er'].rank(method='first'), 4, labels=['q1', 'q2', 'q3', 'q4'])
    out['downbreak_by_er'] = grp(D, 'u10', 'er_q')

    # large moves
    G1 = A.dropna(subset=['r1z', 'u1']).copy()
    G1['zb'] = pd.cut(G1['r1z'], [-99, -2, -1, 0, 1, 2, 99])
    out['next1d_by_r1z'] = grp(G1, 'u1', 'zb')
    G5 = A[(A.pos % 5 == 0)].dropna(subset=['r1z', 'u5']).copy()
    G5['zb'] = pd.cut(G5['r1z'], [-99, -2, -1, 0, 1, 2, 99])
    out['next5d_by_r1z'] = grp(G5, 'u5', 'zb')
    G10 = A[A.pos % 10 == 0].dropna(subset=['rv20', 'u10']).copy()
    G10['vr'] = G10.groupby('coin')['rv20'].rank(pct=True)
    G10['vt'] = pd.cut(G10['vr'], [0, 1/3, 2/3, 1], labels=['lowvol', 'mid', 'highvol'])
    out['next10d_by_vol'] = grp(G10, 'u10', 'vt')
    G10['r20'] = None
    out['next1d_by_weekday'] = grp(A.dropna(subset=['u1']), 'u1', 'wd')

    # trades
    T = []
    for c in data['trades']:
        for w, t in data['trades'][c].items():
            if t is not None and len(t):
                t = t.copy(); t['coin'] = c; T.append(t)
    if T:
        T = pd.concat(T, ignore_index=True)
        T['days'] = T['duration_minutes'] / 1440
        T['fq'] = pd.qcut(T['entry_forecast'].rank(method='first'), 3, labels=['low', 'mid', 'high'])
        out['trades_by_entryfc'] = grp(T, 'net_profit_loss_percent', 'fq')
        out['trades_summary'] = pd.Series({'n': len(T), 'mean_net': T.net_profit_loss_percent.mean(),
                                           'median_net': T.net_profit_loss_percent.median(),
                                           'share_pos': (T.net_profit_loss_percent > 0).mean(),
                                           'mean_days': T.days.mean(), 'max_days': T.days.max()})
    return out
