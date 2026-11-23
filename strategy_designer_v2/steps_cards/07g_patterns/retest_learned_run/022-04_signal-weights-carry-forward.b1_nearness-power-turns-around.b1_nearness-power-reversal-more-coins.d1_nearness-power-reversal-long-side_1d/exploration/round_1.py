def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    comp = 'debug_info.components.power_reversal.last_history_value'
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close'].astype(float)
            r1 = c.pct_change()
            fwd = c.shift(-H) / c - 1
            past5 = c / c.shift(5) - 1
            past20 = c / c.shift(20) - 1
            past60 = c / c.shift(60) - 1
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60).std()
            hi90 = c.rolling(90, min_periods=60).max()
            near = c / hi90 - 1
            lo90 = c.rolling(90, min_periods=60).min()
            pos = (c - lo90) / (hi90 - lo90)
            dfw = pd.DataFrame({
                'coin': coin, 'win': w, 'fwd': fwd, 'past1': r1, 'past5': past5, 'past20': past20,
                'past60': past60, 'vol20': vol20, 'volratio': vol20 / vol60, 'near': near, 'pos': pos,
                'fc': b['forecast'].astype(float),
                'raw': b[comp].astype(float) if comp in b else np.nan,
                'alloc': b['postRebalance_current_allocation'].astype(float),
                'wd': pd.to_datetime(b['timestamp']).dt.dayofweek,
                'year': pd.to_datetime(b['timestamp']).dt.year,
            })
            dfw = dfw.iloc[::H]
            rows.append(dfw)
    d = pd.concat(rows, ignore_index=True)
    d = d.dropna(subset=['fwd'])
    d['ex'] = d['fwd'] - d.groupby('coin')['fwd'].transform('mean')
    def grp(col, q=5):
        x = d.dropna(subset=[col]).copy()
        x['b'] = x.groupby('coin')[col].transform(lambda s: pd.qcut(s.rank(method='first'), q, labels=False))
        g = x.groupby('b')['ex'].agg(['mean', 'std', 'count'])
        g['t'] = g['mean'] / (g['std'] / np.sqrt(g['count']))
        g['raw_fwd_mean'] = x.groupby('b')['fwd'].mean()
        return g
    out = {}
    out['n_grid'] = len(d)
    for col in ['raw', 'past1', 'past5', 'past20', 'past60', 'vol20', 'volratio', 'near', 'pos']:
        out['q_' + col] = grp(col)
    g = d.groupby('wd')['ex'].agg(['mean', 'std', 'count']); g['t'] = g['mean'] / (g['std'] / np.sqrt(g['count']))
    out['weekday'] = g
    g = d.groupby('year')[['ex', 'fwd']].mean(); g['n'] = d.groupby('year').size()
    out['year'] = g
    # forecast positive vs zero
    d['fpos'] = d['fc'] > 0
    g = d.groupby('fpos')['ex'].agg(['mean', 'std', 'count']); g['t'] = g['mean'] / (g['std'] / np.sqrt(g['count']))
    out['fc_pos_vs_zero'] = g
    # per coin t of past20 top vs bottom quintile
    res = {}
    for coin, x in d.dropna(subset=['past20']).groupby('coin'):
        qq = pd.qcut(x['past20'].rank(method='first'), 5, labels=False)
        a, bb = x['ex'][qq == 4], x['ex'][qq == 0]
        res[coin] = [a.mean() - bb.mean(), stats.ttest_ind(a, bb, equal_var=False).statistic, len(x)]
    out['coin_mom20_top_minus_bot'] = pd.DataFrame(res, index=['diff', 't', 'n']).T
    return out
