import numpy as np, pandas as pd

def _ct(x, day):
    d = pd.DataFrame({'x': x, 'day': day}).dropna()
    if len(d) < 5: return np.nan, len(d), 0
    m = d['x'].mean()
    s = (d['x'] - m).groupby(d['day']).sum()
    D = len(s)
    se = np.sqrt(D/(D-1) * (s**2).sum()) / len(d)
    return m/se, len(d), D

def _slope(G, xcol, ycol='z'):
    d = G[[xcol, ycol, 'day']].dropna()
    x = (d[xcol] - d[xcol].mean()) / d[xcol].std()
    y = d[ycol] - d[ycol].mean()
    b = (x*y).sum() / (x*x).sum()
    e = y - b*x
    s = (x*e).groupby(d['day']).sum()
    D = len(s)
    se = np.sqrt(D/(D-1) * (s**2).sum()) / (x*x).sum()
    return round(b, 4), round(b/se, 2), len(d), D

def explore(data):
    H = 10
    recs = []
    for coin, wins in data['bars'].items():
        rows = []
        for w, b in wins.items():
            b = b.sort_values('timestamp').reset_index(drop=True)
            c = b['close'].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(30).std()
            df = pd.DataFrame({'day': pd.to_datetime(b['timestamp']).dt.floor('D'),
                               'fwd': c.shift(-H)/c - 1, 'pos': np.arange(len(c)),
                               'vol': vol, 'alloc': b['postRebalance_current_allocation'].astype(float)})
            for L in [3, 5, 10, 20, 30]:
                df[f'm{L}'] = (c/c.shift(L) - 1) / (vol*np.sqrt(L))
            df['hi20'] = c / c.rolling(20).max() - 1
            df['upshare10'] = (r1 > 0).astype(float).rolling(10).mean()
            df['w'] = w
            rows.append(df)
        cd = pd.concat(rows, ignore_index=True)
        gd = cd[(cd['pos'] % H == 0) & cd['fwd'].notna()]
        drift, sd = gd['fwd'].mean(), gd['fwd'].std()
        cd['u'] = cd['fwd'] - drift; cd['z'] = cd['u']/sd; cd['coin'] = coin
        recs.append(cd)
    A = pd.concat(recs, ignore_index=True)
    out = {}
    # slopes on each grid offset (robustness over grid phase)
    rows = []
    for col in ['m3', 'm5', 'm10', 'm20', 'm30', 'hi20', 'upshare10']:
        r = {'var': col}
        for off in [0, 3, 6]:
            G = A[(A['pos'] % H == off) & A['fwd'].notna()]
            b, t, n, D = _slope(G, col)
            r[f'b_off{off}'] = b; r[f't_off{off}'] = t
        r['n'] = n; r['days'] = D
        rows.append(r)
    out['slopes_z_on_var'] = pd.DataFrame(rows)
    G = A[(A['pos'] % H == 0) & A['fwd'].notna()].copy()
    # per coin slope for m10
    pc = []
    for coin, g in G.groupby('coin'):
        b, t, n, D = _slope(g, 'm10')
        pc.append({'coin': coin, 'b_m10': b, 't': t, 'n': n})
    out['per_coin_m10'] = pd.DataFrame(pc)
    # book: daily returns, largest gains/losses context
    days = []
    for coin, wins in data['days'].items():
        for w, d in wins.items():
            d = d.copy(); d['coin'] = coin; d['w'] = w; days.append(d)
    Dd = pd.concat(days, ignore_index=True)
    bk = Dd.groupby('day').agg(book=('book_return', 'mean'), coin=('coin_return', 'mean')).dropna()
    q = bk['book'].quantile([0.01, 0.05, 0.95, 0.99])
    out['book_tail_q'] = q
    top = bk['book'] >= q.loc[0.99]; bot = bk['book'] <= q.loc[0.01]
    share = pd.Series({'top1pct_sum_share_of_total': bk.loc[top, 'book'].sum()/bk['book'].sum(),
                       'bot1pct_sum_share_of_total': bk.loc[bot, 'book'].sum()/bk['book'].sum(),
                       'ex_top1pct_mean': bk.loc[~top, 'book'].mean(),
                       'all_mean': bk['book'].mean(), 'n_days': len(bk)})
    out['book_tail_share'] = share
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data['trades'].items() for t in ws.values()], ignore_index=True)
    T['dur_d'] = T['duration_minutes']/1440
    T['durq'] = pd.qcut(T['dur_d'].rank(method='first'), 4, labels=['q1', 'q2', 'q3', 'q4'])
    out['trades_by_duration'] = T.groupby('durq', observed=True).agg(n=('dur_d', 'size'), dur=('dur_d', 'mean'),
        pnl=('net_profit_loss_percent', 'mean'), win=('net_profit_loss_percent', lambda x: (x > 0).mean()))
    T['efq'] = pd.qcut(T['entry_forecast'].rank(method='first'), 3, labels=['lo', 'mid', 'hi'])
    out['trades_by_entry_fc'] = T.groupby('efq', observed=True).agg(n=('dur_d', 'size'), fc=('entry_forecast', 'mean'),
        pnl=('net_profit_loss_percent', 'mean'), med=('net_profit_loss_percent', 'median'))
    return out
