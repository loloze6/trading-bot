def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def tm(s):
        s = pd.Series(s).dropna()
        return s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan
    D = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close'].astype(float)
            ts = pd.to_datetime(b['timestamp'])
            r = c.pct_change()
            for i in range(1, len(b)):
                D.append((coin, w, ts[i].year, ts[i].dayofweek, ts[i].strftime('%Y-%m-%d'), r[i]))
    D = pd.DataFrame(D, columns=['coin', 'w', 'yr', 'dow', 'day', 'r']).dropna()
    D['ex'] = D['r'] - D.groupby('coin')['r'].transform('mean')
    # cross-coin mean per day, then weekday t on independent days
    dd = D.groupby(['w', 'day', 'dow'])['ex'].mean().reset_index()
    out['dow_daymean'] = dd.groupby('dow')['ex'].agg(mean='mean', n='count', t=tm)
    out['dow_by_coin_t'] = D.pivot_table(index='coin', columns='dow', values='ex', aggfunc=tm)
    out['dow_by_year_mean'] = D.pivot_table(index='yr', columns='dow', values='ex', aggfunc='mean')
    # Sat minus rest per window: share of windows positive
    D['sat'] = (D['dow'] == 5)
    pw = D.groupby('w').apply(lambda x: x.loc[x.sat, 'ex'].mean() - x.loc[~x.sat, 'ex'].mean())
    out['sat_minus_rest_windows'] = pd.Series({'n_w': len(pw), 'share_pos': (pw > 0).mean(),
                                               'mean': pw.mean(), 't': tm(pw)})
    # weekend (Fri+Sat closes, i.e. Sat+Sun? use dow 4,5) vs Tue/Thu
    # 20-day return grading per coin on 5-day grid
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b['close'].astype(float).reset_index(drop=True)
            for i in range(20, len(c) - 5, 5):
                rows.append((coin, w, c[i] / c[i - 20] - 1, c[i + 5] / c[i] - 1,
                             c[i] / c[i - 1] - 1))
    g = pd.DataFrame(rows, columns=['coin', 'w', 'r20', 'fwd', 'r1'])
    g['ex'] = g['fwd'] - g.groupby('coin')['fwd'].transform('mean')
    out['r20_corr_by_coin'] = g.groupby('coin').apply(
        lambda x: pd.Series({'r': x['r20'].corr(x['ex']), 'n': len(x),
                             't_sign': tm(np.sign(x['r20']) * x['ex'])}))
    # book: largest loss/gain days, coin move that day and the day before
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d['coin'] = coin; d['w'] = w
            d['prev_coin'] = d['coin_return'].shift(1)
            bk.append(d)
    B = pd.concat(bk).dropna(subset=['book_return'])
    q = B['book_return'].quantile([0.02, 0.98])
    out['book_extremes'] = pd.DataFrame({
        'worst2%': B[B.book_return <= q.iloc[0]][['book_return', 'coin_return', 'prev_coin']].mean(),
        'best2%': B[B.book_return >= q.iloc[1]][['book_return', 'coin_return', 'prev_coin']].mean()})
    # positions: long vs short share and gain
    P = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b['close'].astype(float).reset_index(drop=True)
            a = b['postRebalance_current_allocation'].reset_index(drop=True)
            nx = c.shift(-1) / c - 1
            P.append(pd.DataFrame({'a': a, 'g': a * nx, 'nx': nx}))
    P = pd.concat(P).dropna()
    P['side'] = np.sign(P['a'])
    out['by_side'] = P.groupby('side').agg(share=('a', lambda s: len(s) / len(P)),
                                           mean_gain=('g', 'mean'), mean_next=('nx', 'mean'),
                                           t_gain=('g', tm))
    return out
