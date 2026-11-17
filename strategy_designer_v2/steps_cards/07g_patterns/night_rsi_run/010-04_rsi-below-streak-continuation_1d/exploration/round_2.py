import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    C = 'debug_info.components.rsi_below_age.last_history_value'
    d = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy().reset_index(drop=True); x['coin'] = coin; x['w'] = w
            x['wd'] = pd.to_datetime(x['day']).dt.weekday
            x['yr'] = pd.to_datetime(x['day']).dt.year
            r = x['coin_return']
            x['next'] = r.shift(-1)
            x['next3'] = x['close'].shift(-3) / x['close'] - 1
            sd = r.rolling(30, min_periods=15).std().shift(1)
            x['z'] = r / sd
            x['vol30'] = sd
            x['rng'] = np.nan
            d.append(x)
    D = pd.concat(d, ignore_index=True)
    D['ytype'] = np.where(D['yr'] <= 2021, 'early', 'late')
    def tt(s):
        s = s.dropna(); return pd.Series({'mean': s.mean(), 'n': len(s), 't': s.mean() / (s.std() / np.sqrt(len(s)))})
    out['sat return by coin'] = D[D.wd == 5].groupby('coin')['coin_return'].apply(tt).unstack()
    out['sat return by early/late'] = D[D.wd == 5].groupby('ytype')['coin_return'].apply(tt).unstack()
    out['wed return by early/late'] = D[D.wd == 2].groupby('ytype')['coin_return'].apply(tt).unstack()
    out['thu return by early/late'] = D[D.wd == 3].groupby('ytype')['coin_return'].apply(tt).unstack()
    out['sat abs return vs others'] = D.groupby(D.wd == 5)['coin_return'].apply(lambda s: s.abs().mean())
    # next day after large z moves
    E = D.dropna(subset=['z', 'next']).copy()
    E['zb'] = pd.qcut(E['z'], 7, labels=False)
    out['next day by today z septile'] = E.groupby('zb')['next'].apply(tt).unstack()
    E2 = D.dropna(subset=['z', 'next3']).copy()
    E2 = E2.groupby(['coin', 'w']).apply(lambda x: x.iloc[::3]).reset_index(drop=True)
    E2['zb'] = pd.qcut(E2['z'], 5, labels=False)
    out['next3 (grid) by z quintile'] = E2.groupby('zb')['next3'].apply(tt).unstack()
    # vol level -> next day abs and sign
    V = D.dropna(subset=['vol30', 'next']).copy()
    V['vb'] = V.groupby('coin')['vol30'].transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False))
    out['next day by vol30 quintile'] = V.groupby('vb')['next'].apply(tt).unstack()
    # book largest gains/losses: coin return before and after
    B = D.dropna(subset=['book_return']).copy()
    B['prev'] = B.groupby(['coin', 'w'])['coin_return'].shift(1)
    q = B['book_return'].quantile([0.02, 0.98])
    lo = B[B.book_return <= q.iloc[0]]; hi = B[B.book_return >= q.iloc[1]]
    out['around book worst 2%'] = pd.DataFrame({'prev': tt(lo['prev']), 'same': tt(lo['coin_return']), 'next': tt(lo['next'])})
    out['around book best 2%'] = pd.DataFrame({'prev': tt(hi['prev']), 'same': tt(hi['coin_return']), 'next': tt(hi['next'])})
    # run below 50 at short horizons (daily next return), graded
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            r1 = b['close'].shift(-1) / b['close'] - 1
            r3 = b['close'].shift(-3) / b['close'] - 1
            rows.append(pd.DataFrame({'run': b[C].values, 'r1': r1.values, 'r3': r3.values, 'i': np.arange(len(b))}))
    R = pd.concat(rows).dropna(subset=['run'])
    R['rb'] = pd.cut(R['run'], [-61, -30, -15, -6, -0.5, 0.5, 6, 15, 30, 61])
    out['next day by signed run bucket'] = R.groupby('rb')['r1'].apply(tt).unstack()
    R3 = R[R.i % 3 == 0]
    out['next 3d (grid) by signed run bucket'] = R3.groupby('rb')['r3'].apply(tt).unstack()
    return out
