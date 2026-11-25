import numpy as np, pandas as pd
from scipy import stats

def _grid(data, h, fcol='debug_info.components.range_pos.post_pipeline_value'):
    rows = []
    for coin, wins in data['bars'].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df['close'].values
            f = df[fcol].values if fcol in df else np.full(len(df), np.nan)
            raw = df['debug_info.components.range_pos.last_history_value'].values
            ts = pd.to_datetime(df['timestamp'])
            tr60 = pd.Series(c).pct_change(60).values
            for i in range(0, len(df) - h, h):
                rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, f=f[i], raw=raw[i],
                                 r=c[i+h]/c[i]-1, tr=tr60[i], day=ts.iloc[i].floor('D')))
    g = pd.DataFrame(rows).dropna(subset=['f', 'r'])
    g['drift'] = g.groupby('coin')['r'].transform('mean')
    g['x'] = g['r'] - g['drift']
    return g

def _slope(g):
    if len(g) < 10 or g['f'].std() == 0:
        return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
    res = stats.linregress(g['f'], g['x'])
    return pd.Series(dict(n=len(g), slope=res.slope, t=res.slope/res.stderr))

def explore(data):
    out = {}
    g = _grid(data, 5)
    out['h5 pooled'] = _slope(g)
    out['h5 by window'] = g.groupby('win').apply(_slope)
    out['h5 by coin'] = g.groupby('coin').apply(_slope)
    out['h5 by year'] = g.groupby('year').apply(_slope)
    g['q'] = pd.qcut(g['f'], 5, labels=False, duplicates='drop')
    out['h5 by forecast fifth'] = g.groupby('q')['x'].agg(['count', 'mean', 'std']).assign(
        t=lambda d: d['mean']/(d['std']/np.sqrt(d['count'])))
    g['side'] = np.where(g['f'] > 0, 'long', 'short')
    g['sx'] = np.sign(g['f'])*g['x']
    out['h5 by side signed'] = g.groupby('side')['sx'].agg(['count', 'mean', 'std']).assign(
        t=lambda d: d['mean']/(d['std']/np.sqrt(d['count'])))
    g['trend'] = pd.cut(g['tr'], [-np.inf, -0.10, 0.10, np.inf], labels=['falling', 'choppy', 'rising'])
    out['h5 by trend'] = g.groupby('trend').apply(_slope)
    hs = {}
    for h in [1, 2, 3, 5, 10, 20]:
        gh = _grid(data, h)
        s = _slope(gh)
        s['slope_per_usual'] = s['slope']/gh['r'].std()
        hs[h] = s
    out['by horizon'] = pd.DataFrame(hs).T
    return out
