def explore(data):
    import numpy as np, pandas as pd
    frames = []
    for coin, wins in data['bars'].items():
        for w, df in wins.items():
            d = pd.DataFrame()
            c = df['close'].astype(float).values
            ts = pd.to_datetime(df['timestamp'])
            s = pd.Series(c)
            d['pos'] = np.arange(len(df))
            d['ch'] = ((ts.dt.hour + 1) % 24).values
            d['year'] = ts.dt.year.values
            d['f24'] = (s.shift(-24) / s - 1).values
            d['f2'] = (s.shift(-2) / s - 1).values
            d['p24'] = (s / s.shift(24) - 1).values
            d['p168'] = (s / s.shift(168) - 1).values
            r1 = s.pct_change()
            d['vol'] = r1.rolling(720, min_periods=300).std().values
            mad24 = d['p24'].abs().rolling(720, min_periods=300).mean()
            d['z24'] = (d['p24'] / mad24).values
            d['coin'] = coin; d['w'] = w
            frames.append(d)
    B = pd.concat(frames, ignore_index=True)
    grid = B[B['pos'] % 24 == 0].copy()
    cm = grid.groupby('coin')['f24'].mean()
    B['x24'] = B['f24'] - B['coin'].map(cm)
    grid = B[B['pos'] % 24 == 0].copy()
    def summ(g, col='x24'):
        x = g[col].dropna(); n = len(x); m = x.mean()
        return pd.Series({'n': n, 'mean%': 100*m, 't': m/(x.std(ddof=1)/np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    g = grid.dropna(subset=['z24', 'x24']).copy()
    g['zb'] = pd.cut(g['z24'], [-99, -3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3, 99])
    out['A_x24_by_z24_bin'] = g.groupby('zb').apply(summ).round(3)
    low = g[g['z24'] < -1.5]
    out['B_fall_by_coin'] = low.groupby('coin').apply(summ).round(3)
    out['B2_fall_by_year'] = low.groupby('year').apply(summ).round(3)
    out['B3_fall_by_window'] = low.groupby('w').apply(summ).round(3)
    low = low.copy()
    low['up7'] = np.where(low['p168'] > 0, 'up7', 'down7')
    out['C_fall_by_7d_sign'] = low.groupby('up7').apply(summ).round(3)
    low['vq'] = pd.qcut(low['vol'].rank(method='first'), 3, labels=False)
    out['C2_fall_by_vol_tercile'] = low.groupby('vq').apply(summ).round(3)
    # graded product test
    g['prod'] = (-g['z24']).clip(lower=0) * g['x24']
    x = g['prod']; out['D_graded_negz24_times_x24_t'] = float(x.mean()/(x.std()/np.sqrt(len(x))))
    gn = g[g['z24'] < 0]
    out['D2_spearman_z24_x24_on_falls'] = float(gn[['z24', 'x24']].corr(method='spearman').iloc[0, 1])
    out['D3_n_falls'] = int(len(gn))
    # evening hours
    B['f1'] = B.groupby(['coin', 'w'])['f2'].transform(lambda s: s)  # placeholder
    ev = B[B['ch'] == 21].dropna(subset=['f2', 'p24']).copy()
    out['E_2h_after_21_by_coin'] = ev.groupby('coin').apply(lambda g: summ(g, 'f2')).round(4)
    out['E2_2h_after_21_by_year'] = ev.groupby('year').apply(lambda g: summ(g, 'f2')).round(4)
    ev['pq'] = pd.qcut(ev['p24'].rank(method='first'), 5, labels=False)
    out['E3_2h_after_21_by_past24_quintile'] = ev.groupby('pq').apply(lambda g: summ(g, 'f2')).round(4)
    # book largest days
    D = []
    for coin, wins in data['days'].items():
        for w, df in wins.items():
            x = df[['day', 'book_return', 'coin_return']].copy(); x['w'] = w; D.append(x)
    D = pd.concat(D); bk = D.groupby(['w', 'day'])[['book_return', 'coin_return']].mean().reset_index()
    q = bk['book_return'].quantile([0.02, 0.98])
    out['F_book_extreme_days_coin_ret'] = pd.DataFrame({
        'worst2%_book': [bk[bk.book_return <= q.iloc[0]]['book_return'].mean()*100, bk[bk.book_return <= q.iloc[0]]['coin_return'].mean()*100],
        'best2%_book': [bk[bk.book_return >= q.iloc[1]]['book_return'].mean()*100, bk[bk.book_return >= q.iloc[1]]['coin_return'].mean()*100]},
        index=['book%', 'coin%']).round(3)
    return out
