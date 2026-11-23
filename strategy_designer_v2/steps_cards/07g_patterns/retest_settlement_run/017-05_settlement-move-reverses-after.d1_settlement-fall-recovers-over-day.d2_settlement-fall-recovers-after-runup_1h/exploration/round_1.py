def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    frames = []
    for coin, wins in data['bars'].items():
        for w, df in wins.items():
            d = pd.DataFrame()
            c = df['close'].astype(float).values
            ts = pd.to_datetime(df['timestamp'])
            d['coin'] = coin; d['w'] = w
            d['pos'] = np.arange(len(df))
            d['ch'] = ((ts.dt.hour + 1) % 24).values
            d['wd'] = ts.dt.weekday.values
            d['year'] = ts.dt.year.values
            s = pd.Series(c)
            d['f24'] = (s.shift(-24) / s - 1).values
            d['f1'] = (s.shift(-1) / s - 1).values
            d['p1'] = (s / s.shift(1) - 1).values
            d['p2'] = (s / s.shift(2) - 1).values
            d['p24'] = (s / s.shift(24) - 1).values
            d['p168'] = (s / s.shift(168) - 1).values
            mad2 = d['p2'].abs().rolling(720, min_periods=200).mean()
            d['z2'] = d['p2'] / mad2
            d['vol'] = pd.Series(d['p1']).rolling(168, min_periods=100).std().values
            v = df['volume'].astype(float)
            d['relvol'] = (v / v.rolling(168, min_periods=50).median()).values
            d['fc'] = df['forecast'].astype(float).values
            d['coin'] = coin; d['w'] = w
            frames.append(d)
    B = pd.concat(frames, ignore_index=True)
    grid = B[B['pos'] % 24 == 0]
    cm = grid.groupby('coin')['f24'].mean()
    B['x24'] = B['f24'] - B['coin'].map(cm)
    grid = B[B['pos'] % 24 == 0].copy()
    def summ(g, col='x24'):
        x = g[col].dropna()
        n = len(x)
        m = x.mean()
        return pd.Series({'n': n, 'mean%': 100*m, 't': m/(x.std(ddof=1)/np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    out['A_x24_by_closehour'] = B.groupby('ch').apply(summ).round(3)
    out['A2_next1h_by_closehour'] = B.groupby('ch').apply(lambda g: summ(g, 'f1')).round(4)
    out['A3_relvol_by_closehour'] = B.groupby('ch')['relvol'].median().round(3)
    # graded fall: -z2 * x24 by hour (fall side only)
    B['fallz'] = (-B['z2']).clip(lower=0)
    B['gx'] = B['fallz'] * B['x24']
    B['rise_pos'] = B['p168'] > 0
    r = []
    for h in range(24):
        g = B[(B['ch'] == h) & B['z2'].notna() & B['x24'].notna()]
        rho, p = stats.spearmanr(g['z2'], g['x24'])
        gg = g[g['rise_pos']]
        rho2, p2 = stats.spearmanr(gg['z2'], gg['x24'])
        r.append({'ch': h, 'n': len(g), 'rho_z2_x24': rho, 'p': p, 'rho_uptrend': rho2, 'p_up': p2})
    out['B_spearman_2hmove_vs_next24_by_hour'] = pd.DataFrame(r).round(4)
    # forecast quintiles on settlement cases
    S = B[(B['fc'] >= 2) & B['ch'].isin([0, 16])].copy()
    S['q'] = pd.qcut(S['fc'].rank(method='first'), 5, labels=False)
    out['C_fc_quintile'] = S.groupby('q').apply(summ).round(3)
    out['C2_fc_quintile_fc_mean'] = S.groupby('q')['fc'].mean().round(2)
    # past 24h decile on grid
    grid['d24'] = grid.groupby('coin')['p24'].transform(lambda x: pd.qcut(x.rank(method='first'), 10, labels=False))
    out['D_x24_by_past24_decile'] = grid.groupby('d24').apply(summ).round(3)
    grid['d168'] = grid.groupby('coin')['p168'].transform(lambda x: pd.qcut(x.rank(method='first'), 10, labels=False))
    out['D2_x24_by_past168_decile'] = grid.groupby('d168').apply(summ).round(3)
    grid['dv'] = grid.groupby('coin')['vol'].transform(lambda x: pd.qcut(x.rank(method='first'), 5, labels=False))
    out['E_x24_by_vol_quintile'] = grid.groupby('dv').apply(summ).round(3)
    out['F_x24_by_weekday'] = grid.groupby('wd').apply(summ).round(3)
    # book
    D = []
    for coin, wins in data['days'].items():
        for w, df in wins.items():
            x = df[['day', 'book_return', 'coin_return']].copy(); x['w'] = w; x['coin'] = coin
            D.append(x)
    D = pd.concat(D)
    D['day'] = pd.to_datetime(D['day'])
    bk = D.groupby(['w', 'day'])[['book_return', 'coin_return']].mean().reset_index()
    bk['wd'] = bk['day'].dt.weekday; bk['year'] = bk['day'].dt.year
    out['G_book_by_weekday'] = bk.groupby('wd').apply(lambda g: summ(g, 'book_return')).round(4)
    out['G2_book_by_year'] = bk.groupby('year').agg(n=('book_return', 'size'), book=('book_return', 'mean'), coin=('coin_return', 'mean')).mul([1, 100, 100]).round(4)
    out['G3_book_vs_coin_corr'] = float(bk[['book_return', 'coin_return']].corr().iloc[0, 1])
    return out
