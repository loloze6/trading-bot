def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    comps = ['mom', 'rev', 'high', 'vol']
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close'].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(b['timestamp'])
            for i in range(1, len(b)):
                daily.append((coin, w, ts[i].dayofweek, r1[i], abs(r1[i])))
            for i in range(0, len(b) - H, H):
                d = {'coin': coin, 'w': w, 'fwd': c[i + H] / c[i] - 1,
                     'fc': b['forecast'].iloc[i],
                     'r1': r1[i] if i >= 1 else np.nan,
                     'r5': c[i] / c[i - 5] - 1 if i >= 5 else np.nan,
                     'r20': c[i] / c[i - 20] - 1 if i >= 20 else np.nan,
                     'v10': r1[max(1, i - 9):i + 1].std() if i >= 10 else np.nan,
                     'dow': ts[i].dayofweek,
                     'alloc': b['postRebalance_current_allocation'].iloc[i]}
                for k in comps:
                    col = f'debug_info.components.{k}.post_pipeline_value'
                    d[k] = b[col].iloc[i] if col in b else np.nan
                rows.append(d)
    g = pd.DataFrame(rows)
    g['ex'] = g['fwd'] - g.groupby('coin')['fwd'].transform('mean')
    out = {}

    def qtab(col, z=True):
        x = g.dropna(subset=[col, 'ex']).copy()
        if z:
            x['s'] = x.groupby('coin')[col].transform(lambda s: (s - s.mean()) / s.std())
        else:
            x['s'] = x[col]
        x['q'] = x.groupby('coin')['s'].transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False))
        t = x.groupby('q')['ex'].agg(['mean', 'count'])
        t['t'] = x.groupby('q')['ex'].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
        r, p = stats.pearsonr(x['s'], x['ex'])
        t.loc['corr', 'mean'] = r
        t.loc['corr', 'count'] = len(x)
        t.loc['corr', 't'] = r * np.sqrt((len(x) - 2) / (1 - r * r))
        return t

    for col in comps + ['fc', 'r1', 'r5', 'r20', 'v10']:
        out['q_' + col] = qtab(col)

    # sign of each component times excess, per coin
    pc = []
    for coin, x in g.groupby('coin'):
        row = {'coin': coin}
        for k in comps + ['fc']:
            y = x.dropna(subset=[k])
            m = np.sign(y[k]) * y['ex']
            row[k] = m.mean() / (m.std() / np.sqrt(len(m)))
        pc.append(row)
    out['t_sign_by_coin'] = pd.DataFrame(pc).set_index('coin')

    # volatility level vs size of next move
    x = g.dropna(subset=['v10']).copy()
    x['q'] = x.groupby('coin')['v10'].transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False))
    out['vol_q_absfwd'] = x.groupby('q').agg(absfwd=('fwd', lambda s: s.abs().mean()),
                                             fwd=('fwd', 'mean'), n=('fwd', 'count'))

    D = pd.DataFrame(daily, columns=['coin', 'w', 'dow', 'r', 'ar']).dropna()
    D['ex'] = D['r'] - D.groupby('coin')['r'].transform('mean')
    out['dow'] = D.groupby('dow')['ex'].agg(
        mean='mean', n='count', t=lambda s: s.mean() / (s.std() / np.sqrt(len(s))))

    # book: daily returns, gain from drift vs timing
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d.assign(coin=coin, w=w))
    B = pd.concat(bk)
    bd = B.groupby(['w', 'day'])[['book_return', 'coin_return']].mean().dropna()
    out['book'] = pd.Series({'book_mean': bd['book_return'].mean(),
                             'coin_mean': bd['coin_return'].mean(),
                             'corr_book_coin': bd['book_return'].corr(bd['coin_return']),
                             'n_days': len(bd)})
    out['by_window_book'] = B.groupby('w')['book_return'].mean().to_frame('mean_book')
    return out
