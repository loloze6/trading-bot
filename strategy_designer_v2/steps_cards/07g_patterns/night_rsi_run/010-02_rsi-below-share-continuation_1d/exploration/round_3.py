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
            b['vol30'] = b['r1'].rolling(30).std()
            b['z1'] = b['r1'] / b['vol30'].shift(1)
            b['r3p'] = b['close'].pct_change(3)
            b['z3'] = b['r3p'] / (b['vol30'].shift(3) * np.sqrt(3))
            b['share'] = b[fc]
            B.append(b)
    B = pd.concat(B, ignore_index=True)
    # graded reversal: z of past move vs next h-day excess, non-overlapping grid per window
    res = {}
    for h, zc in ((1, 'z1'), (3, 'z1'), (3, 'z3'), (7, 'z3')):
        rows = []
        for (coin, w), b in B.groupby(['coin', 'w']):
            b = b.reset_index(drop=True); c = b['close'].values
            for t in range(0, len(b) - h, h):
                rows.append(dict(coin=coin, z=b[zc].iloc[t], vol=b['vol30'].iloc[t], fwd=c[t + h] / c[t] - 1))
        G = pd.DataFrame(rows).dropna()
        G['ex'] = G['fwd'] - G.groupby('coin')['fwd'].transform('mean')
        for coin, x in G.groupby('coin'):
            sp, p = stats.spearmanr(x['z'], x['ex'])
            lr = stats.linregress(x['z'], x['ex'])
            res[(f'h{h}_{zc}', coin)] = dict(spearman=sp, p=p, slope=lr.slope, t_slope=lr.slope / lr.stderr, n=len(x))
        sp, p = stats.spearmanr(G['z'], G['ex'])
        res[(f'h{h}_{zc}', 'ALL')] = dict(spearman=sp, p=p, slope=np.nan, t_slope=np.nan, n=len(G))
        if h == 1:
            G['vh'] = G.groupby('coin')['vol'].transform(lambda s: (s > s.median()).astype(int))
            out['h1_z1_by_volhalf'] = G.groupby(['coin', 'vh']).apply(lambda x: pd.Series({'sp': stats.spearmanr(x['z'], x['ex'])[0], 'n': len(x)}))
            G['year'] = 0
    out['reversal_spearman'] = pd.DataFrame(res).T
    # by year stability of h1 z1 reversal
    rows = []
    for (coin, w), b in B.groupby(['coin', 'w']):
        b = b.reset_index(drop=True); c = b['close'].values
        for t in range(0, len(b) - 1):
            rows.append(dict(coin=coin, year=pd.Timestamp(b['timestamp'].iloc[t]).year, z=b['z1'].iloc[t], fwd=c[t + 1] / c[t] - 1))
    G = pd.DataFrame(rows).dropna()
    G['ex'] = G['fwd'] - G.groupby('coin')['fwd'].transform('mean')
    out['h1_rev_by_year'] = G.groupby('year').apply(lambda x: pd.Series({'sp': stats.spearmanr(x['z'], x['ex'])[0], 'n': len(x)}))
    # share x vol on 7-day grid
    rows = []
    for (coin, w), b in B.groupby(['coin', 'w']):
        b = b.reset_index(drop=True); c = b['close'].values
        for t in range(0, len(b) - 7, 7):
            rows.append(dict(coin=coin, share=b['share'].iloc[t], vol=b['vol30'].iloc[t], fwd=c[t + 7] / c[t] - 1))
    G = pd.DataFrame(rows).dropna()
    G['ex'] = G['fwd'] - G.groupby('coin')['fwd'].transform('mean')
    G['vh'] = G.groupby('coin')['vol'].transform(lambda s: (s > s.median()).astype(int))
    out['share_h7_by_volhalf'] = G.groupby(['coin', 'vh']).apply(lambda x: pd.Series({'sp': stats.spearmanr(x['share'], x['ex'])[0], 'p': stats.spearmanr(x['share'], x['ex'])[1], 'n': len(x)}))
    return out
