import numpy as np, pandas as pd
from scipy import stats

def _clust(df, col):
    d = df.dropna(subset=[col])
    if len(d) < 5: return (len(d), np.nan, np.nan, np.nan)
    g = d.groupby('ts')[col].sum()
    n_days = len(g)
    t = g.mean() / (g.std(ddof=1) / np.sqrt(n_days)) if n_days > 2 else np.nan
    return (len(d), d[col].mean(), t, n_days)

def _tab(df, by, col):
    rows = {}
    for k, s in df.groupby(by):
        n, m, t, nd = _clust(s, col)
        rows[k] = {'n': n, 'mean': m, 't_day': t, 'days': nd}
    return pd.DataFrame(rows).T

def explore(data):
    bars = data['bars']
    recs20, recs5, recs1 = [], [], []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close'].values
            n = len(c)
            r1 = pd.Series(c).pct_change().values
            vol20 = pd.Series(r1).rolling(20).std().values
            for h, store in ((20, recs20), (5, recs5)):
                for t in range(0, n - h, h):
                    fwd = c[t + h] / c[t] - 1
                    past20 = c[t] / c[t - 20] - 1 if t >= 20 else np.nan
                    past5 = c[t] / c[t - 5] - 1 if t >= 5 else np.nan
                    store.append(dict(coin=coin, w=w, ts=b['timestamp'].iloc[t], fwd=fwd,
                        regime=b['regime'].iloc[t], past20=past20, past5=past5, vol20=vol20[t],
                        dist_raw=b['debug_info.components.dist_low.last_history_value'].iloc[t],
                        dist_std=b['debug_info.components.dist_low.post_pipeline_value'].iloc[t],
                        fc=b['forecast'].iloc[t]))
            for t in range(21, n - 1):
                recs1.append(dict(coin=coin, ts=b['timestamp'].iloc[t], fwd=c[t+1]/c[t]-1,
                                  z=r1[t]/vol20[t-1] if vol20[t-1] > 0 else np.nan,
                                  wd=pd.Timestamp(b['timestamp'].iloc[t+1]).dayofweek,
                                  regime=b['regime'].iloc[t]))
    out = {}
    for name, R in (('h20', pd.DataFrame(recs20)), ('h5', pd.DataFrame(recs5))):
        R['ex'] = R['fwd'] - R.groupby('coin')['fwd'].transform('mean')
        R['volq'] = R.groupby('coin')['vol20'].transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False) if s.notna().sum() > 10 else np.nan)
        R['p20q'] = R.groupby('coin')['past20'].transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False) if s.notna().sum() > 10 else np.nan)
        out[name + ' by regime'] = _tab(R, 'regime', 'ex')
        out[name + ' by past20 quintile'] = _tab(R.dropna(subset=['p20q']), 'p20q', 'ex')
        out[name + ' by vol quintile'] = _tab(R.dropna(subset=['volq']), 'volq', 'ex')
        T = R[R['regime'] == 'trending'].dropna(subset=['dist_raw'])
        if len(T) > 20:
            T = T.copy()
            T['rawq'] = pd.qcut(T['dist_raw'].rank(method='first'), 5, labels=False)
            T['stdq'] = pd.qcut(T['dist_std'].rank(method='first'), 5, labels=False)
            out[name + ' trending by raw dist quintile'] = _tab(T, 'rawq', 'ex')
            out[name + ' raw dist quintile bounds'] = T.groupby('rawq')['dist_raw'].agg(['min', 'max'])
            out[name + ' trending by std dist quintile'] = _tab(T, 'stdq', 'ex')
        if name == 'h20':
            R['p20s'] = np.sign(R['past20'])
            out['h20 regime x past20 sign'] = _tab(R.dropna(subset=['past20']), ['regime', 'p20s'], 'ex')
    D = pd.DataFrame(recs1)
    D['ex'] = D['fwd'] - D.groupby('coin')['fwd'].transform('mean')
    D['zq'] = pd.cut(D['z'], [-99, -2, -1, 0, 1, 2, 99])
    out['h1 by last-day z'] = _tab(D.dropna(subset=['zq']), 'zq', 'ex')
    out['h1 by weekday'] = _tab(D, 'wd', 'ex')
    # book
    dd = []
    for coin, wins in data['days'].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    DD = pd.concat(dd)
    bk = DD.groupby('day')[['book_return', 'coin_return']].mean().dropna()
    out['book daily corr with hold'] = float(bk.corr().iloc[0, 1])
    q = bk['book_return'].quantile([0.02, 0.98])
    out['coin return on book worst 2% days'] = bk[bk.book_return <= q.iloc[0]]['coin_return'].describe()
    out['coin return on book best 2% days'] = bk[bk.book_return >= q.iloc[1]]['coin_return'].describe()
    tr = []
    for coin, wins in data['trades'].items():
        for w, t in wins.items():
            tr.append(t)
    TR = pd.concat(tr)
    out['trades by side'] = TR.groupby('side')['net_profit_loss_percent'].agg(['count', 'mean', 'median'])
    return out
