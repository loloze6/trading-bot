import numpy as np, pandas as pd

def _col(b, name):
    return b[name] if name in b.columns else pd.Series(np.nan, index=b.index)

def _clust(d, col):
    d = d.dropna(subset=[col])
    if len(d) < 5:
        return (len(d), np.nan, np.nan, np.nan)
    g = d.groupby('ts')[col].sum()
    nd = len(g)
    sd = g.std(ddof=1)
    t = g.mean() / (sd / np.sqrt(nd)) if nd > 2 and sd > 0 else np.nan
    return (len(d), d[col].mean(), t, nd)

def _tab(df, by, col):
    rows = {}
    for k, s in df.groupby(by, observed=True):
        n, m, t, nd = _clust(s, col)
        rows[str(k)] = {'n': n, 'mean': m, 't_day': t, 'days': nd}
    return pd.DataFrame(rows).T

def _q(s, k=5):
    s = s.astype(float)
    if s.notna().sum() < 3 * k:
        return pd.Series(np.nan, index=s.index)
    r = s.rank(method='first')
    return pd.qcut(r, k, labels=False)

def explore(data):
    out = {}
    try:
        bars = data['bars']
        recs = {20: [], 5: []}
        recs1 = []
        for coin, wins in bars.items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b['close'].values.astype(float)
                n = len(c)
                r1 = pd.Series(c).pct_change().values
                vol20 = pd.Series(r1).rolling(20).std().values
                draw = _col(b, 'debug_info.components.dist_low.last_history_value').values
                dstd = _col(b, 'debug_info.components.dist_low.post_pipeline_value').values
                fc = b['forecast'].values
                reg = b['regime'].values
                ts = b['timestamp'].values
                hi = b['high'].values.astype(float); lo = b['low'].values.astype(float)
                for h in (20, 5):
                    for t in range(0, n - h, h):
                        recs[h].append(dict(coin=coin, w=w, ts=ts[t], fwd=c[t+h]/c[t]-1,
                            regime=reg[t], past20=(c[t]/c[t-20]-1) if t >= 20 else np.nan,
                            vol20=vol20[t], dist_raw=draw[t], dist_std=dstd[t], fc=fc[t]))
                for t in range(21, n - 1):
                    v = vol20[t-1]
                    rng = (hi[t] - lo[t])
                    recs1.append(dict(coin=coin, ts=ts[t], fwd=c[t+1]/c[t]-1,
                        z=r1[t]/v if v and v > 0 else np.nan,
                        clv=((c[t]-lo[t])/rng) if rng > 0 else np.nan,
                        wd=pd.Timestamp(ts[t+1]).dayofweek, regime=reg[t]))
        for h in (20, 5):
            R = pd.DataFrame(recs[h])
            R['ex'] = R['fwd'] - R.groupby('coin')['fwd'].transform('mean')
            R['volq'] = R.groupby('coin')['vol20'].transform(_q)
            R['p20q'] = R.groupby('coin')['past20'].transform(_q)
            out[f'h{h} by regime'] = _tab(R, 'regime', 'ex')
            out[f'h{h} by past20 quintile (per coin)'] = _tab(R.dropna(subset=['p20q']), 'p20q', 'ex')
            out[f'h{h} by vol quintile (per coin)'] = _tab(R.dropna(subset=['volq']), 'volq', 'ex')
            T = R[(R['regime'] == 'trending')].dropna(subset=['dist_raw', 'dist_std']).copy()
            if len(T) > 30:
                T['rawq'] = _q(T['dist_raw'])
                T['stdq'] = _q(T['dist_std'])
                out[f'h{h} trending by raw dist quintile'] = _tab(T, 'rawq', 'ex')
                out[f'h{h} raw dist bounds'] = T.groupby('rawq')['dist_raw'].agg(['min', 'median', 'max'])
                out[f'h{h} trending by std dist quintile'] = _tab(T, 'stdq', 'ex')
                T['fsign'] = np.sign(T['fc'])
                out[f'h{h} trending by forecast sign'] = _tab(T, 'fsign', 'ex')
            if h == 20:
                R2 = R.dropna(subset=['past20']).copy()
                R2['p20s'] = np.sign(R2['past20'])
                out['h20 regime x past20 sign'] = _tab(R2, ['regime', 'p20s'], 'ex')
        D = pd.DataFrame(recs1)
        D['ex'] = D['fwd'] - D.groupby('coin')['fwd'].transform('mean')
        D['zq'] = pd.cut(D['z'], [-99, -2, -1, 0, 1, 2, 99])
        out['h1 by last-day z'] = _tab(D.dropna(subset=['zq']), 'zq', 'ex')
        D['clvq'] = pd.cut(D['clv'], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
        out['h1 by close location in day range'] = _tab(D.dropna(subset=['clvq']), 'clvq', 'ex')
        out['h1 by weekday'] = _tab(D, 'wd', 'ex')
    except Exception as e:
        out['bars error'] = repr(e)[:200]
    try:
        dd = []
        for coin, wins in data['days'].items():
            for w, d in wins.items():
                dd.append(d.assign(coin=coin, w=w))
        DD = pd.concat(dd)
        bk = DD.groupby('day')[['book_return', 'coin_return']].mean().dropna()
        out['book daily corr with hold'] = float(bk.corr().iloc[0, 1])
        q = bk['book_return'].quantile([0.02, 0.98])
        out['hold return on book worst 2% days'] = bk[bk.book_return <= q.iloc[0]]['coin_return'].describe()
        out['hold return on book best 2% days'] = bk[bk.book_return >= q.iloc[1]]['coin_return'].describe()
    except Exception as e:
        out['days error'] = repr(e)[:200]
    try:
        tr = []
        for coin, wins in data['trades'].items():
            for w, t in wins.items():
                if len(t): tr.append(t)
        TR = pd.concat(tr)
        out['trades by side'] = TR.groupby('side')['net_profit_loss_percent'].agg(['count', 'mean', 'median'])
    except Exception as e:
        out['trades error'] = repr(e)[:200]
    return out
