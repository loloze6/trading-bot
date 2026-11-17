def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    fc = 'debug_info.components.rsi_below_share.last_history_value'
    B = []
    for coin, ws in data['bars'].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            b['coin'] = coin; b['w'] = w
            b['r1'] = b['close'].pct_change()
            b['nxt'] = b['close'].shift(-1) / b['close'] - 1
            b['r30p'] = b['close'].pct_change(30)
            b['vol30'] = b['r1'].rolling(30).std()
            b['z'] = b['r1'] / b['vol30'].shift(1)
            b['dd60'] = b['close'] / b['close'].rolling(60, min_periods=20).max() - 1
            b['gain'] = b['postRebalance_current_allocation'] * b['nxt']
            b['share'] = b[fc]
            B.append(b)
    B = pd.concat(B, ignore_index=True)
    B['ex'] = B['nxt'] - B.groupby('coin')['nxt'].transform('mean')
    # next-day return after large daily moves, graded by z
    Bz = B.dropna(subset=['z', 'ex']).copy()
    Bz['zb'] = pd.cut(Bz['z'], [-99, -2, -1, 0, 1, 2, 99])
    r = Bz.groupby('zb')['ex'].agg(['mean', 'std', 'count']); r['t'] = r['mean'] / (r['std'] / np.sqrt(r['count']))
    out['nextday_by_prev_z'] = r
    # by coin, sign of large moves
    Bz['big'] = np.sign(Bz['z']) * (Bz['z'].abs() > 2)
    r = Bz.groupby(['coin', 'big'])['ex'].agg(['mean', 'std', 'count']); r['t'] = r['mean'] / (r['std'] / np.sqrt(r['count']))
    out['nextday_after_big_by_coin'] = r
    # gain by forecast sign x share quintile: where the long-side gain comes from
    Bg = B.dropna(subset=['gain', 'share']).copy()
    Bg['sq'] = Bg.groupby('coin')['share'].transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False))
    Bg['side'] = np.sign(Bg['postRebalance_current_allocation'])
    r = Bg.groupby(['side', 'sq'])['gain'].agg(['mean', 'std', 'count']); r['t'] = r['mean'] / (r['std'] / np.sqrt(r['count']))
    out['gain_side_sharequint'] = r
    # next-day excess return by share quintile (daily, not grid -- descriptive)
    r = Bg.groupby('sq')['ex'].agg(['mean', 'std', 'count']); r['t'] = r['mean'] / (r['std'] / np.sqrt(r['count']))
    out['nextday_by_sharequint'] = r
    # drawdown-from-60d-high grading of 14d forward on grid
    rows = []
    for (coin, w), b in B.groupby(['coin', 'w']):
        b = b.reset_index(drop=True); c = b['close'].values
        for t in range(0, len(b) - 14, 14):
            rows.append(dict(coin=coin, dd=b['dd60'].iloc[t], vol=b['vol30'].iloc[t], r30=b['r30p'].iloc[t], share=b['share'].iloc[t], fwd=c[t + 14] / c[t] - 1))
    G = pd.DataFrame(rows).dropna()
    G['ex'] = G['fwd'] - G.groupby('coin')['fwd'].transform('mean')
    G['dq'] = G.groupby('coin')['dd'].transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False))
    r = G.groupby('dq')['ex'].agg(['mean', 'std', 'count']); r['t'] = r['mean'] / (r['std'] / np.sqrt(r['count']))
    out['fwd14_by_dd60_quint'] = r
    out['spearman_dd_fwd14'] = G.groupby('coin').apply(lambda x: stats.spearmanr(x['dd'], x['ex'])[0])
    # share effect within vol halves
    G['vh'] = G.groupby('coin')['vol'].transform(lambda s: (s > s.median()).astype(int))
    out['share_spearman_by_volhalf'] = G.groupby(['coin', 'vh']).apply(lambda x: pd.Series({'sp': stats.spearmanr(x['share'], x['ex'])[0], 'n': len(x)}))
    # around book's largest days
    D = pd.concat([d.assign(coin=c, w=w) for c, ws in data['days'].items() for w, d in ws.items()]).dropna(subset=['book_return'])
    D['sgn'] = np.sign(D['book_return']) 
    q_hi = D['book_return'].quantile(0.95); q_lo = D['book_return'].quantile(0.05)
    D['coinabs'] = D['coin_return'].abs()
    out['tail_days'] = pd.DataFrame({
        'top5_coin_ret_mean': [D.loc[D.book_return >= q_hi, 'coin_return'].mean()],
        'top5_long_share': [(D.loc[D.book_return >= q_hi, 'coin_return'] > 0).mean()],
        'bot5_coin_ret_mean': [D.loc[D.book_return <= q_lo, 'coin_return'].mean()],
        'bot5_coin_up_share': [(D.loc[D.book_return <= q_lo, 'coin_return'] > 0).mean()],
    })
    # skew of book daily returns, by coin
    out['book_skew'] = D.groupby('coin')['book_return'].agg(['mean', 'std', 'skew'])
    out['coin_skew'] = D.groupby('coin')['coin_return'].agg(['mean', 'std', 'skew'])
    return out
