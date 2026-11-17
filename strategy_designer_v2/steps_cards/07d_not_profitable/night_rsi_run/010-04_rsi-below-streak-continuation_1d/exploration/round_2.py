def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    fc = 'debug_info.components.rsi_below_age.last_history_value'
    g = []
    for coin in data['bars']:
        for w, b in data['bars'][coin].items():
            b = b.reset_index(drop=True).copy()
            b['f14'] = b['close'].shift(-14) / b['close'] - 1
            b['ret30'] = b['close'] / b['close'].shift(30) - 1
            b['ma100'] = b['close'] / b['close'].rolling(100, min_periods=50).mean() - 1
            b['coin'] = coin; b['w'] = w
            g.append(b.iloc[::14])
    G = pd.concat(g).dropna(subset=['f14'])
    G['ex'] = G['f14'] - G['coin'].map(G.groupby('coin')['f14'].mean())
    S = G[G['forecast'] < 0].copy()
    S['run'] = -S[fc]
    S['gain'] = S['postRebalance_current_allocation'] * S['ex']
    for col in ['ret30', 'ma100']:
        q = pd.qcut(S[col], 3, duplicates='drop')
        out['grid14_by_' + col] = S.groupby(q).agg(n=('ex', 'size'), ex=('ex', 'mean'), gain=('gain', 'mean'),
                                                  run=('run', 'mean'),
                                                  t=('ex', lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    rb = pd.cut(S['run'], [0, 10, 25, 61])
    out['grid14_by_run'] = S.groupby(rb).agg(n=('ex', 'size'), ex=('ex', 'mean'), gain=('gain', 'mean'),
                                             ret30=('ret30', 'mean'))
    # slope of ex on ret30 within shorts (graded depth)
    s2 = S.dropna(subset=['ret30'])
    r = stats.linregress(s2['ret30'], s2['ex'])
    out['slope_ex_on_ret30_shorts'] = pd.Series({'slope': r.slope, 't': r.slope / r.stderr, 'n': len(s2)})
    # all grid bars: ex by ret30 tercile (including flat)
    q = pd.qcut(G['ret30'], 4, duplicates='drop')
    out['grid14_all_by_ret30'] = G.groupby(q).agg(n=('ex', 'size'), ex=('ex', 'mean'),
                                                  t=('ex', lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    # worst 14-day book falls: by state
    D = []
    for coin in data['days']:
        for w, d in data['days'][coin].items():
            b = data['bars'][coin][w].reset_index(drop=True)
            d = d.reset_index(drop=True).copy()
            d['b14'] = d['book_value'].shift(-14) / d['book_value'] - 1
            d['ret30'] = d['close'] / d['close'].shift(30) - 1
            d['pos'] = b['postRebalance_current_allocation'].values[:len(d)]
            D.append(d.iloc[::14])
    D = pd.concat(D).dropna(subset=['b14', 'ret30'])
    worst = D.nsmallest(20, 'b14')
    out['worst20_book14'] = pd.Series({'b14_mean': worst['b14'].mean(), 'ret30_mean': worst['ret30'].mean(),
                                       'pos_mean': worst['pos'].mean(),
                                       'all_ret30_mean': D['ret30'].mean()})
    return out
