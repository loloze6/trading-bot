import numpy as np, pandas as pd
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3 or x.std() == 0: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

def _tday(df, col):
    # day-pooled t of deviations
    g = df.groupby('day')[col].sum()
    if len(g) < 3: return np.nan, len(g)
    return g.mean() / (g.std(ddof=1) / np.sqrt(len(g))) * 1.0, len(g)

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.sort_values('timestamp').reset_index(drop=True).copy()
            c = b['close']
            b['r1'] = c.pct_change()
            b['ret28'] = c / c.shift(28) - 1
            b['ret7'] = c / c.shift(7) - 1
            b['vol20'] = b['r1'].rolling(20).std()
            b['rng'] = (b['high'] - b['low']) / b['close']
            b['rng_z'] = b['rng'] / b['rng'].rolling(28).mean()
            b['volu_z'] = b['volume'] / b['volume'].rolling(28).mean()
            b['f10'] = c.shift(-10) / c - 1
            b['f3'] = c.shift(-3) / c - 1
            b['f1'] = c.shift(-1) / c - 1
            b['pos'] = np.arange(len(b))
            b['coin'] = coin; b['win'] = w
            b['day'] = pd.to_datetime(b['timestamp']).dt.floor('D')
            b['wd'] = pd.to_datetime(b['timestamp']).dt.weekday
            b['calm'] = (b['regime'] == 'mean_reversion').astype(int)
            rows.append(b)
    A = pd.concat(rows, ignore_index=True)
    # drift per coin (over visible windows), grid-based
    out = {}
    for h, col in [(10, 'f10'), (3, 'f3'), (1, 'f1')]:
        g = A[A['pos'] % h == 0]
        d = g.groupby('coin')[col].mean()
        A['d' + col] = A['coin'].map(d)
        A['x' + col] = A[col] - A['d' + col]
    G10 = A[(A['pos'] % 10 == 0)].dropna(subset=['f10', 'ret28'])
    # 1. 28d return quintile x calm, excess 10d return
    G10 = G10.copy()
    G10['q28'] = G10.groupby('coin')['ret28'].transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False))
    t1 = G10.groupby(['calm', 'q28'])['xf10'].agg(['mean', 'count', _t])
    out['xf10 by calm x ret28 quintile'] = t1
    # 2. vol20 tercile
    G10v = G10.dropna(subset=['vol20']).copy()
    G10v['qv'] = G10v.groupby('coin')['vol20'].transform(lambda s: pd.qcut(s.rank(method='first'), 3, labels=False))
    out['xf10 by vol20 tercile x calm'] = G10v.groupby(['qv', 'calm'])['xf10'].agg(['mean', 'count', _t])
    # 3. after large daily moves: next 3d excess, grid 3
    G3 = A[A['pos'] % 3 == 0].dropna(subset=['f3', 'r1', 'vol20']).copy()
    G3['z1'] = G3['r1'] / G3['vol20']
    G3['zb'] = pd.cut(G3['z1'], [-99, -2, -1, 0, 1, 2, 99])
    out['xf3 by today z-move'] = G3.groupby('zb')['xf3'].agg(['mean', 'count', _t])
    # 4. 7-day return quintile, next 3 days
    G3b = G3.dropna(subset=['ret7']).copy()
    G3b['q7'] = G3b.groupby('coin')['ret7'].transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False))
    out['xf3 by ret7 quintile'] = G3b.groupby('q7')['xf3'].agg(['mean', 'count', _t])
    # 5. weekday daily excess
    out['xf1 by weekday'] = A.groupby('wd')['xf1'].agg(['mean', 'count', _t])
    # 6. range spike / volume spike next 3 days
    G3c = G3.dropna(subset=['rng_z', 'volu_z']).copy()
    G3c['qr'] = pd.qcut(G3c['rng_z'].rank(method='first'), 5, labels=False)
    G3c['qvz'] = pd.qcut(G3c['volu_z'].rank(method='first'), 5, labels=False)
    out['xf3 by range-ratio quintile'] = G3c.groupby('qr')['xf3'].agg(['mean', 'count', _t])
    out['xf3 by volume-ratio quintile'] = G3c.groupby('qvz')['xf3'].agg(['mean', 'count', _t])
    # 7. forecast bins vs xf10 on grid
    Gf = A[(A['pos'] % 10 == 0)].dropna(subset=['f10']).copy()
    Gf['fb'] = pd.cut(Gf['forecast'], [-21, -10, -5, -2, -0.0001, 0.0001])
    out['xf10 by forecast bin'] = Gf.groupby('fb')['xf10'].agg(['mean', 'count', _t])
    # 8. book daily returns by window and by year
    D = []
    for coin, wins in data['days'].items():
        for w, d in wins.items():
            d = d.copy(); d['coin'] = coin; d['win'] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(['win', 'day'])[['book_return', 'coin_return']].mean().reset_index()
    out['book by window'] = bk.groupby('win').agg(book_mean=('book_return', 'mean'), coin_mean=('coin_return', 'mean'), n=('day', 'count'))
    # 9. trades
    T = []
    for coin, wins in data['trades'].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t['coin'] = coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T['fb'] = pd.cut(T['entry_forecast'], [-21, -10, -5, -2, 0.5])
    out['trades by entry forecast'] = T.groupby('fb')['net_profit_loss_percent'].agg(['mean', 'count', 'median', _t])
    out['trades by coin'] = T.groupby('coin')['net_profit_loss_percent'].agg(['mean', 'count', _t])
    return out
