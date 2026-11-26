import numpy as np, pandas as pd

def ct(df, col):
    d = df.dropna(subset=[col])
    n = len(d)
    if n < 5: return (n, np.nan, np.nan, 0)
    m = d[col].mean()
    s = (d[col]-m).groupby(d['day']).sum()
    G = len(s)
    se = np.sqrt((s**2).sum()/n**2 * G/(G-1)) if G > 1 else np.nan
    return (n, m, m/se if se else np.nan, G)

def tab(df, by, col):
    rows = []
    for k, g in df.groupby(by, observed=True):
        n, m, t, G = ct(g, col)
        rows.append(dict(key=str(k), n=n, mean_pct=m*100, t=t, days=G))
    return pd.DataFrame(rows)

def explore(data):
    frames = []
    for coin, wins in data['bars'].items():
        for w, b in wins.items():
            b = b.sort_values('timestamp').reset_index(drop=True).copy()
            b['coin'] = coin; b['win'] = w; b['i'] = np.arange(len(b))
            c = b['close']
            b['ret1'] = c.pct_change()
            b['fwd2'] = c.shift(-2)/c - 1
            b['fwd1'] = c.shift(-1)/c - 1
            hh = b['high'].rolling(20, min_periods=20).max()
            ll = b['low'].rolling(20, min_periods=20).min()
            b['rp'] = (c-ll)/(hh-ll)
            b['sd20'] = b['ret1'].rolling(20, min_periods=15).std()
            b['z1'] = b['ret1']/b['sd20'].shift(1)
            b['r5'] = c/c.shift(5)-1
            b['tr60'] = c/c.shift(60)-1
            b['day'] = pd.to_datetime(b['timestamp']).dt.floor('D')
            b['wd'] = pd.to_datetime(b['timestamp']).dt.dayofweek
            b['calm'] = np.where(b['regime'] == 'unknown', 'calm', 'agit')
            frames.append(b)
    B = pd.concat(frames, ignore_index=True)
    grid = B[B['i'] % 2 == 0].copy()
    drift = grid.groupby('coin')['fwd2'].mean()
    grid['ex2'] = grid['fwd2'] - grid['coin'].map(drift)
    grid['rpq'] = pd.cut(grid['rp'], [-0.01, .2, .4, .6, .8, 1.01], labels=['q1', 'q2', 'q3', 'q4', 'q5'])
    grid['zq'] = pd.cut(grid['z1'], [-99, -1.5, -0.5, 0.5, 1.5, 99], labels=['vdown', 'down', 'flat', 'up', 'vup'])
    grid['trend'] = np.select([grid['tr60'] > .1, grid['tr60'] < -.1], ['rising', 'falling'], 'choppy')
    grid.loc[grid['tr60'].isna(), 'trend'] = 'na'
    grid['side'] = np.sign(grid['rp'] - 0.5)
    grid['sx2'] = grid['ex2']*grid['side']
    out = {}
    out['rp_by_calm'] = tab(grid, ['calm', 'rpq'], 'ex2')
    out['z1_by_calm'] = tab(grid, ['calm', 'zq'], 'ex2')
    out['signed_by_trend_calm'] = tab(grid, ['calm', 'trend'], 'sx2')
    # weekday next-day return (all bars, 1-day non-overlapping)
    d1 = B.copy(); d1['ex1'] = d1['fwd1'] - d1['coin'].map(B.groupby('coin')['fwd1'].mean())
    d1['wdn'] = (d1['wd']+1) % 7
    out['nextday_by_weekday_calm'] = tab(d1, ['calm', 'wdn'], 'ex1')
    # book
    D = []
    for coin, wins in data['days'].items():
        for w, d in wins.items():
            d = d.copy(); d['coin'] = coin; d['win'] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(['win', 'day'])[['book_return', 'coin_return']].mean().reset_index()
    bk['wd'] = pd.to_datetime(bk['day']).dt.dayofweek
    bk['yr'] = pd.to_datetime(bk['day']).dt.year
    out['book_by_weekday'] = bk.groupby('wd')['book_return'].agg(['count', 'mean', 'std'])
    out['book_by_year'] = bk.groupby('yr')['book_return'].agg(['count', 'mean', 'std'])
    out['book_by_window'] = bk.groupby('win')[['book_return', 'coin_return']].mean()
    tr = []
    for coin, wins in data['trades'].items():
        for w, t in wins.items():
            if len(t): tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    T['dur_d'] = T['duration_minutes']/1440
    T['durq'] = pd.cut(T['dur_d'], [0, 2.5, 5, 10, 1000])
    out['trades_side'] = T.groupby('side')['net_profit_loss_percent'].agg(['count', 'mean', 'median', lambda x: (x > 0).mean()])
    out['trades_dur'] = T.groupby(['side', 'durq'], observed=True)['net_profit_loss_percent'].agg(['count', 'mean'])
    return out
