import numpy as np, pandas as pd
from scipy import stats

def _grid(df, h):
    c = df['close'].values
    idx = np.arange(0, len(c) - h, h)
    return idx, c[idx + h] / c[idx] - 1

def explore(data):
    out = {}
    bars = data['bars']
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df['close']
            r1 = c.pct_change()
            ret20 = c / c.shift(20) - 1
            ret60 = c / c.shift(60) - 1
            ret5 = c / c.shift(5) - 1
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60).std()
            ts = pd.to_datetime(df['timestamp'])
            for h in (5, 10, 20):
                idx = np.arange(0, len(c) - h, h)
                fwd = c.values[idx + h] / c.values[idx] - 1
                for i, f in zip(idx, fwd):
                    rows.append(dict(coin=coin, w=w, h=h, fwd=f, fc=df['forecast'].iloc[i],
                                     ret5=ret5.iloc[i], ret20=ret20.iloc[i], ret60=ret60.iloc[i],
                                     r1=r1.iloc[i], vol20=vol20.iloc[i], vol60=vol60.iloc[i],
                                     volratio=vol20.iloc[i] / vol60.iloc[i] if vol60.iloc[i] else np.nan,
                                     wd=ts.iloc[i].dayofweek, yr=ts.iloc[i].year,
                                     alloc=df['postRebalance_current_allocation'].iloc[i]))
    g = pd.DataFrame(rows)
    # drift-removed
    drift = g.groupby(['coin', 'h'])['fwd'].transform('mean')
    sd = g.groupby(['coin', 'h'])['fwd'].transform('std')
    g['ex'] = (g['fwd'] - drift) / sd  # in usual-move units
    def bucket_tab(var, h, q=5):
        s = g[g.h == h].dropna(subset=[var, 'ex']).copy()
        s['b'] = s.groupby('coin')[var].transform(lambda x: pd.qcut(x.rank(method='first'), q, labels=False))
        t = s.groupby('b')['ex'].agg(['mean', 'count', 'std'])
        t['t'] = t['mean'] / (t['std'] / np.sqrt(t['count']))
        return t[['mean', 'count', 't']].round(3)
    for var in ['fc', 'ret5', 'ret20', 'ret60', 'vol20', 'volratio']:
        for h in (10, 20):
            out[f'{var} quintile -> fwd{h} (std units)'] = bucket_tab(var, h)
    # correlations per coin, ret60 vs fwd20
    cc = []
    for coin, s in g[g.h == 20].dropna(subset=['ret60']).groupby('coin'):
        r, p = stats.spearmanr(s['ret60'], s['fwd'])
        r2, p2 = stats.spearmanr(s['ret20'], s['fwd'])
        cc.append(dict(coin=coin, n=len(s), rho60=r, p60=p, rho20=r2, p20=p2))
    out['spearman per coin fwd20'] = pd.DataFrame(cc).round(3)
    # daily: weekday, after large moves
    d = []
    for coin, wins in data['days'].items():
        for w, df in wins.items():
            df = df.copy()
            df['coin'] = coin
            df['w'] = w
            df['prev'] = df['coin_return'].shift(1)
            df['wd'] = pd.to_datetime(df['day']).dt.dayofweek
            df['yr'] = pd.to_datetime(df['day']).dt.year
            d.append(df)
    d = pd.concat(d)
    d['z'] = d['coin_return'] / d.groupby('coin')['coin_return'].transform('std')
    t = d.groupby('wd')['z'].agg(['mean', 'count', 'std']); t['t'] = t['mean'] / (t['std'] / np.sqrt(t['count']))
    out['weekday coin return z'] = t.round(3)
    d['pz'] = d['prev'] / d.groupby('coin')['coin_return'].transform('std')
    d['pb'] = pd.cut(d['pz'], [-99, -2, -1, 0, 1, 2, 99])
    t = d.groupby('pb')['z'].agg(['mean', 'count', 'std']); t['t'] = t['mean'] / (t['std'] / np.sqrt(t['count']))
    out['next day z by prev day z'] = t.round(3)
    # book by year and coin
    bk = d.groupby('yr').agg(book=('book_return', 'mean'), coin=('coin_return', 'mean'), n=('book_return', 'count'))
    out['book vs coin by year'] = bk.round(5)
    bc = d.groupby('coin').agg(book=('book_return', 'mean'), coinr=('coin_return', 'mean'), sdb=('book_return', 'std'))
    out['book vs coin by coin'] = bc.round(5)
    # trades long vs short
    tr = pd.concat([df.assign(coin=c) for c, ws in data['trades'].items() for df in ws.values()])
    out['trades by side'] = tr.groupby('side')['profit_loss_percent'].agg(['mean', 'count', 'median']).round(3)
    return out
