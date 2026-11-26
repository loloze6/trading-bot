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
            d['r60'] = cl / cl.shift(60) - 1
            d['rv20'] = d['r1'].rolling(20).std()
            d['r1z'] = d['r1'] / d['rv20'].shift(1)
            ts = d['timestamp']
            try:
                if pd.api.types.is_numeric_dtype(ts):
                    tt = pd.to_datetime(ts, unit='ms', utc=True)
                else:
                    tt = pd.to_datetime(ts, utc=True)
            except Exception:
                tt = pd.to_datetime(ts.astype(str), utc=True, errors='coerce')
            d['wd'] = tt.dt.weekday; d['year'] = tt.dt.year
            d['sig'] = d['regime'] == 'trending'
            d = d.drop(columns=['timestamp'])
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    for h in (1, 3, 5, 10, 20):
        g = A[A.pos % h == 0]
        dr = g.groupby('coin')[f'f{h}'].mean()
        A[f'u{h}'] = A[f'f{h}'] - A.coin.map(dr)

    def st(x):
        x = pd.Series(x).dropna(); n = len(x)
        if n < 2: return pd.Series({'n': n, 'mean': np.nan, 't': np.nan})
        m = x.mean(); s = x.std(ddof=1)
        return pd.Series({'n': n, 'mean': m, 't': m / (s / np.sqrt(n)) if s > 0 else np.nan})
    def grp(df, col, key):
        return df.groupby(key, observed=True)[col].apply(st).unstack()
    def first_per_cell(mask, h=10):
        S = A[mask].copy(); S['cell'] = S.pos // h
        return S.groupby(['coin', 'win', 'cell']).head(1)

    out = {}
    def safe(name, f):
        try:
            out[name] = f()
        except Exception as e:
            out[name] = 'err: ' + str(e)[:80]

    E = first_per_cell(A.sig).dropna(subset=['u10']).copy()
    safe('signal_horizons', lambda: pd.DataFrame({f'u{h}': st(E[f'u{h}']) for h in (1, 3, 5, 10, 20)}).T)
    E['r1_terc'] = pd.qcut(E['r1'].rank(method='first'), 3, labels=['low', 'mid', 'high'])
    safe('sig_by_daygain', lambda: grp(E, 'u10', 'r1_terc'))
    E['bd_terc'] = pd.qcut(E['bdist'].rank(method='first'), 3, labels=['small', 'mid', 'large'])
    safe('sig_by_breakdist', lambda: grp(E, 'u10', 'bd_terc'))
    E['er_terc'] = pd.qcut(E['er'].rank(method='first'), 3, labels=['low', 'mid', 'high'])
    safe('sig_by_er', lambda: grp(E, 'u10', 'er_terc'))
    E['r60_terc'] = pd.qcut(E['r60'].rank(method='first'), 3, labels=['low', 'mid', 'high'])
    safe('sig_by_r60', lambda: grp(E, 'u10', 'r60_terc'))
    safe('sig_by_coin', lambda: grp(E, 'u10', 'coin'))
    safe('sig_by_year', lambda: grp(E, 'u10', 'year'))

    U = first_per_cell((A.bdist > 0) & A.er.notna()).dropna(subset=['u10']).copy()
    U['er_q'] = pd.qcut(U['er'].rank(method='first'), 4, labels=['q1', 'q2', 'q3', 'q4'])
    safe('upbreak_by_er_u10', lambda: grp(U, 'u10', 'er_q'))
    safe('upbreak_by_er_u20', lambda: grp(U.dropna(subset=['u20']), 'u20', 'er_q'))
    U['bd_q'] = pd.qcut(U['bdist'].rank(method='first'), 4, labels=['q1', 'q2', 'q3', 'q4'])
    safe('upbreak_by_dist_u10', lambda: grp(U, 'u10', 'bd_q'))
    D = first_per_cell((A.ldist < 0) & A.er.notna()).dropna(subset=['u10']).copy()
    D['er_q'] = pd.qcut(D['er'].rank(method='first'), 4, labels=['q1', 'q2', 'q3', 'q4'])
    safe('downbreak_by_er_u10', lambda: grp(D, 'u10', 'er_q'))
    D['bd_q'] = pd.qcut((-D['ldist']).rank(method='first'), 4, labels=['q1', 'q2', 'q3', 'q4'])
    safe('downbreak_by_dist_u10', lambda: grp(D, 'u10', 'bd_q'))

    G1 = A.dropna(subset=['r1z', 'u1']).copy()
    G1['zb'] = pd.cut(G1['r1z'], [-99, -2, -1, 0, 1, 2, 99])
    safe('next1d_by_r1z', lambda: grp(G1, 'u1', 'zb'))
    G5 = A[(A.pos % 5 == 0)].dropna(subset=['r1z', 'u5']).copy()
    G5['zb'] = pd.cut(G5['r1z'], [-99, -2, -1, 0, 1, 2, 99])
    safe('next5d_by_r1z', lambda: grp(G5, 'u5', 'zb'))
    G10 = A[A.pos % 10 == 0].dropna(subset=['rv20', 'u10']).copy()
    G10['vr'] = G10.groupby('coin')['rv20'].rank(pct=True)
    G10['vt'] = pd.cut(G10['vr'], [0, 1/3, 2/3, 1], labels=['lowvol', 'mid', 'highvol'])
    safe('next10d_by_vol', lambda: grp(G10, 'u10', 'vt'))
    G10b = A[A.pos % 10 == 0].dropna(subset=['r60', 'u10']).copy()
    G10b['r60q'] = G10b.groupby('coin')['r60'].transform(lambda s: pd.qcut(s.rank(method='first'), 4, labels=False))
    safe('next10d_by_r60q_all', lambda: grp(G10b, 'u10', 'r60q'))
    G10c = A[A.pos % 10 == 0].dropna(subset=['er', 'u10']).copy()
    G10c['erq'] = pd.qcut(G10c['er'].rank(method='first'), 4, labels=False)
    safe('next10d_by_er_all', lambda: grp(G10c, 'u10', 'erq'))
    safe('next1d_by_weekday', lambda: grp(A.dropna(subset=['u1']), 'u1', 'wd'))

    try:
        T = []
        for c in data['trades']:
            for w, t in data['trades'][c].items():
                if t is not None and len(t):
                    t = t.copy(); t['coin'] = c; T.append(t)
        T = pd.concat(T, ignore_index=True)
        T['days'] = T['duration_minutes'] / 1440
        T['fq'] = pd.qcut(T['entry_forecast'].rank(method='first'), 3, labels=['low', 'mid', 'high'])
        out['trades_by_entryfc'] = grp(T, 'net_profit_loss_percent', 'fq')
        out['trades_summary'] = pd.Series({'n': len(T), 'mean_net': T.net_profit_loss_percent.mean(),
                                           'median_net': T.net_profit_loss_percent.median(),
                                           'share_pos': (T.net_profit_loss_percent > 0).mean(),
                                           'mean_days': T.days.mean(), 'max_days': T.days.max(),
                                           'top5_share_of_sum': T.net_profit_loss_percent.nlargest(5).sum() / T.net_profit_loss_percent.sum()})
    except Exception as e:
        out['trades'] = 'err: ' + str(e)[:80]
    return out
