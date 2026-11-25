import numpy as np, pandas as pd

def _tday(df, col):
    g = df.groupby('day')[col].sum()
    if len(g) < 3 or g.std(ddof=1) == 0: return np.nan
    return g.mean() / (g.std(ddof=1) / np.sqrt(len(g)))

def _clslope(df, x, y):
    d = df.dropna(subset=[x, y])
    X = d[x] - d[x].mean(); Y = d[y]
    b = (X * (Y - Y.mean())).sum() / (X ** 2).sum()
    e = (Y - Y.mean()) - b * X
    s = (X * e).groupby(d['day']).sum()
    G = len(s); n = len(d)
    var = (s ** 2).sum() / ((X ** 2).sum() ** 2) * G / (G - 1) * (n - 1) / (n - 2)
    return pd.Series({'slope': b, 't_day': b / np.sqrt(var), 'n': n, 'days': G})

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values('timestamp').reset_index(drop=True).copy()
            c = b['close']
            b['r1'] = c.pct_change()
            b['ret28'] = c / c.shift(28) - 1
            b['vol20'] = b['r1'].rolling(20).std()
            b['z28'] = b['ret28'] / (b['vol20'] * np.sqrt(28))
            for h in (5, 10, 20):
                b['f%d' % h] = c.shift(-h) / c - 1
            b['pos'] = np.arange(len(b))
            b['coin'] = coin; b['win'] = w
            b['day'] = pd.to_datetime(b['timestamp']).dt.floor('D')
            b['year'] = pd.to_datetime(b['timestamp']).dt.year
            b['calm'] = (b['regime'] == 'mean_reversion').astype(int)
            rows.append(b)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    for h in (5, 10, 20):
        g = A[A['pos'] % h == 0]
        A['x%d' % h] = A['f%d' % h] - A['coin'].map(g.groupby('coin')['f%d' % h].mean())
    G = A[A['pos'] % 10 == 0].dropna(subset=['x10', 'z28']).copy()
    G['q'] = G.groupby('coin')['ret28'].transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False))
    res = []
    for (cm, q), d in G.groupby(['calm', 'q']):
        res.append({'calm': cm, 'q': q, 'mean': d['x10'].mean(), 'n': len(d), 'days': d['day'].nunique(), 't_day': _tday(d, 'x10')})
    out['x10 calm x ret28 quintile, day t'] = pd.DataFrame(res)
    sl = {}
    for h in (5, 10, 20):
        Gh = A[A['pos'] % h == 0].dropna(subset=['x%d' % h, 'z28'])
        for cm in (0, 1):
            sl['h%d calm%d' % (h, cm)] = _clslope(Gh[Gh['calm'] == cm], 'z28', 'x%d' % h)
        sl['h%d all' % h] = _clslope(Gh, 'z28', 'x%d' % h)
    out['slope of excess return on z28 (vol-scaled 28d ret)'] = pd.DataFrame(sl).T
    # sign per window: calm slope h10
    pw = {}
    Gc = G[G['calm'] == 1]
    for w, d in Gc.groupby('win'):
        if len(d) > 15: pw[w] = _clslope(d, 'z28', 'x10')
    out['calm slope h10 by window'] = pd.DataFrame(pw).T
    py = {}
    for y, d in Gc.groupby('year'):
        if len(d) > 15: py[y] = _clslope(d, 'z28', 'x10')
    out['calm slope h10 by year'] = pd.DataFrame(py).T
    # positive side only in calm
    out['calm, ret28>0 slope h10'] = _clslope(Gc[Gc['ret28'] > 0], 'z28', 'x10')
    out['calm, ret28<0 slope h10'] = _clslope(Gc[Gc['ret28'] < 0], 'z28', 'x10')
    # trades duration
    T = []
    for coin, wins in data['trades'].items():
        for w, t in wins.items():
            if len(t): T.append(t)
    T = pd.concat(T, ignore_index=True)
    T['days'] = T['duration_minutes'] / 1440
    T['db'] = pd.cut(T['days'], [0, 10.5, 15, 25, 50, 1000])
    out['trades by duration'] = T.groupby('db')['net_profit_loss_percent'].agg(['mean', 'count', 'median'])
    return out
