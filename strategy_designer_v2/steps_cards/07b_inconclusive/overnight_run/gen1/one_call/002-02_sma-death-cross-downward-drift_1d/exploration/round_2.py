import pandas as pd, numpy as np

def wstats(df, col='ex', w='w'):
    if len(df) < 3: return pd.Series({'n': len(df), 'wmean': np.nan, 't': np.nan, 'hit': np.nan})
    x = df[col].values; ww = df[w].values
    m = np.sum(ww*x)/np.sum(ww); n = len(x)
    se = np.sqrt(np.sum(ww**2*(x-m)**2)*n/(n-1))/np.sum(ww)
    return pd.Series({'n': n, 'wmean': m, 't': m/se if se > 0 else np.nan, 'hit': (x > 0).mean()})

def explore(data):
    rows = []
    for coin, wins in data['bars'].items():
        allf = []
        for wk, b in wins.items():
            allf.append((b['close'].shift(-10)/b['close'] - 1).dropna())
        hold = pd.concat(allf).mean()
        for wk, b in wins.items():
            b = b.reset_index(drop=True).copy()
            sp = b['debug_info.components.sma_cross_down.last_history_value']
            b['fwd'] = b['close'].shift(-10)/b['close'] - 1
            b['r10'] = b['close']/b['close'].shift(10) - 1
            b['r60'] = b['close']/b['close'].shift(60) - 1
            b['dd60'] = b['close']/b['close'].rolling(60, min_periods=20).max() - 1
            b['sma20'] = b['close'].rolling(20).mean()
            b['above20'] = b['close'] > b['sma20']
            neg = (b['forecast'] < 0).astype(int)
            grp = (neg != neg.shift()).cumsum()
            b['age'] = neg.groupby(grp).cumsum()
            b['first_neg'] = (neg.iloc[0] == 1)
            b['censored'] = (grp == grp.iloc[0]) & (neg.iloc[0] == 1)
            b['sp'] = sp
            b['ts'] = pd.to_datetime(b['timestamp'])
            s = b.iloc[::10]
            s = s[(s['forecast'] < 0) & s['fwd'].notna()]
            for _, r in s.iterrows():
                rows.append({'coin': coin, 'year': r['ts'].year, 'w': abs(r['forecast']),
                             'ex': -(r['fwd'] - hold), 'r10': r['r10'], 'r60': r['r60'], 'dd60': r['dd60'],
                             'above20': r['above20'], 'age': r['age'], 'cens': r['censored'], 'sp': r['sp']})
    d = pd.DataFrame(rows)
    out = {}
    u = d[~d['cens']].copy()
    u['ageb'] = pd.cut(u['age'], [0, 20, 50, 100, 10000], labels=['<=20', '21-50', '51-100', '>100'])
    out['by_age_uncensored'] = u.groupby('ageb').apply(wstats)
    out['censored_vs_not'] = d.groupby('cens').apply(wstats)
    d['spq'] = pd.qcut(d['sp'], 3, labels=['deepest', 'mid', 'shallow'])
    out['by_raw_spread'] = d.groupby('spq').apply(wstats)
    out['by_above_sma20'] = d.groupby('above20').apply(wstats)
    x = d.dropna(subset=['r10']).copy()
    x['r10q'] = pd.qcut(x['r10'], 3, labels=['fell', 'mid', 'rose'])
    out['by_r10'] = x.groupby('r10q').apply(wstats)
    x = d.dropna(subset=['r60']).copy()
    x['r60q'] = pd.qcut(x['r60'], 3, labels=['fell', 'mid', 'rose'])
    out['by_r60'] = x.groupby('r60q').apply(wstats)
    x = d.dropna(subset=['dd60']).copy()
    x['ddq'] = pd.qcut(x['dd60'], 3, labels=['deep dd', 'mid dd', 'near high'])
    out['by_dd60'] = x.groupby('ddq').apply(wstats)
    x = d.dropna(subset=['dd60']).copy()
    x['ddq'] = pd.qcut(x['dd60'], 3, labels=['deep dd', 'mid dd', 'near high'])
    x['a20'] = np.where(x['above20'], 'above20', 'below20')
    out['dd_x_above20'] = x.groupby(['ddq', 'a20']).apply(wstats)
    out['by_spq_year_hit'] = d.groupby(['spq']).apply(lambda g: g.groupby('year')['ex'].mean()).T if False else d.pivot_table(index='year', columns='spq', values='ex', aggfunc='mean')
    return out
