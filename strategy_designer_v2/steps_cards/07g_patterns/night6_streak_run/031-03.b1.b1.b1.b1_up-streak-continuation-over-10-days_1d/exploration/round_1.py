import numpy as np, pandas as pd

def _ct(df, col):
    d = df[[col, 'day']].dropna()
    if len(d) < 5: return np.nan, len(d), 0
    m = d[col].mean()
    s = (d[col] - m).groupby(d['day']).sum()
    D = len(s)
    se = np.sqrt(D/(D-1) * (s**2).sum()) / len(d)
    return m/se, len(d), D

def _summ(df, by, col='u'):
    rows = []
    for k, g in df.groupby(by, observed=True):
        t, n, D = _ct(g, col)
        rows.append({'grp': str(k), 'mean_u%': round(100*g[col].mean(), 3),
                     'strength': round(g['z'].mean(), 4), 't_day': round(t, 2), 'n': n, 'days': D})
    return pd.DataFrame(rows)

def explore(data):
    H = 10
    recs = []
    for coin, wins in data['bars'].items():
        rows = []
        for w, b in wins.items():
            b = b.sort_values('timestamp').reset_index(drop=True)
            c = b['close'].astype(float)
            r1 = c.pct_change()
            sgn = np.sign(r1).fillna(0)
            streak = np.zeros(len(c))
            for i in range(1, len(c)):
                s = sgn.iloc[i]
                if s == 0: streak[i] = 0
                elif s == np.sign(streak[i-1]) : streak[i] = streak[i-1] + s
                else: streak[i] = s
            f = c.shift(-H)/c - 1
            df = pd.DataFrame({
                'day': pd.to_datetime(b['timestamp']).dt.floor('D'),
                'fwd': f, 'streak': streak,
                'ret30': c/c.shift(30) - 1, 'ret10': c/c.shift(10) - 1,
                'r1': r1, 'vol20': r1.rolling(20).std(),
                'fc': b['forecast'].astype(float),
                'alloc': b['postRebalance_current_allocation'].astype(float),
                'regime': b['regime'].astype(str),
                'rng': (b['high']-b['low'])/b['close'],
                'pos': np.arange(len(c))})
            df['grid'] = (df['pos'] % H == 0)
            df['w'] = w
            rows.append(df)
        cd = pd.concat(rows, ignore_index=True)
        gd = cd[cd['grid'] & cd['fwd'].notna()]
        drift, sd = gd['fwd'].mean(), gd['fwd'].std()
        cd['u'] = cd['fwd'] - drift
        cd['z'] = cd['u'] / sd
        cd['coin'] = coin
        # per coin ranks for vol and r1
        cd['volq'] = pd.qcut(cd['vol20'].rank(method='first'), 3, labels=['lowvol','midvol','highvol'])
        cd['r1z'] = cd['r1'] / cd['vol20']
        cd['rngq'] = pd.qcut(cd['rng'].rank(method='first'), 3, labels=['lowrng','midrng','highrng'])
        recs.append(cd)
    A = pd.concat(recs, ignore_index=True)
    G = A[A['grid'] & A['fwd'].notna()].copy()
    G['stk'] = G['streak'].clip(-5, 5).astype(int)
    G['r30s'] = np.where(G['ret30'] > 0, 'r30pos', 'r30neg')
    G['r1zb'] = pd.cut(G['r1z'], [-99, -2, -1, 0, 1, 2, 99])
    G['r10q'] = pd.qcut(G['ret10'] / (G['vol20']*np.sqrt(10)), 5)
    G['wd'] = G['day'].dt.dayofweek
    G['yr'] = G['day'].dt.year
    G['inpos'] = np.where(G['alloc'] > 0, 'long', 'flat')
    out = {}
    out['by_streak'] = _summ(G, 'stk')
    out['streak_x_r30'] = _summ(G, ['r30s', 'stk'])
    out['by_r1z'] = _summ(G, 'r1zb')
    out['by_ret10_volnorm_quint'] = _summ(G, 'r10q')
    out['by_vol'] = _summ(G, 'volq')
    out['vol_x_r30'] = _summ(G, ['volq', 'r30s'])
    out['by_range'] = _summ(G, 'rngq')
    out['by_weekday'] = _summ(G, 'wd')
    out['by_year'] = _summ(G, 'yr')
    out['by_pos'] = _summ(G, ['r30s', 'inpos'])
    return out
